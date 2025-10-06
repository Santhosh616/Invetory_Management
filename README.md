# Warehouse Management System (Flask)

This is a simple inventory/warehouse management web application built with Flask and SQLAlchemy.
- Database: PostgreSQL (configurable via `DATABASE_URL` env var). Falls back to SQLite for local testing.
- Features: CRUD for Products, Locations, Product Movements, and a Balance report (Product, Warehouse, Qty).

## Setup (Postgres)
1. Create a PostgreSQL database and user.
2. Set environment variable `DATABASE_URL` to your database connection string, e.g.:
   `export DATABASE_URL=postgresql://user:password@localhost:5432/warehouse_db`
3. Install dependencies: `pip install -r requirements.txt`
4. Run `python seed_data.py` to create tables and populate sample data (20 movements included).
5. Run the app: `python app.py` and open `http://127.0.0.1:5000`.

## Notes
- If `DATABASE_URL` is not provided, the app will use SQLite at `warehouse.db` in the project folder.
- The seed script inserts realistic sample products and 4 locations plus 20 sample movements.

## What I changed / suggestions
- Used SQLAlchemy ORM and made primary keys simple text UUIDs for portability.
- Included balance query using SQLAlchemy to compute quantity in each location.
- Provided a seed script that works with Postgres and SQLite.

