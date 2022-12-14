from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from qlnhathuoc import db,app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):  ##Quyền người dùng##
    ADMIN = 1
    USER = 2
    DOCTOR = 3
    NURSE = 4
    CASHIER = 5


class User(BaseModel, UserMixin):  ##Người dùng##
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    fullname = Column(String(50), nullable=False)
    sex = Column(String(10), nullable=False)
    avatar = Column(String(200), default='NULL')
    created_date = Column(DateTime, default=datetime.now())
    phone_number = Column(String(20), default='')
    email = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    phieuhenkham = relationship('DateMedical', backref='user', lazy=True)

    def __str__(self):
        return self.fullname


class DateMedical(BaseModel):  ##Phiếu hẹn khám##
    date_medical = Column(DateTime, default=datetime.now())
    patient_name = Column(String(50), nullable=False)
    is_confirm = Column(Boolean, default=0)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    phieukhambenh = relationship('MedicalRecord', backref='datemedical', lazy=True)


class Patient(BaseModel):  ##Bệnh nhân##
    patient_name = Column(String(50), nullable=False)
    sex = Column(String(15), nullable=False)
    number_of_id_card = Column(String(20), nullable=False)
    phone_number = Column(String(12), nullable=False)
    date_born = Column(DateTime, default=datetime.now())

    phieukhambenh = relationship('MedicalRecord', backref='patient', lazy=True)

    def __str__(self):
        return self.patient_name


class MedicalRecord(BaseModel):  ##Phiếu khám bệnh##
    predict_illness = Column(String(100), nullable=False)
    symptom = Column(String(200), default='')
    date_medical_id = Column(Integer, ForeignKey(DateMedical.id), nullable=False)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)

    hoadon = relationship('Receipt', backref='medicalrecord', lazy=True)


class Receipt(BaseModel):  ##Hóa đơn##
    created_date = Column(DateTime, default=datetime.now())
    medical_record_id = Column(Integer, ForeignKey(MedicalRecord.id), nullable=False)

    donthuoc = relationship('Prescription', backref='receipt', lazy=True)


class TypeMedicine(BaseModel): ##Loại thuốc##
    type_medicine_name = Column(String(60), nullable=False)
    short_description = Column(String(300))

    thuoc = relationship('Medicine', backref='typemedicine', lazy=True)

    def __str__(self):
        return self.type_medicine_name


class Medicine(BaseModel):  ##Thuốc##
    medicine_name = Column(String(60), nullable=False)
    descriptions = Column(String(500), nullable=False)
    price = Column(Float, default=0)
    unit_current = Column(String(20), nullable=False)
    is_stop = Column(Boolean, default=0)
    type_medicine_id = Column(Integer, ForeignKey(TypeMedicine.id), nullable=False)

    donthuoc = relationship('Prescription', backref='medicine', lazy=True)

    def __str__(self):
        return self.medicine_name


class Prescription(BaseModel):  ##Đơn thuốc##
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    quantity = Column(Float, default=1)
    note = Column(Text)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        import hashlib

        password = str(hashlib.md5('123'.encode('utf-8')).hexdigest())
        u1 = User(fullname='Nguyen Phuc', username='admin', password=password,
                  user_role=UserRole.ADMIN, sex='male', email='1951052155phuc@ou.edu.vn',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        u2 = User(fullname='Tran Phuc', username='user', password=str(hashlib.md5('1'.encode('utf-8')).hexdigest()),
                  user_role=UserRole.USER, sex='male', email='1951052155phuc@ou.edu.vn',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        u3 = User(fullname='Mai Phuc', username='doctor', password=str(hashlib.md5('1'.encode('utf-8')).hexdigest()),
                  user_role=UserRole.DOCTOR, sex='male', email='1951052155phuc@ou.edu.vn',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        u4 = User(fullname='Le Phuc', username='nurse', password=str(hashlib.md5('1'.encode('utf-8')).hexdigest()),
                  user_role=UserRole.NURSE, sex='female', email='1951052155phuc@ou.edu.vn',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        db.session.add_all([u1, u2, u3, u4])
        db.session.commit()