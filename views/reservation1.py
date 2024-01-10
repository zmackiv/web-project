from flask import render_template, request, session, redirect, url_for, Blueprint
import forms
from datetime import datetime
from service.user_service import UserService
from service.order_service import OrderService

reservation1 = Blueprint('reservation1', __name__)


@reservation1.route("/", methods=['GET', 'POST'])
def view_reservation_page1():
    user_role = session.get('role')
    prihlasen = session.get('authenticated')
    if user_role == 'klient':
        form = forms.ReservationForm1(request.form)
        if request.method == 'POST' and form.validate():
            session['cas_od'] = request.form['cas_od']
            session['cas_do'] = request.form['cas_do']
            session['datum'] = request.form['datum']
            return redirect(url_for('reservation2.view_reservation_page2'))
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
                return redirect(url_for('reservation1.view_reservation_page1'))
            elif 'zrusit_submit' in request.form:
                OrderService.delete_order(order_id)
            return redirect(url_for('reservation1.view_reservation_page1'))
        return render_template("reservation.jinja", form=form, klient=klient, dostupni_technici=dostupni_technici, past_orders=past_orders, future_conf_orders=future_conf_orders, future_not_conf_orders=future_not_conf_orders, zruseni_orders=zruseni_orders)
    if prihlasen == None:
        return render_template("reservation.jinja")