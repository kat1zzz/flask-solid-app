from flask_app.main.Authorizer.BaseAuthorizers import BaseAuthorizer
from flask_app.main.constants import (
    AUTH_SMS,
    AUTH_EMAIL,
    AUTH_ROBOT
)

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Authorizer_SMS(BaseAuthorizer):
    def __init__(self):
        self.TEMPLATE_NAME = AUTH_SMS
        self.authorized = False

    def verify_code(self, code):
        logger.info(f"Verifying SMS code {code}")
        self.authorized = True

    def verify(self, code):
        logger.info(f"Verifying SMS code {code}")
        self.verify_code(code)

    def is_authorized(self) -> bool:
        return self.authorized

class Authorizer_Email(BaseAuthorizer):

    def __init__(self):
        self.TEMPLATE_NAME = AUTH_EMAIL
        self.authorized = False

    def verify_code(self, code):
        logger.info(f"Verifying Emailauth code {code}")
        self.authorized = True

    def verify(self, code):
        logger.info(f"Verifying Email auth code {code}")
        self.verify_code(code)

    def is_authorized(self) -> bool:
        return self.authorized

class Authorizer_Robot(BaseAuthorizer):

    def __init__(self):
        self.TEMPLATE_NAME = AUTH_ROBOT
        self.authorized = False

    def not_a_robot(self):
        self.authorized = True

    def verify(self, code):
        logger.info(f"Verifying robot")
        self.not_a_robot()

    def is_authorized(self) -> bool:
        return self.authorized

AUTH_MAPPING = {
    AUTH_SMS: Authorizer_SMS(),
    AUTH_EMAIL: Authorizer_Email(),
    AUTH_ROBOT: Authorizer_Robot()
}
