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
ID_1 = -1
ID_2 = -1


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


class Warehouse(db.Model):
    __tablename__ = "warehouse"
    auto_id = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String(200))
    part_quantity = db.Column(db.Integer)

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
        Assembly(assembly_name="Sklop 1",
                 assembly_peaces="5", assembly_price="1000"),
        Assembly(assembly_name="Sklop 2",
                 assembly_peaces="7", assembly_price="1500"),
        Assembly(assembly_name="Sklop 3",
                 assembly_peaces="4", assembly_price="800"),
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
    manufacturing_time = db.Column(db.DateTime, default=datetime.now)
    manufacturing_worker = db.Column(db.Integer)

    first_time = True

    def __repr__(self):
        return "<Name %r>" % self.id

    def getLastManufacturingID(self):
        manufacturing_table = pd.read_sql_table(
            table_name="manufacturing", con=engine)
        column_ID_1 = manufacturing_table["part_id"].tolist()
        if len(column_ID_1):
            return column_ID_1[-1]

        return 39999


class Installation(db.Model):
    __tablename__ = "installation"
    auto_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    installation_id = db.Column(db.Integer)
    part_id = db.Column(db.Integer)
    installation_status = db.Column(db.String(200))
    installation_time = db.Column(db.DateTime, default=datetime.now)
    installation_worker = db.Column(db.Integer)

    first_time = True

    def __repr__(self):
        return "<Name %r>" % self.id

    def getLastInstallationID(self):
        installation_table = pd.read_sql_table(
            table_name="installation", con=engine)
        column_ID_2 = installation_table["installation_id"].tolist()
        if len(column_ID_2):
            return column_ID_2[-1]

        return 79999


class Finished_product(db.Model):
    __tablename__ = "finished_product"
    auto_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    order_status = db.Column(db.Integer)
    buyer_name = db.Column(db.String(500), nullable=False)
    buyer_contact = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.String(500))
    date_finished = db.Column(db.String(500))
    price = db.Column(db.Integer)

    def __repr__(self):
        return "<Name %r>" % self.id


@app.route("/")
def index():
    return render_template("index.html")


def getResourceFromWarehouse(part_detail, table, column):

    input_table = pd.read_sql_table(table_name=table, con=engine)
    raw_mat_name = input_table[column].tolist()

    if table == 'input_warehouse':
        if part_detail in raw_mat_name:
            row = input_table.loc[input_table.name == part_detail]
            return int(row.quantity)

    elif table == 'warehouse':
        if part_detail in raw_mat_name:
            row = input_table.loc[input_table.part_name == part_detail]
            return int(row.part_quantity)

    else:

        return -1


@app.route("/customer")
def customer():
    return render_template("customer.html")


@app.route("/customer_order")
def customerOrder():
    return render_template("customer_order.html")


@app.route("/order_status")
def orderStatus():
    return render_template("order_status.html")


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

                if type(j_part_data[part_name]) == type([]):

                    for part_details in j_part_data[part_name]:

                        part_raw_mat_name = part_details[list(
                            part_details.keys())[0]]
                        part_raw_mat_length = part_details[list(
                            part_details.keys())[1]]
                        length_in_stock = getResourceFromWarehouse(
                            part_raw_mat_name, "input_warehouse", "name")

                        if length_in_stock >= int(part_raw_mat_length):

                            new_value = length_in_stock - \
                                int(part_raw_mat_length)
                            conn = engine.connect()
                            stmt = (
                                update(Input_Warehouse)
                                .where(Input_Warehouse.name == part_raw_mat_name)
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

                if type(j_assembly_data[assembly_name]) == type([]):

                    for assembly_details in j_assembly_data[assembly_name]:

                        for assembly_detail in assembly_details:
                            needed_part_name = assembly_detail
                            needed_part_quantity = assembly_details[assembly_detail]

                            quantity_in_stock = getResourceFromWarehouse(
                                needed_part_name, "warehouse", "part_name")

                            if quantity_in_stock >= int(needed_part_quantity):
                                new_part_value = quantity_in_stock - \
                                    int(needed_part_quantity)
                                conn = engine.connect()
                                stmt = (update(Warehouse).where(
                                    Warehouse.part_name == needed_part_name).values(part_quantity=new_part_value))
                                conn.execute(stmt)
                                db.session.add(new_product)
                                db.session.commit()
                            else:
                                return "Nema dovoljne količine osnovnih elemenata na skladištu!"

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect("/order")
        except all:
            return "Pojavio se problem! Pokušajte ponovno."

    else:
        product = Order.query.order_by(Order.date_created)
        return render_template("order.html", product=product)


@app.route("/first_btn", methods=["POST", "GET"])
def first_button():
    if request.method == "POST":
        raw_mat_name = request.form["sirovac"]
        quantity_value = request.form["kolicina"]

        new_raw_mat = Input_Warehouse(
            name=raw_mat_name, quantity=quantity_value)

        user_table = pd.read_sql_table(
            table_name='input_warehouse', con=engine)

        exists = False

        for _, row in user_table.iterrows():
            if row["name"] == raw_mat_name:
                # print(row["quantity"])
                table_val = row["quantity"]
                updated_value = table_val + int(quantity_value)
                new_raw_mat = Input_Warehouse(
                    name=raw_mat_name, quantity=updated_value)
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

    return warehouse_page()


@app.route("/second_btn", methods=["POST", "GET"])
def second_button():
    if request.method == "POST":
        raw_mat_name = request.form["new_part"]
        quantity_value = request.form["kolicina_1"]

        new_raw_mat = Warehouse(part_name=raw_mat_name,
                                part_quantity=quantity_value)

        user_table = pd.read_sql_table(table_name='warehouse', con=engine)

        exists = False

        for _, row in user_table.iterrows():
            if row["part_name"] == raw_mat_name:
                table_val = row["part_quantity"]
                updated_value = table_val + int(quantity_value)
                new_raw_mat = Warehouse(
                    part_name=raw_mat_name, part_quantity=updated_value)
                exists = True

        try:
            if exists:
                conn = engine.connect()
                stmt = (
                    update(Warehouse)
                    .where(Warehouse.part_name == raw_mat_name)
                    .values(part_quantity=updated_value)
                )
                conn.execute(stmt)
            else:
                db.session.add(new_raw_mat)
            db.session.commit()
            return redirect("/warehouse")
        except all:
            return "Pojavio se problem! Pokušajte ponovno."

    return warehouse_page()


@app.route("/warehouse")
def warehouse_page():
    raw_mat = Input_Warehouse.query.order_by(Input_Warehouse.id)
    part_available = Warehouse.query.order_by(Warehouse.part_name)
    return render_template("warehouse.html", sirovac=raw_mat, availability=part_available)


@app.route("/manufacturing")
def manufacturing():
    product = Manufacturing.query.order_by(Manufacturing.part_id)
    return render_template("manufacturing.html", product=product)


@app.route("/new_manufacturing_form", methods=["POST", "GET"])
def new_manufacturing_form():
    if request.method == "POST":
        global ID_1
        if Manufacturing.first_time:
            ID_1 = Manufacturing().getLastManufacturingID()
            Manufacturing.first_time = False

        new_manufacturing_order_id = request.form["new_manufacturing_order_id"]
        new_manufacturing_machine_id = request.form["new_manufacturing_machine_id"]
        manufacturing_worker_id = request.form["new_manufacturing_worker_id"]
        # new_manufacturing_part_id = request.form["new_manufacturing_part_id"]

        table_val_part_name = ""
        table_val_buyer_name = ""
        table_val_buyer_contact = ""
        table_val_order_date = ""
        table_val_price = 0
        table_val_fin_date = "Ne"

        order_table = pd.read_sql_table(table_name='order', con=engine)

        for _, row in order_table.iterrows():
            if row["order_id"] == int(new_manufacturing_order_id):
                table_val_part_name = row["name"]
                table_val_buyer_name = row["buyer_name"]
                table_val_buyer_contact = row["buyer_contact"]
                table_val_order_date = row["date_created"]

        part_table = pd.read_sql_table(table_name='part', con=engine)

        for _, rows in part_table.iterrows():
            if rows["part_name"] == table_val_part_name:
                table_val_price = rows["part_price"]

        almost_fin_product = Finished_product(order_id=new_manufacturing_order_id, order_status=0, buyer_name=table_val_buyer_name,
                                              buyer_contact=table_val_buyer_contact, date_created=str(table_val_order_date), date_finished=table_val_fin_date, price=table_val_price)

        ID_1 = ID_1+1
        new_manufacturing_element = Manufacturing(order_id=new_manufacturing_order_id, part_id=ID_1,
                                                  machine_id=new_manufacturing_machine_id, manufacturing_status=0, manufacturing_worker=manufacturing_worker_id)

        try:
            db.session.add(new_manufacturing_element)
            db.session.add(almost_fin_product)
            Order.query.filter(
                Order.order_id == int(new_manufacturing_order_id)).delete()
            db.session.commit()
            return redirect("/manufacturing")
        except all:
            return "Pojavio se problem! Pokušajte ponovno."

    new_operating_worker_id = Worker.query.order_by(Worker.worker_id)
    starting_machine_for_manufacturing = Machine.query.order_by(
        Machine.machine_id)
    new_part_for_manufacture = Order.query.filter(
        Order.name.startswith('Osnovni element')).all()
    return render_template("new_manufacturing_form.html", availability=new_part_for_manufacture, machine=starting_machine_for_manufacturing, worker=new_operating_worker_id)


@app.route("/existing_manufacturing_form", methods=["POST", "GET"])
def exisiting_manufacturing_form():
    if request.method == "POST":
        existing_manufacturing_order_id = request.form["existing_manufacturing_order_id"]
        next_manufacturing_machine_id = request.form["next_manufacturing_machine_id"]
        next_manufacturing_worker_id = request.form["next_manufacturing_worker_id"]

        manufacturing_table = pd.read_sql_table(
            table_name='manufacturing', con=engine)

        table_val_auto_id = 0
        table_val_part_id = 0

        for _, row in manufacturing_table.iterrows():
            if row["order_id"] == int(existing_manufacturing_order_id):
                table_val_auto_id = row["auto_id"]
                table_val_part_id = row["part_id"]

        existing_manufacturing_part = Manufacturing(order_id=existing_manufacturing_order_id, part_id=table_val_part_id,
                                                    machine_id=next_manufacturing_machine_id, manufacturing_status=0, manufacturing_worker=next_manufacturing_worker_id)

        conn = engine.connect()
        stmt = (update(Manufacturing).where(Manufacturing.auto_id ==
                table_val_auto_id).values(manufacturing_status=1))
        conn.execute(stmt)

        try:
            db.session.add(existing_manufacturing_part)
            db.session.commit()
            return redirect("/manufacturing")
        except all:
            return "Pojavio se problem! Pokušajte ponovno."

    existing_part_for_manufacture = Manufacturing.query.filter(
        Manufacturing.manufacturing_status.startswith('0')).all()
    next_machine_for_manufacturing = Machine.query.order_by(Machine.machine_id)
    next_operating_worker_id = Worker.query.order_by(Worker.worker_id)
    return render_template("existing_manufacturing_form.html", part=existing_part_for_manufacture, machine=next_machine_for_manufacturing, worker=next_operating_worker_id)


@app.route("/finishing_manufacturing_form", methods=["POST", "GET"])
def fin_man_form():
    if request.method == "POST":
        fin_man_order_id = request.form["finishing_manufacturing_order_id"]
        fin_man_time = datetime.now()
        str_fin_man_time = fin_man_time.strftime("%Y-%m-%d %H:%M:%S.%f")

        manufacturing_table = pd.read_sql_table(
            table_name='manufacturing', con=engine)

        for _, row in manufacturing_table.iterrows():
            if row["order_id"] == int(fin_man_order_id):
                table_val_auto_id = row["auto_id"]

        conn = engine.connect()
        stmt = (update(Manufacturing).where(Manufacturing.auto_id ==
                table_val_auto_id).values(manufacturing_status=1))
        conn.execute(stmt)

        fin_product_table = pd.read_sql_table(
            table_name='finished_product', con=engine)

        for _, rows in fin_product_table.iterrows():
            if rows["order_id"] == int(fin_man_order_id):
                table_value_auto_id = rows["auto_id"]

        conn = engine.connect()
        stmt_1 = (update(Finished_product).where(Finished_product.auto_id ==
                  table_value_auto_id).values(order_status=1, date_finished=str_fin_man_time))
        conn.execute(stmt_1)

        return redirect("/manufacturing")

    finishing_parts = Manufacturing.query.filter(
        Manufacturing.manufacturing_status.startswith('0')).all()
    return render_template("finishing_manufacturing_form.html", part=finishing_parts)


@app.route("/installation")
def installation():
    product = Installation.query.order_by(Installation.installation_id)
    return render_template("installation.html", product=product)


@app.route("/new_installation_form", methods=["POST", "GET"])
def new_installation_form():
    if request.method == "POST":
        global ID_2
        if Installation.first_time:
            ID_2 = Installation().getLastInstallationID()
            Installation.first_time = False

        new_inst_order_id = request.form["new_installation_order_id"]
        new_inst_part_id = request.form["new_installation_part_id"]
        new_inst_worker_id = request.form["new_installation_worker_id"]

        table_val_assembly_name = ""
        table_val_buyer_name = ""
        table_val_buyer_contact = ""
        table_val_order_date = ""
        table_val_price = 0
        table_val_fin_date = "Ne"

        order_table = pd.read_sql_table(table_name='order', con=engine)

        for _, row in order_table.iterrows():
            if row["order_id"] == int(new_inst_order_id):
                table_val_assembly_name = row["name"]
                table_val_buyer_name = row["buyer_name"]
                table_val_buyer_contact = row["buyer_contact"]
                table_val_order_date = row["date_created"]

        assembly_table = pd.read_sql_table(table_name='assembly', con=engine)

        for _, rows in assembly_table.iterrows():
            if rows["assembly_name"] == table_val_assembly_name:
                table_val_price = rows["assembly_price"]

        almost_fin_product = Finished_product(order_id=new_inst_order_id, order_status=0, buyer_name=table_val_buyer_name,
                                              buyer_contact=table_val_buyer_contact, date_created=str(table_val_order_date), date_finished=table_val_fin_date, price=table_val_price)

        ID_2 = ID_2+1
        new_inst_element = Installation(order_id=new_inst_order_id, installation_id=ID_2,
                                        part_id=new_inst_part_id, installation_status=0, installation_worker=new_inst_worker_id)

        try:
            db.session.add(new_inst_element)
            db.session.add(almost_fin_product)
            Order.query.filter(
                Order.order_id == int(new_inst_order_id)).delete()
            db.session.commit()
            return redirect("/installation")
        except all:
            return "Pojavio se problem! Pokušajte ponovno."

    new_part_for_install = Order.query.filter(
        Order.name.startswith('Sklop')).all()
    new_assembly_worker_id = Worker.query.order_by(Worker.worker_id)
    return render_template("/new_installation_form.html", availability=new_part_for_install, worker=new_assembly_worker_id)


@app.route("/existing_installation_form", methods=["POST", "GET"])
def existing_installation_form():
    if request.method == "POST":
        existing_inst_order_id = request.form["existing_installation_order_id"]
        next_inst_part_id = request.form["next_installation_part_id"]
        next_inst_worker_id = request.form["next_installation_worker_id"]

        installation_table = pd.read_sql_table(
            table_name='installation', con=engine)

        table_val_auto_id = 0
        table_val_installation_id = 0

        for _, row in installation_table.iterrows():
            if row["order_id"] == int(existing_inst_order_id):
                table_val_auto_id = row["auto_id"]
                table_val_installation_id = row["installation_id"]

        existing_inst_part = Installation(order_id=existing_inst_order_id, installation_id=table_val_installation_id,
                                          part_id=next_inst_part_id, installation_status=0, installation_worker=next_inst_worker_id)

        conn = engine.connect()
        stmt = (update(Installation).where(Installation.auto_id ==
                table_val_auto_id).values(installation_status=1))
        conn.execute(stmt)

        try:
            db.session.add(existing_inst_part)
            db.session.commit()
            return redirect("/installation")
        except all:
            return "Pojavio se problem! Pokušajte ponovno."

    existing_assembly_for_installation = Installation.query.filter(
        Installation.installation_status.startswith('0')).all()
    next_assembly_worker_id = Worker.query.order_by(Worker.worker_id)
    return render_template("/existing_installation_form.html", assembly=existing_assembly_for_installation, worker=next_assembly_worker_id)


@app.route("/finished_installation_form", methods=["POST", "GET"])
def finished_installation_form():
    if request.method == "POST":
        fin_inst_order_id = request.form["finished_installation_order_id"]
        fin_inst_time = datetime.now()
        str_fin_inst_time = fin_inst_time.strftime("%Y-%m-%d %H:%M:%S.%f")

        installation_table = pd.read_sql_table(
            table_name='installation', con=engine)

        for _, row in installation_table.iterrows():
            if row["order_id"] == int(fin_inst_order_id):
                table_val_auto_id = row["auto_id"]

        conn = engine.connect()
        stmt = (update(Installation).where(Installation.auto_id ==
                table_val_auto_id).values(installation_status=1))
        conn.execute(stmt)

        fin_product_table = pd.read_sql_table(
            table_name='finished_product', con=engine)

        for _, rows in fin_product_table.iterrows():
            if rows["order_id"] == int(fin_inst_order_id):
                table_value_auto_id = rows["auto_id"]

        conn = engine.connect()
        stmt_1 = (update(Finished_product).where(Finished_product.auto_id ==
                  table_value_auto_id).values(order_status=1, date_finished=str_fin_inst_time))
        conn.execute(stmt_1)

        return redirect("/installation")

    finishing_parts = Installation.query.filter(
        Installation.installation_status.startswith('0')).all()
    return render_template("/finished_installation_form.html", installation=finishing_parts)


@app.route("/finishedproduct")
def finished_product():
    finished_products = Finished_product.query.order_by(
        Finished_product.order_id)
    return render_template("finishedproduct.html", product=finished_products)


@app.route("/statistic")
def statistic():
    return render_template("statistic.html")


if __name__ == "__main__":
    HOST = os.environ.get("SERVER_HOST", "localhost")
    # putDataInTablePart()
    # putDataInTableAssembly()
    # putDataInTableMachine()
    # putDataInTableWorker()

    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))

    except ValueError:
        PORT = 5555

    app.run(HOST, PORT)
