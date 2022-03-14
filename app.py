from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orderproduct.db"
app.config["SQLALCHEMY_BINDS"] = {"warehouse": "sqlite:///warehouseproduct.db"}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Name %r>" % self.id


class Warehouse(db.Model):
    __bind_key__ = "warehouse"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Name %r>" % self.id


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/order", methods=["POST", "GET"])
def order():
    if request.method == "POST":
        product_name = request.form["product"]
        new_product = Order(name=product_name)

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect("/order")
        except all:
            return "Pojavio se problem! Pokušajte ponovno."

    else:
        product = Order.query.order_by(Order.date_created)
        return render_template("order.html", product=product)


@app.route("/warehouse", methods=["POST", "GET"])
def skladiste():
    if request.method == "POST":
        sirovac_name = request.form["sirovac"]
        kolicina_name = request.form["kolicina"]
        new_sirovac = Warehouse(name=sirovac_name, quantity=kolicina_name)

        try:
            db.session.add(new_sirovac)
            db.session.commit()
            return redirect("/warehouse")
        except all:
            return "Pojavio se problem! Pokušajte ponovno."

    else:
        sirovac = Warehouse.query.order_by(Warehouse.id)
        return render_template("warehouse.html", sirovac=sirovac)


@app.route("/manufacturing")
def proizvodnja():
    product = Order.query.order_by(Order.date_created)
    return render_template("manufacturing.html", product=product)


@app.route("/finishedproduct")
def gotoviproizvodi():
    return render_template("finishedproduct.html")


if __name__ == "__main__":
    app.run(debug=True)
