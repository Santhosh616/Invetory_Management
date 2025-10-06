from models import db, Product, Location, ProductMovement
from app import create_app
import os, random, datetime
app = create_app()
sample_products = [
    {'name':'Samsung Galaxy S21', 'sku':'SMG-S21', 'description':'Smartphone - 128GB, Phantom Gray'},
    {'name':'HP LaserJet Pro M404dn', 'sku':'HP-LJ-M404', 'description':'Mono Laser Printer'},
    {'name':'Logitech MX Master 3', 'sku':'LOG-MX3', 'description':'Wireless Mouse - Ergonomic'},
    {'name':'Sony WH-1000XM4', 'sku':'SONY-WH1000XM4', 'description':'Wireless Noise Cancelling Headphones'}
]
sample_locations = [
    {'name':'Main Warehouse - Chennai', 'code':'WH-CHN', 'address':'Industrial Estate, Chennai, TN'},
    {'name':'Store - Bengaluru', 'code':'ST-BLR', 'address':'MG Road, Bengaluru, KA'},
    {'name':'Secondary Warehouse - Kochi', 'code':'WH-KCH', 'address':'Kochi Logistics Park, Kerala'},
    {'name':'Return Center - Coimbatore', 'code':'RC-CBE', 'address':'Coimbatore Returns Facility'}
]

with app.app_context():
    db.create_all()
    # clear existing
    ProductMovement.query.delete()
    Product.query.delete()
    Location.query.delete()
    db.session.commit()
    products = []
    for p in sample_products:
        prod = Product(name=p['name'], sku=p['sku'], description=p['description'])
        db.session.add(prod)
        products.append(prod)
    locs = []
    for l in sample_locations:
        loc = Location(name=l['name'], code=l['code'], address=l['address'])
        db.session.add(loc)
        locs.append(loc)
    db.session.commit()

    # create 20 sample movements (deterministic randomness)
    random.seed(42)
    movements = []
    # helper to choose incoming or outgoing or transfer
    for i in range(20):
        prod = random.choice(products)
        action = random.choice(['in','out','transfer','in','transfer'])  # bias to transfers/ins
        qty = random.choice([1,2,3,5,10])
        if action == 'in':
            to = random.choice(locs)
            mv = ProductMovement(product_id=prod.product_id, from_location=None, to_location=to.location_id, qty=qty)
        elif action == 'out':
            fr = random.choice(locs)
            mv = ProductMovement(product_id=prod.product_id, from_location=fr.location_id, to_location=None, qty=qty)
        else: # transfer
            fr, to = random.sample(locs, 2)
            mv = ProductMovement(product_id=prod.product_id, from_location=fr.location_id, to_location=to.location_id, qty=qty)
        db.session.add(mv)
    db.session.commit()
    print('Seeded products, locations and 20 movements')

