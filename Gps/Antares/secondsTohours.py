# -*- coding: utf-8 -*-
"""
    Convert seconds to hours, minute, seconds
"""
from pytz import timezone

def secTohr(sec):
    """
        >>> import secondsTohours
        >>> 

        Versio vieja:
        >>> secondsTohours.secTohr(10453)
        '2:54:13'
        >>> 

        Nueva versión:
        >>> secondsTohours.secTohr(10453)
        datetime.time(2, 54, 13, tzinfo=<UTC>)
        >>> 
    """
    import datetime

    sec = int(sec)

    h = sec / 3600
    sec = sec % 3600
    m = sec / 60
    sec = sec % 60

    #return "%d:%d:%d" % (h, m, sec) 
    return datetime.time(h, m, sec, tzinfo=timezone('UTC')) 

