from flask_app.main.Authorizer.Authorizers import AUTH_MAPPING
from flask_app.main.Payment.PaymentProcessors import PAYMENT_MAPPING
from flask_app.models import cart, items, orders, payment
# from flask_login import current_user
from flask_app import db
from flask_app.main.constants import (
    AUTH_METHODS,
    AUTH_ROBOT,
    PAYMENT_METHODS,
    PAYMENT_PAYPAL,
    STATUS_FAILED,
    STATUS_SUCCESS
)

def place_order_items(user_id=None, payment_body={}):
    payment_method = payment_body.get("payment_method")
    payment_type, authorizer_code = parse_payment_type(payment_method)
    auth_method = payment_body.get("auth_method")
    auth_method, code = parse_authorizer_type(auth_method)

    curr_payment = payment(type=payment_type)
    db.session.add(curr_payment)
    db.session.commit()

    # user_id = current_user.id

    curr_order = orders(user_id=user_id, payment_id=curr_payment.id, order_status="open")
    try:
        Authrizer = AUTH_MAPPING[auth_method]
        Authrizer.verify(code=code)
        PaymentProcessor = PAYMENT_MAPPING.get(payment_type)(authorizer_code,Authrizer)
        PaymentProcessor.pay(curr_order)
        curr_payment.status = STATUS_SUCCESS
        db.session.add(curr_payment)
        db.session.add(curr_order)
        del_all_cart_items(user_id)
        db.session.commit()
    except Exception as e:
        curr_payment.status = STATUS_FAILED
        curr_order.status = STATUS_FAILED
        db.session.commit()
        raise ValueError(+str(e))


def parse_payment_type(payment_body={}):
    type = payment_body.get('type')
    if not type or type not in PAYMENT_METHODS:
        raise ValueError("Payment Method {} not found".format(type))
    if type==PAYMENT_PAYPAL:
        email =  payment_body.get('email',"")
        if not email:
            raise ValueError("email not supplied for your paypal account")
        return type, email
    else:
        code =  payment_body.get('code')
        if not code:
            raise ValueError("code not supplied for {} card".format(type))
        return type, code

def parse_authorizer_type(auth_method={}):
    auth = auth_method.get('auth')
    if not auth or auth not in AUTH_METHODS:
        raise ValueError("3rd Party Authentication method {} not found".format(auth))
    code = auth_method.get('code')
    if auth!=AUTH_ROBOT and not code:
        raise ValueError("code is not supplied for method {}".format(auth))
    return auth, code

def get_cart_items(user_id=None):
    if not user_id:
        raise ValueError("user_id not provided")
    items_list = []
    for item in cart.query.filter_by(user_id=user_id).all():
        items_list.append(item.to_string())
    return items_list

def get_all_items():
    items_list = []
    for item in items.query.all():
        items_list.append(item.to_string())
    return items_list

def del_all_cart_items(user_id=None):
    cart_items = cart.query.filter_by(user_id=user_id).all()
    for cart_item in cart_items:
        db.session.delete(cart_item)

def check_cart_items_exist(user_id=None):
    cart_items = cart.query.filter_by(user_id=user_id).first()
    return True if cart_items else False
