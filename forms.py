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
                          validators=[
                              validators.NumberRange(min=8, max=16, message="Čas musí být mezi 8 a 17"),
                              validators.InputRequired()
                          ])
    cas_do = IntegerField(name='cas_do', label='Čas do',
                          validators=[
                              validators.NumberRange(min=9, max=17, message="Čas musí být mezi 8 a 17"),
                              validators.InputRequired()
                          ])

    def validate(self):
        if not super().validate():
            return False

        if self.cas_od.data >= self.cas_do.data:
            self.cas_od.errors.append("Čas od musí být menší než čas do.")
            return False

        return True

class ReservationForm2(Form):
    adresa = StringField(name='adresa', label='',
                        validators=[validators.Length(min=3, max=40), validators.InputRequired()])
    poznamka = StringField(name='poznamka', label='',
                        validators=[validators.Length(min=0, max=100)])
    stroj = SelectField("", choices=[])

class ObjednavkaForm(Form):
    cena = StringField(name='cena', label='',
                           validators=[validators.Length(min=0, max=5)])
    technik = SelectField("", choices=[])
