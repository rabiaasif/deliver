from flask import request, Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

POSTGRES = {
    'user': 'nytxnomc',
    'pw': 'i-ilLZpUOx26pNnbh8ZBm0mBjBRdc0xO',
    'db': 'nytxnomc',
    'host': 'fanny.db.elephantsql.com',
    'port': '5432',
}


db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, description, quantity):
        self.description = description
        self.quantity = quantity

@app.route('/')
def hello():
    print(1111)
    print(db)
    return '<a href="/addperson"><button> Click here </button></a>'

@app.route("/addperson", methods=['POST'])
def addperson():
    print(22222)
    description = request.form["description"]
    print(description)
    quantity = request.form["quantity"]
    entry = Item(description, quantity)
    print(entry)
    print(22222)
    # db.session.add(entry)
    # db.session.commit()
    return "coming soon" + description 
# if __name__ == '__main__':
#     app.run()