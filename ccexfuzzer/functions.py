# import json
import requests
# import RouteFinder
from json.decoder import JSONDecodeError
from http.client import RemoteDisconnected
# from io import UnsupportedOperation,BufferedRandom
import datetime
from pathos.multiprocessing import ProcessingPool as Pool #  THE REAL MULTIPROCCESSING GOODNESS :D  - Thankyou Jesus!
# import multiprocessing # IS RUBBISH!
from collections import ChainMap # requires python 3.3
from itertools import chain
from requests.packages.urllib3.exceptions import ProtocolError,ConnectionError
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
    coinsymbollist = list(coinsymbolset)

    def make_url(x):  # parralalell proccessing equivelient of - for base in coinsymbollist
        # print("proccess coinsybollist:",coinsymbollist)
        proccess_urls = []
        for pair in coinsymbollist:
            proccess_urls.append(str("https://c-cex.com/t/" + str(x) + "-" + str(pair) + ".json"))#url  with newline oper
        return proccess_urls

    with Pool(None) as p:
        urls = p.map(make_url,coinsymbollist)
        print("pool result",urls)
        urls = list(chain.from_iterable(urls))
    return urls

def apply_blacklist(list_to_filter:list,blacklist_filename:str='blacklist.list'):
    blacklist = read_list_file(blacklist_filename)
    return list(filter(lambda x: x in blacklist,list_to_filter))

# fetch data,parse urls, sanitize data.

def get_coin_buy_prices(api_urls:list):
    coins = list(get_coinnames()) # list changes infrequently, but may occasioonallly cause problems
    exchangerates = {}
    unfinished = [] # urls that werent attempted due to a remote server disconnect
    blacklist = []
    # TODO - Work on a proper add_coin_price progress algo
    def add_coin_price(url):
        # i = 0
        base = url[str(url).rfind('/')+1:str(url).rfind('-')]  # rfinds start from 0 quirk to the rescue!
        try:
            # i += 1
            print(datetime.datetime.now(), 'Progress ','url is', url)
            cachepath = 'cache/' + url[url.rfind('/')+1:]
            with open(cachepath) as cache:
                print('Using Cache',cachepath)
                exchangerate = cache.read().decode() if cache.readable() else requests.get(url).json()
                exchangerate = exchangerate['ticker']['buy']
                print('Base Is',base,'Exchangerate is',exchangerate)
        except JSONDecodeError:
            exchangerate = 0.0
            return {'blacklist':url}
        except (RemoteDisconnected,ProtocolError,ConnectionError): # error cascade below! argh!
            # possible subexceptions go here.
            try:
                exchangerate = 0.0
                return {'TODO':url}
            except ProtocolError:
                try:
                    exchangerate = 0.0
                    return {'TODO': url}
                except ConnectionError:
                    try:
                        exchangerate = 0.0
                        return {'TODO': url}
                    except:
                        try:
                            exchangerate = 0.0
                            return {'TODO': url}
                        except Exception as e:
                            exchangerate = 0.0
                            return {'TODO': url}

        finally:
            return {str(base):[{str(url): float(exchangerate)}]}

    with Pool() as p: # parse the urls for prices
        results = p.map(add_coin_price,api_urls)
        # exchangerates = dict(ChainMap(*results))# *results

    print(results)

    # build the json file, by collating the "results" list of dicts into a json dict by key.
    def collate_by_coin(dict_key):
        flattened_dict = {dict_key:[]}
        for result in results:
            try:
                if result[dict_key]:
                    pair = str(result.values[0])[str(result.values[0]).rfind('-')+1:str(result.values[0]).rfind('.')-1] # get the crossex pair from a url.
                    flattened_dict[dict_key].append({pair:result.values()[1]})
            except Exception as e: # key error .. continue to next iteration
                continue
        return dict(flattened_dict)

    def collate_by_unfinished(results):
        for result in results:
            try:
                if result['TODO']:
                    return result['TODO']
            except Exception as e:
                print('result is',result)
                print(e.with_traceback())



    def collate_by_blacklist(results):
        for result in results:
            if result['blacklist']:
                return result['blacklist']

    # TODO - finish ccex.json
    with Pool() as p:
        # coins = list(dict(ChainMap(*results)).keys())
        exchangerateslist = p.map(collate_by_coin,coins)
        for exchangeratedict in exchangerateslist:
            exchangerates.update(exchangeratedict)

    #   TODO - Collate by 'unfinshed' key.
    with Pool() as p:
        unfinished = p.map(collate_by_unfinished,results)
    #   TODO - Collate by 'blacklist' key.
    #   def
    with Pool() as p:
        blacklist = p.map(collate_by_blacklist,results)

    return {'exchangerates':exchangerates,'unfinished':unfinished,'blacklist':blacklist}

def apply_coin_equivelent_exchanges(coinsymbolset:set,exchangerates:dict): # ETH-ETH = 1 etc.
    for base in coinsymbolset:
        exchangerates[str(base)] = list({str(base):1.0}) + exchangerates[str(base)]
    return exchangerates