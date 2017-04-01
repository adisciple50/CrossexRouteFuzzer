# devs scratchpad of workarounds.

## use this if one list item isnt one newline.
with open('urls.list','w+') as fix:
    bigstr = fix.read()
    bigstr = bigstr.replace('sonhtt','son/nhtt')
    fix.write(bigstr)