# -*- coding: utf-8 -*-
"""
    Autor: Jorge A. Toro
"""
import sys
from DB.pgSQL import PgSQL

def insertLog(data=None):
    """
        Query, que inserta la data en la tabla de Log

        >>> import Log.logDB
        >>> import datetime
        >>> # Si el ANT051 esta registrado en la tabla gps
        >>> data = {'codEvent': '05', 'weeks': '1693', 'dayWeek': '4', 'ageData': '2', 'position': '(4.81534,-75.69489)', 'type': 'R', 'address': ('127.0.0.1', 54436), \
        ... 'geocoding': u'RUEDA MILLONARIA PEREIRA, Calle 18 # CARRERA 7, Pereira, Colombia', 'data': '>REV051693476454+0481534-0756948900102632;ID=ANT051<', 'course': '026', \
        ... 'gpsSource': '3', 'time': '76454', 'lat': '4.81534', 'typeEvent': 'EV', 'lng': '-75.69489', 'datetime': datetime.datetime(2012, 7, 16, 18, 34, 38, 833105), 'speed': 1.0, 'id': 'ANT051'}
        >>> Log.logDB.insertLog(data)
        procpid: 6390
        Actualizando y Cerranda la conexión
        'INSERT 0 1'
        >>>
        >>> # Si el ANT050 no esta registrado en la tabla gps
        >>> data = {'codEvent': '05', 'weeks': '1693', 'dayWeek': '4', 'ageData': '2', 'position': '(4.81534,-75.69489)', 'type': 'R', 'address': ('127.0.0.1', 54436), \
        ... 'geocoding': u'RUEDA MILLONARIA PEREIRA, Calle 18 # CARRERA 7, Pereira, Colombia', 'data': '>REV051693476454+0481534-0756948900102632;ID=ANT051<', 'course': '026', \
        ... 'gpsSource': '3', 'time': '76454', 'lat': '4.81534', 'typeEvent': 'EV', 'lng': '-75.69489', 'datetime': datetime.datetime(2012, 7, 16, 18, 34, 38, 833105), 'speed': 1.0, 'id': 'ANT050'}
        >>> Log.logDB.insertLog(data)
        procpid: 6437
        Actualizando y Cerranda la conexión
        'INSERT 0 0'
        >>> 

    """
    query = """INSERT INTO log_gps (name, address, evento, fecha, posicion, ubicacion, grados, altura, satelites, estado_data, trama)
               VALUES (%(id)s, %(address)s,
                       %(codEvent)s, %(datetime)s,
                       %(position)s, %(geocoding)s,
                       %(course)s, %(altura)s, %(gpsSource)s,
                       %(ageData)s, %(data)s)
            """
    db = PgSQL()
    return db.exe(query, data)

