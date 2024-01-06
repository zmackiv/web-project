from database.database import get_db
from datetime import datetime


class OrderService:

    @staticmethod
    def get_all_user_orders(id_uzivatele):
        db = get_db()

        sql = '''
            SELECT objednavka.*, stroj.model FROM objednavka
            INNER JOIN uzivatel_objednavka ON objednavka.id_objednavka = uzivatel_objednavka.objednavka_id_objednavka
            INNER JOIN stroj ON objednavka.stroj_id_stroj = stroj.id_stroj
            WHERE uzivatel_objednavka.uzivatel_id_uzivatele = ?
        '''
        arguments = [id_uzivatele]

        return db.execute(sql, arguments).fetchall()

    @staticmethod
    def insert_order(datum, cas_od, cas_do, adresa_doruceni, poznamka, stroj, uzivatel_id_uzivatele):
        db = get_db()
        aktualni_cas = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute(
            'INSERT INTO objednavka (timestamp, datum, cas_od, cas_do, adresa_doruceni, vzdalenost_doruceni, poznamka, cena, potvrzeni, stroj_id_stroj, uzivatel_id_uzivatele) VALUES (?, ?, ?, ?, ?, 0, ?, 0, 0, ?, ?)',
            [aktualni_cas, datum, cas_od, cas_do, adresa_doruceni, poznamka, stroj, uzivatel_id_uzivatele]
        )
        db.commit()