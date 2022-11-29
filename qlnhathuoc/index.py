from flask import render_template, request, redirect, session, jsonify
from qlnhathuoc import app





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


if __name__ == '__main__':
    app.run(debug=True)