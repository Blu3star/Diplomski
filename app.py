from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orderproduct.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Name %r>" % self.id


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/order", methods=["POST", "GET"])
# @app.route("/order")
def order():
    if request.method == "POST":
        product_name = request.form["product"]
        new_product = Order(name=product_name)

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect("/order")
        except:
            return "Pojavio se problem! Pokušajte ponovno."

    else:
        product = Order.query.order_by(Order.date_created)
        return render_template("order.html", product=product)


@app.route("/manufacturing")
def proizvodnja():
    return render_template("manufacturing.html")


@app.route("/finishedproduct")
def gotoviproizvodi():
    return render_template("finishedproduct.html")


if __name__ == "__main__":
    app.run(debug=True)
