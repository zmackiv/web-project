from flask import Blueprint, render_template, request
from service.product_service import ProductService
from service.category_service import CategoryService

homepage = Blueprint('homepage', __name__)


@homepage.route("/")
def view_homepage():
    typy_stroje_id_typstroje = request.args.get('typy_stroje_id_typstroje', None, int)
    stroje = ProductService.get_all(typy_stroje_id_typstroje)
    typy_stroje = CategoryService.get_by_id(typy_stroje_id_typstroje) if typy_stroje_id_typstroje is not None else None
    return render_template("index.jinja", stroje=stroje, typy_stroje=typy_stroje,
                           typy_stroje_id_typstroje=typy_stroje_id_typstroje)
