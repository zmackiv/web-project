from flask import render_template, Blueprint

contactpage = Blueprint('contactpage', __name__)


@contactpage.route("/")
def view_contact_page():
    return render_template("contacts.jinja")