from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class UserRegistrationForm(FlaskForm):
    #Things to add- email,pass,university_id,firstname,lastname
    first_name= StringField('First Name 1',validators=[DataRequired(),Length(max=20)])
    last_name= StringField('Last Name 1',validators=[DataRequired(),Length(max=20)])
    email=StringField('Email 1 ', validators=[Email(),DataRequired(),Length(max=40)])
    password=PasswordField('Password 1',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Passoword 1', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up 1')

class LoginForm(FlaskForm):
    email = StringField('Email 1',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password 1', validators=[DataRequired()])
    remember = BooleanField('Remember Me 1')
    submit = SubmitField('Login 1')

    
    
    
    
    

