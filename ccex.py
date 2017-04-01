import json
import requests
import RouteFinder
from json.decoder import JSONDecodeError
from http.client import RemoteDisconnected
from io import UnsupportedOperation,BufferedRandom
import datetime

# begin print available markets
# markets = requests.get("https://c-cex.com/t/api_pub.html?a=getmarkets").json()
# end markets


# get coin names

def get_coinnames(api_url:str='https://c-cex.com/t/coinnames.json'):
    return set(dict(requests.get(api_url).json()).keys())

# list file IO

def read_list_file(filepath):
    with open(filepath,'r') as to_read:
        f = to_read.read().splitlines()
    return list(f)

def write_list_to_file(list:list,filepath):
    with open(filepath, 'a+') as to_write:
        to_write.writelines(list)
    return True

# generate urls to parse

def generate_urls(coinsymbolset:set):
    urls = []
    for base in coinsymbolset:
        for pair in coinsymbolset:
            urls.append(url = str("https://c-cex.com/t/" + str(base) + "-" + str(pair) + ".json"))
    return urls

def apply_blacklist(list_to_filter:list):
    blacklist = read_list_file('blacklist.list')
    return  list(filter(lambda x: x in blacklist,list_to_filter))

def apply_coin_equivelent_exchanges(coinsymbolset:set,exchangerates:dict): # ETH-ETH = 1 etc.
    for base in coinsymbolset:
        exchangerates[str(base)] = list({str(base):1.0}) + exchangerates[str(base)]
    return exchangerates

# fetch data,parse urls, sanitize data.

def get_coin_buy_prices(api_urls:list):
    i = 0
    end = str(int(len(api_urls)))
    exchangerates = {}
    unfinished = [] # urls that werent attempted due to a remote server disconnect
    blacklist = []
    for url in api_urls:
        try:
            i += 1
            print(datetime.datetime.now(), 'Progress ', i, '/' , end , 'url is', url)
            exchangerate = requests.get(url).json()
            base = url[str(url).rfind('/'):str(url).rfind('-')] # rfinds start from 0 quirk to the rescue!
            exchangerate = exchangerate['ticker']['buy']
        except JSONDecodeError:
            exchangerate = 0.0
            blacklist.append(url)
        except RemoteDisconnected:
            exchangerate = 0.0
            unfinished.append(url)
        finally:
            exchangerates[str(base)] = [{str(url): float(exchangerate)}]
    return {'exchangerates':exchangerates,'unfinished':unfinished,'blacklist':blacklist}

def apply_coin_equivelent_exchanges(coinsymbolset:set,exchangerates:dict): # ETH-ETH = 1 etc.
    for base in coinsymbolset:
        exchangerates[str(base)] = list({str(base):1.0}) + exchangerates[str(base)]
    return exchangerates


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