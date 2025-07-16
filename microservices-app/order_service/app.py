import requests
from flask import Flask, jsonify

app = Flask(_name_)

USER_SERVICE_URL = "http://user_service:5001/users/"

@app.route("/orders/<user_id>")
def get_orders(user_id):
    user_response = requests.get(USER_SERVICE_URL + user_id)
    user_data = user_response.json()
    return jsonify({"user": user_data, "orders": [{"order_id": 101, "item": "Laptop"}]})

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5002)
