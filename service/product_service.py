from database.database import get_db


class ProductService:

    @staticmethod
    def get_all(typy_stroje_id_typstroje = None):
        db = get_db()

        sql = "SELECT * FROM stroj WHERE 1=1 "
        arguments = []

        if typy_stroje_id_typstroje is not None:
            sql += " and typy_stroje_id_typstroje = ?"
            arguments.append(typy_stroje_id_typstroje)

        return db.execute(sql, arguments).fetchall()

    def get_dostupne(datum = None, cas_od = None, cas_do = None):
        db = get_db()

        sql = "SELECT id_stroj, model, foto, popis FROM stroj WHERE id_stroj NOT IN ( SELECT stroj_id_stroj FROM objednavka WHERE datum = ? AND ((cas_od >= ? AND cas_od < ?) OR(cas_do > ? AND cas_do <= ?) OR(cas_od <= ? AND cas_do >= ?)))"
        arguments = [datum, cas_od, cas_do, cas_od, cas_do, cas_od, cas_do]

        return db.execute(sql, arguments).fetchall()


    @staticmethod
    def insert_product(model, popis, hod_cena, doprava, foto, typy_stroje):
        db = get_db()
        db.execute(
            'INSERT INTO stroj (model, popis, hodinova_cena, cena_dopravy_km, foto, typy_stroje_id_typstroje) VALUES (?, ?, ?, ?, ?, ?)',
            [model, popis, hod_cena, doprava, foto, typy_stroje]
        )
        db.commit()