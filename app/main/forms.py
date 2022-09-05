from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.main.models import User

class Registrationform(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20, message='სახელის სიგრძე უნდა იყოს 5/20 სიმბოლო')], 
                           render_kw={"placeholder": "სახელი",
                                      'class': 'form-control',
                                      })
    email = EmailField('Email', validators=[DataRequired(), Email(message='ელ. ფოსტის ფორმატი არასწორია')], 
                       render_kw={"placeholder": "ელ.ფოსტა",
                                  'class': 'form-control',})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20, message='პაროლის სიგრძე უნდა იყოს 5/20 სიმბოლო')],
                             render_kw={"placeholder": "პაროლი",
                                    'class': 'form-control',})
    submit = SubmitField('Sign up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('ეს სახელი უკვე დაკავებულია')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('ეს ელ.ფოსტა უკვე დაკავებულია')
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(message='ელ. ფოსტის ფორმატი არასწორია')], 
                       render_kw={"placeholder": "ელ.ფოსტა",
                                  'class': 'form-control',})
                           
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20, message='პაროლის სიგრძე უნდა იყოს 5/20 სიმბოლო')],
                             render_kw={"placeholder": "პაროლი",
                                        'class': 'form-control',})
    submit = SubmitField('Sign in')
    
    def validate_auth(self, email, password):
        user = User.query.filter_by(email=email.data).first()
        if user is None or not user.check_password(password.data):
            raise ValidationError('არასწორი ელ. ფოსტა ან პაროლი')
    