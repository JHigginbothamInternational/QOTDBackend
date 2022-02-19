from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://xwnaiaitppoyqu:0e42ecc55dfc84506f8528848093341064f9c140c5ec31d04777fbf6e791f27c@ec2-44-193-188-118.compute-1.amazonaws.com:5432/d9jc3e3itgov4d"

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    author = db.Column(db.String)

    def __init__(self, text, author):
        self.text = text
        self.author = author

class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    quote = db.Column(db.Integer, nullable=False)

    def __init__(self, day, quote):
        self.day = day
        self.quote = quote

class QuoteSchema(ma.Schema):
    class Meta:
        fields = ("id", "text", "author")

quote_schema = QuoteSchema()
multiple_quote_schema = QuoteSchema(many=True)

class DateSchema(ma.Schema):
    class Meta:
        fields = ("id", "day", "quote")

date_schema = DateSchema()
multiple_date_schema = DateSchema(many=True)




@app.route("/quote/add", methods=["POST"])
def add_quote():
    if request.content_type != "application/json":
        return jsonify("ERROR: Data must be sent as JSON.")

    post_data = request.get_json()
    text = post_data.get("text")
    author = post_data.get("author")

    record = Quote(text, author)
    db.session.add(record)
    db.session.commit()

    return jsonify(quote_schema.dump(record))

@app.route("/quote/get/<id>", methods=["GET"])
def get_quote_by_id(id):
    record = db.session.query(Quote).filter(Quote.id == id).first()
    return jsonify(quote_schema.dump(record))

@app.route("/date/add", methods=["POST"])
def create_initial_date():
    record_check = db.session.query(Date).first()
    if record_check is not None:
        return jsonify("ERROR: Date has already been initialized.")

    if request.content_type != "application/json":
        return jsonify("ERROR: Data must be sent as JSON.")

    post_data = request.get_json()
    day = post_data.get("day")
    quote = post_data.get("quote")

    record = Date(day, quote)
    db.session.add(record)
    db.session.commit()

    return jsonify(date_schema.dump(record))

if __name__ == "__main__":
    app.run(debug=True)