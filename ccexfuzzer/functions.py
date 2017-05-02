# import json
import requests
# import RouteFinder
from json.decoder import JSONDecodeError
from http.client import RemoteDisconnected
# from io import UnsupportedOperation,BufferedRandom
import datetime
from pathos.multiprocessing import ProcessingPool as Pool #  THE REAL MULTIPROCCESSING GOODNESS :D  - Thankyou Jesus!
# import multiprocessing # IS RUBBISH!

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
        list = map(lambda x: x + "\n", list)
        to_write.writelines(list)
    return True

# generate urls to parse

# TODO being tricky.. sort generate_urls
def generate_urls(coinsymbolset:set):
    urls = []
    coinsymbollist = list(coinsymbolset)

    def make_url(x):  # parralalell proccessing equivelient of - for base in coinsymbollist
        # print("proccess coinsybollist:",coinsymbollist)
        for pair in coinsymbollist:
            return str("https://c-cex.com/t/" + str(x) + "-" + str(pair) + ".json")

    with Pool(None) as p:
        urls = p.map(make_url,coinsymbollist)
        print("pool result",urls)
    return urls

def apply_blacklist(list_to_filter:list,blacklist_filename:str='blacklist.list'):
    blacklist = read_list_file(blacklist_filename)
    return list(filter(lambda x: x in blacklist,list_to_filter))

# fetch data,parse urls, sanitize data.

def get_coin_buy_prices(api_urls:list):
    # i = 0
    end = str(int(len(api_urls)))
    exchangerates = {}
    unfinished = [] # urls that werent attempted due to a remote server disconnect
    blacklist = []
    def add_coin_price(url):
        i = 0
        base = url[str(url).rfind('/'):str(url).rfind('-')]  # rfinds start from 0 quirk to the rescue!
        try:
            i += 1
            print(datetime.datetime.now(), 'Progress ', i, '/' , end , 'url is', url)
            exchangerate = requests.get(url).json()

            exchangerate = exchangerate['ticker']['buy']
        except JSONDecodeError:
            exchangerate = 0.0
            blacklist.append(url)
        except RemoteDisconnected:
            exchangerate = 0.0
            unfinished.append(url)
        finally:
            exchangerates[str(base)] = [{str(url): float(exchangerate)}]
    with Pool() as p:
        p.map(add_coin_price,api_urls)
    return {'exchangerates':exchangerates,'unfinished':unfinished,'blacklist':blacklist}

def apply_coin_equivelent_exchanges(coinsymbolset:set,exchangerates:dict): # ETH-ETH = 1 etc.
    for base in coinsymbolset:
        exchangerates[str(base)] = list({str(base):1.0}) + exchangerates[str(base)]
    return exchangerates