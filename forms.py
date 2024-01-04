from wtforms import Form, IntegerField, StringField, SelectField, PasswordField, validators

class SignInForm(Form):
    email = StringField(name='email', label='Email', validators=[validators.Length(min=3, max=50), validators.InputRequired(), validators.Email()])
    password = PasswordField(name='password', label='Heslo', validators=[validators.Length(min=3), validators.InputRequired()])

class RegistrationForm(Form):
    name = StringField(name='name', label='Jméno', validators=[validators.Length(min=3, max=20), validators.InputRequired()])
    surname = StringField(name='surname', label='Příjmení', validators=[validators.Length(min=3, max=20), validators.InputRequired()])
    email = StringField(name='email', label='Email', validators=[validators.Length(min=3, max=50), validators.InputRequired(), validators.Email()])
    password = PasswordField(name='password', label='Heslo', validators=[validators.Length(min=3), validators.InputRequired()])

class AddProductForm(Form):
    model = StringField(name='model', label='Model', validators=[validators.Length(min=3, max=20), validators.InputRequired()])
    popis = StringField(name='popis', label='Popis', validators=[validators.Length(min=3, max=150), validators.InputRequired()])
    hod_cena = IntegerField(name='hod_cena', label='Hodinová cena', validators=[validators.Length(min=3, max=20), validators.InputRequired()])
    doprava = IntegerField(name='doprava', label='Cena dopravy za km', validators=[validators.Length(min=3, max=20), validators.InputRequired()])
    foto = StringField(name='foto', label='Foto', validators=[validators.Length(min=3, max=80), validators.InputRequired()])
    typy_stroje = SelectField('Typy strojů', choices=[])


class ReservationForm1(Form):
    datum = StringField(name='datum', label='Datum',
                       validators=[validators.Length(min=3, max=20), validators.InputRequired()])
    cas_od = IntegerField(name='cas_od', label='Čas od',
                          validators=[validators.Length(min=1, max=10), validators.InputRequired()])
    cas_do = IntegerField(name='cas_do', label='Čas do',
                        validators=[validators.Length(min=1, max=10), validators.InputRequired()])
