from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def view_homepage():
    return render_template("index.jinja")

@app.route("/reservation")
def view_products_page():
    return render_template("reservation.jinja")

@app.route("/contacts")
def view_contact_page():
    return render_template("contacts.jinja")

@app.route("/account")
def view_account_page():
    return render_template("account.jinja")

# First endpoint
@app.route("/welcome")
def view_welcome_page():
    return render_template("welcome_page.jinja", name="Mr Yoda")


app.run('0.0.0.0', port=5000)