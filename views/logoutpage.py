from flask import session, redirect, url_for, Blueprint

logoutpage = Blueprint('logoutpage', __name__)


@logoutpage.route('/')
def logout():
    session.pop('authenticated')
    session.pop('email')
    session.pop('role')
    session.pop('jmeno')
    session.pop('prijmeni')

    return redirect(url_for('homepage.view_homepage'))