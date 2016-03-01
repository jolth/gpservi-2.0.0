# -*- coding: UTF-8 -*-
import os
import sys
from datetime import datetime

class sendData:
    """
    """
    def __init__(self, f, server, address, data):
        #self.server = server
        #self.address = address
        self.data = data
        self.file = f
        #self.file = os.getcwd() + '/out'
        with open(self.file, 'r') as f:
            # Nombre del Dispositivo
            self.device = f.readline().replace('\n', '');

        #print >>sys.stderr, data  
        #if self.device == self.data['id']:
        if data.find(self.device) is not -1:
           print "#################  Device a Enviar Data:", self.device 
           self.send(server, address)
            
        
    def send(self, server, address): 
        #self.server.sendto('>SXADP10103148111847<', self.address)
        with open(self.file, 'r') as f:
            f.readline()
            s = 0
            for l in f:
                # Send data
                #server.sendto('>SXADP10103148111847<', self.address)
                #sent = server.sendto('0×00 0×01 0×04 0×00'+l, address)
                print >>sys.stderr, '<-' * 34
                print >>sys.stderr, 'Fecha: %s' % datetime.now()
                print >>sys.stderr, 'ID: %s' % self.device
                print >>sys.stderr, 'IP/Port: %s/%s' % (address[0], address[1])
                d = '\x00\x01\x04\x00 ' + l
                #print >>sys.stderr, d 
                #sent = server.sendto('\x00\x01\x04\x00 '+l.replace('\n', ''), address)
                sent = server.sendto(d, address)
                print >>sys.stderr, 'Sending: "%s"' % l 
                #if l == 'AT$RESET' or l == 'at$reset'

        # Eliminamos el fichero de Envio
        #print >>sys.stderr, 'Eliminando %s' % self.file
        os.remove(self.file)

        # Receive response
        print >>sys.stderr, 'Waiting to Receive:\n'
        d, s = server.recvfrom(4096)
        #print >>sys.stderr, 'received "%s"' % d
        print >>sys.stderr, d
        print >>sys.stderr, '->' * 34

        #os.delete(self.file)
        #os.delete(self.file)
