from flask_image_repo import db, login_man
from datetime import datetime
from flask_login import UserMixin

@login_man.user_loader
def load_user (seller_id):
    return Seller.query.get(int(seller_id))

class Seller(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    images = db.relationship("Image", backref="seller", lazy=True)
    orders = db.relationship("Order", backref="sell", lazy=True)

    def __repr__(self):
        return f"Seller('{self.username}', '{self.email}', '{self.password}')"

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    name = db.Column(db.String(20), nullable=False, default='NO NAME')
    price = db.Column(db.Integer, nullable=False, default=0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    discount = db.Column(db.Integer, nullable=True, default=0)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    order = db.relationship('Order', backref='image', lazy=True)

    def __repr__(self):
        return f"Images('{self.image_file}', '{self.name}', '{self.price}', '{self.discount}', '{self.stock}')"

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(125), nullable=False)
    last_name = db.Column(db.String(125), nullable=False)
    customer_email = db.Column(db.String(25), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    payment = db.Column(db.String(25), nullable=False)
    order = db.relationship('Order', backref='order', lazy=True)

    def __repr__(self):
        return f"Orders('{self.order_date}', '{self.customer_username}')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)

    def __repr__(self):
        return f"Orders('{self.order_date}')"