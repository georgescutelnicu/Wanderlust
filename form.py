from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class RegistrationForm(FlaskForm):
    """
        Form for user registration.

        Attributes:
            username (StringField): User's desired username.
            email (StringField): User's email address.
            password (PasswordField): User's password.
            confirm_password (PasswordField): Confirm user's password.
            submit (SubmitField): Submit button for form submission.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=16),
                                                   Regexp('^[a-zA-Z0-9]*$',
                                                          message='Username must contain only letters and numbers.')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """
        Form for user login.

        Attributes:
            email (StringField): User's email address.
            password (PasswordField): User's password.
            submit (SubmitField): Submit button for form submission.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
