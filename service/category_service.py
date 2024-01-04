from database.database import get_db


class CategoryService:

    @staticmethod
    def get_all():
        db = get_db()
        return db.execute(
            "SELECT * FROM typy_stroje"
        ).fetchall()

    @staticmethod
    def get_by_id(id):
        db = get_db()
        return db.execute(
            "SELECT * FROM typy_stroje WHERE id_typstroje = ?",
            [id]
        ).fetchone()