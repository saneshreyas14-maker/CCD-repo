from flask import Flask, jsonify, request
from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

app = Flask(__name__)

menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()


@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify({"items": menu.get_items()})


@app.route('/report', methods=['GET'])
def get_report():
    return jsonify({
        "resources": coffee_maker.report(),
        "profit": money_machine.report()
    })


@app.route('/order', methods=['POST'])
def order():
    data = request.get_json(force=True)
    if not data or 'drink' not in data:
        return jsonify({"error": "missing 'drink' in body"}), 400

    drink_name = data['drink']
    paid = float(data.get('paid', 0.0))

    drink = menu.find_drink(drink_name)
    if not drink:
        return jsonify({"error": "drink not found"}), 404

    if not coffee_maker.is_resource_sufficient(drink):
        return jsonify({"error": "resources not sufficient"}), 409

    if not money_machine.make_payment(drink.cost, paid):
        return jsonify({
            "error": "insufficient payment",
            "required": drink.cost
        }), 402

    coffee_maker.make_coffee(drink)
    return jsonify({
        "status": "success",
        "drink": drink.name,
        "cost": drink.cost
    })


if __name__ == '__main__':
    # for local development; Jenkins will also run `python app.py`
    app.run(host='0.0.0.0', port=5000)
