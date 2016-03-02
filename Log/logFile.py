# -*- coding: utf8 -*-
"""
  Modulo que crea y gestiona el fichero de log

  Author: Jorge A. Toro
  Date: 02-02-2012

  Usage:

"""

def createLogFile(arch):
    """
        Create file of Log

        usage:
        createLogFile('/tmp/log')
    """
    with open(arch, 'w') as  f:
        if f.tell() == 0:
            print >> f, 'ID'.center(8), 'IP,Port'.center(24), \
            'Date'.center(12), 'Time'.center(10), \
            'Event'.center(9), 'Latitude'.center(10), \
            'Longitude'.center(12), 'Geocoding'.center(36), \
            'Data'.center(62)
            print >> f, ('-'*6).ljust(8), ('-'*22).ljust(24), \
            ('-'*10).ljust(14), ('-'*8).ljust(10), \
            ('-'*6).ljust(6), ('-'*10).ljust(11), \
            ('-'*10).ljust(12), ('-'*34).ljust(36), \
            ('-'*60).ljust(62)
    return True

def logFile(arch, endFile=0, **data):
    """
       Fichero de Log

       Imprime la imformación contenida **data
       a el fichero de log descrito por arch.

       usage:
       logFile('/tmp/log', final_buffer, foo1='data', foo2='data', ...)
       logFile('/tmp/log', final_buffer, foo='data', {'foo1':'data', 'foo2':'data', ...})
    """
    import time
    import codecs

    with codecs.open(arch, 'a+', 'utf-8') as f:
        f.seek(endFile)
        print >> f, ("%(id)s" % data['raw']).ljust(8), \
        ("%(address)s" % data['raw']).ljust(26), \
        (time.strftime('%D')).ljust(12), \
        (time.strftime("%H:%M:%S")).ljust(10), \
        ("%(codEvent)s" % data['raw']).ljust(6), \
        ("%(lat)s" % data['raw']).ljust(11), \
        ("%(lng)s" % data['raw']).ljust(12), \
        ("%(geocoding)s" % data['raw']).ljust(36), \
        ("%(data)s" % data['raw']).ljust(62)
        endFile = f.tell()
    return endFile

