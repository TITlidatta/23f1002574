from .database import db


class User(db.Model):
    __tablename__="User"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    username=db.Column(db.String(150))
    email=db.Column(db.String(150),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    active=db.Column(db.Integer,nullable=True)
    roles=db.Column(db.String(150))

class Servicemen(db.Model):
    __tablename__="Servicemen"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    id_u=db.Column(db.Integer,db.ForeignKey('User.id'))
    name=db.Column(db.String(150),db.ForeignKey('User.username'))
    Docreate=db.Column(db.String(10))
    service=db.Column(db.String(150),db.ForeignKey('Service.name'))
    experience=db.Column(db.String(150))
    description=db.Column(db.String(250))
    rating=db.Column(db.Integer)
    status=db.Column(db.String(150))
    imgx=db.Column(db.String(150))

class Service(db.Model):
    __tablename__="Service"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    name=db.Column(db.String(150))
    description=db.Column(db.String(150))
    price=db.Column(db.Integer)
    time=db.Column(db.Integer) #in hours
    img = db.Column(db.String(150))

class Blocklist(db.Model):
    __tablename__="Blocklist"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    c_id=db.Column(db.Integer)
    sm_id=db.Column(db.Integer)

class ServiceOffer(db.Model):
    __tablename__="ServiceOffer"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    sm_id=db.Column(db.Integer,db.ForeignKey('Servicemen.id'))
    s_id=db.Column(db.Integer,db.ForeignKey('Service.id'))
    c_id=db.Column(db.Integer,db.ForeignKey('User.id'))
    DoRequest=db.Column(db.String(10))
    DoComplete=db.Column(db.String(10))
    service_status=db.Column(db.String(150))
    remarks=db.Column(db.String(150))
    c_no = db.Column(db.String(15))
    