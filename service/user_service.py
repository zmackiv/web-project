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

    def get_technik(id_objednavka):
        db = get_db()

        objednavka_info = db.execute(
            "SELECT datum, cas_od, cas_do FROM objednavka WHERE id_objednavka = ?",
            [id_objednavka]
        ).fetchone()

        if not objednavka_info:
            return []

        datum, cas_od, cas_do = objednavka_info

        sql = '''SELECT id_uzivatele, prijmeni 
                 FROM uzivatel 
                 JOIN typy_uzivatele on uzivatel.typy_uzivatele_id_typuzivatele = typy_uzivatele.id_typuzivatele
                 WHERE id_uzivatele NOT IN 
                 ( SELECT uo.uzivatel_id_uzivatele 
                 FROM uzivatel_objednavka uo
            JOIN objednavka o ON uo.objednavka_id_objednavka = o.id_objednavka
            WHERE o.id_objednavka != ? AND (
                (o.datum = ? AND o.cas_od >= ? AND o.cas_od < ?) OR
                (o.datum = ? AND o.cas_do > ? AND o.cas_do <= ?) OR
                (o.datum = ? AND o.cas_od <= ? AND o.cas_do >= ?)
            )) and typy_uzivatele.nazev ='technik' '''
        arguments = [id_objednavka, datum, cas_od, cas_do, datum, cas_od, cas_do, datum, cas_od, cas_do]

        return db.execute(sql, arguments).fetchall()