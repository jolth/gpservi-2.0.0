# -*- coding: utf-8 -*-
import datetime
from pytz import timezone

def gv_time(time):
    """return time"""
    return time[-6:]


def gv_date(date):
    """return date"""
    return date[:8]

def gv_device_status(status): 
    """return status the of device"""
    s = int(status[:2],16)
    #if  s >= int('21',16) <= int('22',16):
    if s == int('21',16) or s == int('22',16):
        return 't'      
    #elif s >= int('11',16) <= int('12',16):
    elif s == int('11',16) or s == int('12',16): 
        return 'f'
    # develop: 16(Tow), 1A(Fake Tow), 42(Sensor Rest), 42(Sensor Motion)
    return None
