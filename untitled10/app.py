from flask import Flask, render_template, redirect, url_for, flash, request, g, jsonify, Response
from flask_pagedown import PageDown
from flask_wtf import FlaskForm
from wtforms.validators import required
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField, StringField
import markdown
import bleach
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_wtf.csrf import CSRFProtect
import os


pagedown = PageDown()
app = Flask(__name__)
pagedown.init_app(app)
app.config["SECRET_KEY"] = "12345678"
csrf = CSRFProtect(app)


@app.route('/')
def editor():
    return render_template('ckeditor5.html')


@csrf.exempt
@app.route('/img', methods=['POST'])
def img_load():
    file = request.files['upload']
    suffix = file.filename.rsplit('.', 1)[1]
    name = uuid.uuid4().hex + '.' + suffix
    while os.path.exists(os.path.join(os.getcwd(), 'static', name)):
        name = uuid.uuid4().hex + '.' + suffix
    file.save(os.path.join(os.getcwd(), 'static', name))
    response = {
                'uploaded': True,
                'url': 'imgs/' + name
                }
    return jsonify(response)


@app.route('/imgs/<img_name>')
def load(img_name):
    image = os.path.join(os.getcwd(), 'static', img_name)
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


@app.route('/edit', methods=['POST'])
def ck_editor():
    form = request.form.get('content')
    print(form)
    return redirect(url_for('editor'))