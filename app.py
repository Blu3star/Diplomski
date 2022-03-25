from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
import pandas as pd

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

engine = create_engine("sqlite:///database.db", echo=False)
meta_data = db.MetaData(bind=engine)
db.MetaData.reflect(meta_data)
session = sessionmaker(bind=engine)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Name %r>" % self.id


class Warehouse(db.Model):
    __tablename__ = "warehouse"
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
        user_table = pd.read_sql_table(table_name="warehouse", con=engine)
        exists = False
        for _, row in user_table.iterrows():
            if row["name"] == sirovac_name:
                print(row["quantity"])
                table_val = row["quantity"]
                updated_value = table_val + int(kolicina_name)
                new_sirovac = Warehouse(name=sirovac_name, quantity=updated_value)
                exists = True

        try:
            if exists:
                conn = engine.connect()
                stmt = (
                    update(Warehouse)
                    .where(Warehouse.name == sirovac_name)
                    .values(quantity=updated_value)
                )
                conn.execute(stmt)
            else:
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

    import os

    HOST = os.environ.get("SERVER_HOST", "localhost")

    try:

        PORT = int(os.environ.get("SERVER_PORT", "5555"))

    except ValueError:

        PORT = 5555

    app.run(HOST, PORT)

# if __name__ == "__main__":
#     app.run(debug=True)
