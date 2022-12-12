from qlnhathuoc.models import User, Medicine, TypeMedicine, Patient, Receipt, DateMedical, MedicalRecord , Prescription
from qlnhathuoc import app, db
from flask_login import current_user
from sqlalchemy import func
import hashlib



def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def register(name, username, password, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(name=name, username=username.strip(), password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()




def load_medicine():
    return Medicine.query.all()

def get_medicine(id=None, name=None):
    query = Medicine.query.filter(Medicine.is_stop == False)
    if id:
        query = query.filter(Medicine.id == int(id))
    if name:
        query = query.filter(Medicine.medicine_name.contains(name))
    return query.all()

def stats_revenue(kw=None, from_date=None, to_date=None):
    query = db.session.query(Medicine.id, Medicine.medicine_name, Medicine.unit_current,
                            func.sum(Prescription.quantity * Medicine.price), func.count(Prescription.quantity * Medicine.price) ) \
        .join(Prescription, Prescription.medicine_id.__eq__(Medicine.id), isouter=True)

    if kw:
        query = query.filter(Medicine.medicine_name.contains(kw))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))

    return query.group_by(Medicine.id).order_by(Medicine.id).all()


def count_medicine_by_cate():
    return db.session.query(Medicine.id, Medicine.medicine_name, Medicine.unit_current,
                            func.sum(Prescription.quantity), func.count(Prescription.quantity) ) \
        .join(Prescription, Prescription.medicine_id.__eq__(Medicine.id), isouter=True) \
        .group_by(Medicine.id).all()


def total_revenue_medicine():
    return db.session.query( func.sum(Medicine.price * Prescription.quantity) ) \
        .join(Prescription, Prescription.medicine_id.__eq__(Medicine.id), isouter=True) \
        .filter(Medicine.id.__eq__(Prescription.medicine_id)).all()



def count_money_exam():
    return db.session.query(func.count(DateMedical.id) * 100000 ) \
            .filter(DateMedical.is_confirm.__eq__(1)).all()
