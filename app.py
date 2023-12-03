from flask import Flask, render_template
from database import database

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

@app.route("/account")
def view_account_page():
    return render_template("account.jinja")

# First endpoint
@app.route("/my_account")
def view_my_account_page():
    return render_template("my_account.jinja")

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)