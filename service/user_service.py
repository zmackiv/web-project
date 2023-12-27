import config
import hashlib
from database.database import get_db


class UserService():

    @staticmethod
    def verify(email, password):
        db = get_db()
        hashed_passorwd = hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode())
        # print(hashed_passorwd.hexdigest())

        user = db.execute('''
            SELECT uzivatel.id_uzivatele, uzivatel.email, uzivatel.jmeno, uzivatel.prijmeni, typy_uzivatele.nazev
            FROM uzivatel 
            JOIN typy_uzivatele ON (typy_uzivatele_id_typuzivatele = typy_uzivatele.id_typuzivatele)
            WHERE email = ? AND heslo = ?''', [email, hashed_passorwd.hexdigest()]).fetchone()
        if user:
            return user
        else:
            return None



    @staticmethod
    def registrate(name, surname, email, password):
        db = get_db()
        hashed_password = hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode())

        sql = '''
            INSERT INTO uzivatel (jmeno, prijmeni, email, heslo, typy_uzivatele_id_typuzivatele) VALUES (?, ?, ?, ?, ?)
        '''

        params = (name, surname, email, hashed_password.hexdigest(), 3)

        db.execute(sql, params)

        db.commit()