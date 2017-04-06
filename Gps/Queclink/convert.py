# -*- coding: utf-8 -*-
import datetime
from pytz import timezone

def gv_time(time):
    """return time"""
    return time[-6:]


def gv_date(date):
    """return date"""
    return date[:8]

def gv_device_status(status, tag=None): 
    """return status the of device"""
    s = int(status[:2],16)
    if tag is not None:
        if tag == 'ignition':
            if s == int('21',16) or s == int('22',16): #ignition on reset/ on motion
                return 't'      
            elif s == int('11',16) or s == int('12',16): #ingition off reset/off motion
                return 'f'
        elif tag == 'tow': #16(Tow), 1A(Fake Tow)
            if s == int('1A',16): return 10 #event number to 'towed'
            elif s == int('16',16): return 10 #event number to 'towed'
        elif tag == 'ign_signal': #41(Sensor Rest), 42(Sensor Motion)
            if s == int('42',16): return None #event number to 'without ignition signal'
            elif s == int('41',16): return None #event number to 'without ignition signal'
    else: return tag

def gv_get_event_code(event):
    """get the event code"""
