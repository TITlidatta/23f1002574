from flask import Flask, request,render_template,redirect,url_for,render_template_string,Response
from flask import jsonify
from flask import current_app 
from .models import User,Service,ServiceOffer,Servicemen,Blocklist
from .database import db
from sqlalchemy import or_ 
import matplotlib
from io import StringIO
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import yagmail
import smtplib
import pandas as pd
import numpy as np
from applications import tasks
from datetime import datetime

def setup_routes(app):

    @app.route('/tolog', methods=['GET', 'POST'])
    def tolog():
        if request.method == 'POST':
            print('here')
            burima=request.get_json()
            email=burima['email']
            pas=burima['password']
            user = User.query.filter(User.email==email).first()
            if user.password==pas :
                if user.roles=='customer':
                    user.active=1
                    db.session.commit()
                    return jsonify({"redirect_url": url_for('customer', id=user.id),"x":0})
                if user.roles=='professional':
                    user.active=1
                    db.session.commit()
                    print('hereeeee')
                    return jsonify({"redirect_url": url_for('professional', id=user.id),"x":0})
                    
            else:
                return jsonify({"redirect_url": url_for('tolog'),"x":1})
          
        return render_template('login.html')
    @app.route('/logout/<int:id>',methods=['GET'])
    def logout(id):
        x=User.query.filter(User.id==id).first()
        x.active=0
        db.session.commit()
        return render_template('login.html')

    @app.route('/customer/<int:id>',methods=["POST","GET"])
    def customer(id):
        u = User.query.filter(User.id == id).first()
        un=u.username
        Sx= Service.query.all()
        H = [
               {
                'name': S.name,
                'img': S.img,
                'description': S.description,
                'price': S.price,
                'time': S.time
            }
            for S in Sx
        ]
        return render_template('customer.html',un=un,SS=H,idd=id)

    @app.route('/',methods=['GET'])
    def home():
        return redirect(url_for('tolog'))
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            print('here')
            email = request.form.get('email')
            print(email)
            password = request.form.get('password')
            name = request.form.get('Name')
            print(name)
            rolee = request.form.get('role')
            user = User(email=email, password=password,username=name,roles=rolee)
            print('here0')
            db.session.add(user)
            user.active=1
            db.session.commit()
            print('h55ere')
            user_id=user.id
            if(rolee=='customer'):
                return redirect(url_for('customer', id=user_id))
            else:
                return redirect(url_for('verifyou',idu=user_id))
        else:
            return render_template('register.html')
        
    @app.route('/orders/<string:name>')
    def orders(name):
        cid=User.query.filter(User.username == name).first().id
        Sx= ServiceOffer.query.filter(ServiceOffer.c_id == cid,ServiceOffer.service_status=='undone').all()
        N = [
               {
                'sid'  : S.id,
                'sname': Service.query.filter(Service.id ==S.s_id).first().name,
                'sman': Servicemen.query.filter(Servicemen.id ==S.sm_id).first().name,
                'date': S.DoRequest,
                'status': S.service_status
            }
            for S in Sx
        ]
        Sk= ServiceOffer.query.filter(ServiceOffer.c_id == cid,or_(ServiceOffer.service_status=='done',ServiceOffer.service_status=='c_reject',ServiceOffer.service_status=='p_reject')).all()
        blocked=Blocklist.query.filter(Blocklist.c_id==cid).all()
        bl=[]
        for item in blocked:
            bl.append(item.sm_id)
        O = [
               {
                'sid'  : S.id,
                'sname': Service.query.filter(Service.id ==S.s_id).first().name,
                'sman': Servicemen.query.filter(Servicemen.id ==S.sm_id).first().name,
                'date': S.DoRequest,
                'status': S.service_status,
                'smid' : S.sm_id,
                **({'blstat': 'blo'} if S.sm_id not in bl else {'blstat': 'unblo'})
            }
            for S in Sk
        ]
        return render_template('orders.html',N=N,O=O,idd=cid)
    
    @app.route('/order/<string:sname>/<string:uname>')
    def order(sname,uname):
        s=sname
        print(uname)
        uh=User.query.filter(User.username==uname).first().id
        xi=Service.query.filter(Service.name==sname).first().img
        p=Service.query.filter(Service.name==sname).first().price
        print(sname)
        Sk= Servicemen.query.filter(Servicemen.service == sname).all()
        blocked=Blocklist.query.filter(Blocklist.c_id==uh).all()
        bl=[]
        for item in blocked:
            bl.append(item.sm_id)
        X=[]
        for item in Sk:
            if item.id in bl or item.status =='n_verified':
                continue
            else:
                X.append(item)
        O = [
               {
                'name': S.name,
                'exp': S.experience,
                'des': S.description,
                'rate': S.rating
            }
            for S in X
        ]
        print(Sk)
        print(X)
        return render_template('order.html',s=s,p=p,L=O,u=uname,xi=xi,uh=uh)
    @app.route('/place',methods=['POST'])
    def place():
        if request.method=='POST':
            det= request.get_json()
            print(det)
            uu=det['cname']
            sname=det['sname']
            sman=det['sman']
            address=det['adrs']
            phone=det['ph']
            s_id=Service.query.filter(Service.name == sname).first().id
            sm_id=Servicemen.query.filter(Servicemen.name == sman).first().id
            user_id=User.query.filter(User.username == uu).first().id
            vb=Servicemen.query.filter(Servicemen.name == sman).first().id_u
            email=User.query.filter(User.id == vb).first().email

            current_date = datetime.now()
            tt= current_date.strftime("%Y-%m-%d")
            news=ServiceOffer(sm_id=sm_id,s_id=s_id,c_id=user_id,service_status='undone',c_no=phone,DoRequest=tt)
            db.session.add(news)
            db.session.commit()
            sender_email = "suneha2003datta@gmail.com"
            receiver_email = "suvadipbanerjee02@gmail.com"
            subject = "Order Placed"
            body = "Thank you for placing your order. The details were provided here\n  Service type " +sname+ "\nProfessional "+sman+"\nCustomer name " + uu + "\n " + "Address  "+ address +  "\nPhone " + phone +"\nRegards Urbanlife"
            server=smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(sender_email,'hevejrxokhqmxswp')
            print(body)
            server.sendmail(sender_email,receiver_email,body)
            print('donr')

            return jsonify({'redirect_url': url_for("customer",id=user_id)})
    
    @app.route('/remark/<int:sid>',methods=['POST'])
    def remark(sid):
        if request.method=='POST':
            print('herer')
            rema= request.get_json()
            Sk= ServiceOffer.query.filter(ServiceOffer.id==sid).first()
            Sk.remarks=rema
            db.session.commit()
            print('her')
            return jsonify({'statusofit': 'ok'})
    @app.route('/cancel/<int:sid>',methods=['POST'])
    def cancel(sid):
        #remove sid 
        if request.method=='POST':
            A=ServiceOffer.query.filter(ServiceOffer.id==sid).first()
            A.service_status='c_reject'
            db.session.commit()
            phone=A.c_no
            uu=User.query.filter(User.id==A.c_id).first().username
            vb=Servicemen.query.filter(Servicemen.id == A.sm_id).first().id_u
            email=User.query.filter(User.id == vb).first().email
        #email to sman
            sender_email = "suneha2003datta@gmail.com"
            receiver_email = "suvadipbanerjee02@gmail.com"
            subject = "Order Canceled"
            body = "This is to inform your order id "+ str(sid) +" has been cancelled by customer . The details were provided here  Customer name " + uu + " " + " Phone " + phone + " "+ " For address details look into the previous email of the order notification. Regards Urbanlife"
            server=smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(sender_email,'hevejrxokhqmxswp')
            print(body)
            server.sendmail(sender_email,receiver_email,body)
            print('donr')
            return jsonify({'statusofit': 'ok'})
    
    @app.route('/profile/<string:m>',methods=['GET','POST'])
    def profile(m):
        id=User.query.filter(User.username==m).first().id
        service_name=Servicemen.query.filter(Servicemen.name==m).first().service
        service_desc=Service.query.filter(Service.name==service_name).first().description
        name_m = m
        exp=Servicemen.query.filter(Servicemen.name==m).first().experience
        dex=Servicemen.query.filter(Servicemen.name==m).first().description
        rate=Servicemen.query.filter(Servicemen.name==m).first().rating
        imgx=Servicemen.query.filter(Servicemen.name==m).first().imgx
        return render_template('profile.html',id=id,imgx=imgx,service_name=service_name,service_desc=service_desc,name_m=name_m,exp=exp,dex=dex,rate=rate)
    
    @app.route('/professional/<int:id>',methods=['GET','POST'])
    def professional(id):
        yy=Servicemen.query.filter(Servicemen.id_u==id).first().id
        m=Servicemen.query.filter(Servicemen.id_u==id).first().name
        if(Servicemen.query.filter(Servicemen.id_u==id).first().status=='n_verified'):
            return """ 
        <html>
            <head><title>Verification Pending</title></head>
            <body>
            <h2 style="margin-left:45vw;margin-top:40vh;"><i>Urbanlife</i><h2>
                <h3 style="margin-left:40vw;margin-top:5vh;">You will be notified shortly</h3>
            </body>
        </html>
        """
        print(yy)
        Sx= ServiceOffer.query.filter(ServiceOffer.sm_id == yy, ServiceOffer.service_status=='undone').all()
        print(Sx)
        N = [
               {
                'sid'  : S.id,
                'sname': Service.query.filter(Service.id ==S.s_id).first().name,
                'sman': Servicemen.query.filter(Servicemen.id ==S.sm_id).first().name,
                'date': S.DoRequest,
                'status': S.service_status
            }
            for S in Sx
        ]
        Sk= ServiceOffer.query.filter(ServiceOffer.sm_id == yy,ServiceOffer.service_status=='done').all()
        O = [
               {
                'sid'  : S.id,
                'sname': Service.query.filter(Service.id ==S.s_id).first().name,
                'sman': Servicemen.query.filter(Servicemen.id ==S.sm_id).first().name,
                'date': S.DoRequest,
                'status': S.service_status
            }
            for S in Sk
        ]
        print(N,O)
        return render_template('profession.html',N=N,O=O,m=m,idd=id)
    
    @app.route('/accept/<int:sid>',methods=['POST'])
    def accept(sid):
        x=ServiceOffer.query.filter(ServiceOffer.id==sid).first()
        x.service_status='done'
        db.session.commit()
        current_date = datetime.now()
        tt= current_date.strftime("%Y-%m-%d")
        x.DoComplete=tt
        db.session.commit()
        return jsonify({'statusofit': 'ok'})
    
    @app.route('/reject/<int:sid>',methods=['POST'])
    def reject(sid):
        A=ServiceOffer.query.filter(ServiceOffer.id==sid).first()
        A.service_status='p_reject'
        db.session.commit()
        email=User.query.filter(User.id==A.c_id).first().email
        p=Servicemen.query.filter(Servicemen.id==A.sm_id).first().name
        do=A.DoRequest
        st=Service.query.filter(Service.id==A.s_id).first().name
        sender_email = "suneha2003datta@gmail.com"
        receiver_email = "suvadipbanerjee02@gmail.com"
        subject = "Order Canceled"
        body = "This is to inform your ordered service of order id "+ str(sid) +" has been rejected by professional you selected . The details were provided here \n Professioanl name " + p + "\n " + " Service type  " + st + "\n "+ " Date of order " + do + " \n"+"Regards Urbanlife"
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(sender_email,'hevejrxokhqmxswp')
        print(body)
        server.sendmail(sender_email,receiver_email,body)
        print('donr')
        
        return jsonify({'statusofit': 'ok'})
    
    @app.route('/verifyou/<int:idu>',methods=['GET','POST'])
    def verifyou(idu):
        if request.method=='GET':
            Sx=Service.query.all()
            SS = [S.name for S in Sx]
            return render_template('verifyou.html',idu=idu,SS=SS)
        else:
            print('here')
            file = request.files['file']
            fn = file.filename
            if file:
                print('yes')
            file_path = "C:/Users/suneh/MAD2_23f1002574/profnew/"+fn
            file.save(file_path)
            sender_email = "suneha2003datta@gmail.com"
            receiver_email = "suvadipbanerjee02@gmail.com" #admin
            subject = "New Professional enrolled"
            body = "Please verify the newly joined professional. The details are attached "
            yag = yagmail.SMTP(sender_email, "hevejrxokhqmxswp")
            yag.send(receiver_email, subject, body, attachments=file_path)
            return jsonify({'statusofit': 'ok'})
        
    @app.route('/getin',methods=['POST'])
    def getin():
        if request.method=='POST':
            data=request.get_json()
            print(data)
            sn=data['sname']
            i=data['imgc']
            e=data['exp']
            d=data['des']
            u=data['idu']
            n=User.query.filter(User.id==u).first().username
            current_date = datetime.now()
            tt= current_date.strftime("%d.%m.%Y")
            news=Servicemen(id_u=u,name=n,Docreate=tt,service=sn,experience=e,description=d,status='n_verified',imgx=i)
            db.session.add(news)
            db.session.commit()
            return jsonify({'statusofit': 'ok'})
        
    @app.route('/admin',methods=['GET','POST'])
    def admin():
        Cx= Cx = User.query.filter(User.roles  == 'customer').all()
        C = [
               {
                'id'  : c.id,
                'name': c.username,
                'email': c.email
            }
            for c in Cx
        ]
        Px= Servicemen.query.all()
        P = [
               {
                'id'  : p.id,
                'name': p.name,
                'doc': p.Docreate,
                'ser'  : p.service,
                'des': p.description,
                'exp': p.experience,
                'rate'  : p.rating,
                'status': p.status,
            }
            for p in Px
        ]
        Ox= ServiceOffer.query.all()
        O = [
               {
                'id'  : o.id,
                'sname': Service.query.filter(Service.id==o.s_id).first().name,
                'dob': o.DoRequest,
                'doc'  : o.DoComplete,
                'prof': Servicemen.query.filter(Servicemen.id==o.sm_id).first().name,
                'cust': User.query.filter(User.id==o.c_id).first().username,
                'remark'  : o.remarks,
                'status': o.service_status,
                'cno': o.c_no,
            }
            for o in Ox
        ]
        Sx= Service.query.all()
        S = [
               {
                'id'  : s.id,
                'name': s.name,
                'price': s.price,
                'dex':s.description,
                'time':s.time
            }
            for s in Sx
        ]
        return render_template('admin.html',CC=C,PP=P,OO=O,SS=S)
    
    @app.route('/custhist/<int:id>',methods=['GET'])
    def custhist(id):
        ofd=ServiceOffer.query.filter(ServiceOffer.c_id==id).all()
        Serv=[]
        Cancel=0
        count = len(ofd)
        Price=[]
        for item in ofd:
            Serv.append(Service.query.filter(Service.id==item.s_id).first().name)
            Price.append(Service.query.filter(Service.id==item.s_id).first().price)
            if item.service_status == 'c_reject':
                Cancel+=1
        non=count-Cancel
        pi=[non,Cancel]
        item_counts = Counter(Serv)
        labels, counts = zip(*item_counts.items())
        plt.figure(figsize=(8, 6))
        plt.bar(labels, counts)
        plt.xticks(rotation=45)
        plt.xlabel('Services Opted')
        plt.ylabel('Count')
        plt.tight_layout()  
        plt.savefig('C:/Users/suneh/MAD2_23f1002574/static/chist.png')
        plt.close()
        x_values = range(1, len(Price) + 1)
        plt.figure(figsize=(8, 6))
        plt.plot(x_values, Price, marker='o', linestyle='-', color='b')
        plt.tight_layout()
        plt.savefig('C:/Users/suneh/MAD2_23f1002574/static/line.png')
        plt.close()
        labels = ['Remaining Orders', 'Cancelled orders']
        plt.figure(figsize=(6, 6))
        plt.pie(pi, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.savefig('C:/Users/suneh/MAD2_23f1002574/static/cancel.png')
        plt.close()

        return render_template('custhist.html')
    
    @app.route('/profhist/<string:name>',methods=['GET'])
    def profhist(name):
        him=Servicemen.query.filter(Servicemen.name==name).first().id
        hims=Servicemen.query.filter(Servicemen.name==name).first().service
        himss=Service.query.filter(Service.name==hims).first().id
        X= ServiceOffer.query.filter(ServiceOffer.sm_id==him).all()# total services of him
        xc=len(ServiceOffer.query.filter(ServiceOffer.sm_id==him,ServiceOffer.service_status=='p_reject').all())
        x=len(X)-xc
        Y= ServiceOffer.query.filter(ServiceOffer.s_id==himss).all()# total services of his service type 
        yc=len(ServiceOffer.query.filter(ServiceOffer.sm_id==him,ServiceOffer.service_status=='done').all())
        y=len(Y)-yc
        rej=[xc,x]
        done=[yc,y]
        labels = ['Rejected Orders', 'Remaining offered']
        plt.figure(figsize=(6, 6))
        plt.pie(rej, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.savefig('C:/Users/suneh/MAD2_23f1002574/static/rej.png')
        plt.close()
        labels = ['Orders done ', 'remaining orders of this Service type']
        plt.figure(figsize=(6, 6))
        plt.pie(done, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.savefig('C:/Users/suneh/MAD2_23f1002574/static/done.png')
        plt.close()
        return render_template('profhist.html')

    @app.route('/custremove/<int:id>',methods=['POST'])
    def custremove(id):
        cause=request.get_json()
        h=User.query.filter(User.id==id).first()
        email=h.email
        sender_email = "suneha2003datta@gmail.com"
        receiver_email = "suvadipbanerjee02@gmail.com"
        subject = "Account deleted"
        body = "This is to inform that your account has been removed by admin due to the following cause \n " + cause
        yag = yagmail.SMTP(sender_email, "hevejrxokhqmxswp")
        yag.send(receiver_email, subject, body)  
        db.session.delete(h)
        db.session.commit()
        return jsonify({'statusofit': 'ok'})
    
    @app.route('/profverify/<string:name>',methods=['POST'])
    def profverify(name):
        S=Servicemen.query.filter(Servicemen.name==name).first()
        S.status='verified'
        db.session.commit()
        sender_email = "suneha2003datta@gmail.com"
        receiver_email = "suvadipbanerjee02@gmail.com"
        subject = "Profile Verified for login"
        body = "This is to inform that your profile has been approved by the admin. \n You can now login to your account . \n Thank you for your patience."
        yag = yagmail.SMTP(sender_email, "hevejrxokhqmxswp")
        yag.send(receiver_email, subject, body)  
        return jsonify({'statusofit': 'ok'})
    
    @app.route('/profunverify/<string:name>',methods=['POST'])
    def profunverify(name):
        S=Servicemen.query.filter(Servicemen.name==name).first()
        S.status='n_verified'
        db.session.commit()
        sender_email = "suneha2003datta@gmail.com"
        receiver_email = "suvadipbanerjee02@gmail.com"
        subject = "Account Under Verification"
        body = "This is to inform that your account has been marked under verification by admin due to some document misleading informations. \n Kindly wait for further communication " 
        yag = yagmail.SMTP(sender_email, "hevejrxokhqmxswp")
        yag.send(receiver_email, subject, body)  
        return jsonify({'statusofit': 'ok'})
    
    @app.route('/profremove/<string:name>',methods=['POST'])
    def profremove(name):
        cause=request.get_json()
        g=Servicemen.query.filter(Servicemen.name==name).first()
        #xx=g.id_u
        #h=User.query.filter(User.id==xx).first()
        #email=h.email
        #remove user
        sender_email = "suneha2003datta@gmail.com"
        receiver_email = "suvadipbanerjee02@gmail.com"
        subject = "Account deleted"
        body = "This is to inform that your account has been removed by admin due to the following cause \n " + cause
        yag = yagmail.SMTP(sender_email, "hevejrxokhqmxswp")
        yag.send(receiver_email, subject, body)  
        #db.session.delete(h)
        #db.session.commit()
        db.session.delete(g)
        db.session.commit()
        return jsonify({'statusofit': 'ok'})
    
    @app.route('/servicedes/<int:id>',methods=['POST'])
    def servicedes(id):
        ddv=request.get_json()
        S=Service.query.filter(Service.id==id).first()
        S.description=ddv
        db.session.commit()
        return jsonify({'statusofit': 'ok'})
    
    @app.route('/servicep/<int:id>',methods=['POST'])
    def servicep(id):
        pp=request.get_json()
        S=Service.query.filter(Service.id==id).first()
        S.price=pp
        db.session.commit()
        return jsonify({'statusofit': 'ok'})
    
    @app.route('/ratee/<string:sman>',methods=['POST'])
    def ratee(sman):
        r=request.get_json()
        S=Servicemen.query.filter(Servicemen.name==sman).first()
        if S.rating==np.nan or S.rating=='':
            xu=0
        else:
            xu=S.rating
        S.rating=(xu+int(r))/2
        db.session.commit()
        return jsonify({'statusofit': 'ok'})
    
    @app.route('/hello',methods=['GET','POST'])
    def hello():
        if request.method=='POST':
            job=tasks.report.apply_async(countdown=10) # BURIMA
            result=job.wait()
            df = pd.DataFrame(result)
            csv_file = StringIO()
            df.to_csv(csv_file, index=False)
            csv_file.seek(0)  
            response = Response(
                   csv_file.getvalue(),
                   mimetype="text/csv",
                   headers={
                        "Content-Disposition": "attachment; filename=report.csv"
                   }
                )
            return response

    @app.route('/serviceAdd',methods=['POST'])
    def serviceAdd():
        if request.method=='POST':
            r=request.get_json()
            nam=r['namee']
            dexx=r['dex']
            imm=r['im']
            ppp=r['pp']
            ttt=r['tt']
            new=Service(name=nam,description=dexx,price=ppp,time=ttt,img=imm)
            db.session.add(new)
            db.session.commit()
            return jsonify({'statusofit': 'ok'})
    
    @app.route('/serviced/<int:id>',methods=['POST'])
    def serviced(id):
        if request.method=='POST':
            g=Service.query.filter(Service.id==id).first()
            db.session.delete(g)
            db.session.commit()
            return jsonify({'statusofit': 'ok'})
    
    @app.route('/blockk/<int:id>/<int:sid>',methods=['POST'])
    def blockk(id,sid):
        if request.method=='POST':
            new=Blocklist(c_id=id,sm_id=sid)
            db.session.add(new)
            db.session.commit()
            return jsonify({'statusofit': 'ok'})
    
    @app.route('/unblockk/<int:id>/<int:sid>',methods=['POST'])
    def unblockk(id,sid):
        if request.method=='POST':
            g=Blocklist.query.filter(Blocklist.c_id==id,Blocklist.sm_id==sid).first()
            db.session.delete(g)
            db.session.commit()
            return jsonify({'statusofit': 'ok'})
    
    @app.route('/nam/<int:n>',methods=['POST'])
    def nam(n):
        ddv=request.get_json()
        S=Servicemen.query.filter(Servicemen.id==n).first()
        mm=S.name
        U=User.query.filter(User.username==mm).first()
        U.username=ddv
        S.name=ddv
        db.session.commit()
        return jsonify({'statusofit': 'ok'})

    @app.route('/dep/<int:d>',methods=['POST'])
    def dep(d):
        ddv=request.get_json()
        S=Servicemen.query.filter(Servicemen.id==d).first()
        S.description=ddv
        db.session.commit()
        return jsonify({'statusofit': 'ok'})

    @app.route('/exp/<int:e>',methods=['POST'])
    def exp(e):
        ddv=request.get_json()
        S=Servicemen.query.filter(Servicemen.id==e).first()
        S.experience=ddv
        db.session.commit()
        return jsonify({'statusofit': 'ok'})

    @app.route('/Search/<int:id>/<string:val>',methods=["POST","GET"])
    def Search(id,val):
        if request.method == "GET":
            u = User.query.filter(User.id == id).first()
            un=u.username
            Sx= Service.query.all()
            H = [
                {
                    'name': S.name,
                    'img': S.img,
                    'description': S.description,
                    'price': S.price,
                    'time': S.time
                }
                for S in Sx
            ]
            X=[]
            print(H,H[0])
            for item in H:
                if item['name'] == val: # if similarity of val with item.name
                    X.append(item)
            return render_template('customerS.html',un=un,SS=X,idd=id)

        

      

            
