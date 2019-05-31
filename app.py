from flask import Flask, render_template, redirect, url_for, flash, request, session, g, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired
from wtforms.fields import SubmitField, StringField
import markdown
from bs4 import BeautifulSoup
import nltk
import uuid
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header


app = Flask(__name__)

pagedown = PageDown(app)

app.config['SECRET_KEY'] = "afsfa"
csrf = CSRFProtect(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin@127.0.0.1:3306/userdata"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Subscribe(db.Model):
    __tablename__ = 'subscribes'
    id = db.Column(db.Integer, primary_key=True)
    adress = db.Column(db.String(128), unique=True)


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


@app.route('/')
def index():
    return redirect(url_for('ral'))


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
        return render_template('log.html', index_library=index_library)
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
    if g.username:
        title = request.form.get('title')
        content = request.form.get('content')
        con = BeautifulSoup(content, 'html.parser').get_text()[:100]
        indexs = Index(title=title[:128], content=con)
        db.session.add(indexs)
        db.session.commit()
        with open(os.path.join(os.getcwd(), 'templates', str(indexs.id)+'.html'), 'w') as html:
            html.write('<h1>' + title + '</h1>' + content)
        sendemail(title, 'http:////127.0.0.1:5000//details//str(indexs.id)')
    return redirect(url_for('lsuss'))


@csrf.exempt
@app.route('/img', methods=['POST'])
def img_load():
    file = request.files['upload']
    suffix = file.filename.rsplit('.', 1)[1]
    name = uuid.uuid4().hex + '.' + suffix
    while os.path.exists(os.path.join(os.getcwd(), 'static', 'imgs', name)):
        name = uuid.uuid4().hex + '.' + suffix
    file.save(os.path.join(os.getcwd(), 'static', 'imgs', name))
    response = {
                'uploaded': True,
                'url': '/static/imgs/' + name
                }
    return jsonify(response)


@app.route('/imgs/<img_name>')
def load(img_name):
    image = os.path.join(os.getcwd(), 'static', 'imgs', img_name)
    if not os.path.exists(image):
        return '', 404
    suffix = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif'
    }
    mine = suffix[str(image.rsplit('.', 1)[1])]
    with open(image, 'rb') as file:
        img = file.read()
    return Response(img, mimetype=mine)


@app.route('/details/<int:act_id>')
def details(act_id):
    return render_template(str(act_id)+'.html')


@app.before_request
def test():
    username = session.get('username')
    password = session.get('password')
    g.username = None
    if username:
        user = User.query.filter(and_(User.username == username, User.password == password)).first()
        if user:
            g.username = username


@app.route('/sendemail')
def sendemail(title, url):
    emails = [i for i in Subscribe.query.all()]
    e_mails = [i for i in emails.adress]
    smtp = smtplib.SMTP()
    smtp.connect('smtp.qq.com')
    prot: 465
    smtp.login('1509636344@qq.com', 'zxcaftjfhqtnibeb')
    message = MIMEText('<a href = "{}">{}</h1>'.format(url, title), 'html', 'utf-8')  # 邮件内容
    message['From'] = Header("adoption", 'utf-8')                             # 发送者
    message['To'] = Header("you", 'utf-8')                               # 接收者
    subject = '订阅更新啦'                                        # 邮件标题
    message['Subject'] = Header(subject, 'utf-8')                           # 还是邮件标题
    smtp.sendmail('1509636344@qq.com', e_mails, message.as_string())
    smtp.quit()


@app.route('/search', methods=['GET', 'POST'])
def search():
    aim = request.form.get('aim')
    print(aim)
    aims = [index for index in Index.query.filter(Index.title.like('%{}%'.format(aim)))]
    print(aims)
    return render_template('search.html', index=aims)


@app.context_processor
def name():
    username = session.get('username')
    return {'username': username}

'''
db.drop_all()
db.create_all()
'''

if __name__ == '__main__':
    app.run(Debug=True)
