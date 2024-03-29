# -*- coding: utf-8 -*-
# Author: Jorge A. Toro
#
import sys
import datetime
import StringIO
from UserDict import UserDict
import simplejson as json
from Gps.Antares.convert import latWgs84ToDecimal, lngWgs84ToDecimal
from Gps.Antares.secondsTohours import secTohr
#from Gps.Antares.gpsdate import GpsToMjd, MjdToDate 
from Gps.SkyPatrol.convert import degTodms, skpDate, skpTime, fechaHoraSkp
from Gps.SkyPatrol.convert import mTokm
from Gps.common import MphToKph, NodeToKph
from Gps.common import ignitionState, ignitionStatett8750
import Location.geomapgoogle
import Location.geocoding
import Location.nominatim
from Gps.Queclink import convert
from Gps.Coban.convert import code_event, tk_date, tk_time, tk_datetime, tk_speed


def tagData(dFile, position, bit=None, seek=0):
    """
        Toma un punto de partida (position), cantidad de bit y un punto de
        referencia para leer los bit(según el método seek() de los fichero).
        Además dataFile el cual es objeto StringIO.
    """
    try:
        dFile.seek(position, seek)
        tagdata = dFile.read(bit)
    except: sys.stderr.write("Error al obtener el Tag Data")
    return tagdata

# Clase que actua como un diccionario
class Device(UserDict):
    """ Store Device"""
    def __init__(self, deviceData=None, address=None):
        UserDict.__init__(self)
        self["data"] = deviceData
        #self["address"] = address
        self["address"] = "%s,%s" % address
        #self["geocoding"] = None
        # Fecha y hora (del sistema)
        # se comenta self['datetime'] para realizar 
        # el time zone en las Skypatrol
        #self["datetime"] = datetime.datetime.now()

class ANTDevice(Device):
    """
        Dispositivo Antares
    """
    tagDataANT = {  # (position, bit, seek, function_tagData, function_convert )
                    #"id"        : (-6, 6, 2, tagData)#, # ID de la unidad
                    "id"        : (-6, None, 2, tagData, None), # ID de la unidad
                    "type"      : (0, 1, 0, tagData, None),
                    "typeEvent" : (1, 2, 0, tagData, None),     # 
                    "codEvent"  : (3, 2, 0, tagData, None),     # Codigo de evento activado (en Antares de 00 a 49, en e.Track de 00 a 99)
                    "weeks"     : (5, 4, 0, tagData, None),     # Es el numero de semanas desde 00:00AM del 6 de enero de 1980.
                    "dayWeek"   : (9, 1, 0, tagData, None),     # 0=Domingo, 1=Lunes, etc hasta 6=sabado.
                    #"time"      : (10, 5, 0, tagData, None),    # Hora expresada en segundos desde 00:00:00AM
                    "secondsDay"      : (10, 5, 0, tagData, None),    # Hora expresada en segundos desde 00:00:00AM
                    "time"      : (10, 5, 0, tagData, secTohr),    # Hora expresada en segundos desde 00:00:00AM
                    "lat"       : (15, 8, 0, tagData, latWgs84ToDecimal),    # Latitud
                    "lng"       : (23, 9, 0, tagData, lngWgs84ToDecimal),    # Longitud
                    "speed"     : (-18, 3, 2, tagData, MphToKph),   # Velocidad en MPH
                    "course"    : (-15, 3, 2, tagData, None),   # Curso en grados
                    "gpsSource" : (-12, 1, 2, tagData, None),   # Fuente GPS. Puede ser 0=2D GPS, 1=3D GPS, 2=2D DGPS, 3=3D DGPS, 6=DR, 8=Degraded DR.     
                    "ageData"   : (-11, 1, 2, tagData, None)    # Edad del dato. Puede ser 0=No disponible, 1=viejo (10 segundos) ó 2=Fresco (menor a 10 segundos)
                    #odometer
                 }


    def __parse(self, data):
        self.clear()
        try:
            dataFile = StringIO.StringIO(data[1:-1]) # remove '<' y '>'
            #
            for tag, (position, bit, seek, parseFunc, convertFunc) in self.tagDataANT.items():
                self[tag] = convertFunc and convertFunc(parseFunc(dataFile, position, bit, seek)) or parseFunc(dataFile, position, bit, seek)

            self['odometer'] = None
            # Creamos una key para la altura (estandar), ya que las tramas actuales no la incluyen:
            self['altura'] = None
            # Creamos una key para el dato position:
            self['position'] = "(%(lat)s,%(lng)s)" % self

            # Date/Datetime
            #mjd = GpsToMjd(int(self['weeks']), int(self['secondsDay']))
            #date = MjdToDate(mjd, 1980, 1, 6)

            #self['date'] = MjdToDate(mjd, 1980, 1, 6)
            #self['date'] = ("%d, %d, %d" % (date[0], date[1], date[2]+int(self['dayWeek']))).split(',')
            #self["datetime"] = None 

            #date = ("%d, %d, %d" % (date[0], date[1], date[2]+int(self['dayWeek']))).split(',')
            #self["date"] = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            #self["datetime"] = fechaHoraSkp(self["date"], self["time"]) 
            self["datetime"] = datetime.datetime.fromtimestamp((315964800000 + ((int(self['weeks'])* 7 + int(self['dayWeek'])) * 24 * 60 * 60 + int(self['secondsDay'])) * 1000) // 1000) 

            # Realizamos la Geocodificación. Tratar de no hacer esto
            # es mejor que se realize por cada cliente con la API de GoogleMap
            self["geocoding"] = None
            #self["geocoding"] = Location.geocoding.regeocodeGMap('%s,%s' % (self["lat"], self["lng"]))
            self["geocoding"] = Location.nominatim.Openstreetmap(self["lat"],
                    self["lng"]).decodeJSON()
        except Exception: print(sys.exc_info()) #sys.stderr.write('Error Inesperado:', sys.exc_info())
        finally: dataFile.close()


    def __setitem__(self, key, item):
        if key == "data" and item:
            self.__parse(item)
        # Llamamos a __setitem__ de nuestro ancestro
        Device.__setitem__(self, key, item)

def tagDataskp(dList, start, end, name):
    """
        Toma una posición para obtener de la lista dList.
    """
    try:
        #if end is not None: 
        if end:
            #tagdata = ",".join(dList[start:end + 1])
            tagdata = dList[start:end + 1]
        else:
            tagdata = dList[start]
    except:
        from datetime import datetime
        sys.stderr.write("Error al obtener el Tag Data: %s, %s. Evento: %s [%s].\n" % (name, dList[2], dList[1], str(datetime.now()))) # dList[2] el 'id'
    return tagdata or None

class SKPDevice(Device):
    """
        Dispositivo Skypatrol
    """
    # ['', '5', 'SKP87', '$GPRMC', '122408.00', 'A', '0441.935953', 'N', '07404.450302', 'W', '0.0', '0.0', '180912', '5.5', 'E', 'A*2F']
    # ['', '5', 'SKP002', 'GPRMC', '225235.00', 'A', '0502.87758', 'N', '07530.30432', 'W', '0.000', '0.0', '191012', 'A*42']
    # ['', '6', 'SKP001', '459', 'GPRMC', '155120.00', 'A', '0502.87300', 'N', '07530.33326', 'W', '0.000', '0.0', '031212', 'A*40']
    #
    # dataList:  ['', '\x00\x04\x02\x10\x00', '1', 'SKP000', '206', 'GPRMC', '165919.00', 'A', '0502.30467', 'N', '07527.54462', 'W', '0.000', '0.0', '220217', 'A*4C', '43']
    #            [ 0,                      1,   2,        3,     4,       5,           6,   7,            8,   9,            10,  11,      12,    13,       14,     15,   16]
    # 23022017:  ['5', 'SKP000', '207', 'GPRMC', '231019.00', 'A', '0502.30514', 'N', '07527.55054', 'W', '0.000', '0.0', '230217', 'A*43', '43']
    #            [  0,        1,     2,       3,           4,   5,            6,   7,             8,   9,      10,    11,       12,     13,  14,]
    tagDataSKP = {
    #               "key"       : (position_start, position_end, function_tagData, nameTag, function_convert)
                    "id"        : (2, None, tagDataskp, 'id', None), # ID de la unidad
                    "type"      : (0, None, tagDataskp, 'type', None),
                    "typeEvent" : (0, None, tagDataskp, 'typeEvent', None), # 
                    "ignition"  : (3, None, tagDataskp, 'ignition', ignitionState), # 
                    "codEvent"  : (1, None, tagDataskp, 'codEvent', None), # Codigo de evento activado (en Antares de 00 a 49, en e.Track de 00 a 99)
                    "weeks"     : (0, None, tagDataskp, 'weeks', None), # Es el numero de semanas desde 00:00AM del 6 de enero de 1980.
                    "dayWeek"   : (0, None, tagDataskp, 'dayWeek', None), # 0=Domingo, 1=Lunes, etc hasta 6=sabado.
                    "time"      : (5, None, tagDataskp, 'time', skpTime), # Hora expresada en segundos desde 00:00:00AM
                    "lat"       : (7, 8, tagDataskp, 'lat', degTodms), # Latitud
                    "lng"       : (9, 10, tagDataskp, 'lng', degTodms), # Longitud
                    "speed"     : (11, None, tagDataskp, 'speed', NodeToKph),   # Velocidad en MPH
                    "course"    : (12, None, tagDataskp, 'course', None), # Curso en grados
                    "gpsSource" : (0, None, tagDataskp, 'gpsSource', None), # Fuente GPS. Puede ser 0=2D GPS, 1=3D GPS, 2=2D DGPS, 3=3D DGPS, 6=DR, 8=Degraded DR. # Problema DB si no son enteros    
                    "ageData"   : (0, None, tagDataskp, 'ageData', None), # Edad del dato. Puede ser 0=No disponible, 1=viejo (10 segundos) ó 2=Fresco (menor a 10 segundos) # Problema DB si no son enteros
                    "date"  : (13, None, tagDataskp, 'date', skpDate), # Fecha 
                    "odometer"  : (15, None, tagDataskp, 'odometer', mTokm) # Odómetro
                 }

    def __parse(self, data):
        self.clear()
        try:
            import re
            #print "DATA:", data
            #data = data.replace('\x00\x04\x02\x10\x00',',')
            #print "data0:", data #(Print de Prueba)
            ####
            # data = '     5                 SKP87 $GPRMC,122408.00,A,0441.935953,N,07404.450302,W,0.0,0.0,180912,5.5,E,A*2F'
            #data = data.replace(' ', ',')
            # ',,,,,5,,,,,,,,,,,,,,,,,SKP87,$GPRMC,122408.00,A,0441.935953,N,07404.450302,W,0.0,0.0,180912,5.5,E,A*2F'
            #print "data1:", data #(Print de Prueba)
            #data = re.sub(r",,", "", data)
            # ',5,SKP87,$GPRMC,122408.00,A,0441.935953,N,07404.450302,W,0.0,0.0,180912,5.5,E,A*2F'
            #print "data2:", data
            #dataList = data.split(',')
            data = data.strip().replace(' ',',')
            dataList = [i for i in data.split(',') if i and i !=
                    '\x00\x04\x02\x10\x00']
            #print "[%d]:%s" % (len(dataList), dataList) #debugging
            #dataList = [i for i in data.split(',') if i]
            # ['', '5', 'SKP87', '$GPRMC', '122408.00', 'A', '0441.935953', 'N', '07404.450302', 'W', '0.0', '0.0', '180912', '5.5', 'E', 'A*2F']
            #['7', 'SKP002', 'GPRMC', '224431.00', 'A', '0502.87359', 'N', '07530.30060', 'W', '0.000', '0.0', '191012', 'A*47']
            #
            dataList.insert(0, '') # Crear para los datos que son necesarios.
            #dataList.append('')
            #print "dataList: ", dataList #(Print de Prueba)
            #raise SystemExit(1)
            for tag, (position_start, position_end, parseFunc, nameTag, convertFunc) in self.tagDataSKP.items():
                self[tag] = convertFunc and convertFunc(parseFunc(dataList, position_start, position_end, nameTag)) or parseFunc(dataList, position_start, position_end, nameTag)

            # Creamos una key para la altura (estandar), ya que las tramas actuales no la incluyen:
            self['altura'] = None
            # Creamos una key para el dato position:
            self['position'] = "(%(lat)s,%(lng)s)" % self

            # Fecha y Hora del dispositivo:
            #self["fechahora"] = fechaHoraSkp(self["date"], self["time"]) 
            self["datetime"] = fechaHoraSkp(self["date"], self["time"])

            #print "-" * 20
            #print self
            #raise SystemExit(1)
            # Realizamos la Geocodificación. Tratar de no hacer esto
            # es mejor que se realize por cada cliente con la API de GoogleMap
            self["geocoding"] = None
            #self["geocoding"] = json.loads(Location.geomapgoogle.regeocode('%s,%s' % (self["lat"], self["lng"])))[0]
            #self["geocoding"] = Location.geocoding.regeocodeOSM('%s,%s' % (self["lat"], self["lng"])) # Dejo de funcionar el 16-09-2015
            #self["geocoding"] = Location.geocoding.regeocodeGMap('%s,%s' % (self["lat"], self["lng"])) # Dejo de funcionar el 17-09-2015
            # Nominatim:
            #self["geocoding"] = Location.nominatim.Openstreetmap((self["lat"], self["lng"]))
            self["geocoding"] = Location.nominatim.Openstreetmap(self["lat"], self["lng"]).decodeJSON()
            #print "-" * 20
            #print self
            #raise SystemExit(1)
        except Exception: print(sys.exc_info()) #sys.stderr.write('Error Inesperado:', sys.exc_info())
        #finally: dataFile.close()

    def __setitem__(self, key, item):
        if key == "data" and item:
            self.__parse(item)
        # Llamamos a __setitem__ de nuestro ancestro
        Device.__setitem__(self, key, item)


class TTDevice(Device):
    """
        Dispositivo Skypatrol TT8750 & ENFORA
    """
    #[18]:['', '5', 'TT013', 'D1', 'DF', '$GPRMC', '213210.00', 'A', '0523.663818', 'N', '07535.950195', 'W', '0.0', '0.0', '270217', '4.6', 'E', 'A*24']
    tagDataSKP = {  # (position_start, position_end, function_tagData, nameTag, function_convert )
                    "id"        : (2, None, tagDataskp, 'id', None), # ID de la unidad
                    "type"      : (0, None, tagDataskp, 'type', None),
                    "typeEvent" : (3, None, tagDataskp, 'typeEvent', None), # 
                    "ignition"  : (4, None, tagDataskp, 'ignition', ignitionStatett8750), # HACER ESTO 
                    "codEvent"  : (1, None, tagDataskp, 'codEvent', None), # Codigo de evento activado (en Antares de 00 a 49, en e.Track de 00 a 99)
                    "weeks"     : (0, None, tagDataskp, 'weeks', None), # Es el numero de semanas desde 00:00AM del 6 de enero de 1980.
                    "dayWeek"   : (0, None, tagDataskp, 'dayWeek', None), # 0=Domingo, 1=Lunes, etc hasta 6=sabado.
                    "time"      : (6, None, tagDataskp, 'time', skpTime), # Hora expresada en segundos desde 00:00:00AM
                    "lat"       : (8, 9, tagDataskp, 'lat', degTodms), # Latitud
                    "lng"       : (10, 11, tagDataskp, 'lng', degTodms), # Longitud

                    "speed"     : (12, None, tagDataskp, 'speed', NodeToKph),   # Velocidad en MPH
                    "course"    : (13, None, tagDataskp, 'course', None), # Curso en grados
                    "gpsSource" : (0, None, tagDataskp, 'gpsSource', None), # Fuente GPS. Puede ser 0=2D GPS, 1=3D GPS, 2=2D DGPS, 3=3D DGPS, 6=DR, 8=Degraded DR. # Problema DB si no son enteros    
                    "ageData"   : (0, None, tagDataskp, 'ageData', None), # Edad del dato. Puede ser 0=No disponible, 1=viejo (10 segundos) ó 2=Fresco (menor a 10 segundos) # Problema DB si no son enteros
                    "date"  : (14, None, tagDataskp, 'date', skpDate), # Fecha 
                    "odometer"  : (0, None, tagDataskp, 'odometer', None) # Odómetro
                 }

    def __parse(self, data):
        self.clear()
        try:
            import re
            data = data.strip().replace(' ',',')
            dataList = [i for i in data.split(',') if i and i !=
                    '\x00\x04\x02\x00']
            dataList.insert(0, '')
            #print "[%d]:%s" % (len(dataList), dataList)
            #[18]:['', '5', 'TT013', 'D1', 'DF', '$GPRMC', '213210.00', 'A', '0523.663818', 'N', '07535.950195', 'W', '0.0', '0.0', '270217', '4.6', 'E', 'A*24']
            for tag, (position_start, position_end, parseFunc, nameTag, convertFunc) in self.tagDataSKP.items():
                self[tag] = convertFunc and convertFunc(parseFunc(dataList, position_start, position_end, nameTag)) or parseFunc(dataList, position_start, position_end, nameTag)
            #print "[%d]:%s" % (len(dataList), dataList)
            #print "-" * 100
            #print self
            #raise SystemExit(1)
            # Creamos una key para la altura (estandar), ya que las tramas actuales no la incluyen:
            self['altura'] = None
            # Creamos una key para el dato position:
            self['position'] = "(%(lat)s,%(lng)s)" % self
            # Fecha y Hora del dispositivo:
            self["datetime"] = fechaHoraSkp(self["date"], self["time"])
            # Realizamos la Geocodificación. Tratar de no hacer esto
            # es mejor que se realize por cada cliente con la API de GoogleMap
            self["geocoding"] = None
            #self["geocoding"] = Location.geocoding.regeocodeGMap('%s,%s' % (self["lat"], self["lng"]))
            self["geocoding"] = Location.nominatim.Openstreetmap(self["lat"],
                    self["lng"]).decodeJSON()
            #print "-" * 100 # debugging
            #print self # debugging
        except Exception: print(sys.exc_info()) #sys.stderr.write('Error Inesperado:', sys.exc_info())

    def __setitem__(self, key, item):
        if key == "data" and item:
            self.__parse(item)
        # Llamamos a __setitem__ de nuestro ancestro
        Device.__setitem__(self, key, item)


class HUNTDevice(Device):
    """
        Dispositivo Hunter
    """
    pass


class GVDevice(Device):
    """
        Dispositivo Skypatrol
    """
    # Position Related Report
    # [23]: ['+RESP:GTSOS', '2F0500', '862193026878108', 'GV001', '', '', '10', '1', '1', '0.0', '0', '2139.3', '-75.459194', '5.038412', '20170406171445', '', '', '', '', '', '0.7', '', '0EDC$']
    # Fixed report
    # [31]: ['+RESP:GTFRI', '2F0500', '862193026878108', 'GV001', '', '', '10', '1', '1', '0.0', '0', '2139.0', '-75.459166', '5.038386', '20170406142915', '', '', '', '', '', '0.7', '', '', '', '100', '210100', '', '', '', '', '0E20$']
    #       [ 0,             1,        2,                 3,       4 ,   5,   6,   7,     8,    9,       10,           11,         12,               13,    14,    15,       16,      17]
    # Not support:
    # Device Information Report
    # Report of Real Time Querying
    tagDataGV = {
    #               "key"       : (position_start, position_end, function_tagData, nameTag, function_convert)
                    "id"        : (3, None, tagDataskp, 'id', None), # ID de la unidad
                    "type"      : (4, None, tagDataskp, 'type', None),
                    "typeEvent" : (4, None, tagDataskp, 'typeEvent', None), # 
                    "altura"    : (10, None, tagDataskp, 'altura', None),
                    "ignition"  : (4, None, tagDataskp, 'ignition', None), # 
                    #"ignition"  : (24, None, tagDataskp, 'ignition', None), # 
                    "codEvent"  : (0, None, tagDataskp, 'codEvent', convert.gv_get_event_code),
                    "weeks"     : (4, None, tagDataskp, 'weeks', None), # Es el numero de semanas desde 00:00AM del 6 de enero de 1980.
                    "dayWeek"   : (4, None, tagDataskp, 'dayWeek', None), # 0=Domingo, 1=Lunes, etc hasta 6=sabado.
                    "lat"       : (12, None, tagDataskp, 'lat', None), # Latitud
                    "lng"       : (11, None, tagDataskp, 'lng', None), # Longitud
                    "speed"     : (8, None, tagDataskp, 'speed', None),   # Velocidad en MPH
                    "course"    : (9, None, tagDataskp, 'course', None), # azumuth
                    "gpsSource" : (4, None, tagDataskp, 'gpsSource', None), # Fuente GPS. Puede ser 0=2D GPS, 1=3D GPS, 2=2D DGPS, 3=3D DGPS, 6=DR, 8=Degraded DR. # Problema DB si no son enteros    
                    "ageData"   : (4, None, tagDataskp, 'ageData', None), # Edad del dato. Puede ser 0=No disponible, 1=viejo (10 segundos) ó 2=Fresco (menor a 10 segundos) # Problema DB si no son enteros
                    "date"      : (13, None, tagDataskp, 'date', convert.gv_date), # Fecha 
                    "time"      : (13, None, tagDataskp, 'time', convert.gv_time), # Hora expresada en segundos desde 00:00:00AM
                    "odometer"  : (19, None, tagDataskp, 'odometer', None) # Odómetro
                }
    # Event Report: +RESP:GTIGN, +RESP:GTIGF
    # [22]: ['+RESP:GTIGN', '2F0500', '862193026878108', 'GV001', '', '9274', '0', '0.0', '0', '2139.0', '-75.459166', '5.038386', '20170406170427', '', '', '', '', '', '', '0.7', '', '0EC3$']
    #       [            0,        1,                 2,       3, 4 ,      5,   6,     7,   8,        9,           10,         11,               12, 13, 14, 15, 16, 17, 18,    19, 20,      21]
    tag_event_report = {
    #               "key"       : (position_start, position_end, function_tagData, nameTag, function_convert)
                    "id"        : (3, None, tagDataskp, 'id', None), # ID de la unidad
                    "type"      : (4, None, tagDataskp, 'type', None),
                    "typeEvent" : (4, None, tagDataskp, 'typeEvent', None), # 
                    "altura"    : (9, None, tagDataskp, 'altura', None),
                    "ignition"  : (4, None, tagDataskp, 'ignition', None), #altered for "ignition state" more below 
                    "codEvent"  : (0, None, tagDataskp, 'codEvent', convert.gv_get_event_code),
                    "weeks"     : (4, None, tagDataskp, 'weeks', None), 
                    "dayWeek"   : (4, None, tagDataskp, 'dayWeek', None),
                    "lat"       : (11, None, tagDataskp, 'lat', None), # Latitud
                    "lng"       : (10, None, tagDataskp, 'lng', None), #Longitud
                    "speed"     : (7, None, tagDataskp, 'speed', None), #velocidad en KM
                    "course"    : (8, None, tagDataskp, 'course', None), # azumuth
                    "gpsSource" : (4, None, tagDataskp, 'gpsSource', None), 
                    "ageData"   : (4, None, tagDataskp, 'ageData', None), 
                    "date"      : (12, None, tagDataskp, 'date', convert.gv_date), #Date 
                    "time"      : (12, None, tagDataskp, 'time', convert.gv_time), #Time
                    "odometer"  : (19, None, tagDataskp, 'odometer', None) # Odómetro
            }
    # Event Report: +RESP:GTMPN:, +RESP:GTMPF:, +RESP:GTBTC:, +RESP:GTCRA:
    # [19]: ['+RESP:GTMPF', '2F0500', '862193026878108', 'GV001', '', '0', '0.0', '0', '2139.3', '-75.459194', '5.038412', '20170406210524', '', '', '', '', '', '', '1050$']
    #       [            0,        1,                 2,       3, 4 ,   5,     6,   7,        8,            9,         10,               11, 12, 13, 14, 15, 16, 17,     18,]
    tag_event_bub_crash = {
    #               "key"       : (position_start, position_end, function_tagData, nameTag, function_convert)
                    "id"        : (3, None, tagDataskp, 'id', None), # ID de la unidad
                    "type"      : (4, None, tagDataskp, 'type', None),
                    "typeEvent" : (4, None, tagDataskp, 'typeEvent', None), # 
                    "altura"    : (8, None, tagDataskp, 'altura', None),
                    "ignition"  : (4, None, tagDataskp, 'ignition', None), #altered for "ignition state" more below 
                    "codEvent"  : (0, None, tagDataskp, 'codEvent', convert.gv_get_event_code),
                    "weeks"     : (4, None, tagDataskp, 'weeks', None), 
                    "dayWeek"   : (4, None, tagDataskp, 'dayWeek', None),
                    "lat"       : (10, None, tagDataskp, 'lat', None), # Latitud
                    "lng"       : (9, None, tagDataskp, 'lng', None), #Longitud
                    "speed"     : (6, None, tagDataskp, 'speed', None), #velocidad en KM
                    "course"    : (7, None, tagDataskp, 'course', None), # azumuth
                    "gpsSource" : (4, None, tagDataskp, 'gpsSource', None), 
                    "ageData"   : (4, None, tagDataskp, 'ageData', None), 
                    "date"      : (11, None, tagDataskp, 'date', convert.gv_date), #Date 
                    "time"      : (11, None, tagDataskp, 'time', convert.gv_time), #Time
                    "odometer"  : (4, None, tagDataskp, 'odometer', None) # Odómetro
            }


    def __parse(self, data):
        self.clear()
        stack = self.tagDataGV

        try:
            dataList = data.split(',') # Crear para los datos que son necesarios.
            if dataList[4]:
                dataList.insert(4, '')
            #print "dataList[%s]: %s" % (len(dataList), dataList) #(Print de Prueba)
            #raise SystemExit(1)
            #select type of 'stack'
            #if dataList[0] == '+RESP:GTIGN' or dataList[0] == '+RESP:GTIGF':
            if ('GTIGN' in dataList[0]) or ('GTIGF' in dataList[0]):
                stack = self.tag_event_report
            elif ('GTMPN' in dataList[0]) or ('GTMPF' in dataList[0]):
                stack = self.tag_event_bub_crash
            #else: stack = self.tagDataGV
            #print "-" * 20
            #print self

            # ignition state
            #if len(dataList) < 23:
            #    stack['ignition'] = (4, None, tagDataskp, 'ignition', None)

            for tag, (position_start, position_end, parseFunc,nameTag,convertFunc) in stack.items():
                self[tag] = convertFunc and convertFunc(parseFunc(dataList, position_start, position_end, nameTag)) or parseFunc(dataList, position_start, position_end, nameTag)
            #print "-" * 20
            #print self
            #device ignition output status
            if len(dataList) > 29:
                self["ignition"] = convert.gv_device_status(dataList[24], tag="ignition")
            # Creamos una key para el dato position:
            self['position'] = "(%(lat)s,%(lng)s)" % self
            # Fecha y Hora del dispositivo:
            self["datetime"] = fechaHoraSkp(self["date"], self["time"])
            # Nominatim:
            self["geocoding"] = None
            self["geocoding"] = Location.nominatim.Openstreetmap(self["lat"], self["lng"]).decodeJSON()
            #print "-" * 20
            #print self
            #raise SystemExit
        except Exception: print(sys.exc_info()) #sys.stderr.write('Error Inesperado:', sys.exc_info())

    def __setitem__(self, key, item):
        if key == "data" and item:
            self.__parse(item)
        # Llamamos a __setitem__ de nuestro ancestro
        Device.__setitem__(self, key, item)


class imeiDevice(Device):
    """
        Dispositivo TK303F
    """
    # ['imei', '864180038790106', 'tracker', '191120155455', '', 'F', '205455.00', 'A', '0502.30489', 'N', '07527.55108', 'W', '0.000', '0', '']
    # [     0,                 1,         2,              3,  4,   5,           6,   7,            8,   9,            10,  11,      12,  13, 14]
    ## protocol 18:
    # ['imei', '868166052272770', 'tracker', '230721155900', '', 'F', '155900.000', 'A', '0502.30245', 'N', '07527.54983', 'W', '0.00', '348.94', '', '1', '0', '0.00%', '', '']
    # [     0,                 1,         2,              3,  4,   5,            6,   7,            8,   9,            10,  11,     12,       13, 14,  15,  16,      17, 18, 19]
    tagDataTK = {
    #               "key"       : (position_start, position_end, function_tagData, nameTag, function_convert)
                    "id"        : (1, None, tagDataskp, 'id', None), # ID de la unidad
    #                "type"      : (0, None, tagDataskp, 'type', None),
    #                "typeEvent" : (0, None, tagDataskp, 'typeEvent', None), # 

    #                "ignition"  : (15, None, tagDataskp, 'ignition', None), # REVISAR para agregar en la trama 

                    "codEvent"  : (2, None, tagDataskp, 'codEvent', code_event), # Codigo de evento activado (en Antares de 00 a 49, en e.Track de 00 a 99)
    #                "weeks"     : (0, None, tagDataskp, 'weeks', None), # Es el numero de semanas desde 00:00AM del 6 de enero de 1980.
    #                "dayWeek"   : (0, None, tagDataskp, 'dayWeek', None), # 0=Domingo, 1=Lunes, etc hasta 6=sabado.
    #                "time"      : (5, None, tagDataskp, 'time', skpTime), # Hora expresada en segundos desde 00:00:00AM
                    "lat"       : (8, 9, tagDataskp, 'lat', degTodms), # Latitud
                    "lng"       : (10, 11, tagDataskp, 'lng', degTodms), # Longitud

                    "speed"     : (12, None, tagDataskp, 'speed', tk_speed), # REVISAR que si concuerde
                    "course"    : (13, None, tagDataskp, 'course', None), # Curso en grados - REVISAR
    #                "altura"    : (14, None, tagDataskp, 'altura', None), # REVISAR para agregar en la trama

    #                "gpsSource" : (0, None, tagDataskp, 'gpsSource', None), # Fuente GPS. Puede ser 0=2D GPS, 1=3D GPS, 2=2D DGPS, 3=3D DGPS, 6=DR, 8=Degraded DR. # Problema DB si no son enteros    
    #                "ageData"   : (0, None, tagDataskp, 'ageData', None), # Edad del dato. Puede ser 0=No disponible, 1=viejo (10 segundos) ó 2=Fresco (menor a 10 segundos) # Problema DB si no son enteros
    #                "date"  : (13, None, tagDataskp, 'date', skpDate), # Fecha 
                    "date"  : (3, None, tagDataskp, 'date', tk_date), # datetime
                    "time"  : (6, None, tagDataskp, 'time', tk_time), # zero_time_zone
    #                "odometer"  : (15, None, tagDataskp, 'odometer', mTokm) # Odómetro
                 }

    def __parse(self, data):
        self.clear()
        try:
            import re
            
            data = re.sub(r"[:;]", ",", data)
            dataList = data.split(',')[:-1]
            #print dataList #(Print de Prueba)

            for tag, (position_start, position_end, parseFunc, nameTag, convertFunc) in self.tagDataTK.items():
                self[tag] = convertFunc and convertFunc(parseFunc(dataList, position_start, position_end, nameTag)) or parseFunc(dataList, position_start, position_end, nameTag)

            # Creamos una key para la altura (estandar), ya que las tramas actuales no la incluyen:
            #self['altura'] = None
            # Creamos una key para el dato position:
            self['position'] = "(%(lat)s,%(lng)s)" % self
            self['altura'] = None
            self['gpsSource'] = None
            self['ageData'] = None
            self['odometer'] = None
            if len(dataList) > 14:
                #print "ING: ", dataList[15]
                #ign = int(dataList[15])
                self['ignition'] = 't' if int(dataList[15]) == 1 else 'f'
                #print "IGN:", self['ignition']

            # Fecha y Hora del dispositivo:
            #self["fechahora"] = fechaHoraSkp(self["date"], self["time"]) 
            self["datetime"] = fechaHoraSkp(self["date"], self["time"])
            #self['datetime'] = tk_datetime(self['date'], self['time']) 
            # Realizamos la Geocodificación. Tratar de no hacer esto
            # es mejor que se realize por cada cliente con la API de GoogleMap
            self["geocoding"] = None
            #self["geocoding"] = json.loads(Location.geomapgoogle.regeocode('%s,%s' % (self["lat"], self["lng"])))[0]
            #self["geocoding"] = Location.geocoding.regeocodeOSM('%s,%s' % (self["lat"], self["lng"])) # Dejo de funcionar el 16-09-2015
            #self["geocoding"] = Location.geocoding.regeocodeGMap('%s,%s' % (self["lat"], self["lng"])) # Dejo de funcionar el 17-09-2015
            # Nominatim:
            #self["geocoding"] = Location.nominatim.Openstreetmap((self["lat"], self["lng"]))
            self["geocoding"] = Location.nominatim.Openstreetmap(self["lat"], self["lng"]).decodeJSON()
            #print "-" * 20
            #print self
            #raise SystemExit
        except Exception: print(sys.exc_info()) #sys.stderr.write('Error Inesperado:', sys.exc_info())
        #finally: dataFile.close()

    def __setitem__(self, key, item):
        if key == "data" and item:
            self.__parse(item)
        # Llamamos a __setitem__ de nuestro ancestro
        Device.__setitem__(self, key, item)


def typeDevice(data):
    """
        Determina que tipo de Dispositivo GPS es dueña de la data.

        Usage:
            >>> import devices
            >>> 
            >>> data='>REV041674684322+0481126-0757378200000012;ID=ANT001<'
            >>> devices.typeDevice(data)
            'ANT'
            >>>
            >>> type(devices.typeDevice(''))
            <type 'NoneType'>
            >>>
            >>> if devices.typeDevice('') is not None: print "Seguir con el programa..."
            ... 
            >>> if devices.typeDevice(data) is not None: print "Seguir con el programa..."
            ... 
            Seguir con el programa...
            >>> 
    """
    # Dispositivos soportados:
    types = ('ANT', 'SKP', 'TT', 'GV', 'imei')

    typeDev = lambda dat: ("".join(
                            [d for d in types
                            if dat.find(d) is not -1])
                        )
    return typeDev(data) or None #raise

#
def getTypeClass(data, address=None, module=sys.modules[Device.__module__]):
    """
        Determina que clase debe manejar un determinado dispositivo y
        retorna un diccionario con la trama procesada.

        Recibe la data enviada por el dispositivo (data), y opcionalmente
        el nombre del módulo donde se encuentra la clase que manipula este
        tipo de dispositivo (module). La clase manejador debe tener un
        formato compuesto por 'TIPO_DISPOSITIVO + Device' por ejemplo: ANTDevice,
        SKPDevice, etc.

        Usage:
            >>> import devices
            >>> 
            >>> data='>REV001447147509+2578250-0802813901519512;ID=ANT001<'
            >>> devices.getTypeClass(data)
            {'codEvent': '00', 'weeks': '1447', 'dayWeek': '1', 'ageData': '2', \
            'type': 'R', 'data': '>REV001447147509+2578250-0802813901519512;ID=ANT001<', \
            'course': '195', 'gpsSource': '1', 'time': '47509', 'lat': '+2578250', \
            'typeEvent': 'EV', 'lng': '-08028139', 'speed': '015', 'id': 'ANT001'}
            >>> print "\n".join(["%s=%s" % (key,value) for key, value in devices.getTypeClass(data).items()])
            codEvent=00
            weeks=1447
            dayWeek=1
            ageData=2
            type=R
            data=>REV001447147509+2578250-0802813901519512;ID=ANT001<
            course=195
            gpsSource=1
            time=47509
            lat=+2578250
            typeEvent=EV
            lng=-08028139
            speed=015
            id=ANT001
            >>> 
    """
    import re

    #data = data.replace('\n','')
    #data = data.strip('\n')
    data = re.sub(r"[\r\n]+", "", data)

    # Determinamos la clase manejadora adecuado según el dispositivo
    dev = "%sDevice" % typeDevice(data)
    #print "-"*80
    #print "Devices: ", dev
    #print "-"*80
    #raise SystemExit(0)

    #return dev
    def getClass(module, dev):
        """
            Retorna una referencia a la clase manejadora.
            Usage:
            >>> getClass(module, 'ANTDevice')
            <class devices.ANTDevice at 0xb740435c>
            >>> getClass(module, 'SKPDevice')
            <class devices.SKPDevice at 0xb740438c>
            >>> getClass(module, '')
            <class devices.Device at 0xb740426c>
            >>> 
        """
        return hasattr(module, dev) and getattr(module, dev) or Device

    return getClass(module, dev)(data, address)

