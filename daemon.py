# -*- coding: UTF-8 -*-
"""
    Daemons for GPS

    Autor: Jorge A. Toro [jolthgs@gmail.com]

    Usage:
    >>> import daemon
    >>> d = daemon.DaemonUDP('', 50007, 256)
    >>> d.start()
    Server run :50007
    >>> d.run()

    >>> d1 = daemon.DaemonTCP('127.0.0.1', 50009, 256)
    >>> d1.start()
    >>> d1.run()

"""
import sys
import os
import socket
import threading
from Log.logFile import createLogFile, logFile
from Load.loadconfig import load
import Devices.devices

class DaemonUDP:
    """
        Server UDP
    """
    endfile = 0
    lock = threading.Lock()

    def __init__(self, host, port, buffering):

        self.host = host
        self.port = port
        self.buffering = buffering
        self.server = None # Servidor UDP activo 
        self.running = 1
        self.thread = None # Hilo actual de la instacia del objeto daemon

    def start(self):
        """
            Prepara el servidor
        """

        if createLogFile(str(load('FILELOG', 'FILE'))): # Creamos el fichero de Log
            try:
                self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Creamos el Socket Server 
                self.server.bind((self.host, self.port))
                print >> sys.stdout, ("Server run %s:%s" % (self.host, self.port))

            except socket.error, (value, message):
                if self.server:
                    self.server.close()
                print >> sys.stderr, "Could not open socket:", message
                sys.exit(1)

    def run(self):
        """
            threading
        """
        # Bucle Principal
        while self.running:
            try:
                data, address = self.server.recvfrom(self.buffering) # Esperamos por un cliente UDP

                ### SendDevice 
                #print >>sys.stderr, address
                #fdata = os.getcwd() + '/SendDevices/out'
                fdata = '/tmp/out'
                if os.path.exists(fdata):
                    #print >> sys.stderr, "**** SendDevice ****\n"
                    from SendDevices import SD
                    SD.sendData(fdata, self.server, address, data)
                # Send configuration from UDP to all AVL
                #if data.find('SKP'):
                #    command = 'AT$TTNR=1200,0&W'
                #    command = 'AT$TTSMSDST=4,"85482"&W'
                #    head = '\x00\x01\x04\x00 '
                #    self.server.sendto(head + command, address)
                #    d, s = self.server.recvfrom(4096)
                #    print >> sys.stderr, "%s\n%s : %s\n%s" % ("#"*30, d, data, "#"*30)

                self.thread = threading.Thread(target=self.threads, args=(data, address, self.__class__.lock, ))
                self.thread.start()
            except KeyboardInterrupt:
                sys.stderr.write("\rExit, KeyboardInterrupt\n")
                try:
                    sys.stdout.write("Exit App... \n")
                    self.server.close()
                    self.thread.join() # Esperamos hasta que se termine la ejecución del ultimo hilo
                                       # activo, para terminar la ejecución del programa.
                    raise SystemExit("Se terminaron de ejecutar todos los dispositivos activos en el servidor")
                except AttributeError, NameError: pass
                break # Salimos del bucle principal

    def threads(self, data, address, lock):
        """
            run thread
        """
        #import Devices

        #print "Data: " + data, "Nombre Hilo: " + self.thread.getName(), "Lock: " + str(lock)
        print >> sys.stdout, "Data:%s|Hilo: %s" % (data, self.thread.getName())
        #print "Hilo actual: ", threading.currentThread()
        #print "Hilos presentes:",  threading.enumerate()

        # Parse Devices
        rawData = Devices.devices.getTypeClass(data, address) # retorna la data analizada en un diccionario
        if not rawData.has_key('id'): # Si la trama no tiene ID 
            print >> sys.stdout, rawData#, '\n'
            return # Termina de ejecutar el hilo

        #print "rawData:", rawData #debugging

        ### Eventos
        import Event.captureEvent
        event = Event.captureEvent.parseEvent(rawData) # Si se gestiona retorna el nombre del 
                                                       # evento gestionado. Si no retorna None.
        #print "Evento Gestionado:", event
        print >> sys.stdout, "Evento Gestionado: %s" % (event)
        # End Event

        ### Escribe el la Tabla de Log
        import Log.logDB as LogDB
        LogDB.insertLog(rawData)
        # End Tabla de Log

        #### Escribe en el Fichero de Log
        lock.acquire(True)
        self.__class__.endfile = logFile(str(load('FILELOG', 'FILE')),
                                         self.__class__.endfile,
                                         raw=rawData)
        lock.release()
        # End Fichero de Log

        ### SendDevice 
        #print "IP/PORT:", address
        #fdata = os.getcwd() + '/SendDevices/out'
        #if os.path.exists(os.getcwd() + '/SendDevices/out'):
        #if os.path.exists(fdata):
        #    print >> sys.stdout, "**** SendDevice ****\n"
        #    from SendDevices import SD 
        #    SD.sendData(fdata, self.server, address, rawData)

class DaemonTCP:
    """
        Server TCP

    """
    def __init__(self, host, port, buffering):
        self.host = host
        self.port = port
        self.buffering = buffering
        self.server = None
    def start(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
            print ("Server run %s:%s" % (self.host, self.port))
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket:", message
            sys.exit(1)
    def run(self):
        pass
