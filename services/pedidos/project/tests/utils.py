from project import db
from project.api.models import Customer, Product


def add_customer(name):
    user = Customer(name=name)
    db.session.add(user)
    db.session.commit()
    return user


def add_product(name):
    product = Product(name=name)
    db.session.add(product)
    db.session.commit()
    return product
