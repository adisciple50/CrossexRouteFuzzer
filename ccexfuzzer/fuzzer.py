from ccexfuzzer.functions import *
import json
from RouteFinder import *
import multiprocessing


def run():

    urls = []
    coin_names = set(get_coinnames())

    try:
        with open('urls.list', 'r'): # only checks if file exists
            urls = read_list_file('urls.list')
    except:
        with open('urls.list', 'w+') as urlslist:
            urls = generate_urls(coin_names)
            print("coin_names:",coin_names)
            print(urls)
            urlslist.writelines(urls)


    try:
        with open('blacklist.list','r'):
            urls = apply_blacklist(urls)
    except Exception as e:
        with open('blacklist.list', 'x'):
            pass

    results = get_coin_buy_prices(urls)

    with open('ccex.json','w') as ccexjson:
        ccexjson.writelines(json.dumps(results['exchangerates']))
    write_list_to_file(results['blacklist'],'blacklist.list')
    write_list_to_file(results['unfinished'],'unfinished.list') # writes urls that werent able to return data, because the server disconnected before the run.


def resume_unfinished(unfinished:str='unfinished.list'):
    results = get_coin_buy_prices(read_list_file(unfinished))

    with open('ccex.json', 'w') as ccexjson:
        ccexjson.writelines(json.dumps(results['exchangerates']))
    with open(unfinished,'w') as ufile:
        ufile.truncate() # clear infinished before rewriting.
    write_list_to_file(results['blacklist'], 'blacklist.list')
    write_list_to_file(results['unfinished'],'unfinished.list')  # writes urls that werent able to return data, because the server disconnected before the run.


if __name__ == '__main__':
    # print(list(get_coinnames()))
    run()
    # print(try_routes(('GBP',), 'GBP', 1.0,dict(json.loads(open('ccex.json','r').read()))))