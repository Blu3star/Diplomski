import json
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

with open("part.json", "r") as f_p:
    j_part_data = json.load(f_p)

with open("assembly.json", "r") as f_a:
    j_assembly_data = json.load(f_a)
print(j_part_data)
print(j_assembly_data)


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


def putDataInTablePart():
    part_data = [
        Part(
            part_name="Osnovni element 1",
            part_raw_mat="Čelična šipka 20x20",
            part_length="100",
            part_price="200",
        ),
        Part(
            part_name="Osnovni element 2",
            part_raw_mat="Čelična šipka 30x30",
            part_length="200",
            part_price="300",
        ),
        Part(
            part_name="Osnovni element 3",
            part_raw_mat="Čelična šipka 20x20",
            part_length="150",
            part_price="250",
        ),
    ]
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    session.add_all(part_data)
    session.commit()

    part_table = pd.read_sql_table(table_name="part", con=engine)
    print(part_table)


class Assembly(db.Model):
    __tablename__ = "assembly"
    assembly_id = db.Column(db.Integer, primary_key=True)
    assembly_name = db.Column(db.String(200))
    assembly_peaces = db.Column(db.Integer)
    assembly_price = db.Column(db.Integer)

    def __repr__(self):
        return "<Name %r>" % self.id


def putDataInTableAssembly():
    assembly_data = [
        Assembly(assembly_name="Sklop 1", assembly_peaces="5", assembly_price="1000"),
        Assembly(assembly_name="Sklop 2", assembly_peaces="7", assembly_price="1500"),
        Assembly(assembly_name="Sklop 3", assembly_peaces="4", assembly_price="800"),
    ]
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    session.add_all(assembly_data)
    session.commit()

    assembly_table = pd.read_sql_table(table_name="assembly", con=engine)
    print(assembly_table)


class Machine(db.Model):
    __tablename__ = "machine"
    machine_id = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String(200))
    machine_tool = db.Column(db.String(200))
    last_tool_change_date = db.Column(db.String(200))
    last_machine_service_date = db.Column(db.String(200))
    number_of_machined_parts = db.Column(db.Integer)

    def __repr__(self):
        return "<Name %r>" % self.id


def putDataInTableMachine():
    machine_data = [
        Machine(
            machine_name="Tokarilica",
            machine_tool="Tokarski nož",
            last_tool_change_date="12.10.2021",
            last_machine_service_date="11.2.2022",
            number_of_machined_parts="10",
        ),
        Machine(
            machine_name="Glodalica",
            machine_tool="Glodalo",
            last_tool_change_date="10.6.2021",
            last_machine_service_date="5 ozujka 2020",
            number_of_machined_parts="12",
        ),
        Machine(
            machine_name="Bušilica",
            machine_tool="Svrdlo",
            last_tool_change_date="04 travnja. 2022",
            last_machine_service_date="10 sijecnja 2021",
            number_of_machined_parts="5",
        ),
    ]

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    session.add_all(machine_data)
    session.commit()

    machine_table = pd.read_sql_table(table_name="machine", con=engine)
    print(machine_table)


class Worker(db.Model):
    __tablename__ = "worker"
    worker_id = db.Column(db.Integer, primary_key=True)
    worker_name = db.Column(db.String(500))
    worker_department = db.Column(db.String(200))

    def __repr__(self):
        return "<Name %r>" % self.id


def putDataInTableWorker():
    worker_data = [
        Worker(worker_name="Marko Maric", worker_department="Proizvodnja"),
        Worker(worker_name="Ante Antic", worker_department="Proizvodnja"),
        Worker(worker_name="Ivo Ivic", worker_department="Montaža"),
    ]

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    session.add_all(worker_data)
    session.commit()

    worker_table = pd.read_sql_table(table_name="worker", con=engine)
    print(worker_table)


class Manufacturing(db.Model):
    __tablename__ = "manufacturing"
    auto_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    part_id = db.Column(db.Integer)
    machine_id = db.Column(db.Integer)
    manufacturing_status = db.Column(db.String(200))
    manufacturing_time = db.Column(db.String(200))
    manufacturing_worker = db.Column(db.Integer)

    def __repr__(self):
        return "<Name %r>" % self.id


class Installation(db.Model):
    __tablename__ = "installation"
    auto_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    installation_id = db.Column(db.Integer)
    part_id = db.Column(db.Integer)
    installation_status = db.Column(db.String(200))
    installation_time = db.Column(db.String(200))
    installation_worker = db.Column(db.Integer)

    def __repr__(self):
        return "<Name %r>" % self.id


@app.route("/")
def index():
    return render_template("index.html")


def getResourceFromWarehouse(part_detail):
    input_table = pd.read_sql_table(table_name="input_warehouse", con=engine)
    raw_mat_name = input_table["name"].tolist()
    if part_detail in raw_mat_name:
        print("getResourceFromWarehouse")
        row = input_table.loc[input_table.name == part_detail]
        print(row)
        return int(row.quantity)
    else:
        print("error")
        return -1


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

        for part_name in j_part_data:
            if product_name == part_name:
                print(part_name)
                if type(j_part_data[part_name]) == type([]):
                    for part_details in j_part_data[part_name]:
                        print(part_details)
                        print(part_details[list(part_details.keys())[0]])
                        length_in_stock = getResourceFromWarehouse(
                            part_details[list(part_details.keys())[0]]
                        )
                        if length_in_stock >= int(
                            part_details[list(part_details.keys())[1]]
                        ):
                            new_value = length_in_stock - int(
                                part_details[list(part_details.keys())[1]]
                            )
                            conn = engine.connect()
                            stmt = (
                                update(Input_Warehouse)
                                .where(
                                    Input_Warehouse.name
                                    == part_details[list(part_details.keys())[0]]
                                )
                                .values(quantity=new_value)
                            )
                            conn.execute(stmt)
                            db.session.add(new_product)
                            db.session.commit()
                            return redirect("/order")
                        else:
                            return "Nema dovoljne količine materijala na skladištu!"

        for assembly_name in j_assembly_data:
            if product_name == assembly_name:
                print(assembly_name)
                if type(j_assembly_data[assembly_name]) == type([]):
                    for assembly_details in j_assembly_data[assembly_name]:
                        print(assembly_details)
                        print(assembly_details[list(assembly_details.keys())[0]])

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


@app.route("/installation")
def installation():
    return render_template("installation.html")


@app.route("/finishedproduct")
def finished_product():
    return render_template("finishedproduct.html")


@app.route("/statistic")
def statistic():
    return render_template("statistic.html")


if __name__ == "__main__":
    HOST = os.environ.get("SERVER_HOST", "localhost")
    putDataInTablePart()
    putDataInTableAssembly()
    putDataInTableMachine()
    putDataInTableWorker()

    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))

    except ValueError:
        PORT = 5555

    app.run(HOST, PORT)
