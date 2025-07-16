from flask import Flask, jsonify

app = Flask(_name_)

@app.route("/users/<user_id>")
def get_user(user_id):
    users = {"1": {"id": 1, "name": "Alice"}, "2": {"id": 2, "name": "Bob"}}
    return jsonify(users.get(user_id, {"error": "User not found"}))

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5001)
