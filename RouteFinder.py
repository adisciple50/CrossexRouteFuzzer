import json
from itertools import chain,combinations,permutations,islice

rates = dict(json.loads(open("sample.json","r").read()))


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def generate_routes(rates):
    uniquecombos = list(powerset(rates.keys()))
    shuffleduniquecombos = []
    print(uniquecombos)
    for t in uniquecombos:
        l = permutations(t,len(t))
        # print(l)
        shuffleduniquecombos.extend(l)
    return shuffleduniquecombos
# print(generate_routes(rates))


def try_route(symbols:tuple,initialstake:float):
    subtotal = initialstake
    slice1 = islice(symbols,0,None,2)
    slice2 = islice(symbols,1,None,2)
    for symbol1,symbol2 in list(zip(slice1,slice2)):
        subtotal = rates[symbol1][symbol2]
    return subtotal

def try_routes(startcurrency,endcurrency,initialfloat):
    for route in generate_routes(rates):
        try_route(route)