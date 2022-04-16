from flask import Flask , jsonify , request , render_template
import requests
import time
from pymongo import MongoClient
import sys

app = Flask(__name__)

client = MongoClient("mongodb+srv://nishankbhola:MLDsIAwoBhGkkIPL@cluster0.yfhci.mongodb.net/Crypto_db?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.get_database("Crypto_db")
records = db.Bitcoin_price

# getting data from mongo DB Atlas and pushing it to frontend 
@app.route("/")
def index():
    usdrate = list(records.find({} , {"bpi":{"USD":{"rate_float":1}}}))
    usdrate = usdrate[::-1]
    usdRate = usdrate[0]['bpi']['USD']['rate_float']


    GBPrate = list(records.find({} , {"bpi":{"GBP":{"rate_float":1}}}))
    GBPrate = GBPrate[::-1]
    GBPrate = GBPrate[0]['bpi']['GBP']['rate_float']

    eurorate = list(records.find({} , {"bpi":{"EUR":{"rate_float":1}}}))
    eurorate = eurorate[::-1]
    eurorate = eurorate[0]['bpi']['EUR']['rate_float']
    #print(usdRate)
    data = {'usd':usdRate , 'pounds':GBPrate , 'euro':eurorate}
    return render_template('index.html', data=data)   


#Fetching data from coindesk api and storing it to MongoDB cluster
@app.route("/getData")
def getData():
    client = MongoClient("mongodb+srv://nishankbhola:MLDsIAwoBhGkkIPL@cluster0.yfhci.mongodb.net/Crypto_db?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client.get_database("Crypto_db")
    records = db.Bitcoin_price
    while True:
        r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        if r.status_code == 200:
            data = r.json()
            print(data)
            time.sleep(60)
        else:
            print("can't")
            exit()


# getting data from mongo DB Atlas and pushing it to frontend (USD Line chart)
@app.route("/linechart")
def linechart():
    data = {}
    for x in records.find({},{ "_id": 0, "time":{"updated":1}, "bpi":{"USD":{"rate_float":1}}}):
        #print(x['bpi']['USD']['rate_float'])
        data[x['time']['updated']] = x['bpi']['USD']['rate_float']    
    return render_template('linechart.html' , data=data)   

# getting data from mongo DB Atlas and pushing it to frontend (GBP Line chart)
@app.route("/linechartgbp")
def linechartgbp():
    data = {}
    for x in records.find({},{ "_id": 0, "time":{"updated":1}, "bpi":{"GBP":{"rate_float":1}}}):
        #print(x['bpi']['USD']['rate_float'])
        data[x['time']['updated']] = x['bpi']['GBP']['rate_float']    
    return render_template('linechartgbp.html' , data=data)   

# getting data from mongo DB Atlas and pushing it to frontend (EUR Line chart)
@app.route("/linecharteur")
def linecharteur():
    data = {}
    for x in records.find({},{ "_id": 0, "time":{"updated":1}, "bpi":{"EUR":{"rate_float":1}}}):
        #print(x['bpi']['USD']['rate_float'])
        data[x['time']['updated']] = x['bpi']['EUR']['rate_float']    
    return render_template('linecharteur.html' , data=data)  

if __name__ == "__main__":
    app.run()