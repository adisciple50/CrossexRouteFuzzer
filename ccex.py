import json
import requests
import RouteFinder
from json.decoder import JSONDecodeError
from http.client import RemoteDisconnected
from io import UnsupportedOperation
import datetime

# print available markets
markets = requests.get("https://c-cex.com/t/api_pub.html?a=getmarkets").json()

# print(markets)

# end markets

# establish base coins
'''
basecoins = []

for instrement in markets['result']:
    # print(instrement)
    basecoins.append(instrement['BaseCurrency'])

basecoins = set(basecoins)


print("Detected Base Coins: ",basecoins)
'''

# begin update ccex-example.json

exchangerates = {}

# get coin names
coinnames = requests.get('https://c-cex.com/t/coinnames.json').json()
coinnames = set(dict(coinnames).keys())

# begin exchange rate collation
i = 1
with open('blacklist.list','r+') as blacklist:
    try:
        blacklisted = blacklist.read().splitlines()
    except UnsupportedOperation as UO:
        blacklisted = []
    for base in coinnames:
        for pair in coinnames:
            try:
                if base == pair:
                    exchangerate = 1.0
                else:
                    url = str("https://c-cex.com/t/" + str(base) + "-" + str(pair) + ".json")
                    if url in blacklist:
                        continue
                    print(datetime.datetime.now(),i,'url is', url)
                    i+=1
                    exchangerate = requests.get(url).json()
                    exchangerate = exchangerate['ticker']['buy']
            except JSONDecodeError as ke:
                exchangerate = 0.0
                blacklist.write('\n'.join(url))
            except RemoteDisconnected as  RD:
                exchangerates = 0.0
            exchangerates[str(base)] = [{str(pair):float(exchangerate)}]

# end exchange rate collation

# write current exchangerates current exchange rates to file, but continue to use values in memory.

ccexjson = open("ccex.json",'w')
ccexjson.write(json.dumps(exchangerates))
ccexjson.close()






# begin fuzz routes

routes = RouteFinder.powerset(coinnames)
# rates = dict(json.loads(open('ccex-example.json').read()))

print(RouteFinder.try_routes(("USD",),"USD",2.5,exchangerates))

# end fuzz routes