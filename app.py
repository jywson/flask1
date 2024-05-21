from flask import Flask, render_template, url_for
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
        return "Product not found", 404

if __name__ == '__main__':
    app.run(debug=True)