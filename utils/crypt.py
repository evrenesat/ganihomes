from itertools import izip, cycle
from urllib2 import base64

def sxor(data, decrypt=False, key='8239e9ehdu2$ # D ^@ $^d2frg456g4er62-r*/-*f823*-4f8324-*fd-*'):
    if decrypt:
        return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(base64.standard_b64decode(data), cycle(key)))
    else:
        return base64.standard_b64encode(''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key))))
