from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nytxnomc:i-ilLZpUOx26pNnbh8ZBm0mBjBRdc0xO@fanny.db.elephantsql.com/nytxnomc'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.secret_key = 'secret string'

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, pname, color):
        self.description = description
        self.quantity = quantity

@app.route('/')
def hello():
    return '<a href="/addperson"><button> Click here </button></a>'

@app.route("/addperson")
def addperson():
    return "coming soon"
# if __name__ == '__main__':
#     app.run()