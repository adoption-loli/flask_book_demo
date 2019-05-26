from flask import Flask,render_template
from flask_pagedown import PageDown
from flask_wtf import Form
from wtforms.validators import required
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField


pagedown = PageDown()
app = Flask(__name__)
pagedown.init_app(app)
app.config["SECRET_KEY"] = "12345678"


class PostForm(Form):
    body = PageDownField("Post:", validators=[required()])
    submit = SubmitField("Submit")


@app.route('/')
def hello_world():
    form=PostForm()
    return render_template('new_post.html', form=form)


if __name__ == '__main__':
    app.run()
