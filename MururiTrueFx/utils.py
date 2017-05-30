

# pad a list with null - http://stackoverflow.com/a/3438818
def rjust( targetlistlength:int, list_to_pad:list ,fillvalue=''):
    return ([fillvalue] * (targetlistlength - len(list_to_pad))) + list_to_pad

def ljust(targetlistlength:int, list_to_pad:list ,fillvalue=''):
    return self + [fillvalue] * (targetlistlength - len(list_to_pad))

def actual_figure(bigbid,bidpips):
    return float(bigbid) + (float(bidpips) / 100000)