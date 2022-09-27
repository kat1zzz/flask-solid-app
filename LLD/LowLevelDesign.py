from abc import ABC, abstractmethod

class Cart:
    def __init__(self):
        self.items = []
        self.prices = []
        self.status = "open"

    def add_item(self, name, price):
        self.items.append(name)
        self.prices.append(price)

    def cart_price(self):
        total_price = 0
        for i in range(len(self.prices)):
            total_price += self.prices[i]
        return total_price


class BaseAuthorizer(ABC):
    @abstractmethod
    def is_authorized(self) -> bool:
        pass

class SMSAuthorizer(BaseAuthorizer):
    def __init__(self):
        self.authorized = False

    def verify_code(self, code):
        print("Verifying SMS code {}".format(code))
        self.authorized = True

    def verify(self, code):
        self.verify_code(code)

    def is_authorized(self) -> bool:
        return self.authorized

class EmailAuthorizer(BaseAuthorizer):
    def __init__(self):
        self.authorized = False

    def verify_code(self, code):
        print("Verifying Email Auth code {}".format(code))
        self.authorized = True

    def verify(self, code):
        self.verify_code(code)

    def is_authorized(self) -> bool:
        return self.authorized

class RobotAuthorizer(BaseAuthorizer):
    def __init__(self):
        self.authorized = False

    def i_am_not_a_robot(self):
        self.authorized = True

    def verify(self, code=None):
        self.i_am_not_a_robot()

    def is_authorized(self) -> bool:
        return self.authorized


class BasePaymentProcessor(ABC):
    @abstractmethod
    def pay(self, cart):
        # to be implemented in sub class
        pass

class DebitPaymentProcessor(BasePaymentProcessor):
    def __init__(self, security_code, authorizer: BaseAuthorizer):
        self.security_code = security_code
        self.authorizer = authorizer

    def pay(self, cart):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized for transaction")
        print("Processing debit cart payment")
        print("Verifying security code: {}".format(self.security_code))
        cart.status = "paid"

class PaypalPaymentProcessor(BasePaymentProcessor):
    def __init__(self, email_address, authorizer: BaseAuthorizer):
        self.email_address = email_address
        self.authorizer = authorizer

    def pay(self, cart):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
        print("Processing paypal payment type")
        print("Using email address: {}".format(self.email_address))
        cart.status = "paid"


cart = Cart()
cart.add_item("Keyboard", 100)
cart.add_item("SSD", 5000)
cart.add_item("USB cable", 100)

print(cart.cart_price())

authorizer = SMSAuthorizer()
authorizer.verify(465839)
processor = DebitPaymentProcessor("first@email.com", authorizer)
processor.pay(cart)


authorizer = RobotAuthorizer()
authorizer.verify()
processor = PaypalPaymentProcessor("second@email.com", authorizer)
processor.pay(cart)
