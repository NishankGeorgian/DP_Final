import requests
import time
from pymongo import MongoClient

client = MongoClient("mongodb+srv://nishankbhola:MLDsIAwoBhGkkIPL@cluster0.yfhci.mongodb.net/Crypto_db?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.get_database("Crypto_db")
records = db.Bitcoin_price
while True:
    r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    if r.status_code == 200:
        data = r.json()
        print(data)
        time.sleep(100)
        break
    else:
        print("can't")
        exit()