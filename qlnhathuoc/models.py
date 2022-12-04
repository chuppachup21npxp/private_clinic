from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from src import db
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin



class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum): ##Quyền người dùng##
    ADMIN = 1
    USER = 2
    DOCTOR = 3
    NURSE = 4
    CASHIER = 5

class User(BaseModel, UserMixin): ##Người dùng##
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    fullname = Column(String(50), nullable=False)
    sex = Column(String(10), nullable=False)
    avatar = Column(String(200), default='NULL')
    created_date = Column(DateTime, default=datetime.now())
    phone_number = Column(String(20), default='')
    email = Column(String(50), nullable=False)
    user_role = Column(Enum(QuyenNguoiDung), default=QuyenNguoiDung.USER)

    phieuhenkham = relationship('DateMedical', backref='user', lazy=True)

    def __str__(self):
        return self.fullname

class DateMedical(BaseModel): ##Phiếu hẹn khám##
    date_medical = Column(DateTime, default=datetime.now())
    patient_name = Column(String(50), nullable=False)
    is_confirm = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    phieukhambenh = relationship('MedicalRecord', backref='datemedical', lazy=True)

class Patient(BaseModel): ##Bệnh nhân##
    patient_name = Column(String(50), nullable=False)
    sex = Column(String(15), nullable=False)
    number_of_id_card = Column(String(20), nullable=False)
    phone_number = Column(String(12), nullable=False)

    phieukhambenh = relationship('MedicalRecord', backref='patient', lazy=True)

    def __str__(self):
        return self.patient_name

class MedicalRecord(BaseModel): ##Phiếu khám bệnh##
    predict_illness = Column(String(100), nullable=False)
    symptom = Column(String(200), default='')
    date_medical_id = Column(Integer, ForeignKey(DateMedical.id), nullable=False)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)

    hoadon = relationship('Receipt', backref='medicalrecord', lazy=True)

class Receipt(BaseModel): ##Hóa đơn##
    created_date = Column(DateTime, default=datetime.now())
    medical_record_id = Column(Integer, ForeignKey(MedicalRecord.id), nullable=False)

    donthuoc = relationship('Prescription', backref='receipt', lazy=True)

class TypeMedicine(BaseModel):
    type_medicine_name = Column(String(60), nullable=False)
    description = descriptions = Column(String(300))

    thuoc = relationship('Medicine', backref='typemedicine', lazy=True)

    def __str__(self):
        return self.type_medicine_name

class Medicine(BaseModel):
    medicine_name = Column(String(60), nullable=False)
    descriptions = Column(String(500), nullable=False)
    price = Column(Float, default=0)
    unit_current = Column(String(20), nullable=False)
    type_medicine_id = Column(Integer, ForeignKey(TypeMedicine.id), nullable=False)

    donthuoc = relationship('Prescription', backref='medicine', lazy=True)

    def __str__(self):
        return self.medicine_name

class Prescription(BaseModel): ##Đơn thuốc##
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    quantity = Column(Float, default=1)
    note = Column(Text)