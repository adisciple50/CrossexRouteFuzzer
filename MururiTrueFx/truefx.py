import urllib

import urllib.request as truefx
from urllib.error import HTTPError


# url = 'http://webrates.truefx.com/rates/connect.html' - in case of endpoint change please refactor - or "find and replace".

def login(username:str,password:str,symbols:list,qualifier='eurates',pollformat='csv',snapshot=True,url='http://webrates.truefx.com/rates/connect.html'):
    # make snapshot pythonic
    if snapshot:
        snapshot = 'y'
    else:
        snapshot = 'n'

    symbol_param = symbols[0] if len(symbols) == 1 else symbols.join(',')

    login_url = str(
        url + '?u=' + username + '&p=' + password + '&q=' + qualifier + '&c=' + symbol_param + '&f=' + pollformat + '&s=' + snapshot)
    with truefx.urlopen(login_url) as response:
        if response == 'not authorized':
            raise HTTPError(login_url,401,'Incorrect Username And/Or Password')
        else:
            return response.read().decode()



def poll_one_pair(auth_response:str,url='http://webrates.truefx.com/rates/connect.html'):
    with truefx.urlopen(url + '?id=' + auth_response) as results:
        response = results.read().decode()
        # print('response is',response) #uncomment for debug
        poll_response = dict(zip(['currency-pair', 'millisecond-timestamp', 'bigbid','bidpips', 'high','low', 'pollopen'],
                        response.split(',')))
        poll_response.update({'response':response})
        if response:  # dont print blank reponses
            return poll_response
        else:
            print('No Response')
            False

