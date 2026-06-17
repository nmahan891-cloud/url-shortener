from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, URLField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, URL, Optional
from wtforms.validators import ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('این نام کاربری قبلاً ثبت شده است.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('این ایمیل قبلاً ثبت شده است.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class URLForm(FlaskForm):
    original_url = URLField('URL', validators=[DataRequired(), URL()])
    custom_code = StringField('Custom Code', validators=[Optional(), Length(min=3, max=20)])
    expires_days = SelectField('Expires', choices=[
        (0, 'Never'),
        (1, '1 Day'),
        (7, '7 Days'),
        (30, '30 Days'),
        (90, '90 Days')
    ], coerce=int)
    submit = SubmitField('Shorten URL')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Message')