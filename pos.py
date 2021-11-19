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

@app.route('/')
def hello():
    return '<a href="/additem"><button> Click here </button></a>'

@app.route("/additem", methods=['POST'])
def add_item():
    description = request.form["description"]
    quantity = request.form["quantity"]
    price = request.form["price"]
    entry = Item(description, quantity, price)
    db.session.add(entry)
    db.session.commit()
    return "coming soon" + description 


@app.route("/get-menu-items")
def add_item():
    return "coming soon"
