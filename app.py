from flask import Flask, render_template, request, flash, session, redirect, url_for
from database import database
import forms
from datetime import datetime
from service.user_service import UserService
from service.product_service import ProductService
from service.category_service import CategoryService
from service.order_service import OrderService

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)

@app.route("/")
def view_homepage():
    typy_stroje_id_typstroje = request.args.get('typy_stroje_id_typstroje', None, int)
    stroje = ProductService.get_all(typy_stroje_id_typstroje)
    typy_stroje = CategoryService.get_by_id(typy_stroje_id_typstroje) if typy_stroje_id_typstroje is not None else None
    return render_template("index.jinja", stroje=stroje, typy_stroje=typy_stroje, typy_stroje_id_typstroje=typy_stroje_id_typstroje)

@app.route("/reservation1-2", methods=['GET', 'POST'])
def view_reservation_page1():
    user_role = session.get('role')
    if user_role == 'klient':
        form = forms.ReservationForm1(request.form)
        if request.method == 'POST':
            session['cas_od'] = request.form['cas_od']
            session['cas_do'] = request.form['cas_do']
            session['datum'] = request.form['datum']
            return redirect(url_for('view_reservation_page2'))
        return render_template("reservation.jinja", form=form)
    if user_role == 'technik':
        orders = OrderService.get_all_user_orders(session.get('id_uzivatele'))
        return render_template("reservation.jinja", orders=orders)

    if user_role == 'dispecer':
        return render_template("reservation.jinja")
    if user_role == 'admin':
        return render_template("reservation.jinja")

@app.route("/reservation2-2", methods=['GET', 'POST'])
def view_reservation_page2():
    form = forms.ReservationForm2(request.form)
    dostupne_stroje = ProductService.get_dostupne(session['datum'], session['cas_od'], session['cas_do'])
    form.stroj.choices = [(item['id_stroj'], item['model']) for item in dostupne_stroje]
    if request.method == 'POST':
        if 'reservation_submit' in request.form:
            OrderService.insert_order(
                datum=session['datum'],
                cas_od=session['cas_od'],
                cas_do=session['cas_do'],
                adresa_doruceni=request.form['adresa'],
                poznamka=request.form['poznamka'],
                stroj=request.form['stroj'],
                uzivatel_id_uzivatele=session['id_uzivatele'],
            )
            return redirect(url_for('view_my_account_page'))
    return render_template("reservation2.jinja", form=form, dostupne_stroje=dostupne_stroje)
@app.route("/contacts")
def view_contact_page():
    return render_template("contacts.jinja")

@app.route("/account", methods=['GET', 'POST'])
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
                return redirect(url_for('view_my_account_page'))
        elif 'registration_submit' in request.form:
            UserService.registrate(
                request.form['name'],
                request.form['surname'],
                request.form['email'],
                request.form['password'],
            )
            flash('User inserted')
            return redirect(url_for('view_my_account_page'))

    if session.get('authenticated'):
        return redirect(url_for('view_my_account_page'))

    return render_template("account.jinja", sign_in_form=sign_in_form, registration_form=registration_form)

# First endpoint
@app.route("/my_account", methods=['GET', 'POST'])
def view_my_account_page():
    user_role = session.get('role')
    if user_role == 'klient':
        today_date = datetime.now().strftime('%d-%m-%Y')
        orders = OrderService.get_all_user_orders(session.get('id_uzivatele'))
        past_orders = OrderService.get_past_user_orders(session.get('id_uzivatele'), today_date)
        future_orders = OrderService.get_future_user_orders(session.get('id_uzivatele'), today_date)
        return render_template("my_account.jinja", past_orders=orders, future_orders=orders)
    if user_role == 'technik':
        return render_template("my_account.jinja")
    if user_role == 'dispecer':
        new_product_form = forms.AddProductForm(request.form)
        typy_stroje = CategoryService.get_all()
        new_product_form.typy_stroje.choices = [(item['id_typstroje'], item['nazev']) for item in typy_stroje]
        if request.method == 'POST':
            ProductService.insert_product(
                model=request.form['model'],
                popis=request.form['popis'],
                hod_cena=request.form['hod_cena'],
                doprava=request.form['doprava'],
                foto=request.form['foto'],
                typy_stroje=request.form['typy_stroje'],
            )
            flash('Stroj byl přidán')
        return render_template("my_account.jinja", new_product_form=new_product_form, typy_stroje=typy_stroje)
    if user_role == 'admin':
        return render_template("my_account.jinja")

@app.route('/logout')
def logout():
    session.pop('authenticated')
    session.pop('email')
    session.pop('role')
    session.pop('jmeno')
    session.pop('prijmeni')

    return redirect(url_for('view_homepage'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)