from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from flask_sqlalchemy import SQLAlchemy
import json
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_tables():
    db.create_all()

@app.before_request
def before_request():
    create_tables()

def load_products():
    with open('data/products.json', 'r', encoding='utf-8') as f:
        return json.load(f)

category_names = {
    "clothing": "Одежда",
    "shoes": "Обувь"
}

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    resp = make_response(redirect(url_for('greeting')))
    resp.set_cookie('name', name)
    resp.set_cookie('email', email)
    return resp

@app.route('/greeting')
def greeting():
    name = request.cookies.get('name')
    if name:
        return render_template('greeting.html', name=name)
    else:
        return redirect(url_for('form'))

@app.route('/logout', methods=['POST'])
def logout():
    resp = make_response(redirect(url_for('form')))
    resp.delete_cookie('name')
    resp.delete_cookie('email')
    return resp

@app.route('/category/<category_name>')
def category(category_name):
    products = load_products()
    category_products = [p for p in products if p['category'] == category_name]
    category_display_name = category_names.get(category_name, category_name)
    return render_template('category.html', category_name=category_display_name, products=category_products)

@app.route('/product/<product_name>')
def product(product_name):
    products = load_products()
    product = next((p for p in products if p['name'] == product_name), None)
    if product:
        return render_template('product.html', product=product)
    else:
        return "Товар не найден", 404

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Адрес электронной почты уже существует')
        return redirect(url_for('register'))
    
    new_user = User(first_name=first_name, last_name=last_name, email=email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
