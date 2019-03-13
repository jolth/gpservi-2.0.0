# -*- coding: utf-8 -*-
import datetime
from pytz import timezone

def gv_time(time):
    """return time"""
    #return time[-6:]
    return datetime.time(int(time[-6:][:2]), int(time[-6:][2:4]),
            int(time[-6:][-2:]), tzinfo=timezone('UTC'))
    
def gv_date(date):
    """return date"""
    #return date[:8]
    return datetime.date(int(date[:8][:-4]), int(date[:8][4:6]), int(date[:8][6:]))

def gv_device_status(status, tag=None): 
    """return status the of device"""

    # detection digital input(IGN) trame :GTFRI
    if len(status) == 2 and tag == 'ignition':
        return 't' if int(status, 2) > 0 else 'f'

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
    #if event == '+RESP:GTFRI': return '5' #programated report
    #elif event == '+RESP:GTSOS': return '1' #panic report
    #elif event == '+RESP:GTSPD': return '2' #speed alarm
    #elif event == '+RESP:GTIGN': return '6' #ignition on report
    #elif event == '+RESP:GTIGF': return '7' #ignition off report
    #elif event == '+RESP:GTMPN': return '8' #connecting main power supply   
    #elif event == '+RESP:GTMPF': return '9' #disconnecting main power supply
    if event[6:] == 'GTFRI': return '5' #programated report
    elif event[6:] == 'GTSOS': return '1' #panic report
    elif event[6:] == 'GTSPD': return '2' #speed alarm
    elif event[6:] == 'GTIGN': return '6' #ignition on report
    elif event[6:] == 'GTIGF': return '7' #ignition off report
    elif event[6:] == 'GTMPN': return '8' #connecting main power supply   
    elif event[6:] == 'GTMPF': return '9' #disconnecting main power supply
    else: return None
