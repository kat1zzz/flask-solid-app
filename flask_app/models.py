from enum import unique
from flask_app.main.constants import DEFAULT_AUTH, STATUS_PENDING
from flask_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return user2.query.get(user_id)

class user2(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String(400), nullable=False)
    def to_string(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "username": self.username
        }

class orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user2.id"), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey("payment.id"), nullable=False)
    order_status = db.Column(db.String, nullable=STATUS_PENDING)

class cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user2.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    def to_string(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "item_id": self.item_id
        }

class items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=0)
    def to_string(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }

class payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=DEFAULT_AUTH)
    status = db.Column(db.String, nullable=STATUS_PENDING)
