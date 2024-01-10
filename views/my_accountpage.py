from flask import render_template, request, flash, session, redirect, url_for, Blueprint
import forms
from datetime import datetime
from service.user_service import UserService
from service.product_service import ProductService
from service.category_service import CategoryService
from service.order_service import OrderService

my_accountpage = Blueprint('my_accountpage', __name__)


@my_accountpage.route("/", methods=['GET', 'POST'])
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
            return redirect(url_for('my_accountpage.view_my_account_page'))
        return render_template("my_account.jinja", past_orders=past_orders, future_orders=future_orders)
    if user_role == 'technik':
        return render_template("my_account.jinja")
    if user_role == 'dispecer':
        new_product_form = forms.AddProductForm(request.form)
        typy_stroje = CategoryService.get_all()
        new_product_form.typy_stroje.choices = [(item['id_typstroje'], item['nazev']) for item in typy_stroje]

        stroje = ProductService.get_all_stroj_typ()

        if request.method == 'POST':
            akce = request.form['action']

            if akce == 'add':
                ProductService.insert_product(
                    model=request.form['model'],
                    popis=request.form['popis'],
                    hod_cena=request.form['hod_cena'],
                    doprava=request.form['doprava'],
                    foto=request.form['foto'],
                    typy_stroje=request.form['typy_stroje'],
                )
                flash('Stroj byl přidán')
            if akce == 'delete':
                id_stroj = request.form['id_stroj']
                ProductService.delete_product(id_stroj)

            return redirect(url_for('my_accountpage.view_my_account_page'))

        return render_template("my_account.jinja", new_product_form=new_product_form, typy_stroje=typy_stroje, stroje=stroje)
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

            return redirect(url_for('my_accountpage.view_my_account_page'))

        return render_template("my_account.jinja", users=all_users)
