from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.product import Product
from app.utils.images import delete_product_image, is_allowed_file, upload_product_image

bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def _parse_price(raw):
    try:
        return Decimal(str(raw))
    except (InvalidOperation, TypeError):
        return None


def _parse_installment_plans(raw):
    """Keeps only well-formed {months, monthly} entries; silently drops the rest."""
    if not isinstance(raw, list):
        return []

    plans = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        try:
            months = int(entry.get("months"))
            monthly = float(entry.get("monthly"))
        except (TypeError, ValueError):
            continue
        if months > 0 and monthly >= 0:
            plans.append({"months": months, "monthly": monthly})
    return plans


def _parse_tags(raw):
    if not isinstance(raw, list):
        return []
    tags = [str(tag).strip() for tag in raw if str(tag).strip()]
    return tags[:8]


@bp.get("/products")
@jwt_required()
def list_all_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return jsonify({"items": [p.to_dict() for p in products]})


@bp.get("/products/<int:product_id>")
@jwt_required()
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())


@bp.post("/products")
@jwt_required()
def create_product():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "Product name is required."}), 400

    price = _parse_price(data.get("price"))
    if price is None or price < 0:
        return jsonify({"error": "A valid, non-negative price is required."}), 400

    product = Product(
        description=(data.get("description") or "").strip(),
        price=price,
        currency=(data.get("currency") or "USD").upper(),
        category=(data.get("category") or "General").strip() or "General",
        subcategory=(data.get("subcategory") or "").strip(),
        brand=(data.get("brand") or "").strip(),
        images=data.get("images") or [],
        tags=_parse_tags(data.get("tags")),
        installment_plans=_parse_installment_plans(data.get("installment_plans")),
        in_stock=bool(data.get("in_stock", True)),
        is_active=bool(data.get("is_active", True)),
    )
    product.set_name(name)

    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201


@bp.put("/products/<int:product_id>")
@jwt_required()
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json(silent=True) or {}

    if "name" in data:
        name = (data.get("name") or "").strip()
        if not name:
            return jsonify({"error": "Product name cannot be empty."}), 400
        product.set_name(name)

    if "price" in data:
        price = _parse_price(data.get("price"))
        if price is None or price < 0:
            return jsonify({"error": "A valid, non-negative price is required."}), 400
        product.price = price

    if "description" in data:
        product.description = (data.get("description") or "").strip()
    if "currency" in data:
        product.currency = (data.get("currency") or "USD").upper()
    if "category" in data:
        product.category = (data.get("category") or "General").strip() or "General"
    if "subcategory" in data:
        product.subcategory = (data.get("subcategory") or "").strip()
    if "brand" in data:
        product.brand = (data.get("brand") or "").strip()
    if "images" in data:
        product.images = data.get("images") or []
    if "tags" in data:
        product.tags = _parse_tags(data.get("tags"))
    if "installment_plans" in data:
        product.installment_plans = _parse_installment_plans(data.get("installment_plans"))
    if "in_stock" in data:
        product.in_stock = bool(data.get("in_stock"))
    if "is_active" in data:
        product.is_active = bool(data.get("is_active"))

    db.session.commit()
    return jsonify(product.to_dict())


@bp.delete("/products/<int:product_id>")
@jwt_required()
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    for image_url in product.images or []:
        delete_product_image(image_url)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted."})


@bp.post("/upload-image")
@jwt_required()
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files["file"]
    if file.filename == "" or not is_allowed_file(file.filename):
        return jsonify({"error": "Unsupported or missing file."}), 400

    try:
        url = upload_product_image(file)
    except Exception as exc:  # Cloudinary/network errors
        return jsonify({"error": f"Image upload failed: {exc}"}), 502

    return jsonify({"url": url}), 201
