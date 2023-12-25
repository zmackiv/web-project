from flask import Flask, render_template, request, flash, session, redirect, url_for
from database import database
import forms
from service.user_service import UserService

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)

@app.route("/")
def view_homepage():
    return render_template("index.jinja")

@app.route("/reservation")
def view_reservation_page():
    return render_template("reservation.jinja")

@app.route("/contacts")
def view_contact_page():
    return render_template("contacts.jinja")

@app.route("/account", methods=['GET', 'POST'])
def view_account_page():
    form = forms.SignInForm(request.form)
    if request.method == 'POST':
        user = UserService.verify(email=request.form['email'], password=request.form['password'])
        if not user:
            flash('Incorrect email or password')
        else:
            session['authenticated'] = 1
            session['email'] = user['email']
            session['nazev'] = user['nazev']
            flash('Success')
            return redirect(url_for('view_my_account_page'))
    return render_template("account.jinja", form=form)

# First endpoint
@app.route("/my_account")
def view_my_account_page():
    return render_template("my_account.jinja")

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)