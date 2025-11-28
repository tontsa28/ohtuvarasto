from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto

app = Flask(__name__)


class WarehouseStore:
    def __init__(self):
        self.warehouses = {}
        self.next_id = 1

    def add(self, name, tilavuus, alku_saldo):
        self.warehouses[self.next_id] = {
            "name": name,
            "varasto": Varasto(tilavuus, alku_saldo)
        }
        self.next_id += 1

    def get(self, warehouse_id):
        return self.warehouses.get(warehouse_id)

    def remove(self, warehouse_id):
        if warehouse_id in self.warehouses:
            del self.warehouses[warehouse_id]

    def all(self):
        return self.warehouses


store = WarehouseStore()


@app.route("/")
def index():
    return render_template("index.html", warehouses=store.all())


@app.route("/create", methods=["POST"])
def create():
    name = request.form.get("name", "New Warehouse")
    try:
        tilavuus = float(request.form.get("tilavuus", 0))
        alku_saldo = float(request.form.get("alku_saldo", 0))
        store.add(name, tilavuus, alku_saldo)
    except ValueError:
        pass
    return redirect(url_for("index"))


def handle_edit_action(varasto, action, amount):
    if action == "add":
        varasto.lisaa_varastoon(amount)
    elif action == "take":
        varasto.ota_varastosta(amount)


def process_edit(data):
    name = request.form.get("name")
    if name:
        data["name"] = name
    try:
        amount = float(request.form.get("amount", 0))
        handle_edit_action(data["varasto"], request.form.get("action"), amount)
    except ValueError:
        pass


@app.route("/edit/<int:warehouse_id>", methods=["POST"])
def edit(warehouse_id):
    data = store.get(warehouse_id)
    if data:
        process_edit(data)
    return redirect(url_for("index"))


@app.route("/delete/<int:warehouse_id>", methods=["POST"])
def delete(warehouse_id):
    store.remove(warehouse_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
