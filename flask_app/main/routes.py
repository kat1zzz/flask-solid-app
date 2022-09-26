from flask import Blueprint, request
from flask import jsonify

from flask_app.main.utils import (
    check_cart_items_exist,
    get_all_items,
    get_cart_items,
    place_order_items
)

from flask_app import db, bcrypt
from flask_login import login_manager, login_user, logout_user, login_required, current_user

user = Blueprint('user', __name__)

from flask_app.models import user2, cart , items

@user.route("/register2", methods=["GET", "POST"])
def register2():
    body = request.get_json()
    user = user2.query.filter_by(email=body.get('email')).first()
    if(user):
        return " user \'{}\' is already registered".format(user.email)
    else:
        user = user2(email=body.get('email'))
        db.session.add(user)
        db.session.commit()
        return "user with email = {} is registered".format(user.email)


@user.route("/login2", methods=["GET", "POST"])
def login2():
    body = request.get_json()
    email = body.get('email')
    if(email):
        user = user2.query.filter_by(email=email).first()
        login_user(user,force=True)
        return "success : {}, {}, {}".format(current_user.id, current_user.email, current_user.name)
    else:
        return "error in login user", 500

@user.route('/logout')
@login_required
def log_out():
    logout_user()
    return "Logged out successfully!"

@user.route("/get_items", methods=["GET"])
@login_required
def get_items():
    try:
        items_list = get_all_items()
        return jsonify({"items": items_list})
    except Exception as e:
        return str(e), 500

@user.route("/add_items", methods=["POST"])
@login_required
def add_items():
    body = request.get_json()
    try:
        db_items = []
        for item in body.get('items',[]):
            name = item.get("name","")
            price = item.get("price",0)
            item = items(name=name, price=price)
            db_items.append(item)
        db.session.bulk_save_objects(db_items)
        db.session.commit()
        items_list = get_all_items()
        return jsonify({"items": items_list})
    except Exception as e:
        return str(e), 500

@user.route("/add_items_cart", methods=["POST"])
@login_required
def add_items_cart():
    body = request.get_json()
    try:
        user_id = body.get('user_id') #current_user.id
        items = body.get('items',[])
        db_carts = []
        for item in items:
            curr_cart = cart(user_id=user_id, item_id=item)
            db_carts.append(curr_cart)

        db.session.bulk_save_objects(db_carts)
        db.session.commit()
        items_list = get_cart_items(user_id)
        return jsonify({"cart_items": items_list})
    except:
        return "couldn't added items to cart", 500

@user.route("/get_items_cart", methods=["GET"])
@login_required
def get_items_cart(user_id=None):
    try:
        user_id = request.args.get('user_id')
        items_list = get_cart_items(user_id)
        return jsonify({"cart_items": items_list})
    except Exception as e:
        return str(e), 500

@user.route("/place_order", methods=["POST"])
@login_required
def place_order():
    body = request.get_json()
    user_id = body.get('user_id') #current_user.id
    payment_body = body.get('payment')
    try:
        if not check_cart_items_exist(user_id):
            raise ValueError("Cart is empty, cant place")
        place_order_items(user_id, payment_body)
    except Exception as e:
        return str(e), 500

    return "successfully placed order"