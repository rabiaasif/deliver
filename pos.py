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

    def __init__(self, id, description, quantity):
        self.id = id
        self.description = description
        self.quantity = quantity

@app.route('/')
def hello():
    print(1111)
    return '<a href="/addperson"><button> Click here </button></a>'

@app.route("/addperson", methods=['POST'])
def addperson():
    print(22222)
    description = request.form["description"]
    print(description)
    quantity = request.form["quantity"]
    entry = Item(3, description, quantity)
    print(entry)
    print(22222)
    db.session.add(entry)
    db.session.commit()
    return "coming soon" + description 
# if __name__ == '__main__':
#     app.run()