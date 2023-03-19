from flask import Flask, jsonify, request
import json


app = Flask(__name__)


@app.route("/getcoins")
def getcoins():
    coins = [[]]
    coins[0] = json.load(open("pairs/data.json", "r", encoding="utf-8"))[
        int(request.args.get("start", 0)):int(request.args.get("stop", 20000))
    ]
    total = [{"total": len(coins[0])}]
    coins.append((total))
    return coins

@app.route("/getcoin")
def getcoin():
    coins = json.load(open("pairs/data.json", "r", encoding="utf-8"))
    coinDetail = [coin for coin in coins if coin['symbol'] == request.args.get("symbol").upper()]
    return json.dumps(coinDetail)

@app.route("/getcoinlist")
def getcoinlist():
    coins = json.load(open("pairs/data.json", "r", encoding="utf-8"))
    _coins = request.args.get("symbols").split(',')
    coinDetail = []
    for _coin in _coins:
        coinDetail.append([coin for coin in coins if coin['symbol'] == _coin.upper()])
    return json.dumps(coinDetail)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
