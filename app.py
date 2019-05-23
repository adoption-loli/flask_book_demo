from flask import Flask
from flask import Flask, render_template, redirect, url_for, flash, request,session,g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = "afsfa"
CSRFProtect(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin@127.0.0.1:3306/userdata"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128), unique=False)


@app.route('/ral', methods=['GET', 'POST'])
def ral():
    return render_template('ral.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    if user:
        session['username'] = username
        session['password'] = password
        return redirect(url_for('lsuss'))
    else:
        return '用户名或密码错误'


@app.route('/login', methods=['GET'])
def lsuss():
    return render_template('log.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('susername')
    password = request.form.get('spassword')
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('ral'))


@app.before_request
def test():
    username = session.get('username')
    password = session.get('password')
    if username:
        user = User.query.filter(and_(User.username == username, User.password == password)).first()
        if user:
            return render_template('log.html')


@app.context_processor
def name():
    username = session.get('username')
    return {'username': username}


db.drop_all()
db.create_all()


if __name__ == '__main__':
    app.run(Debug=True)
