from flask import Flask, render_template, request, jsonify, make_response
from hash_map_sc import HashMap

app = Flask(__name__)

map = HashMap(capacity=5)

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("app.html")


@app.route('/process', methods=['POST', 'GET'])
def process():
    req = request.get_json()
    print(map)
    hash = hashOperation(req["op"], req["key"], req["value"])
    print(map)
    entry = {
        "hash": hash,
        "key": req["key"],
        "value": req["value"],
        "op": req["op"]
    }
    res = make_response(jsonify(entry), 200)
    return res


def hashOperation(op, key, value):
    if op == "insert":
        return map.put(key, value)
    elif op == "delete":
        return map.remove(key)
    elif op == "reset":
        return map.clear()



if __name__ == "__main__":
    app.run(debug=True)