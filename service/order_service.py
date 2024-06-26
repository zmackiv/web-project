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
            'INSERT INTO objednavka (timestamp, datum, cas_od, cas_do, adresa_doruceni, vzdalenost_doruceni, poznamka, cena, potvrzeni, stroj_id_stroj, zruseni) VALUES (?, ?, ?, ?, ?, 0, ?, 0, 0, ?, 0)',
            [aktualni_cas, datum, cas_od, cas_do, adresa_doruceni, poznamka, stroj]
        )
        db.commit()

        id_posledni = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        db.execute(
            'INSERT INTO uzivatel_objednavka (uzivatel_id_uzivatele, objednavka_id_objednavka) VALUES (?, ?)',
            [uzivatel_id_uzivatele, id_posledni]
        )
        db.commit()

    @staticmethod
    def update_zruseni_order(id_objednavka):
        db = get_db()
        db.execute(
            'UPDATE objednavka SET zruseni = 1 WHERE id_objednavka = ?',
            [id_objednavka])
        db.commit()

    @staticmethod
    def get_past_user_orders( today_date = None, id_uzivatele = None):
        db = get_db()

        sql = '''
            SELECT objednavka.*, stroj.model
            FROM objednavka
            INNER JOIN uzivatel_objednavka ON objednavka.id_objednavka = uzivatel_objednavka.objednavka_id_objednavka
            INNER JOIN stroj ON objednavka.stroj_id_stroj = stroj.id_stroj
            WHERE 1=1 
            '''
        arguments = []

        if today_date is not None:
            sql += " and DATE(objednavka.datum) < ?"
            arguments.append(today_date)

        if id_uzivatele is not None:
            sql += " and uzivatel_objednavka.uzivatel_id_uzivatele = ?"
            arguments.append(id_uzivatele)



        return db.execute(sql, arguments).fetchall()

    @staticmethod
    def get_future_user_orders( today_date = None, id_uzivatele = None, conf = None, zruseni = None ):
        db = get_db()

        sql = '''
                SELECT objednavka.*, stroj.model
                FROM objednavka
                INNER JOIN uzivatel_objednavka ON objednavka.id_objednavka = uzivatel_objednavka.objednavka_id_objednavka
                INNER JOIN stroj ON objednavka.stroj_id_stroj = stroj.id_stroj
                WHERE 1=1 
                '''
        arguments = []

        if today_date is not None:
            sql += " and DATE(objednavka.datum) >= ?"
            arguments.append(today_date)

        if conf is not None:
            sql += " and objednavka.potvrzeni = ?"
            arguments.append(conf)

        if id_uzivatele is not None:
            sql += " and uzivatel_objednavka.uzivatel_id_uzivatele = ?"
            arguments.append(id_uzivatele)

        if zruseni is not None:
            sql += " and zruseni = ?"
            arguments.append(zruseni)

        return db.execute(sql, arguments).fetchall()

    def update_order(id_objednavka, technik, cena):
        db = get_db()

        db.execute(' UPDATE objednavka SET cena = ?, potvrzeni = 1 WHERE id_objednavka = ?',
                    [cena, id_objednavka])
        db.commit()

        db.execute(' INSERT INTO uzivatel_objednavka (uzivatel_id_uzivatele, objednavka_id_objednavka) VALUES (?, ?)',
                   [technik, id_objednavka])
        db.commit()

    def delete_order(id_objednavka):
        db = get_db()

        db.execute('DELETE FROM objednavka WHERE id_objednavka = ?', [id_objednavka])

        db.commit()

        db = get_db()

        db.execute('DELETE FROM uzivatel_objednavka WHERE objednavka_id_objednavka = ?', [id_objednavka])

        db.commit()


