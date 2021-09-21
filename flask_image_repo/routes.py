from flask import render_template, url_for, flash, redirect, request
from flask_image_repo.forms import LoginForm, SignupForm, BuyForm, ImageForm
from flask_image_repo import app, db, bcrypt
from flask_image_repo.models import Seller, Image, Customer, Order
from flask_login import login_user, current_user, logout_user, login_required, login_required

images = [
    {
        'title': 'Beach',
        'price': '$100'
    },
    {
        'title': 'Shoe',
        'price': '$101'
    }
]

@app.route("/")
def home():
    db_images = Image.query.all()

    images = []
    if len(db_images) != 0:
        for db_image in db_images:
            dis_price = db_image.price - (db_image.price*(db_image.discount)/100.00)

            images.append({
                "id":  db_image.id,
                "name":  db_image.name,
                "src":   url_for('static', filename='images/' + db_image.image_file),
                "price": "$%.2f" % (db_image.price),
                "stock": "%d left" % (db_image.stock),
                "discounted": "$%.2f" % (dis_price),
            })

    return render_template('home.html', images=images)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    form = SignupForm()

    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        seller = Seller(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(seller)
        db.session.commit()
        flash('Successful, login to new account.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html', title='Signup', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        seller = Seller.query.filter_by(email=form.email.data).first()
        if seller and bcrypt.check_password_hash(seller.password, form.password.data):
            login_user(seller)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Password or Email is incorrect try again!', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    db_images = Seller.query.get(current_user.id).images

    images = []
    for db_image in db_images:
        dis_price = db_image.price - (db_image.price*(db_image.discount)/100.00)

        images.append({
            "id":  db_image.id,
            "name":  db_image.name,
            "src":   url_for('static', filename='images/' + db_image.image_file),
            "price": "$%.2f" % (db_image.price),
            "stock": "%d left" % (db_image.stock),
            "discounted": "$%.2f" % (dis_price),
        })

    orders = Seller.query.get(current_user.id).orders

    order_l = []
    for order in orders:
        order_l.append({
            "image_name":  Image.query.get(order.image_id).name,
            "price": "$%.2f" % (Image.query.get(order.image_id).price),
            "customer_name":  Customer.query.get(order.customer_id).first_name+" "+Customer.query.get(order.customer_id).last_name,
            "customer_address":  Customer.query.get(order.customer_id).address,
            "customer_email":  Customer.query.get(order.customer_id).customer_email,
        })
    return render_template('account.html', title='Account', images=images, order_l=order_l)

@app.route("/buy/<image_id>", methods=['GET', 'POST'])
def buy(image_id):
    form = BuyForm()

    if not image_id:
        return render_template("home.html", message="Invalid product ID!")

    if form.validate_on_submit():
        if not Customer.query.filter_by(customer_email=form.email.data).all():
            customer = Customer(first_name=form.first_name.data, last_name=form.last_name.data, customer_email=form.email.data, address=form.address.data, payment=form.payment.data)
            db.session.add(customer)
            db.session.commit()

        customer_id = Customer.query.get(Customer.query.filter_by(customer_email=form.email.data).first().id)

        order = Order(amount=1, customer_id=customer_id.id, image_id=Image.query.get(image_id).id)
        db.session.add(order)
        db.session.commit()
        flash('Your Order is Being processed', 'success')
        return redirect(url_for('home'))

    return render_template('buy.html', title='buy', form=form)

@app.route("/update/<image_id>", methods=['GET', 'POST'])
@login_required
def update(image_id):
    image= Image.query.get(image_id)
    form = ImageForm()
    if form.validate_on_submit():
        image.name = form.name.data
        image.stock = form.stock.data
        image.discount = form.discount.data
        image.price = form.price.data
        db.session.commit()
        flash('The image information has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = image.name
        form.stock.data = image.stock
        form.discount.data = image.discount
        form.price.data = image.price

    return render_template('image.html', title='update', form=form)
