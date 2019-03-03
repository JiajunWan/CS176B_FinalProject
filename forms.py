from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class InformationForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])   # Add possible address verification
    submit = SubmitField('Start')