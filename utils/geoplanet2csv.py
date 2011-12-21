#!/usr/bin/python
__author__ = 'Evren Esat Ozkan'

import sys,os
from collections import defaultdict

class Sayac:
    def __init__(self):
        self.SAYAC=0
    def __call__(self):
        self.SAYAC +=1
        return self.SAYAC



place_types_file = open('ptypes.txt','w')
outfile = open('geoplanet.txt','w')

pt=Sayac()
place_types = defaultdict(pt)



buffer = []
say = 0
for l in open(sys.argv[1],'r'):
    s = l.replace('"','').split('\t')
    s[2]=s[2][:100]
    del s[3]
    s[3]=str(place_types[s[3]])
    buffer.append(','.join(s))
    if len(buffer)==10000:
        say+=1
        outfile.write("".join(buffer))
        buffer=[]
        print say
place_types_file.write(repr(place_types.items()))


