from flask import Flask
from database import database


from views.homepage import homepage
from views.reservation1 import reservation1
from views.reservation2 import reservation2
from views.contactpage import contactpage
from views.accountpage import accountpage
from views.my_accountpage import my_accountpage
from views.logoutpage import logoutpage

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)

app.register_blueprint(homepage, url_prefix='/')
app.register_blueprint(reservation1, url_prefix='/reservation1-2')
app.register_blueprint(reservation2, url_prefix='/reservation2-2')
app.register_blueprint(contactpage, url_prefix='/contacts')
app.register_blueprint(accountpage, url_prefix='/account')
app.register_blueprint(my_accountpage, url_prefix='/my_account')
app.register_blueprint(logoutpage, url_prefix='/logout')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)