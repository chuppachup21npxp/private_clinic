from flask import render_template, request, redirect, session, jsonify, url_for
from qlnhathuoc import app, dao, admin, login, __init__ , models
from flask_login import login_user, logout_user, login_required
from qlnhathuoc.decorators import annonymous_user
import cloudinary.uploader
import urllib


@app.route("/")
def index():

    return render_template('index.html')
@app.route("/info")
def info():
    return render_template('info.html')

@app.route("/info-doctor")
def info_doctor():
    return render_template('info-doctor.html')

@app.route("/doctor", methods=['post', 'get'])
@login_required
def doctor_checkup_medical():
    msg1=''
    check = dao.check_user_role(current_user, UserRole.DOCTOR)
    if check == False:
        msg1 = 'Bạn không có quyền ở trang này'

    return render_template('doctor/index.html', msg1=msg1, check=check)


@app.route("/contact")
def contact():
    check = True
    return render_template('contact.html', check=check)

@app.route('/login-doctor', methods=['post'])
def login_doctor():
    msg =''
    username = request.form['username']
    password = request.form['password']
    check = dao.check_user_role()

    user = dao.auth_user(username=username, password=password)
    if user:
        check = dao.check_user_role(user, UserRole.DOCTOR)
        if check == True:
            login_user(user=user)
            return redirect('/doctor')
        else:
            msg = 'Bạn không có quyền truy cập vào trang này'
    else:
        msg = 'Tên đăng nhập hoặc mật khẩu không đúng'
    return render_template('/doctor', msg=msg)

@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method.__eq__('post'):
        name = request.form['name']
        username = request.form.get['username']
        password = request.form.get['password']
        confirm = request.form.get['confirm']
        avatar = request.form.get['avatar']

        if password.__eq__(confirm):

            try:
                dao.register(name=name,
                             username=username,
                             password=password,
                             avatar=avatar)

                return redirect(url_for('login'))
            except:
                err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
@annonymous_user
def login_my_user():
    msg = ''
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user=user)
            check = dao.check_user_role(user, UserRole.DOCTOR)
            if check == True:
                return redirect(url_for('doctor_checkup_medical'))
            return redirect(url_for('index'))
        else:
            msg = 'tài khoản hay mật khẩu không chính xác'


    return render_template('login.html')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    from qlnhathuoc.admin import *
    app.run(debug=True)