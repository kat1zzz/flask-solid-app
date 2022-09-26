from abc import ABC, abstractmethod

class BasePaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        # to be implemented by sub class
        pass
