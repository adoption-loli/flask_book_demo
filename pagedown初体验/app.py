from flask import Flask, render_template, redirect, url_for, flash, request
from flask_pagedown import PageDown
from flask_wtf import FlaskForm
from wtforms.validators import required
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField
from markdown import markdown
import bleach
from flask_sqlalchemy import SQLAlchemy


pagedown = PageDown()
app = Flask(__name__)
pagedown.init_app(app)
app.config["SECRET_KEY"] = "12345678"


class PostForm(FlaskForm):
    body = PageDownField("Post:")
    submit = SubmitField("Submit")


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    forms = PostForm()
    return render_template('new_post.html', form=forms)


@app.route('/print', methods=['POST'])
def print123():
    form = PostForm(request.form)
    print(str(form.body.data))
    return 'hhh'


if __name__ == '__main__':
    app.run()
