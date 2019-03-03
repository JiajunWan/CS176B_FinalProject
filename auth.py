from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class AuthForm(FlaskForm):
    authcode = StringField('AuthCode', validators=[DataRequired()])   
    submit = SubmitField('Submit')