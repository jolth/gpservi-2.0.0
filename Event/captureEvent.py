# -*- coding: UTF-8 -*-
"""
    Módulo que permite gestionar los distintos eventos enviados por
    los dispositivos GPS.

    Autor   : Jorge A. Toro
    email   : jolthgs@gmail.com, jolth@esdebian.org
    date    : vie jul 20 07:49:38 COT 2012
    version : 1.0.0

    Usage:
        >>> import datetime
        >>> import Event.captureEvent
        >>>
        >>>data = {'codEvent': '06', 'weeks': '1693', 'dayWeek': '4', 'ageData': '2', 'position': '(4.81534,-75.69489)', \
        'type': 'R', 'address': '127.0.0.1,45840', 'geocoding': u'RUEDA MILLONARIA PEREIRA, Calle 18 # CARRERA 7, Pereira, Colombia',\ 
        'data': '>REV061693476454+0481534-0756948900102632;ID=ANT051<', 'course': '026', 'gpsSource': '3', 'time': '76454', 'lat': '4.81534', \
        'typeEvent': 'EV', 'lng': '-75.69489', 'datetime': datetime.datetime(2012, 7, 23, 7, 31, 26, 608343), 'speed': 1.0, 'id': 'ANT051', 'altura': None}
        >>> 
        >>> event = Event.captureEvent.parseEvent(data)
        INSERT: event6
        Insert Positions_gps
        procpid: 3729
        RETURN: 88 5
        Insert Eventos
        Actualizando y Cerrando la conexión
        >>> 
        >>> event
        'Start'
        >>> 

"""
import sys
import traceback


def insertEvent(evento):
    def insert(data):
        """
            Llama la función PL/pgSQL.
        """
        from DB.pgSQL import PgSQL
        #print "\nINSERT:", evento.__name__#(Print de Prueba)
        ###### SQL:
        # Insert Positions:
        queryPositions = """SELECT fn_save_event_position_gps(%(id)s, %(position)s, %(geocoding)s,
                         %(speed)s, %(altura)s, %(course)s, %(gpsSource)s,
                         %(address)s, %(datetime)s, %(odometer)s);"""
        # Insert Eventos:
        queryEventos = """INSERT INTO eventos(gps_id, positions_gps_id, type, fecha)
                          VALUES (%(gps_id)s, %(positions_id)s, %(codEvent)s, %(datetime)s);"""

        try:
            #print "Insert Positions_gps"#(Print de Prueba) # Print de prueba
            db = PgSQL()
            db.cur.execute(queryPositions, data) # INSERT positions_gps

            #if evento.__name__ == "event5": return evento(data) # Terminamos la ejecucion Llamando a event5
            try:
                # Si no se realiza la inserción no retorna nada.
                data['positions_id'], data['gps_id'] = eval(db.cur.fetchone()[0]) # No exite en gps retorna (None,). Si active=f retorna ('(,)',). 
                                                                                  # Para lo cual sucede una excepción y se termina la ejecución. 
            except:
                #print "Se termina de Gestionar el Evento", evento.__name__#(Print de Prueba)
                return # Se termina la ejecución. 
            #print "RETURN:", data['positions_id'], data['gps_id'] #(Print de Prueba)# print de prueba 
            # Esto para que no guarde el event5 en la tabla eventos:
            if evento.__name__ == "event5": return evento(data) # Terminamos la ejecucion Llamando a event5

            # Insert Eventos:
            #print "Insert Eventos" #(Print de Prueba)# Print de prueba
            db.cur.execute(queryEventos, data) # INSERT eventos

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print >> sys.stderr, '-'*60
            print >> sys.stderr, "*** print exception <<insertEvent>>:"
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                               limit=2, file=sys.stderr)
            print >> sys.stderr, '-'*60
            return
        finally:
            print >> sys.stderr, "Actualizando y Cerrando la conexión"#(Print de Prueba)
            # Realizamos los cambios en la DB
            db.conn.commit()
            # Cerramos la comunicación
            db.cur.close()
            db.conn.close()
        return evento(data)
    return insert


def insertReport(): pass

# Funciones Manejadoras de Eventos:
@insertEvent
def event1(data=None):
    """
        >>> from DB.pgSQL import PgSQL
        >>> db = PgSQL()
        procpid: 3945
        >>> query = ""SELECT c.id AS cliente_id, v.placa, c.nombre1, c.nombre2, c.apellido1, c.apellido2,
                     ... p.phone, tp.name
                     ... FROM vehiculos v
                     ... JOIN gps AS g ON (g.id=v.gps_id)
                     ... JOIN clientes_vehiculos AS cv ON (cv.vehiculo_id=v.id)
                     ... JOIN clientes AS c ON (c.id=cv.cliente_id)
                     ... JOIN phones_all AS pa ON (pa.client_id=c.id)
                     ... JOIN phones AS p ON (p.id=pa.phone_id)
                     ... JOIN type_phone AS tp ON (tp.id=p.type)
                     ... WHERE g.name = %(id)s;""
         >>> db.cur.execute(query, data)
         >>> db.cur.fetchall()
         [(1, 'rjm270', 'jorge', 'alonso', 'toro', 'hoyos', '3202433506', 'celular')]
         >>> 

    """
    #print "ID VEHICULO:", data['id']#(Print de Prueba)
    #print >> sys.stdout, "ID Vehiculo" + data['id']#(Print de Prueba)

    query = """SELECT c.id AS cliente_id, v.placa, p.phone, tp.name,
    c.nombre1, c.nombre2, c.apellido1, c.apellido2
    FROM vehiculos v
    JOIN gps AS g ON (g.id=v.gps_id)
    JOIN clientes_vehiculos AS cv ON (cv.vehiculo_id=v.id)
    JOIN clientes AS c ON (c.id=cv.cliente_id)
    JOIN phones_all AS pa ON (pa.client_id=c.id)
    JOIN phones AS p ON (p.id=pa.phone_id)
    JOIN type_phone AS tp ON (tp.id=p.type)
    WHERE g.name = %(id)s;"""

    try:
        from DB.pgSQL import PgSQL
        db = PgSQL()
        db.cur.execute(query, data)
        msg = u"Evento de PANICO\n"
        for i in db.cur.fetchall():
            # [(1, 'rjm270', 'jorge', 'alonso', 'toro', 'hoyos', '3202433506', 'celular')]
            veh, tel, tipo = (i[1].upper(), i[2], i[3])
            #print >> sys.stderr, "EL VEHICULO: " + veh
            #print >> sys.stdout, "EL VEHICULO: " + veh
            #print >> sys.stderr, "EL TEL: " + tel
            #print >> sys.stdout, "EL TEL: " + tel
            #print >> sys.stderr, "EL TIPO: " + tipo
            #print >> sys.stdout, "EL TIPO: " + tipo
            #nom = i[2].capitalize()+' '+i[3].capitalize()+' '+i[4].capitalize()+' '+i[5].capitalize()
            nom = i[4].capitalize()+' '+(i[5] and i[5].capitalize() or '')+' '+(i[6] and i[6].capitalize() or '')+' '+(i[7] and i[7].capitalize() or '')
            #nom = nom.encode('utf-8')
            nom = unicode(nom, 'utf-8')
            #print >> sys.stderr, "EL NOMEBRE: " + nom
            msg += u"""
            Vehiculo: %s
            Cliente: %s
            %s: %s
            """ % (veh, nom, tipo, tel)
        msg += u"""
        Fecha: %s
        """ % (data['datetime'].strftime("%F %H:%M:%S"))
        msg += u"""
        Ubicación: %(geocoding)s

        <http://maps.google.com/maps?q=%(lat)s,%(lng)s>

        """ % data

        #import SMail
        from SMail import smail
        # sender
        #sender = 'rastree@devmicrosystem.com'
        # receptores del mensaje
        #receivers = {'Soporte':'soporte@devmicrosystem.com', 'Diana Duque':'diana.duque@devmicrosystem.com', 'Demouser':'demouser@rastree.com'}
        receivers = {'Eventos': 'eventos'}
        #print "MENSAJE:", msg
        subject = u"Mensaje de Panicon(%s) Vehículo %s" % (data['id'], veh)
        #print "SUBJECT", subject
        #SMail.smail.sendMail(receivers, subject, msg)
        msg = msg.encode('utf-8')
        smail.sendMail(receivers, subject, msg)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print >> sys.stderr, '-'*60
        print >> sys.stderr, "*** print exception <<query_select_panic>>:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                           limit=2, file=sys.stderr)
        print >> sys.stderr, '-'*60
    finally:
        print >> sys.stderr, "Actualizando y Cerrando la conexión"
        # Realizamos los cambios en la DB
        db.conn.commit()
        # Cerramos la comunicación
        db.cur.close()
        db.conn.close()

    return "Panic" # Retornamos una cadena con el tipo de Evento 

@insertEvent
def event2(data=None): return "Speeding"
@insertEvent
def event5(data=None):
    #queryIgnition = """INSERT INTO vehicle_state()"""
    queryIgnition = """SELECT fn_insert_ingnition_state(%(gps_id)s,  %(ignition)s, NULL, NULL, NULL, %(datetime)s);"""
    try:
        from DB.pgSQL import PgSQL
        db = PgSQL()
        db.cur.execute(queryIgnition, data)
        #print "Se guarda el estado de ignition"#(Print de Prueba) # Print de prueba
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print >> sys.stderr, '-'*60
        print >> sys.stderr, "*** print exception <<insertEventReport>>:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                           limit=2, file=sys.stderr)
        print >> sys.stderr, '-'*60
        return "No se guarda el Report"
    finally:
        print >> sys.stderr, "Actualizando y Cerrando la conexión"
        # Realizamos los cambios en la DB
        db.conn.commit()
        # Cerramos la comunicación
        db.cur.close()
        db.conn.close()
    return "Report"

@insertEvent
def event6(data=None):
    # Insert vehicle_state:
    #queryVehiState = """SELECT fn_ingresar_vehicle_state(%(gps_id)s,  't', NULL, NULL, NULL);"""
    queryVehiState = """SELECT fn_ingresar_vehicle_state(%(gps_id)s,  't', NULL, NULL, NULL, %(datetime)s);"""
    try:
        from DB.pgSQL import PgSQL
        db = PgSQL()
        db.cur.execute(queryVehiState, data)
        #print "Se guardan los estados del vehiculo"#(Print de Prueba) # Print de prueba
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print >> sys.stderr, '-'*60
        print >> sys.stderr, "*** print exception <<insertEventStart>>:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                           limit=2, file=sys.stderr)
        print >> sys.stderr, '-'*60
        return "No se guarda el Start"
    finally:
        print >> sys.stderr, "Actualizando y Cerrando la conexión"
        # Realizamos los cambios en la DB
        db.conn.commit()
        # Cerramos la comunicación
        db.cur.close()
        db.conn.close()
    return "Start"

@insertEvent
def event7(data=None):
    # Insert vehicle_state:
    #queryVehiState = """SELECT fn_ingresar_vehicle_state(%(gps_id)s,  'f', NULL, NULL, NULL);"""
    queryVehiState = """SELECT fn_ingresar_vehicle_state(%(gps_id)s,  'f', NULL, NULL, NULL, %(datetime)s);"""
    try:
        from DB.pgSQL import PgSQL
        db = PgSQL()
        db.cur.execute(queryVehiState, data)
        #print "Se guardan los estados del vehiculo"#(Print de Prueba) # Print de prueba
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print >> sys.stderr, '-'*60
        print >> sys.stderr, "*** print exception <<insertEventShutdown>>:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                           limit=2, file=sys.stderr)
        print >> sys.stderr, '-'*60
        return "No se guarda el Start"
    finally:
        print >> sys.stderr, "Actualizando y Cerrando la conexión"
        # Realizamos los cambios en la DB
        db.conn.commit()
        # Cerramos la comunicación
        db.cur.close()
        db.conn.close()

    return "Shutdown"

@insertEvent
def event8(data=None): return "Bateri on"
@insertEvent
def event9(data=None): return "Bateri off"

def parseEvent(data=None):
    """
        Analiza y determina que hacer con cada uno de los eventos.
        Llama a getTypeEvent
    """
    # Si es llamable, se llama a la función manajadora. si no, se retorna None 
    # y no se ejecuta ninguna secuancia para el dato ingresado.
    #return callable(getTypeEvent(data)) and getTypeEvent(data)(data) # Retorna False 
    return (callable(getTypeEvent(data)) or None) and getTypeEvent(data)(data) # Retorna None.


def getTypeEvent(data=None, module=sys.modules[parseEvent.__module__]):
    """
        >>> import captureEvent
        >>> import datetime
        >>>data = {'codEvent': '05', 'weeks': '1693', 'dayWeek': '4', 'ageData': '2', \
        'position': '(4.81534,-75.69489)', 'type': 'R', 'address': '127.0.0.1,50637', \ 
        'geocoding': u'RUEDA MILLONARIA PEREIRA, Calle 18 # CARRERA 7, Pereira, Colombia', \
        'data': '>REV051693476454+0481534-0756948900102632;ID=ANT051<', 'course': '026', \
        'gpsSource': '3', 'time': '76454', 'lat': '4.81534', 'typeEvent': 'EV', 'lng': '-75.69489', \
        'datetime': datetime.datetime(2012, 7, 20, 8, 50, 9, 154217), 'speed': 1.0, 'id': 'ANT051', 'altura': None}
        >>> captureEvent.getTypeEvent(data)
        <function event5 at 0xb7395844>
        >>> 
    """
    try:
        # Nombre de la Función Manejadora:
        event = "event%s" % int(data['codEvent'])
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print >> sys.stderr, '-'*60
        print >> sys.stderr, "*** print exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stderr)
        print >> sys.stderr, '-'*60
        return # None

    # Retorna la función Manejadora:
    return hasattr(module, event) and getattr(module, event) or None


