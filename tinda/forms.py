from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    submit = SubmitField('Sign in')

class RegisterUser(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    description = TextAreaField('description',
                        validators=[DataRequired()])
    date = DateField('Date of birth',
                        validators=[DataRequired()])
    location = SelectField('Country',
                        choices=[], validators=[DataRequired()])
    submit = SubmitField('Register')



# class AddCustomerForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#     CPR_number = IntegerField('CPR_number',
#                         validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Add')


# class DirectCustomerLoginForm(FlaskForm):
#     p = IntegerField('CPR_number!!!', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')

# class CustomerLoginForm(FlaskForm):
#     id = IntegerField('CPR_number!!!!', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')

# class EmployeeLoginForm(FlaskForm):
#     id = IntegerField('Id', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')

# class TransferForm(FlaskForm):
#     amount = IntegerField('amount', 
#                         validators=[DataRequired()])
#     #sourceAccountTest = SelectField('From Account test:', choices=dropdown_choices, validators=[DataRequired()])
#     sourceAccount = SelectField('From Account:'  , choices=[], coerce = int, validators=[DataRequired()])
#     targetAccount = SelectField('Target Account:', choices=[], coerce = int, validators=[DataRequired()])
#     submit = SubmitField('Confirm')

# class DepositForm(FlaskForm):
#     amount = IntegerField('amount', 
#                        validators=[DataRequired()])
#     submit = SubmitField('Confirm')
    
# class InvestForm(FlaskForm):
#     submit = SubmitField('Confirm')