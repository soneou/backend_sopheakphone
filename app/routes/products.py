from flask import Blueprint, jsonify, request

from app.models.product import Product

bp = Blueprint("products", __name__, url_prefix="/api/products")


@bp.get("")
def list_products():
    query = Product.query.filter_by(is_active=True)

    category = request.args.get("category")
    if category:
        query = query.filter(Product.category == category)

    subcategory = request.args.get("subcategory")
    if subcategory:
        query = query.filter(Product.subcategory == subcategory)

    brand = request.args.get("brand")
    if brand:
        query = query.filter(Product.brand == brand)

    search = request.args.get("search")
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    page = request.args.get("page", default=1, type=int)
    per_page = min(request.args.get("per_page", default=24, type=int), 100)

    pagination = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        {
            "items": [p.to_dict() for p in pagination.items],
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
        }
    )


@bp.get("/categories")
def list_categories():
    """Returns each active category with its distinct subcategories, e.g.
    [{"name": "Laptop", "subcategories": ["Notebook Consumer", ...]}, ...]
    """
    rows = (
        Product.query.filter_by(is_active=True)
        .with_entities(Product.category, Product.subcategory)
        .distinct()
        .all()
    )

    tree = {}
    for category, subcategory in rows:
        subs = tree.setdefault(category, set())
        if subcategory:
            subs.add(subcategory)

    categories = [
        {"name": name, "subcategories": sorted(subs)}
        for name, subs in sorted(tree.items())
    ]
    return jsonify({"categories": categories})


@bp.get("/<slug>")
def get_product(slug):
    product = Product.query.filter_by(slug=slug, is_active=True).first()
    if not product:
        return jsonify({"error": "Product not found."}), 404
    return jsonify(product.to_dict())
