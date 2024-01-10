from flask import render_template, request, flash, session, redirect, url_for, Blueprint
import forms
from service.user_service import UserService

accountpage = Blueprint('accountpage', __name__)


@accountpage.route("/", methods=['GET', 'POST'])
def view_account_page():
    sign_in_form = forms.SignInForm(request.form)
    registration_form = forms.RegistrationForm(request.form)
    if request.method == 'POST':
        if 'sign_in_submit' in request.form:
            user = UserService.verify(email=request.form['email'], password=request.form['password'])
            if not user:
                flash('Incorrect email or password')
            else:
                session['authenticated'] = 1
                session['id_uzivatele'] = user['id_uzivatele']
                session['email'] = user['email']
                session['jmeno'] = user['jmeno']
                session['prijmeni'] = user['prijmeni']
                session['role'] = user['nazev']
                flash('Success')
                return redirect(url_for('my_accountpage.view_my_account_page'))
        elif 'registration_submit' in request.form:
            UserService.registrate(
                request.form['name'],
                request.form['surname'],
                request.form['email'],
                request.form['password'],
            )
            flash('User inserted')
            return redirect(url_for('accountpage.view_account_page'))

    if session.get('authenticated'):
        return redirect(url_for('my_accountpage.view_my_account_page'))

    return render_template("account.jinja", sign_in_form=sign_in_form, registration_form=registration_form)
