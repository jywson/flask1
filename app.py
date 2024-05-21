from flask import Flask, render_template, request, redirect, url_for, make_response
import json

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)