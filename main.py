import os
from flask import Flask, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

class Administrator(db.Model):
    __tablename__ = 'administrator'
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(30), nullable = False)

    def __init__(self, login, password):
        self.login = login
        self.password = password



class Posts(db.Model):
    __tablename__ = 'posts'  
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)  
    img = db.Column(db.String(100), nullable=False) 
    continent = db.Column(db.String(100), nullable = False)
    created_on = db.Column(db.Date(), default = datetime.utcnow)

    def __init__(self, title, text, img, continent):
        self.title = title
        self.text = text
        self.img = img
        self.continent = continent



@app.route('/')

def index():
    message = 'Enter your login and password'
    return render_template('index.html', message=message)


@app.route('/admin', methods=['GET'])
def Admin():

    return render_template('login.html')


@app.route('/admin', methods=['POST'])
def admin_login():
    login = request.form['login']
    password = request.form['password']
    admin = Administrator.query.filter_by(login=login).all()

    if admin == []:
        message = "Enter correct login"
        return render_template('login.html', message=message)

    else: 
        if Administrator.query.filter_by(password=password).all() == []:
            message = "Enter correct password"
            return render_template('login.html', message=message)
        else:
            return render_template('adArticle.html')
   

@app.route('/add_post', methods=['GET'])
def post():
    return render_template('adArticle.html')

@app.route('/add_post', methods=['POST'])
def creap_post():

    title = request.form['title']
    text = request.form['text']
    URL = request.form['URL']
    continent = request.form['continent']

    row =  Posts(title, text, URL, continent)
    db.session.add(row)
    db.session.commit()
    return render_template('adArticle.html')


@app.route('/<username>')
def show_user_profile(username):
    return render_template ('index.html', user_name = username)
 

@app.route('/index/')
def index_hi():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/Articl')
def Article():
    articles = Posts.query.all()
    return render_template('discover.html', articles=articles)

@app.route('/details/<id>')
def details(id):
    article = Posts.query.filter_by(id=id).first()

    return render_template('details.html', article=article)

if __name__ == "__main__":
    app.run()