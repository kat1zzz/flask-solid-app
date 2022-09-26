from abc import ABC, abstractmethod

class BaseAuthorizer(ABC):
    @abstractmethod
    def is_authorized(self) -> bool:
        # to be implemented by child class
        pass
