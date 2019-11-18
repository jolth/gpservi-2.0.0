#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Se debe crear un fichero como el siguiente:
KP005
AT$TTIODB=1,0
AT$TTNETWD=5,3,0,1
AT$TTSMSDST=1,"3144339861"
AT&W
Ctrl+d
"""
#from DB.pgSQL import PgSQL
#import psycopg2
#import StringIO
#import cStringIO
import sys

#f = open('../out', 'w')
#f = open('out', 'w')
f = open('/tmp/out', 'w')
#f = cStringIO.StringIO()

#def createDataSend(f):
while 1:
    try:
        f.write(raw_input('>>> '))
        f.write('\n')
    except EOFError:
        f.close()
        break

#f.seek(0)
#print >> sys.stdout, "Send..."
#print f.readline()
#print f.readline()
