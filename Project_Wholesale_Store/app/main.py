from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from .models import db, User, Product
from .repositories import ProductRepository

bp = Blueprint('main', __name__)

product_repo = ProductRepository()

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return "Пользователь с таким именем уже существует"
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('main.index'))
        else:
            return "Некорректные логин или пароль"
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@bp.before_request
def require_login():
    allowed_routes = ['main.login', 'main.register']
    if request.endpoint and request.endpoint.startswith('main.') and request.endpoint not in allowed_routes:
        if 'user_id' not in session:
            return redirect(url_for('main.login'))

@bp.route('/')
def index():
    products = product_repo.get_all()
    return render_template('index.html', products=products)

@bp.route('/add', methods=['GET'])
def add_form():
    return render_template('add_product.html')

@bp.route('/products', methods=['POST'])
def add_or_delete_product():
    if 'delete_id' in request.form:
        delete_id = int(request.form['delete_id'])
        product = product_repo.get_by_id(delete_id)
        if product:
            product_repo.delete(product)
        return redirect(url_for('main.index'))
    elif 'name' in request.form:
        name = request.form['name']
        description = request.form['description']
        try:
            price = float(request.form['price'])
            quantity = float(request.form['quantity'])
        except ValueError:
            return "Некорректные данные для цены или количества", 400
        new_product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity
        )
        product_repo.add(new_product)
        return redirect(url_for('main.index'))
    else:
        return "Некорректный запрос", 400

@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = product_repo.get_by_id(product_id)
    if not product:
        abort(404)
    return render_template('product_detail.html', product=product)

@bp.route('/product/<int:product_id>/edit', methods=['GET'])
def edit_product_form(product_id):
    product = product_repo.get_by_id(product_id)
    if not product:
        abort(404)
    return render_template('edit_product.html', product=product)

@bp.route('/product/<int:product_id>/update', methods=['POST'])
def update_product(product_id):
    product = product_repo.get_by_id(product_id)
    if not product:
        abort(404)
    name = request.form['name']
    description = request.form['description']
    try:
        price = float(request.form['price'])
        quantity = float(request.form['quantity'])
    except ValueError:
        return "Некорректные данные для цены или количества", 400
    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity
    product_repo.update()
    return redirect(url_for('main.index'))