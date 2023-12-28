from database.database import get_db


class ProductService:

    @staticmethod
    def get_all(typy_stroje_id_typstroje = None):
        db = get_db()

        sql = "SELECT * FROM stroj WHERE 1=1 "
        arguments = []

        if typy_stroje_id_typstroje is not None:
            sql += " and typy_stroje_id_typstroje <= ?"
            arguments.append(typy_stroje_id_typstroje)

        return db.execute(sql, arguments).fetchall()


    @staticmethod
    def insert_product(model, popis, hod_cena, doprava, foto, typy_stroje):
        db = get_db()
        db.execute(
            'INSERT INTO stroj (model, popis, hodinova_cena, cena_dopravy_km, foto, typy_stroje_id_typstroje) VALUES (?, ?, ?, ?, ?, ?)',
            [model, popis, hod_cena, doprava, foto, typy_stroje]
        )
        db.commit()