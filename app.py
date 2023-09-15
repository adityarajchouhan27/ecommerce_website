# from curses import flash
from flask import Flask, render_template, request, redirect, url_for, session
import random
import stripe
from flask import jsonify

# Configure Stripe with your secret key
stripe.api_key = 'your_stripe_secret_key'

app = Flask(__name__)
app.secret_key = "aditya27"

# Database to store registered users (in-memory for simplicity)
users_db = {}


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users_db[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users_db and users_db[username] == password:
            session['username'] = username
            return redirect(url_for('otp_verification'))

    return render_template('login.html')


@app.route('/otp_verification', methods=['GET', 'POST'])
def otp_verification():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        otp_input = request.form['otp']
        otp_generated = session.get('otp')

        # if otp_input == otp_generated:
        #     return "OTP Verification Successful!"
        # else:
        #     return "Invalid OTP. Please try again."

    # Generate and store the OTP in the session
    otp = str(random.randint(1000, 9999))
    session['otp'] = otp
    return render_template('product_catalog.html', products=products)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


# Add a route for changing the password
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        if username in users_db and users_db[username] == old_password:
            users_db[username] = new_password
            return "Password changed successfully."
        else:
            return "Invalid old password. Please try again."

    return render_template('change_password.html')


# Add a route for resetting the password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        # Check if the email exists in the user database
        for username, user_email in users_db.items():
            if user_email == email:
                # Generate and send a new password (for simplicity, we'll just print it)
                new_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
                users_db[username] = new_password
                return f"Your new password is: {new_password}"

        return "Email not found. Please try again."

    return render_template('forgot_password.html')

# Define a list of products with their details
products = [
    {
        'id': 1,
        'name': 'Product 1',
        'description': 'Description for Product 1',
        'amount': 10.99,
        'image_url': '/static/product1.jpg',
    },
    {
        'id': 2,
        'name': 'Product 2',
        'description': 'Description for Product 2',
        'amount': 15.99,
        'image_url': '/static/product2.jpg',
    },
    # Add more products as needed
]

# ...

# # Initialize a session variable for the shopping cart
# app.config['CART_KEY'] = 'cart'
# if 'cart' not in session:
#     session['cart'] = []

# # ...

# # Add a route to display the shopping cart
# @app.route('/cart')
# def view_cart():
#     cart = session['cart']
#     cart_products = [product for product in products if product['id'] in cart]
#     return render_template('cart.html', cart_products=cart_products)

# # Add a route to add a product to the cart
# @app.route('/add_to_cart/<int:product_id>')
# def add_to_cart(product_id):
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     if product_id not in session['cart']:
#         session['cart'].append(product_id)
#         flash('Product added to the cart', 'success')
#     else:
#         flash('Product is already in the cart', 'warning')
#     return redirect(url_for('view_cart'))

# # Add a route to remove a product from the cart
# @app.route('/remove_from_cart/<int:product_id>')
# def remove_from_cart(product_id):
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     if product_id in session['cart']:
#         session['cart'].remove(product_id)
#         flash('Product removed from the cart', 'success')
#     else:
#         flash('Product is not in the cart', 'warning')
#     return redirect(url_for('view_cart'))


# @app.route('/charge', methods=['POST'])
# def charge():
#     token = request.json.get('token')

#     try:
#         charge = stripe.Charge.create(
#             amount=1000,  # The amount in cents (adjust as needed)
#             currency='usd',
#             description='Example Charge',
#             source=token,
#         )
#         return jsonify(success=True)
#     except stripe.error.StripeError as e:
#         return jsonify(success=False, error=str(e))

# # Update the /cart route to display the checkout button
# @app.route('/cart')
# def view_cart():
#     cart = session['cart']
#     cart_products = [product for product in products if product['id'] in cart]
#     return render_template('cart.html', cart_products=cart_products)

# # Add a route for the checkout process
# @app.route('/checkout', methods=['GET', 'POST'])
# def checkout():
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         # Handle the checkout form (if needed)
#         pass

#     return render_template('checkout.html')


if __name__ == '__main__':
    app.run(debug=True)
