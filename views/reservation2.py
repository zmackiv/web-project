from flask import render_template, request, session, redirect, url_for, Blueprint
import forms
from service.product_service import ProductService
from service.order_service import OrderService

reservation2 = Blueprint('reservation2', __name__)


@reservation2.route("/", methods=['GET', 'POST'])
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
            return redirect(url_for('my_accountpage.view_my_account_page'))
    return render_template("reservation2.jinja", form=form, dostupne_stroje=dostupne_stroje)