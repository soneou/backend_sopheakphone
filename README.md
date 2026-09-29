# Sopheak Mobile — Backend (Flask API)

A catalog-only API: browse/search products publicly, manage them through a
password-protected admin API. Products optionally carry a list of
installment plans (months + monthly amount) alongside their cash price.
There is no checkout or payment — buyers are directed to contact you on
Telegram/Facebook/WhatsApp/phone instead.

## Stack

- Flask + Flask-SQLAlchemy + Flask-Migrate
- MySQL in production (Aiven), SQLite automatically for local dev
- Flask-JWT-Extended for a single admin account (no user table/signup)
- Cloudinary for product image hosting (Render's free tier wipes local files
  on every restart, so images can't live on disk there)

## Local development

```bash
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash; use venv\Scripts\activate.bat on cmd
pip install -r requirements.txt

cp .env.example .env
# generate a password hash and put it in .env as ADMIN_PASSWORD_HASH
python scripts/hash_password.py "your-chosen-password"

flask db upgrade         # creates dev.db (SQLite) with the products table
python scripts/seed.py   # optional: adds 3 sample products

flask run                # http://localhost:5000
```

## Project layout

```
app/
  config.py        # env-driven config, normalizes Aiven's mysql:// URL
  extensions.py     # db, migrate, jwt, cors singletons
  models/product.py
  routes/
    products.py     # public: list/search/categories/detail
    auth.py          # POST /api/auth/login
    admin.py         # JWT-protected CRUD + image upload
  utils/images.py    # Cloudinary upload/delete helpers
scripts/
  hash_password.py   # generate ADMIN_PASSWORD_HASH
  seed.py             # sample data for local dev
wsgi.py               # app entrypoint (gunicorn wsgi:app)
```

## API

Public:
- `GET /api/products?category=&subcategory=&search=&page=` — paginated, active products only
- `GET /api/products/categories` — categories with their distinct subcategories, e.g.
  `{"categories": [{"name": "Laptop", "subcategories": ["Gaming", "Notebook Consumer"]}]}`
- `GET /api/products/<slug>` — includes `installment_plans: [{months, monthly}, ...]`

Auth:
- `POST /api/auth/login` `{username, password}` -> `{access_token}`

Admin (send `Authorization: Bearer <token>`):
- `GET /api/admin/products` — includes hidden/out-of-stock products
- `GET/POST /api/admin/products`, `PUT/DELETE /api/admin/products/<id>`
- `POST /api/admin/upload-image` — multipart `file`, returns `{url}`

## Deploying

### 1. Database on Aiven (MySQL, free tier)

1. Create a MySQL service on [Aiven](https://aiven.io).
2. Copy the **Service URI** (looks like `mysql://avnadmin:...@...aivencloud.com:12345/defaultdb`).
3. Set it as `DATABASE_URL` in Render's environment variables (see below).
   The app rewrites `mysql://` to `mysql+pymysql://` and enables TLS
   automatically — no manual editing needed.

### 2. Images on Cloudinary (free tier)

1. Create a free account at [cloudinary.com](https://cloudinary.com).
2. From the dashboard, copy `Cloud name`, `API Key`, `API Secret`.
3. Set `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`.

### 3. API on Render (free tier)

1. Push this `backend/` folder to a GitHub repo.
2. In Render, "New +" -> "Web Service", pick the repo (root directory:
   `backend` if it's part of a monorepo).
3. Render auto-detects `render.yaml`. Otherwise set manually:
   - Build command: `pip install -r requirements.txt`
   - Start command: `flask db upgrade && gunicorn wsgi:app`
4. Add the environment variables from `.env.example`:
   `SECRET_KEY`, `JWT_SECRET_KEY`, `DATABASE_URL`, `ADMIN_USERNAME`,
   `ADMIN_PASSWORD_HASH`, `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`,
   `CLOUDINARY_API_SECRET`, `FRONTEND_ORIGINS` (your Vercel URL(s), comma
   separated).
5. Deploy. Render's free tier spins down when idle — the first request
   after a while will be slow (cold start), which is expected.

Generate `ADMIN_PASSWORD_HASH` locally with:
```bash
python scripts/hash_password.py "your-chosen-password"
```
Never commit `.env` — it's gitignored.
