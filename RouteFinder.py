import json
from itertools import chain,combinations,permutations,islice
from multiprocessing import Pool

if __name__ == '__main__':
    rates = dict(json.loads(open("sample.json","r").read()))

# print(rates)

# from itertools doc recipies - https://docs.python.org/3.6/library/itertools.html
def powerset(iterable):
    # "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def generate_routes(rates):
    uniquecombos = list(powerset(rates.keys()))
    uniquecombos.pop(0)
    shuffleduniquecombos = []
    print(uniquecombos)
    def shuffle_extender(unique_combos):
        l = permutations(t, len(t))
        # print(l)
        shuffleduniquecombos.extend(l)
    with Pool() as p:
        p.map(shuffle_extender,uniquecombos)
    for t in uniquecombos:
        l = permutations(t,len(t))
        # print(l)
        shuffleduniquecombos.extend(l)
    return shuffleduniquecombos
# print(generate_routes(rates))


def try_route(currentrates,symbols:tuple,initialstake:float,startcurrency:tuple=('GBP',)):
    print("recieved symbols",symbols)
    subtotal = initialstake
    zipped = []
    symbols = symbols + startcurrency
    # start pairing tupples
    for i in range(len(symbols)):
        try:
            pair = tuple((symbols[i],symbols[i+1],))
            print("pair",pair)
            zipped.append(pair)
        except Exception as e:

            print("end reached?",e)
            continue


    print("zipped : ",zipped)
    for symbol1,symbol2 in zipped:
        print("symbol1",symbol1)
        print("symbol2",symbol2)
        rate = currentrates[str(symbol1)][0][str(symbol2)]
        if rate == "N/A":
            continue
        print("rate",rate)
        subtotal = subtotal * rate
        print("Start Symbol", symbol1 , "End Symbol" , symbol2, "New Balance (currency is now end symbol)",subtotal)
    return subtotal

def try_routes(startcurrency:tuple,endcurrency,initialstake:float,rates):
    results = {}
    routes = generate_routes(rates)
    def crunch_route(route):
        empty = ()
        if route == empty:
            pass
        newroute = tuple(startcurrency) + tuple(route)
        print("newroute", newroute)
        if newroute[-1] == endcurrency and newroute[0] == str(startcurrency[0]):
            result = try_route(rates, newroute, initialstake, startcurrency=startcurrency)
            results[newroute] = result
    with Pool as p:
        p.map(crunch_route,routes)
    return results


if __name__ == '__main__':
    print(try_routes(('GBP',),'GBP',1.0))
