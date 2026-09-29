import re
import unicodedata
from datetime import datetime, timezone

from app.extensions import db


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True, default="")
    price = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="USD")
    category = db.Column(db.String(100), nullable=False, default="General", index=True)
    subcategory = db.Column(db.String(100), nullable=False, default="", index=True)
    brand = db.Column(db.String(100), nullable=False, default="")
    images = db.Column(db.JSON, nullable=False, default=list)
    tags = db.Column(db.JSON, nullable=False, default=list)
    installment_plans = db.Column(db.JSON, nullable=False, default=list)
    in_stock = db.Column(db.Boolean, nullable=False, default=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def set_name(self, name: str) -> None:
        self.name = name
        base_slug = slugify(name) or "product"
        slug = base_slug
        suffix = 1
        query = Product.query.filter_by(slug=slug)
        if self.id is not None:
            query = query.filter(Product.id != self.id)
        while query.first() is not None:
            suffix += 1
            slug = f"{base_slug}-{suffix}"
            query = Product.query.filter_by(slug=slug)
            if self.id is not None:
                query = query.filter(Product.id != self.id)
        self.slug = slug

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "price": float(self.price) if self.price is not None else None,
            "currency": self.currency,
            "category": self.category,
            "subcategory": self.subcategory or "",
            "brand": self.brand or "",
            "images": self.images or [],
            "tags": self.tags or [],
            "installment_plans": self.installment_plans or [],
            "in_stock": self.in_stock,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
