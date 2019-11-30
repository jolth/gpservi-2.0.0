#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from pytz import timezone
from Load.loadconfig import load

def code_event(event):
    """get the event code"""
    if event == 'tracker': return 5
    elif event == 'acc on': return 6
    elif event == 'acc off': return 7
    elif event == 'help me': return 1
    elif event == 'speed': return 2
    elif event == 'ac alarm': return 9
    else: return None

def tk_date(datetimezone):
    date = datetime.date(2000 + int(datetimezone[:2]), 
        int(datetimezone[2:4]), int(datetimezone[4:6]))
    return date
    
def tk_time(zero_time_zone):
    time = datetime.time(int(zero_time_zone[:2]), int(zero_time_zone[2:4]),
        int(zero_time_zone[4:6]), int(zero_time_zone[-2]), tzinfo=timezone('UTC'))
    return time

def tk_datetime(date, time): 
    return datetime.datetime.combine(date, time)
