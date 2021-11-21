from flask import request, Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://nytxnomc:i-ilLZpUOx26pNnbh8ZBm0mBjBRdc0xO@fanny.db.elephantsql.com/nytxnomc"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(100), unique=True, nullable=False)
    item_modifier_id = db.Column(db.Integer, db.ForeignKey('item_modifier.id'))

    def __init__(self, description, quantity, price, item_modifier_id):
        self.description = description
        self.quantity = quantity
        self.price = price
        self.item_modifier_id = item_modifier_id

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
    quantity = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __init__(self, order_id, item_id, quantity):
        self.order_id = order_id
        self.item_id = item_id
        self.quantity = quantity

class ItemModifier(db.Model):
    __tablename__ = 'item_modifier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subgroup = db.Column(db.Integer, db.ForeignKey('item_modifier.id'))

    def __init__(self, name, subgroup):
        self.name = name
        self.subgroup = subgroup

@app.route('/')
def hello():
    description = "<div>"
    description += "<h2> View Menu </h2>"
    description += "<p> Go to <a href=\"/menu\"> /menu </a> This is a get request and doesnt require any additional information </p>"
    description += "<h2> Add Menu Item </h2>"
    description += "<p> Go to <a href=\"/add-item\"> /add-item </a> This is a post request and requires some additional information. Click 'Body' on post man and select 'x-www-form-urlencoded'. Required params: quantity (int), description (str), and price (int). item_modifier_id (int) is optional </p>"
    description += "<h2> Add Modifier </h2>"
    description += "<p> Go to <a href=\"/add-modifier\"> /add-modifier </a> This is a post request. Required body: name (str). Optional: subgroup (int) an id of another modifier</p>"
    description += "<h2> Delete Menu Item </h2>"
    description += "<p> Go to <a href=\"/delete-item-by-id/<id>\"> /delete-item-by-id/<id> </a> This is a delete request. Replace <id> with an item id to remove it from the menu. id is a required field</p>"
    description += "<h2> Update Menu Item </h2>"
    description += "<p> Go to <a href=\"/update-item-by-id/<id>\"> /update-item-by-id/<id> </a> This is a post request. This request takes optional body: quantity (int), description (str), price (int), item_modifier_id (int) </p>"
    description += "<h2> Create An Order </h2>"
    description += "<p> Go to <a href=\"/add-order\"> /add-order </a> This is a post request. it requires 'items' in the following format 4:1, 5:1 (item_id:quantity, item_id2:quantity,...). notes(str) is optional</p>"
    description += "</div>"    
    return description

@app.route("/add-item", methods=['POST'])
def add_item():
    try:
        form_to_dict = request.form.to_dict()
        description = request.form["description"]
        quantity = request.form["quantity"]
        price = request.form["price"]
        item_modifier_id = None
        item_modifier = "<p> Modifier group: None </p>"
        if 'item_modifier_id' in form_to_dict:
            item_modifier_id = request.form['item_modifier_id']
            modifier = ItemModifier.query.filter_by(id = item_modifier_id).first().name
            item_modifier = "<p> Modifier Group: " + modifier +"</p>"
        entry = Item(description, quantity, float(price), item_modifier_id)
        db.session.add(entry)
        db.session.commit()
        return "<div> <h3>Added Item to Menu</h3>" +  "<br> Item id: "+ str(entry.id) +  "<p> Description: " + description +  "<p> <p>Quantity:" + str(quantity) + "</p> price: $" + price + " </p>" +  item_modifier + " </div>"
    except:
        return "Something went wrong...Check the spelling of the data provided. Please make sure there is no $ infront of price"

@app.route("/add-modifier", methods=['POST'])
def add_modifier():
    try:
        form_to_dict = request.form.to_dict()
        name = request.form["name"]
        subgroup = None
        if 'subgroup' in form_to_dict:
            subgroup = request.form["subgroup"]
        entry = ItemModifier(name, subgroup)
        db.session.add(entry)
        db.session.commit()
        return "Added Modifier: <br> id:" + str(entry.id) + "<br> name:" + name
    except:
        return "Something went wrong...Body should include: name (required), and subgroup(optional)"

@app.route("/menu")
def get_menu():
    try:
        menu_items = "<div> <h1> Menu </h1>"
        menu_items  += " <table> <tr> <th>ID</th> <th>Description</th> <th>Price</th> <th>Modifer</th> </tr>"
        for item in Item.query.all():
            modifier = ""
            if item.item_modifier_id:
                modifier = ItemModifier.query.filter_by(id = item.item_modifier_id).first().name
            menu_items +=  "<tr>" + "<td>"+ str(item.id) + "</td>" + "<td>" +item.description + "</td>" + "<td>" + "$" + item.price + "</td>" + "<td>" + modifier + "</td>" +  "</tr>"
        return menu_items + "</table> </div>"
    except:
        "Something went wrong..."

@app.route("/delete-item-by-id/<id>", methods=["DELETE"])
def delete_item(id):
    try:
        item = Item.query.filter_by(id=id).first()
        db.session.delete(item)
        db.session.commit()
        return "<div> <h3>Deleted item</h3> <p> Item Id: " + str(item.id) + "</p> <p> Item Description:" + item.description
    except:
        return "Something went wrong...perhaps this item does not exist"

@app.route("/update-item-by-id/<id>", methods=["POST"])
def update_item(id):
    try:
        form_to_dict = request.form.to_dict()
        item = Item.query.filter_by(id=id).first()
        if 'description' in form_to_dict:
            item.description = request.form['description']
        if 'price' in form_to_dict:
            item.price = float(request.form['price'])
        if 'quantity' in form_to_dict:
            item.quantity = request.form['quantity']
        modifier = "<br> Modifier Group: Not Updated"
        if item.item_modifier_id:
            modifier = "<br> Modifier Group: " + ItemModifier.query.filter_by(id = item.item_modifier_id).first().name
        if 'item_modifier_id' in form_to_dict:
            item.item_modifier_id = request.form['item_modifier_id']
            modifier = "<br> Modifier Group: " + ItemModifier.query.filter_by(id = item.item_modifier_id).first().name
        item = db.session.merge(item)
        db.session.commit()
        return "<div> <h3>Added Item to updated </h3> Description: " + item.description + " <br> Quantity: " + str(item.quantity) + " <br> Price: $" + item.price + modifier + "</div>"
    except:
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
        for id_and_quantity in items:
            item_id = id_and_quantity.split(":")[0]
            quantity = id_and_quantity.split(":")[-1]
            item = Item.query.filter_by(id=item_id).first()
            if int(quantity) > int(item.quantity):
                return item.description + " only has " + str(item.quantity) + " available"
            payment_amount += float(quantity) * float(item.price)
        order = Order(note, payment_amount)
        db.session.add(order)
        order_description = ""
        for id_and_quantity in items:
            item_id = id_and_quantity.split(":")[0]
            quantity = id_and_quantity.split(":")[-1]
            item = Item.query.filter_by(id=item_id).first()
            order_description += "(" + str(quantity) + ") " + item.description 
            if id_and_quantity != items[-1]:
                order_description += ", "
            entry = ItemsOrdered(order.id, item.id, quantity)
            item.quantity = int(item.quantity) - int(quantity)
            item = db.session.merge(item)
            db.session.add(entry)
        db.session.commit()
        return  "<div> The order id: "+ str(order.id) + "<br> Order: " + order_description + ". <br> The payment amount: $" + str(payment_amount) + "<br> Additional notes: " + note
    except:
        return "Something went wrong...to create an order provide items ids and quantity 4:1, 5:1 (item_id:quantity, item_id2:quantity,...)- should not be in quotes. Confirm that your item id exists"

if __name__ == '__main__':  
    app.run()