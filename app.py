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
    prihlasen = session.get('authenticated')
    if user_role == 'klient':
        form = forms.ReservationForm1(request.form)
        if request.method == 'POST':
            session['cas_od'] = request.form['cas_od']
            session['cas_do'] = request.form['cas_do']
            session['datum'] = request.form['datum']
            return redirect(url_for('view_reservation_page2'))
        return render_template("reservation.jinja", form=form)
    if user_role == 'technik':
        today_date = datetime.now().strftime('%Y-%m-%d')
        past_orders = OrderService.get_past_user_orders(today_date, session.get('id_uzivatele'))
        future_orders = OrderService.get_future_user_orders(today_date, session.get('id_uzivatele'))
        return render_template("reservation.jinja", past_orders=past_orders, future_orders=future_orders)

    if user_role == 'dispecer' or user_role == 'admin':
        form = forms.ObjednavkaForm(request.form)
        today_date = datetime.now().strftime('%Y-%m-%d')
        past_orders = OrderService.get_past_user_orders(today_date)
        future_conf_orders = OrderService.get_future_user_orders(today_date, conf=1)
        future_not_conf_orders = OrderService.get_future_user_orders(today_date, conf=0)
        zruseni_orders = OrderService.get_future_user_orders(today_date, zruseni=1)
        order_id = (request.form.get('id_objednavka'))
        klient = {}
        if future_not_conf_orders:
            for order in future_not_conf_orders:
                id_objednavka = order['id_objednavka']
                dostupni_technici = UserService.get_technik(id_objednavka)
                klient[id_objednavka] = UserService.get_klient(id_objednavka)
        else: dostupni_technici = []
        form.technik.choices = [(item['id_uzivatele'], item['prijmeni']) for item in dostupni_technici]
        if request.method == 'POST':
            if 'obj_submit' in request.form:
                OrderService.update_order(
                    id_objednavka=order_id,
                    technik=request.form['technik'],
                    cena=request.form['cena'],
            )
                return redirect(url_for('view_reservation_page1'))
            elif 'zrusit_submit' in request.form:
                OrderService.delete_order(order_id)
            return redirect(url_for('view_reservation_page1'))
        return render_template("reservation.jinja", form=form, klient=klient, dostupni_technici=dostupni_technici, past_orders=past_orders, future_conf_orders=future_conf_orders, future_not_conf_orders=future_not_conf_orders, zruseni_orders=zruseni_orders)
    if prihlasen == None:
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
            return redirect(url_for('view_account_page'))

    if session.get('authenticated'):
        return redirect(url_for('view_my_account_page'))

    return render_template("account.jinja", sign_in_form=sign_in_form, registration_form=registration_form)

# First endpoint
@app.route("/my_account", methods=['GET', 'POST'])
def view_my_account_page():
    if not session.get('authenticated'):
        return render_template("my_account.jinja")

    user_role = session.get('role')

    if user_role == 'klient':
        today_date = datetime.now().strftime('%Y-%m-%d')
        orders = OrderService.get_all_user_orders(session.get('id_uzivatele'))
        past_orders = OrderService.get_past_user_orders(today_date, session.get('id_uzivatele') )
        future_orders = OrderService.get_future_user_orders(today_date, session.get( 'id_uzivatele') )
        if request.method == 'POST':
            id_objednavka = request.form['id_objednavka']
            if 'delete' in request.form:
                OrderService.update_zruseni_order(id_objednavka)
            return redirect(url_for('view_my_account_page'))
        return render_template("my_account.jinja", past_orders=past_orders, future_orders=future_orders)
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
        all_users = UserService.get_all_users()
        if request.method == 'POST':
            akce = request.form['action']
            id_uzivatele = request.form['id_uzivatele']

            if akce == 'change_type':
                novy_typ_uctu = request.form['novy_typ_uctu']
                UserService.update_user_type(id_uzivatele, novy_typ_uctu)

            elif akce == 'delete':
                UserService.delete_user(id_uzivatele)

            return redirect(url_for('view_my_account_page'))

        return render_template("my_account.jinja", users=all_users)

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