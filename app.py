from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Product, Location, ProductMovement
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')

    # PostgreSQL connection (change values if needed)
    db_user = os.environ.get('DB_USER', 'postgres')
    db_pass = os.environ.get('DB_PASS', 'shadow123')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '5432')
    db_name = os.environ.get('DB_NAME', 'warehouse')  # fixed DB name

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    )

    db.init_app(app)
    return app

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

# Products
@app.route('/products')
def products():
    products = Product.query.order_by(Product.name).all()
    return render_template('products.html', products=products)

@app.route('/product/new', methods=['GET','POST'])
def new_product():
    if request.method == 'POST':
        name = request.form['name']
        sku = request.form['sku']
        desc = request.form.get('description')
        if not name or not sku:
            flash('Name and SKU are required', 'danger')
            return redirect(url_for('new_product'))
        prod = Product(name=name, sku=sku, description=desc)
        db.session.add(prod)
        db.session.commit()
        flash('Product added', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', product=None)

@app.route('/product/edit/<product_id>', methods=['GET','POST'])
def edit_product(product_id):
    prod = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        prod.name = request.form['name']
        prod.sku = request.form['sku']
        prod.description = request.form.get('description')
        db.session.commit()
        flash('Product updated', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', product=prod)

# Locations
@app.route('/locations')
def locations():
    locs = Location.query.order_by(Location.name).all()
    return render_template('locations.html', locations=locs)

@app.route('/location/new', methods=['GET','POST'])
def new_location():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        addr = request.form.get('address')
        if not name or not code:
            flash('Name and Code required', 'danger')
            return redirect(url_for('new_location'))
        loc = Location(name=name, code=code, address=addr)
        db.session.add(loc)
        db.session.commit()
        flash('Location added', 'success')
        return redirect(url_for('locations'))
    return render_template('location_form.html', location=None)

@app.route('/location/edit/<location_id>', methods=['GET','POST'])
def edit_location(location_id):
    loc = Location.query.get_or_404(location_id)
    if request.method == 'POST':
        loc.name = request.form['name']
        loc.code = request.form['code']
        loc.address = request.form.get('address')
        db.session.commit()
        flash('Location updated', 'success')
        return redirect(url_for('locations'))
    return render_template('location_form.html', location=loc)

# Movements
@app.route('/movements')
def movements():
    moves = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).limit(200).all()
    return render_template('movements.html', movements=moves)

@app.route('/movement/new', methods=['GET','POST'])
def new_movement():
    products = Product.query.order_by(Product.name).all()
    locations = Location.query.order_by(Location.name).all()
    if request.method == 'POST':
        product_id = request.form['product_id']
        from_location = request.form.get('from_location') or None
        to_location = request.form.get('to_location') or None
        qty = int(request.form['qty'])
        if not product_id or qty <= 0:
            flash('Product and positive qty required', 'danger')
            return redirect(url_for('new_movement'))
        mv = ProductMovement(product_id=product_id, from_location=from_location, to_location=to_location, qty=qty)
        db.session.add(mv)
        db.session.commit()
        flash('Movement recorded', 'success')
        return redirect(url_for('movements'))
    return render_template('movement_form.html', products=products, locations=locations)

# Balance report
@app.route('/report/balance')
def report_balance():
    products = Product.query.order_by(Product.name).all()
    locations = Location.query.order_by(Location.name).all()
    balances = []
    for p in products:
        for loc in locations:
            in_q = db.session.query(db.func.coalesce(db.func.sum(ProductMovement.qty),0)).filter(
                ProductMovement.product_id==p.product_id,
                ProductMovement.to_location==loc.location_id
            ).scalar()
            out_q = db.session.query(db.func.coalesce(db.func.sum(ProductMovement.qty),0)).filter(
                ProductMovement.product_id==p.product_id,
                ProductMovement.from_location==loc.location_id
            ).scalar()
            net = (in_q or 0) - (out_q or 0)
            if net != 0:
                balances.append({'product':p.name, 'warehouse':loc.name, 'qty':net})
    return render_template('balance.html', balances=balances)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
