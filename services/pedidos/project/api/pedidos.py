from flask import Blueprint, jsonify, request, render_template
from project.api.models import Customer, Product, Order, Item
from project import db
from sqlalchemy import exc

pedidos_blueprint = Blueprint(
    'pedidos', __name__, template_folder='./templates')


@pedidos_blueprint.route('/pedidos/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong'
        })


@pedidos_blueprint.route('/customers/', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return render_template('customers.html', customer=customers)


@pedidos_blueprint.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    """Obtener detalles de usuario único """
    response_object = {
        'status': 'failed',
        'mensaje': 'El usuario no existe'
    }
    try:
        cus = Customer.query.filter_by(id=int(id)).first()
        if not cus:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': cus.id,
                    'name': cus.name,
                }
            }
            return jsonify(response_object), 200
        # return render_template('user.html', user=user)
    except ValueError:
        return jsonify(response_object), 404


@pedidos_blueprint.route('/customers/', methods=['POST'])
def index():
    customer = Customer()
    customer.name = request.form['name']
    db.session.add(customer)
    db.session.commit()
    customers = Customer.query.all()
    return render_template('customers.html', customer=customers)


@pedidos_blueprint.route('/customers', methods=['POST'])
def add_customer():
    post_data = request.get_json()
    response_object = {
            'status': 'failed',
            'message': 'carga invalida.'
    }
    if not post_data:
        return jsonify(response_object), 400
    name = post_data.get('name')
    try:
        customer = Customer.query.filter_by(name=name).first()
        if not customer:
            db.session.add(Customer(name=name))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{name} ha sido agregado!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'lo siento. el name ya existe.'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400


@pedidos_blueprint.route('/customer/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Obtener detalles de usuario único """
    response_object = {
        'status': 'failed',
        'mensaje': 'El usuario no existe'
    }
    try:
        user = Customer.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'name': user.name
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@pedidos_blueprint.route('/customers/<int:id>', methods=['PUT'])
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    customer.import_data(request.json)
    db.session.add(customer)
    db.session.commit()
    return jsonify({})


@pedidos_blueprint.route('/products/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return render_template('product.html', product=products)


@pedidos_blueprint.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    return jsonify(Product.query.get_or_404(id).export_data())


@pedidos_blueprint.route('/products/', methods=['POST'])
def new_product():
    product = Product()
    product.name = request.form['name']
    db.session.add(product)
    db.session.commit()
    products = Product.query.all()
    return render_template('product.html', product=products)


@pedidos_blueprint.route('/products/<int:id>', methods=['PUT'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    product.import_data(request.json)
    db.session.add(product)
    db.session.commit()
    return jsonify({})


@pedidos_blueprint.route('/orders/', methods=['GET'])
def get_orders():
    return jsonify({'orders': [
        order.get_url() for order in Order.query.all()
        ]})


@pedidos_blueprint.route('/customers/<int:id>/orders/', methods=['GET'])
def get_customer_orders(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({'orders': [order.get_url() for order in
                               customer.orders.all()]})


@pedidos_blueprint.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    return jsonify(Order.query.get_or_404(id).export_data())


@pedidos_blueprint.route('/customers/<int:id>/orders/', methods=['POST'])
def new_customer_order(id):
    customer = Customer.query.get_or_404(id)
    order = Order(customer=customer)
    order.import_data(request.json)
    db.session.add(order)
    db.session.commit()
    return jsonify({}), 201, {'Location': order.get_url()}


@pedidos_blueprint.route('/orders/<int:id>', methods=['PUT'])
def edit_order(id):
    order = Order.query.get_or_404(id)
    order.import_data(request.json)
    db.session.add(order)
    db.session.commit()
    return jsonify({})


@pedidos_blueprint.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({})


@pedidos_blueprint.route('/orders/<int:id>/items/', methods=['GET'])
def get_order_items(id):
    order = Order.query.get_or_404(id)
    return jsonify({'items': [item.get_url() for item in order.items.all()]})


@pedidos_blueprint.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    return jsonify(Item.query.get_or_404(id).export_data())


@pedidos_blueprint.route('/orders/<int:id>/items/', methods=['POST'])
def new_order_item(id):
    order = Order.query.get_or_404(id)
    item = Item(order=order)
    item.import_data(request.json)
    db.session.add(item)
    db.session.commit()
    return jsonify({}), 201, {'Location': item.get_url()}


@pedidos_blueprint.route('/items/<int:id>', methods=['PUT'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    item.import_data(request.json)
    db.session.add(item)
    db.session.commit()
    return jsonify({})


@pedidos_blueprint.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({})
