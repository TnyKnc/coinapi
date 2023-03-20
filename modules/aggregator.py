import requests
import json
import random


def get_tokens():
    mexcc = json.load(open("pairs/mexc.json", "r", encoding="utf-8"))
    added = []
    coins = []

    r = requests.get("https://data.gateapi.io/api2/1/marketlist").json()['data']

    for i in r:
        if i['symbol'] not in added and i['pair'][-4:] == "usdt":
            sy = ""
            if i['trend'] == "up":
                sy = "+"

            if i['symbol'] in ["BTC", "ETH", "BNB", "SOL", "AVAX"]:
                priceo = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={i['symbol']}USDT").json()[
                    'price']
                added.append(i['symbol'])
                coins.append((float(i['vol_b'].replace(",", "")) * float(i['rate'].replace(",", "")), {
                    "name": i['name'],
                    "symbol": i['symbol'],
                    "price": str('{:,.2f}'.format(float(f"{float(priceo):.2f}"))),
                    "volume": str('{:,.2f}'.format(int(float(i["vol_b"].replace(",", ""))))),
                    "24hchange": sy + i['rate_percent'],

                }))
            else:

                added.append(i['symbol'])
                coins.append((float(i['vol_b'].replace(",", "")) * float(i['rate'].replace(",", "")), {
                    "name": i['name'],
                    "symbol": i['symbol'],
                    "price": str('{:,.2f}'.format(
                        int(float(f'{float(i["rate"].replace(",", "")) * random.uniform(0.9997, 1.0003):.2f}')))),
                    "volume": str('{:,.2f}'.format(int(float(i["vol_b"].replace(",", ""))))),
                    "24hchange": sy + i['rate_percent'],

                }))

    r = requests.get("https://www.mexc.com/open/api/v2/market/ticker").json()

    for i in r['data']:
        if i['symbol'].replace("_USDT", "") not in added and i['symbol'][-4:] == "USDT":
            added.append(i['symbol'].replace("_USDT", ""))
            try:

                coins.append((float(i['vol_b'].replace(",", "")) * float(i['rate'].replace(",", "")), {
                    "name": mexcc[i['symbol'].replace("_USDT", "")],
                    "symbol": i['symbol'].replace("_USDT", ""),
                    "price": float(i['last'].replace(",", "")) * random.uniform(0.9997, 1.0003),
                    "volume": float(i['volume'].replace(",", "")),
                    "24hchange": i['change_rate']
                }))
            except KeyError:
                pass

    return coins


def sort_them(mylist: list) -> list:
    for i in range(len(mylist)):
        i = 0
        while i < len(mylist) - 1:
            if mylist[i][0] > mylist[i + 1][0]:
                x = mylist[i]
                mylist[i] = mylist[i + 1]
                mylist[i + 1] = x
            i += 1

    mylist.reverse()
    return mylist


def checkerr():
    coins = [i[1] for i in sort_them(get_tokens())]

    json.dump(coins, open("pairs/data.json", "w", encoding="utf-8"))


""" checkerr() """
