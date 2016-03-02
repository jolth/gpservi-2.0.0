#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Server GPS

    Autor: Jorge A. Toro [jolthgs@gmail.com]
"""
import daemon
from Load.loadconfig import load

if __name__ == "__main__":
    server = daemon.DaemonUDP(
                str(load('DAEMON', 'DAEMONHost')),
                int(load('DAEMON', 'DAEMONPort')),
                int(load('DAEMON', 'DAEMONBuffer'))
             )
    server.start()
    server.run()
