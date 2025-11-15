from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from config import Config
from telegram_bot import TelegramNotifier
import json

app = Flask(__name__)
app.config.from_object(Config)

# Sample product data
PRODUCTS = [
    {
        'id': 1,
        'name': 'Wireless Headphones',
        'price': 79.99,
        'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
        'description': 'High-quality wireless headphones with noise cancellation'
    },
    {
        'id': 2,
        'name': 'Smart Watch',
        'price': 199.99,
        'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
        'description': 'Feature-rich smartwatch with fitness tracking'
    },
    {
        'id': 3,
        'name': 'Laptop Stand',
        'price': 49.99,
        'image': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400',
        'description': 'Ergonomic aluminum laptop stand'
    },
    {
        'id': 4,
        'name': 'Mechanical Keyboard',
        'price': 129.99,
        'image': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400',
        'description': 'RGB mechanical keyboard with blue switches'
    },
    {
        'id': 5,
        'name': 'USB-C Hub',
        'price': 39.99,
        'image': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400',
        'description': 'Multi-port USB-C hub with HDMI and SD card reader'
    },
    {
        'id': 6,
        'name': 'Wireless Mouse',
        'price': 29.99,
        'image': 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=400',
        'description': 'Ergonomic wireless mouse with precision tracking'
    }
]

@app.route('/')
def home():
    """Home page"""
    return render_template('home.html', featured_products=PRODUCTS[:3])

@app.route('/shop')
def shop():
    """Shop page with all products"""
    return render_template('shop.html', products=PRODUCTS)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return redirect(url_for('shop'))
    
    # Get 3 random related products (excluding current product)
    related = [p for p in PRODUCTS if p['id'] != product_id][:3]
    
    return render_template('product_detail.html', product=product, related_products=related)

@app.route('/cart')
def cart():
    """Shopping cart page"""
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    
    # Find product
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404
    
    # Get or create cart
    if 'cart' not in session:
        session['cart'] = []
    
    cart = session['cart']
    
    # Check if product already in cart
    existing_item = next((item for item in cart if item['id'] == product_id), None)
    if existing_item:
        existing_item['quantity'] += 1
    else:
        cart.append({
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'image': product['image'],
            'quantity': 1
        })
    
    session['cart'] = cart
    session.modified = True
    
    return jsonify({'success': True, 'cart_count': len(cart)})

@app.route('/update-cart', methods=['POST'])
def update_cart():
    """Update cart item quantity"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    cart = session.get('cart', [])
    
    for item in cart:
        if item['id'] == product_id:
            if quantity <= 0:
                cart.remove(item)
            else:
                item['quantity'] = quantity
            break
    
    session['cart'] = cart
    session.modified = True
    
    return jsonify({'success': True})

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    """Remove item from cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    
    session['cart'] = cart
    session.modified = True
    
    return jsonify({'success': True})

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout page"""
    cart_items = session.get('cart', [])
    
    if not cart_items:
        return redirect(url_for('cart'))
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        # Clear cart and show success (no Telegram notification for orders)
        session['cart'] = []
        session.modified = True
        return render_template('order_success.html')
    
    return render_template('checkout.html', cart_items=cart_items)

@app.route('/about')
def about():
    """About us page"""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Send contact message to Telegram
        notifier = TelegramNotifier()
        contact_data = {
            'name': name,
            'email': email,
            'phone': 'N/A',
            'address': f'Contact Message: {message}',
            'items': []
        }
        notifier.send_order(contact_data)
        
        return render_template('contact.html', success=True)
    
    return render_template('contact.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
