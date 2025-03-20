from applications.workers import celery
from datetime import datetime
from celery.schedules import crontab
from collections import defaultdict
import yagmail
from sqlalchemy.sql import func
from flask import jsonify
from flask import current_app as app
from applications.models import User,ServiceOffer,Service,Servicemen

@celery.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
    sender.add_periodic_task(
        crontab(day_of_week='*') ,
        dail.s()
    )

    sender.add_periodic_task(
        crontab(day_of_month=14),
        month.s(),
    )


@celery.task()
def dail():
    with app.app_context():
        S = defaultdict(list)
        x=ServiceOffer.query.filter(ServiceOffer.service_status=='undone').all()
        
        for s in x:
            hh=Servicemen.query.filter(Servicemen.id==s.sm_id).first().name
            val = f"id {s.id}  customer {User.query.filter(User.id == s.c_id).first().username}  date of request {s.DoRequest}\n\n"
            S[hh].append(val)
        for k,v in S.items():
            email=User.query.filter(User.username==k).first().email
            body="Please check your Undone requests \n"
            for i in v:
                body+=i
            sender_email = "suneha2003datta@gmail.com"
            receiver_email = "suvadipbanerjee02@gmail.com" #professional email
            subject = "Leftover Service update"
            yag = yagmail.SMTP(sender_email, "hevejrxokhqmxswp")
            yag.send(receiver_email, subject, body)
        
    

@celery.task()
def month():
    with app.app_context():
        u=User.query.filter(User.roles=='customer').all()
        mmc = datetime.now().strftime("%m")
        for i in u :
            nm=i.username
            email=i.email
            idc=i.id
            prc=len(ServiceOffer.query.filter(ServiceOffer.service_status=='p_reject',ServiceOffer.c_id==idc,func.substr(ServiceOffer.DoRequest,6,2)==mmc).all())
            crc=len(ServiceOffer.query.filter(ServiceOffer.service_status=='c_reject',ServiceOffer.c_id==idc,func.substr(ServiceOffer.DoRequest,6,2)==mmc).all())
            ords=len(ServiceOffer.query.filter(ServiceOffer.c_id==idc,func.substr(ServiceOffer.DoRequest,6,2)==mmc).all())
            body=f"Total rejected orders by servicemen is {prc} \n Net canceled orders is  {crc} \n Total placed orders is  {ords}"
            sender_email = "suneha2003datta@gmail.com"
            receiver_email = "suvadipbanerjee02@gmail.com" #professional email
            subject = "Monthly report of orders in Urbanlife"
            yag = yagmail.SMTP(sender_email, "hevejrxokhqmxswp")
            yag.send(receiver_email, subject, body)
    

@celery.task()
def report():
    with app.app_context():
        c=ServiceOffer.query.filter(ServiceOffer.service_status=='p_reject').all()
        O = [
               {
                'id'  : S.id,
                'cid': S.c_id,
                'smid': S.sm_id,
                'date': S.DoRequest,
                'rem': S.remarks
            }
            for S in c
        ]
        return O