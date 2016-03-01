# -*- coding: utf-8 -*-
"""
 Módulo de funciones corriente o cumunes para los dispositivos.
"""

def MphToKph(speed):
    import math
    return math.floor(float(speed) * 1.609344)

def NodeToKph(speed):
    import math
    return math.floor(float(speed) * 1.852)
  
def ignitionState(state):
    state = int(state)
    #print "**"*34
    #print "State", state
    #print "**"*34
    if state > 255:
        #return True
        return 't'
    else:
        #return False
        return 'f'

def ignitionStatett8750(state):
    i = int(state, 16)
    #print "**"*34
    #print "State", i
    #print "**"*34
    if i > 220:
        return 't'
    elif i <= 220:
        return 'f'
