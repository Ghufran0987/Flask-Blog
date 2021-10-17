from enum import unique
from threading import currentThread
from flask import Flask,render_template,flash,redirect,url_for,request
from flask.sessions import NullSession
import flask_login
from flask_login.utils import login_user
import sqlalchemy
from form import RegistrationForm,LoginForm,UpdateForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
import secrets
from flask_login import LoginManager
from flask_login import UserMixin,current_user
from flask_login import logout_user,login_required
from PIL import Image
import os






app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']='230c3f69504bd95c3254d7ec81923f02'

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'


@login_manager.user_loader


def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(20),nullable=False,default='default.jpg')
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}','{self.password}'"
    
    


class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post'{self.title},{self.date_posted}'"

    






posts=[
    {
        'author':'dsadsad',
        'title':'Blog Post 1',
        'content':'First Post Content',
        'Date':'April 20 2021'
    },
    {
        'author':'dsadsad',
        'title':'Blog Post 2',
        'content':'First Post Content',
        'Date':'April 20 2021'
    },
    {
        'author':'dsadsad',
        'title':'Blog Post 3',
        'content':'First Post Content',
        'Date':'April 20 2021'
    },
    {
        'author':'dsadsad',
        'title':'Blog Post 4',
        'content':'First Post Content',
        'Date':'April 20 2021'
    }
]

@app.route("/")




@app.route("/hello_world")
def hello_world():
    return render_template('home.html',posts=posts)
@app.route("/register",methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for{form.username.data}!','success')
        return redirect(url_for('hello_world'))
    return render_template('register.html',title='Form',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hellow_world'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            return redirect(url_for('hello_world'))
        else:
            flash('Login Unsuccesfull')
    return render_template('login.html',title='Form',form=form)

@app.route("/logout")

def logout():
    logout_user()
    return redirect(url_for('hello_world'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form=UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()

        flash('Your Account Has Been Updated!!!','success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    

    image_file=url_for('static',filename='profile_pic/' + current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)
    
    
    

@app.route("/aboutus")
def aboutus():
    return render_template('about.html',title='About')




