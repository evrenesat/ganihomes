#!/usr/bin/python
__author__ = 'Evren Esat Ozkan'

import sys

outfile = open('geoaliases.txt','w')



buffer = []
say = 0
first = 1
for l in open(sys.argv[1],'r'):
    if first:
        first = 0
        continue
    s = l.replace('"','').split('\t')
    if s[3] in [u'JPN\n',u'CHI\n',u'KOR\n']: continue
#    print '|%s|'%s[3]
#    break
    s[1]=s[1][:100]
    buffer.append('\t'.join(s[:2]))
    if len(buffer)==10000:
        say+=1
        outfile.write("\n".join(buffer))
        outfile.write("\n")
        buffer=[]
        print say



