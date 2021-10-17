



from os import X_OK
import flask
from flask_wtf import FlaskForm
import flask_wtf
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, EqualTo,Length,Email, ValidationError
from flask_login import current_user
from flask_wtf.file import FileField,FileAllowed 


class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])

    email=StringField('Email',validators=[DataRequired(),Email()])
    
    password=PasswordField('Password',validators=[DataRequired()])

    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])

    submit=SubmitField('Sign Up')


class UpdateForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])

    email=StringField('Email',validators=[DataRequired(),Email()])
    
    picture=FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])

    submit=SubmitField('Update')

    

    
    
class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    
    password=PasswordField('Password',validators=[DataRequired()])

    submit=SubmitField('Login')