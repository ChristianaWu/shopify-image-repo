from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, ValidationError, NumberRange, Optional
from flask_image_repo.models import Seller

class LoginForm (FlaskForm):
	email = StringField('Email',
		validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')
	
class SignupForm(FlaskForm):
    username = StringField('Username',
    	validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
    	validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        seller = Seller.query.filter_by(username=username.data).first()
        if seller:
            raise ValidationError('Choose a different username. This one is already taken.')

    def validate_email(self, email):
        seller = Seller.query.filter_by(email=email.data).first()
        if seller:
            raise ValidationError('This email already has an account.')

class BuyForm(FlaskForm):
    first_name = StringField('First Name',
        validators=[DataRequired(), Length(min=2, max=100)])
    last_name = StringField('Last Name',
        validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    address = StringField('Address',
        validators=[DataRequired()])
    payment = StringField('Payment',
        validators=[DataRequired()])
    submit = SubmitField('Buy')

class ImageForm(FlaskForm):
    name = StringField('First Name',
        validators=[Optional(), Length(min=2, max=100)])
    price = IntegerField('Price',
        validators=[Optional()])
    stock = IntegerField('Stock',
        validators=[Optional()])
    discount = IntegerField('Discount',
        validators=[Optional(), NumberRange(min=0, max=100)])
    submit = SubmitField('Update')







