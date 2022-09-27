# SOLID Principles demonstration used in this project.
  Visit [PaymenthProcessors](https://github.com/kat1zzz/flask-solid-app/tree/master/flask_app/main/Payment) and [Authrizors](https://github.com/kat1zzz/flask-solid-app/tree/master/flask_app/main/Authorizer) classes for easy understanding.

# Single responsibility principle
  `single class is responsible for single handling action.`

  cart is responsible for dealing with items only not payment or authrizer
  similar payment is responsible for payment only, and so on for authrizer



# Open-Closed Principle
  `classes should be open for extension and closed to modification.`

  we have created [BasePaymentProcessor](https://github.com/kat1zzz/flask-solid-app/blob/master/flask_app/main/Payment/BaseProcessor.py) to extend and add payment methods, this way [BasePaymentProcessor](https://github.com/kat1zzz/flask-solid-app/blob/master/flask_app/main/Payment/BaseProcessor.py) is closed for modification but we can still add payment method like [PaypalPaymentProcessor](https://github.com/kat1zzz/flask-solid-app/blob/af5581f951a3a383f3eb527f646b362f723afba3/flask_app/main/Payment/PaymentProcessors.py#L34) with inheriting [BasePaymentProcessor](https://github.com/kat1zzz/flask-solid-app/blob/master/flask_app/main/Payment/BaseProcessor.py).



# Liskov Substitution Principle
  `Subclasses should be substitutable for their base classes. This means that, given that class B
  is a subclass of class A, we should be able to pass an object of class B to any method that expects an object of class A and the method should not give any weird output in that case.`

  we have created two payment method(paypal and debit card) with same [BasePaymentProcessor](https://github.com/kat1zzz/flask-solid-app/blob/master/flask_app/main/Payment/BaseProcessor.py) but their auth method is different, debit card is processed by security_code while paypal auth is processed by email_address, we have changed this in PaymentProcessor contstructor [init](https://github.com/kat1zzz/flask-solid-app/blob/af5581f951a3a383f3eb527f646b362f723afba3/flask_app/main/Payment/PaymentProcessors.py#L12) method as if we had security_code in [BasePaymentProcessor](https://github.com/kat1zzz/flask-solid-app/blob/master/flask_app/main/Payment/BaseProcessor.py), this will violate [PaypalPaymentProcessor](https://github.com/kat1zzz/flask-solid-app/blob/af5581f951a3a383f3eb527f646b362f723afba3/flask_app/main/Payment/PaymentProcessors.py#L34) as email_address
  is required instead of security_code.



# Interface Segregation Principle
  `This is about separating the interfaces, it is better to have several specific interfaces instead
  of one general interface.`

  we have created several interfaces [SMSAuthorizer](https://github.com/kat1zzz/flask-solid-app/blob/af5581f951a3a383f3eb527f646b362f723afba3/flask_app/main/Authorizer/Authorizers.py#L8), EmailAuthorizer while they have same authentication
  method security_code ? because these dont have to dependenct on one interface, so that we can change it later,
  similar with payment methods DebitPaymentProcessor, [PaypalPaymentProcessor](https://github.com/kat1zzz/flask-solid-app/blob/af5581f951a3a383f3eb527f646b362f723afba3/flask_app/main/Payment/PaymentProcessors.py#L34).

# Dependency Inversion Principle
  `Classes should depend upon interfaces or abstract classes instead of concrete classes and functions.`

  in this case each PaymentProcessor have [authorizer: BaseAuthorizer](https://github.com/kat1zzz/flask-solid-app/blob/af5581f951a3a383f3eb527f646b362f723afba3/flask_app/main/Payment/PaymentProcessors.py#L12) which is abstract class and follows this principle,
  [SMSAuthorizer](https://github.com/kat1zzz/flask-solid-app/blob/af5581f951a3a383f3eb527f646b362f723afba3/flask_app/main/Authorizer/Authorizers.py#L8) can be used for PaymentProcessors like `authorizer: SMSAuthorizer` but instead of dependeing on
  concrete classes like [SMSAuthorizer](https://github.com/kat1zzz/flask-solid-app/blob/af5581f951a3a383f3eb527f646b362f723afba3/flask_app/main/Authorizer/Authorizers.py#L8), RobotAuthorizer we used abstract class [BaseAuthorizer](https://github.com/kat1zzz/flask-solid-app/blob/master/flask_app/main/Authorizer/BaseAuthorizers.py).
