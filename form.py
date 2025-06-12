from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp


PASSWORD_REGEX = Regexp(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%^&*()_+\[\]\.<>\?]).{6,18}$",
    message=(
        "Password must be 6 to 18 characters long, include uppercase, lowercase, "
        "number, and one special character from ~!@#$%^&*()_+[].<>?"
    )
)

USER_REGEX = Regexp(
    r"^[a-zA-Z0-9]{4,16}$",
    message="Username must be 4 to 16 characters long, containing only letters and numbers with no spaces."
)


class RegistrationForm(FlaskForm):
    """
        Form for user registration.

        Fields:
            username (StringField): User's desired username. 4-16 alphanumeric chars.
            email (StringField): User's email address.
            password (PasswordField): User's password with complexity requirements.
            confirm_password (PasswordField): Confirmation of the password.
            submit (SubmitField): Form submit button.
    """
    username = StringField("Username", validators=[
        DataRequired(message="Username is required."),
        USER_REGEX
    ])
    email = StringField("Email", validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address.")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="Password is required."),
        PASSWORD_REGEX
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo("password", message="Passwords must match.")
    ])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    """
        Form for user login.

        Fields:
            email (StringField): User's email address.
            password (PasswordField): User's password.
            submit (SubmitField): Form submit button.
    """
    email = StringField("Email", validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address.")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="Password is required."),
    ])
    submit = SubmitField("Log In")


class ResendVerificationForm(FlaskForm):
    """
        Form for resending account verification email.

        Fields:
            email (StringField): User's email address, required and must be valid.
            submit (SubmitField): Submit button to trigger resend.
    """
    email = StringField("Email", validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address.")
    ])
    submit = SubmitField("Resend Verification Email")
