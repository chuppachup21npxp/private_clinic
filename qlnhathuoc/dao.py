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
    query = Medicine.query.filter(is_stop == False)
    if id:
        query = query.filter(Medicine.id == int(id))
    if name:
        query = query.filter(Medicine.medicine_name.contains(name))
    return query.all()



def count_medicine_by_cate():
    return db.session.query(TypeMedicine.id, TypeMedicine.type_medicine_name, func.count(Medicine.id))\
                     .join(Medicine, Medicine.type_medicine_id.__eq__(TypeMedicine.id), isouter=True)\
                     .group_by(TypeMedicine.id).all()