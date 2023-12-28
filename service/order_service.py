from database.database import get_db


class OrderService:

    @staticmethod
    def get_all_user_orders(id_uzivatele):
        db = get_db()

        sql = '''
            SELECT objednavka.* FROM objednavka
            INNER JOIN uzivatel_objednavka ON objednavka.id_objednavka = uzivatel_objednavka.objednavka_id_objednavka
            WHERE uzivatel_objednavka.uzivatel_id_uzivatele = ?
        '''
        arguments = [id_uzivatele]

        return db.execute(sql, arguments).fetchall()