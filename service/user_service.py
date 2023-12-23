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
            SELECT uzivatel.id, uzivatel.email, uzivatel.is_active, typy_uzivatele.id_typuzivatele
            FROM uzivatel 
            JOIN typy_uzivatele ON (typy_uzivatele_id_typuzivatele = typy_uzivatele.id_typyuzivatele)
            WHERE email = ? AND password = ?''', [email, hashed_passorwd.hexdigest()]).fetchone()
        if user:
            return user
        else:
            return None