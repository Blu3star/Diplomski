from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

engine = create_engine("sqlite:///database.db", echo=False)
meta_data = db.MetaData(bind=engine)
db.MetaData.reflect(meta_data)
session = sessionmaker(bind=engine)

ID = -1


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    order_id = db.Column(db.Integer)
    name = db.Column(db.String(500), nullable=False)
    buyer_name = db.Column(db.String(500), nullable=False)
    buyer_contact = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    first_time = True

    def __repr__(self):
        return "<Name %r>" % self.id

    def getLastOrderID(self):
        order_table = pd.read_sql_table(table_name="order", con=engine)
        column_ID = order_table["order_id"].tolist()
        if len(column_ID):
            return column_ID[-1]

        return 9999


class Input_Warehouse(db.Model):
    __tablename__ = "input_warehouse"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Name %r>" % self.id


class Part(db.Model):
    __tablename__ = "part"
    part_id = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String(200))
    part_raw_mat = db.Column(db.String(500))
    part_length = db.Column(db.Integer)
    part_price = db.Column(db.Integer)

    def __repr__(self):
        return "<Name %r>" % self.id


class Assembly(db.Model):
    __tablename__ = "assembly"
    assembly_id = db.Column(db.Integer, primary_key=True)
    assembly_name = db.Column(db.String(200))
    assembly_peaces = db.Column(db.Integer)
    assembly_price = db.Column(db.Integer)

    def __repr__(self):
        return "<Name %r>" % self.id


class Machine(db.Model):
    __tablename__ = "machine"
    machine_id = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String(200))
    machine_tool = db.Column(db.String(200))
    tool_change_interval = db.Column(db.String(200))
    machine_service = db.Column(db.String(200))
    machined_parts = db.Column(db.Integer)

    def __repr__(self):
        return "<Name %r>" % self.id


class Worker(db.Model):
    __tablename__ = "worker"
    worker_id = db.Column(db.Integer, primary_key=True)
    worker_name = db.Column(db.String(500))
    worker_department = db.Column(db.String(200))

    def __repr__(self):
        return "<Name %r>" % self.id


class Manufacturing(db.Model):
    __tablename__ = "manufacturing"
    auto_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    machine_id = db.Column(db.Integer)
    manufacturing_status = db.Column(db.String(200))
    manufacturing_time = db.Column(db.String(200))
    manufacturing_worker = db.Column(db.Integer)

    def __repr__(self):
        return "<Name %r>" % self.id


class Installation(db.Model):
    __tablename__ = "installation"
    auto_id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer)
    installation_status = db.Column(db.String(200))
    installation_time = db.Column(db.String(200))
    installation_worker = db.Column(db.Integer)

    def __repr__(self):
        return "<Name %r>" % self.id


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/order", methods=["POST", "GET"])
def order():
    global ID
    if Order.first_time:
        ID = Order().getLastOrderID()
        Order.first_time = False

    if request.method == "POST":
        product_name = request.form["product"]
        new_buyer_name = request.form["buyer_name"]
        new_buyer_contact = request.form["phone"]

        ID = ID + 1
        new_product = Order(
            name=product_name,
            buyer_name=new_buyer_name,
            buyer_contact=new_buyer_contact,
            order_id=ID,
        )

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
def warehouse():
    if request.method == "POST":
        raw_mat_name = request.form["sirovac"]
        quantity_value = request.form["kolicina"]
        new_raw_mat = Input_Warehouse(name=raw_mat_name, quantity=quantity_value)
        user_table = pd.read_sql_table(table_name="input_warehouse", con=engine)
        exists = False
        for _, row in user_table.iterrows():
            if row["name"] == raw_mat_name:
                print(row["quantity"])
                table_val = row["quantity"]
                updated_value = table_val + int(quantity_value)
                new_raw_mat = Input_Warehouse(name=raw_mat_name, quantity=updated_value)
                exists = True

        try:
            if exists:
                conn = engine.connect()
                stmt = (
                    update(Input_Warehouse)
                    .where(Input_Warehouse.name == raw_mat_name)
                    .values(quantity=updated_value)
                )
                conn.execute(stmt)
            else:
                db.session.add(new_raw_mat)
            db.session.commit()
            return redirect("/warehouse")
        except all:
            return "Pojavio se problem! Pokušajte ponovno."

    else:
        raw_mat = Input_Warehouse.query.order_by(Input_Warehouse.id)
        return render_template("warehouse.html", sirovac=raw_mat)


@app.route("/manufacturing")
def manufacturing():
    product = Order.query.order_by(Order.date_created)
    return render_template("manufacturing.html", product=product)


@app.route("/finishedproduct")
def finished_product():
    return render_template("finishedproduct.html")


if __name__ == "__main__":
    HOST = os.environ.get("SERVER_HOST", "localhost")

    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))

    except ValueError:
        PORT = 5555

    app.run(HOST, PORT)
