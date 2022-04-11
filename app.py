from os import name
from flask import Flask, render_template, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import StringField, TextAreaField, Form, PasswordField, validators
import passlib.hash
from wtforms.fields.core import BooleanField


app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "py_blog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


class RegistrationForm(Form):
    name = StringField("İsim", [validators.Length(min=4, max=25)])
    username = StringField('Kullanıcı Adı', [validators.Length(min=4, max=25)])
    email = StringField('Email ', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password uyuşmuyor')
    ])
    confirm = PasswordField('Pasword Tekrar')
    accept_tos = BooleanField('Kabul', [validators.DataRequired()])


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)

    if(request.method == "POST" and form.validate()):

        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        sorgu = "insert into users(name,username,email,password) values(%s,%s,%s,%s)"
        cursor.execute(sorgu, (name, username, email, password))
        mysql.connection.commit()
        cursor.close()
        return render_template('index.html', form=form)

    else:
        return render_template('register.html', form=form)


@app.route('/')
def index():
    articles = [
        {"id": "0", "title": "Başlık 1", "Content": "İçerik 1 "},
        {"id": "1", "title": "Başlık 2", "Content": "İçerik 2 "},
        {"id": "2", "title": "Başlık 3", "Content": "İçerik 3 "}

    ]

    return render_template("index.html", answer="Evet", articles=articles)


@app.route('/about')
def about():

    return render_template("about.html")


@app.route('/article/<string:id>')
def detail(id):

    return "Article ID: "+id


if __name__ == "__main__":
    app.run(debug=True)
