from flask import Flask, render_template
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


# @app.route("/order", methods=["POST", "GET"])
@app.route("/order")
def order():
    # if request.method == "POST":
    #     naruci_proizvod = request.form["proizvod"]
    #     novi_proizvod = Order(content=naruci_proizvod)
    #     try:
    #         db.session.add(novi_proizvod)
    #         db.session.commit()
    #         return redirect("/order")
    #     except:
    #         return "Greška u naručivanju proizvoda. Molim pokušajte ponovno."
    # else:
    #     order = Order.query.order_by(Order.date_created)
    return render_template("order.html")


@app.route("/proizvodnja")
def proizvodnja():
    return render_template("proizvodnja.html")


@app.route("/gotoviproizvodi")
def gotoviproizvodi():
    return render_template("gotoviproizvodi.html")


if __name__ == "__main__":
    app.run(debug=True)
