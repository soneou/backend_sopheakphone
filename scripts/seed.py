"""Seed the database with sample products across several categories.

Usage:
    python scripts/seed.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.extensions import db
from app.models.product import Product

SAMPLE_PRODUCTS = [
    # Smart Phone
    {
        "name": "Samsung Galaxy S24 - 8GB/256GB",
        "description": "6.2\" Dynamic AMOLED display, triple camera system, and all-day battery life.",
        "price": 799.00,
        "category": "Smart Phone",
        "subcategory": "Android",
        "brand": "Samsung",
        "images": ["https://picsum.photos/seed/galaxy-s24/600/600"],
        "tags": ["256GB", "New", "Battery 100%"],
        "installment_plans": [
            {"months": 6, "monthly": 140},
            {"months": 9, "monthly": 98},
            {"months": 12, "monthly": 76},
        ],
    },
    {
        "name": "Apple iPhone 15 - 128GB",
        "description": "A16 Bionic chip, Dynamic Island, and a 48MP main camera.",
        "price": 899.00,
        "category": "Smart Phone",
        "subcategory": "iPhone",
        "brand": "Apple",
        "images": ["https://picsum.photos/seed/iphone-15/600/600"],
        "tags": ["128GB", "Condition 98%", "Battery 92%"],
        "installment_plans": [
            {"months": 6, "monthly": 155},
            {"months": 9, "monthly": 109},
            {"months": 12, "monthly": 85},
        ],
    },
    {
        "name": "Xiaomi Redmi Note 13 - 8GB/256GB",
        "description": "Great value everyday phone with a 108MP camera and fast charging.",
        "price": 249.00,
        "category": "Smart Phone",
        "subcategory": "Android",
        "brand": "Xiaomi",
        "images": ["https://picsum.photos/seed/redmi-note13/600/600"],
        "tags": ["256GB", "New", "Battery 100%"],
        "installment_plans": [
            {"months": 6, "monthly": 46},
            {"months": 9, "monthly": 32},
        ],
    },
    # Computer / Laptop
    {
        "name": "Dell Latitude 5440 - Intel Core i5-1335U / 16GB / 512GB SSD",
        "description": "Business-grade 14\" laptop with a durable chassis, great battery life, and a fingerprint reader.",
        "price": 899.00,
        "category": "Computer",
        "subcategory": "Laptop",
        "brand": "Dell",
        "images": ["https://picsum.photos/seed/dell-latitude/600/600"],
        "tags": ["16GB RAM", "512GB SSD", "Condition 95%"],
    },
    {
        "name": "HP ProBook 440 G11 - Intel Core i7-1355U / 16GB / 1TB SSD",
        "description": "Sleek, lightweight business notebook built for productivity on the go.",
        "price": 1049.00,
        "category": "Computer",
        "subcategory": "Laptop",
        "brand": "HP",
        "images": ["https://picsum.photos/seed/hp-probook/600/600"],
    },
    {
        "name": "MSI Modern 15 - Intel Core Ultra 5-120U / 8GB / 512GB SSD",
        "description": "Everyday 15.6\" FHD laptop, thin and light with all-day battery life.",
        "price": 599.00,
        "category": "Computer",
        "subcategory": "Laptop",
        "brand": "MSI",
        "images": ["https://picsum.photos/seed/msi-modern/600/600"],
    },
    {
        "name": "ASUS Vivobook 15 - Intel Core i5-1334U / 16GB / 512GB SSD",
        "description": "A reliable all-rounder for study, work, and streaming.",
        "price": 649.00,
        "category": "Computer",
        "subcategory": "Laptop",
        "brand": "Asus",
        "images": ["https://picsum.photos/seed/asus-vivobook/600/600"],
    },
    {
        "name": "HP EliteBook 840 G5 (Used) - Intel Core i5-8350U / 8GB / 256GB SSD",
        "description": "Well-maintained second-hand business laptop, fully tested and ready to use.",
        "price": 259.00,
        "category": "Computer",
        "subcategory": "Laptop",
        "brand": "HP",
        "images": ["https://picsum.photos/seed/hp-elitebook/600/600"],
    },
    {
        "name": "ASUS TUF F16 FX607VU - Intel Core i5-210H / 16GB / RTX 4050",
        "description": "144Hz FHD+ display, RTX 4050 graphics, and TUF-grade durability for gaming on the move.",
        "price": 1149.00,
        "category": "Computer",
        "subcategory": "Laptop",
        "brand": "Asus",
        "images": ["https://picsum.photos/seed/asus-tuf/600/600"],
    },
    # Computer / Desktop
    {
        "name": "Custom Ryzen 5 Home & Office Desktop - 16GB / 512GB SSD",
        "description": "Compact desktop tower ready for browsing, office work, and light editing.",
        "price": 429.00,
        "category": "Computer",
        "subcategory": "Desktop",
        "brand": "Custom Build",
        "images": ["https://picsum.photos/seed/desktop-office/600/600"],
    },
    {
        "name": "Custom Ryzen 7 Gaming Desktop - RTX 4060 / 32GB / 1TB SSD",
        "description": "High-performance gaming tower with RGB lighting and top-tier cooling.",
        "price": 1299.00,
        "category": "Computer",
        "subcategory": "Desktop",
        "brand": "Custom Build",
        "images": ["https://picsum.photos/seed/desktop-gaming/600/600"],
    },
    # Computer / Components
    {
        "name": "Kingston Fury Beast 16GB DDR5 5200MHz",
        "description": "High-speed desktop memory module for gaming and creative workloads.",
        "price": 39.00,
        "category": "Computer",
        "subcategory": "Components",
        "brand": "Kingston",
        "images": ["https://picsum.photos/seed/kingston-ram/600/600"],
    },
    {
        "name": "Samsung 980 Pro 1TB NVMe SSD",
        "description": "Blazing-fast PCIe 4.0 SSD for gaming rigs and content creation.",
        "price": 79.00,
        "category": "Computer",
        "subcategory": "Components",
        "brand": "Samsung",
        "images": ["https://picsum.photos/seed/samsung-ssd/600/600"],
    },
    # Tablet
    {
        "name": "Apple iPad 10th Gen - 64GB Wi-Fi",
        "description": "10.9\" Liquid Retina display, A14 Bionic chip, and all-day battery life.",
        "price": 449.00,
        "category": "Tablet",
        "subcategory": "iPad",
        "brand": "Apple",
        "images": ["https://picsum.photos/seed/ipad-10/600/600"],
        "tags": ["64GB", "New", "Wi-Fi"],
        "installment_plans": [
            {"months": 6, "monthly": 80},
            {"months": 9, "monthly": 56},
        ],
    },
    {
        "name": "Samsung Galaxy Tab S9 - 128GB",
        "description": "AMOLED 2X display, S Pen included, and IP68 water resistance.",
        "price": 799.00,
        "category": "Tablet",
        "subcategory": "Android",
        "brand": "Samsung",
        "images": ["https://picsum.photos/seed/galaxy-tab-s9/600/600"],
        "tags": ["128GB", "New", "S Pen included"],
        "installment_plans": [
            {"months": 6, "monthly": 140},
            {"months": 9, "monthly": 98},
            {"months": 12, "monthly": 76},
        ],
    },
    {
        "name": "Xiaomi Pad 6 - 128GB",
        "description": "144Hz display and a large 8840mAh battery, great value for everyday use.",
        "price": 349.00,
        "category": "Tablet",
        "subcategory": "Android",
        "brand": "Xiaomi",
        "images": ["https://picsum.photos/seed/xiaomi-pad-6/600/600"],
        "tags": ["128GB", "New", "144Hz"],
    },
    # Accessories
    {
        "name": "Logitech G102 Lightsync Gaming Mouse",
        "description": "Lightweight gaming mouse with customizable RGB and 8000 DPI sensor.",
        "price": 18.50,
        "category": "Accessories",
        "subcategory": "Mouse",
        "brand": "Logitech",
        "images": ["https://picsum.photos/seed/logitech-mouse/600/600"],
    },
    {
        "name": "Logitech K380 Multi-Device Bluetooth Keyboard",
        "description": "Compact wireless keyboard that pairs with up to 3 devices.",
        "price": 32.00,
        "category": "Accessories",
        "subcategory": "Keyboard",
        "brand": "Logitech",
        "images": ["https://picsum.photos/seed/logitech-keyboard/600/600"],
    },
]

app = create_app()

with app.app_context():
    db.create_all()
    for item in SAMPLE_PRODUCTS:
        if Product.query.filter_by(name=item["name"]).first():
            continue
        product = Product(
            description=item["description"],
            price=item["price"],
            category=item["category"],
            subcategory=item.get("subcategory", ""),
            brand=item.get("brand", ""),
            images=item["images"],
            tags=item.get("tags", []),
            installment_plans=item.get("installment_plans", []),
        )
        product.set_name(item["name"])
        db.session.add(product)
    db.session.commit()
    print(f"Seeded {Product.query.count()} product(s) total.")
