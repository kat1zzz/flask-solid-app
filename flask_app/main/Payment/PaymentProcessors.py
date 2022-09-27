from flask_app.main.Payment.BaseProcessor import BasePaymentProcessor
from flask_app.main.Authorizer.BaseAuthorizers import BaseAuthorizer
from flask_app.main.constants import (
    STATUS_SUCCESS,
    PAYMENT_CREDIT,
    PAYMENT_DEBIT,
    PAYMENT_PAYPAL
)

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DebitPaymentProcessor(BasePaymentProcessor):

    def __init__(self, security_code, authorizer: BaseAuthorizer):
        self.security_code = security_code
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
        logger.info("Processing debit payment type")
        logger.info(f"Verifying security code: {self.security_code}")
        order.order_status = STATUS_SUCCESS

class CreditPaymentProcessor(BasePaymentProcessor):

    def __init__(self, security_code, authorizer: BaseAuthorizer):
        self.security_code = security_code
        self.authorizer = authorizer

    def pay(self, order):
        logger.info("Processing credit payment type")
        logger.info(f"Verifying security code: {self.security_code}")
        order.order_status = STATUS_SUCCESS

class PaypalPaymentProcessor(BasePaymentProcessor):

    def __init__(self, email_address, authorizer: BaseAuthorizer):
        self.email_address = email_address
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
        logger.info("Processing paypal payment type")
        logger.info(f"Using email address: {self.email_address}")
        order.order_status = STATUS_SUCCESS

PAYMENT_MAPPING = {
    PAYMENT_CREDIT: CreditPaymentProcessor,
    PAYMENT_DEBIT: DebitPaymentProcessor,
    PAYMENT_PAYPAL: PaypalPaymentProcessor
}
