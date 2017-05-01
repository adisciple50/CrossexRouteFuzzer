# import json
import requests
# import RouteFinder
from json.decoder import JSONDecodeError
from http.client import RemoteDisconnected
# from io import UnsupportedOperation,BufferedRandom
import datetime
from multiprocessing import Pool

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

def generate_urls(coinsymbolset:set):
    urls = []
    def make_url(coinsymbolset:set):
        for pair in coinsymbolset:
            urls.append(str("https://c-cex.com/t/" + str(base) + "-" + str(pair) + ".json"))
    with Pool() as p:
        p.map(make_url,list(coinsymbolset))
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