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


class Index(db.Model):
    __tablename__ = 'indexs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.String(128))


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


@app.route('/if_login', methods=['GET', 'POST'])
def lsuss():
    index_library = [index for index in Index.query.all()]
    if g.username:
        return render_template('log.html',index_library=index_library)
    else:
        return render_template('ral.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('susername')
    password = request.form.get('spassword')
    user = User.query.filter(and_(User.username == username)).first()
    if not user:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
    else:
        return '已注册'
    return redirect(url_for('ral'))


@app.route('/add_index', methods=['POST'])
def add_index():
    title = request.form.get('title')
    content = request.form.get('content')
    if len(content) > 100:
        content = content[:100] + '...'
    if len(title) > 100:
         title = title[:100] + '...'
    index = Index(title=title, content=content)
    db.session.add(index)
    db.session.commit()
    return redirect(url_for('lsuss'))


@app.before_request
def test():
    username = session.get('username')
    password = session.get('password')
    g.username = None
    if username:
        user = User.query.filter(and_(User.username == username, User.password == password)).first()
        if user:
            g.username = username


@app.context_processor
def name():
    username = session.get('username')
    return {'username': username}


db.drop_all()
db.create_all()


if __name__ == '__main__':
    app.run(Debug=True)
