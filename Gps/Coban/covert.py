#!/usr/bin/env python
# -*- coding: utf-8 -*-

def code_event(event):
    """get the event code"""
    if event == 'tracker': return 5
    elif event == 'acc on': return 6
    elif event == 'acc off': return 7
    elif event == 'help me': return 1
    elif event == 'speed': return 2
    elif event == 'ac alarm': return 9
    else: return None
