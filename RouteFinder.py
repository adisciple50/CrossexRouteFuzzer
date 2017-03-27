import json
from itertools import chain,combinations,permutations,islice

rates = dict(json.loads(open("sample.json","r").read()))

# print(rates)

# from itertools doc recipies - https://docs.python.org/3.6/library/itertools.html
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def generate_routes(rates):
    uniquecombos = list(powerset(rates.keys()))
    uniquecombos.pop(0)
    shuffleduniquecombos = []
    print(uniquecombos)
    for t in uniquecombos:
        l = permutations(t,len(t))
        # print(l)
        shuffleduniquecombos.extend(l)
    return shuffleduniquecombos
# print(generate_routes(rates))


def try_route(symbols:tuple,initialstake:float):
    print("recieved symbols",symbols)
    subtotal = initialstake
    zipped = []
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
        rate = rates[str(symbol1)][0][str(symbol2)]
        if rate == "N/A":
            continue
        print("rate",rate)
        subtotal = rate / subtotal
    return subtotal

def try_routes(startcurrency:tuple,endcurrency,initialstake:float):
    results = {}
    for route in generate_routes(rates):
        empty = ()
        if route == empty:
            pass
        print(route)
        if route[-1] == endcurrency and route[0] != startcurrency:
            result = try_route(startcurrency + tuple(route),initialstake)
            results[route] = result
    return results

print(try_routes(('GBP',),'GBP',1.0))