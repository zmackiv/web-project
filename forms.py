from wtforms import Form, IntegerField, StringField, SelectField, PasswordField, validators

class SignInForm(Form):
    email = StringField(name='email', label='Email', validators=[validators.Length(min=3, max=50), validators.InputRequired(), validators.Email()])
    password = PasswordField(name='password', label='Password', validators=[validators.Length(min=3), validators.InputRequired()])

