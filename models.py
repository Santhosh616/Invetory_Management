import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def gen_uuid():
    return str(uuid.uuid4())

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.String, primary_key=True, default=gen_uuid)
    name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'

class Location(db.Model):
    __tablename__ = 'location'
    location_id = db.Column(db.String, primary_key=True, default=gen_uuid)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return f'<Location {self.name}>'

class ProductMovement(db.Model):
    __tablename__ = 'product_movement'
    movement_id = db.Column(db.String, primary_key=True, default=gen_uuid)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    from_location = db.Column(db.String, db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.String, db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.String, db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product', backref='movements')
    from_loc = db.relationship('Location', foreign_keys=[from_location])
    to_loc = db.relationship('Location', foreign_keys=[to_location])

    def __repr__(self):
        return f'<Movement {self.movement_id} {self.qty}>'
