from flask import request, Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://nytxnomc:i-ilLZpUOx26pNnbh8ZBm0mBjBRdc0xO@fanny.db.elephantsql.com/nytxnomc"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)
# migrate = Migrate(app, db)



class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, description, quantity, price):
        self.description = description
        self.quantity = quantity
        self.price = price

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_amount = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(100))

    def __init__(self, note, payment_amount):
        self.note = note
        self.payment_amount = payment_amount        

class ItemsOrdered(db.Model):
    __tablename__ = 'items_ordered'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __init__(self, order_id, item_id):
        self.order_id = order_id
        self.item_id = item_id


@app.route('/')
def hello():
    return "go to -> /update-item-by-id/<id> to update an item on the menu. This is a post request and it has optional data to enter description, quantity, and price. id is required\n \
    go to -> /add-item to add an item to the menu. This is a post request and it requires a description, quantity, and price \n \
    go to -> /get-menu-items to retrive menu items. this is a get request and does not require any extra params or data \n \
    go to -> /add-order to add an order from the menu. this is a post request. items is required and it takes the form item_id1,item_id3...,item_idn. note is optional  \
    go to -> /delete-item-by-id/<id> to delete a menu item. replace <id> with the id you wish to delete \n"

@app.route("/add-item", methods=['POST'])
def add_item():
    try:
        description = request.form["description"]
        quantity = request.form["quantity"]
        price = request.form["price"]
        entry = Item(description, quantity, price)
        db.session.add(entry)
        db.session.commit()
        return "Added Item to Menu: " + description + " quantity:" + str(quantity) + " price: $" + price
    except:
        return "Something went wrong...Menu items take a price, quantity, and description. Please try again."

@app.route("/get-menu-items")
def get_menu():
    try:
        menu_items = "<div> <h1> Menu </h1>"
        menu_items  += " <table> <tr> <th>ID</th> <th>Description</th> <th>Price</th></tr>"
        for item in Item.query.all():
            menu_items +=  "<tr>" + "<td>"+ str(item.id) + "</td>" + "<td>" +item.description + "</td>" + "<td>" + "$" + item.price + "</td>" + "</tr>"
        return menu_items + "</table> </div>"
    except:
        "Something went wrong..."

@app.route("/delete-item-by-id/<id>", methods=["DELETE"])
def delete_item(id):
    try:
        item = Item.query.filter_by(id=id).first()
        db.session.delete(item)
        db.session.commit()
        return "deleted item: " + str(item.id) + " " + item.description
    except Exception as e:
        return "Something went wrong...perhaps this item does not exist"

@app.route("/update-item-by-id/<id>", methods=["POST"])
def update_item(id):
    try:
        form_to_dict = request.form.to_dict()
        item = Item.query.filter_by(id=id).first()
        if 'description' in form_to_dict:
            item.description = request.form['description']
        if 'price' in form_to_dict:
            item.price = request.form['price']
        if 'quantity' in form_to_dict:
            item.quantity = request.form['quantity']
        item = db.session.merge(item)
        db.session.commit()
        return "Added Item to updated: " + item.description + " quantity:" + str(item.quantity) + " price: $" + item.price
    except Exception as e:
        print(e)
        return "Something went wrong... Please try again."

@app.route("/add-order", methods=['POST'])
def add_order():
    try:
        form_to_dict = request.form.to_dict()
        note = ""
        if 'note' in form_to_dict:
            note = request.form['note']
        items = request.form["items"].split(",")
        payment_amount = 0
        for id in items:
            item = Item.query.filter_by(id=id).first()
            payment_amount += int(item.price)
        order = Order(note, payment_amount)
        db.session.add(order)
        order_description = ""
        for id in items:
            item = Item.query.filter_by(id=id).first()
            order_description += item.description
            if id != items[-1]:
                order_description += ", "
            entry = ItemsOrdered(order.id, item.id)
            db.session.add(entry)
        db.session.commit()
        return "Added Order: " + order_description + ". \n The payment amount is: $" + str(payment_amount) + "\n Additional notes: " + note
    except Exception as e:
        print(e)
        return "Something went wrong...to create an order provide items ids seperated by commas 1,2,3,4..."
