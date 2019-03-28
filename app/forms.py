from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import User, Pkg

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    phone = IntegerField('Mobile Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class PackageInfo(FlaskForm):

    package = IntegerField('Phone Number', validators=[DataRequired()])
    courier = SelectField('Courier', choices = [('Amazon','Amazon'),('Bluedart','BlueDart'),('Flipkart','Flipkart'),('PayTM','PayTM'),('FedEx','FedEx')],validators=[DataRequired()])
    submit = SubmitField('Add Courier')


