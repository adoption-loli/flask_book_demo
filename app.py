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


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    if user:
        session['username'] = username
        return 'username'
    else:
        return '用户名或密码错误'


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()


@app.before_request
def test():
    username = session.get('username')
    if username:
        return render_template('log.html')
    else:
        ral()


@app.context_processor
def name():
    username = session.get('username')
    return { 'username': username }


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(Debug = True)
