# -*- coding: utf-8 -*-
from __future__ import division
from pytz import timezone

def deg_to_dms(num, signo):
    """
    """
    point = num.find('.')
    d = num[:point-2]
    m = num[point-2:]
    m = float(m) / 60
    numero = float(d) + m
    if signo in ['S','W']:
        return numero * (-1)
    return numero

def degTodms(s):
    """
    """
    #s = s.split(',')
    num = s[0]
    signo = s[1]
    point = num.find('.')
    d = num[:point-2]
    m = num[point-2:]
    m = float(m) / 60
    numero = float(d) + m
    if signo in ['S','W']:
        return numero * (-1)
    return numero

def skpDate(date):
    """
        Retorna un datetime con la fecha en que la unidad genero la trama.

        >>> date = '041212'
        >>> datetime.date(2000 + int(date[4:6]), int(date[2:4]), int(date[0:2])) 
        datetime.date(2012, 12, 4)
        >>>
    """
    import datetime
    return datetime.date(2000 + int(date[4:6]), int(date[2:4]), int(date[0:2]))

def skpTime(time):
    """
        Retorna un datetime con la hora en que la unidad genero la trama.

        >>> time = '212753.00'
        >>> datetime.time(int(time[0:2]), int(time[2:4]), int(time[4:6]), int(time[-2]))
        datetime.time(21, 27, 53)
        >>> 
    """
    import datetime
    return datetime.time(int(time[0:2]), int(time[2:4]), int(time[4:6]), int(time[-2]), tzinfo=timezone('UTC'))

def fechaHoraSkp(date, time):
    """
        Crea un datetime para la fecha y la hora en que la unidad
        genero la trama.

        >>> from datetime import datetime
        >>> from pytz import timezone
        >>>
        >>> d1 = date(2012, 12, 4)
        >>> d2 = time(21, 27, 53, tzinfo=timezone('UTC'))
        >>> d3 = datetime.combine(d1, d2)
        >>> d3
        datetime.datetime(2012, 12, 4, 21, 27, 53, tzinfo=<UTC>)
        >>> d3.astimezone(timezone('America/Bogota'))
        datetime.datetime(2012, 12, 4, 16, 27, 53, tzinfo=<DstTzInfo 'America/Bogota' COT-1 day, 19:00:00 STD>)
        >>>

    """
    #import datetime
    #return datetime.datetime(date.year, date.month, date.day, 
    #               time.hour, time.minute, time.second, time.microsecond)
    from datetime import datetime
    from Load.loadconfig import load
    #gmt = -5
    #gmt = int(load('CONFIGURE', 'GMT'))
    utc = load('CONFIGURE', 'UTC')
    #return datetime.combine(date, time)
    dt = datetime.combine(date, time)
    #return dt.astimezone(timezone('America/Bogota'))
    return dt.astimezone(timezone(str(utc)))

def mTokm(meters):
    return "{:,} km".format(meters / 1000)
