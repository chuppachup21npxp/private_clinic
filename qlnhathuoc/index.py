from flask import render_template, request, redirect, session, jsonify
from qlnhathuoc import app, dao, admin, login, utils
from flask_login import login_user, logout_user
from qlnhathuoc.decorators import annonymous_user
import cloudinary.uploader


@app.route("/")
def index():
    return render_template('index.html',)
@app.route("/info")
def info():
    return render_template('info.html')

@app.route("/doctor")
def doctor():
    return render_template('doctor.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

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
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=password,
                             avatar=avatar)

                return redirect('/login')
            except:
                err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
@annonymous_user
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            n = request.args.get("next")
            return redirect(n if n else '/')

    return render_template('login.html')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if _name_ == '_main_':
    app.run(debug=True)