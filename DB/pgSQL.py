# -*- coding: utf-8 -*-
"""
    Módulo que provee una interfaz de conexión más intuitiva y con
    la capacidad de resolver errores en tiempo de ejecución.

    Autor: Jorge A. Toro [jolthgs@gmail.com]
"""
import sys
import traceback
import psycopg2 as pgsql



def connection(args=None): 
    """ 
        args, puede ser una cadena con todos los datos para conectarse a la base de datos o 
        simplemente enviarse sin datos, para lo cual tomara la configuración por defecto 
        almacenada en el fichero de configuración "config.cfg" (en la sección [DATABASE]).
        así:

        
        Usage:
        >>> from DB.pgSQL import connection

        >>> connection("dbname='test010' user='postgres' host='localhost' password='qwerty'") # Con argumentos
        >>> connection() # Sin argumento
        <connection object at 0xb715a72c; dsn: 'dbname='test009' user='postgres' host='localhost' password=xxxxxxxx', closed: 0>
        >>> conn = connection()
        >>> cursor = conn.cursor()
        >>> cursor.execute("select * from gps")
        >>> print cursor.fetchall()
        [(11, 'GPS0003', 2, False, datetime.datetime(2012, 7, 13, 8, 11, 31, 945952, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=1140, name=None))), ...]
        >>>

    """
    if args is None:
        from Load.loadconfig import load

        args = {}
        
        args['dbname'] = load('DATABASE', 'DBNAME')
        args['user'] = load('DATABASE', 'USER')
        args['host'] = load('DATABASE', 'HOST')
        args['password'] = load('DATABASE', 'PASSWORD')

        args = " ".join(["%s=\'%s\'" % (k, v) for k, v in args.items()])

    # Conexión a la base de datos: 
    try:
        conn = pgsql.connect(args)
    except pgsql.OperationalError, e:
        print >> sys.stderr, "\nNo se pudo poner en marcha la base de datos.\n"
        print >> sys.stderr, e
        print >> sys.stdout, 'Error: Revisar el archivo de error.log'
        sys.exit(1)

    # Retornamos la conexión
    return conn

        
class PgSQL(object):
    """ 
        Crea un obejto conexión para la base de datos especificada.

        Recibe los mismos datos que la función connection(args=None). Por lo tanto, si se quiere usar la 
        conexión a la base de datos por defecto se debe llamar a PgSQL() sin argumentos, asi:
        >>> conn = pgSQL.PgSQL()

        Usage:
            >>> import pgSQL
            >>> db = pgSQL.PgSQL("dbname='test009' user='postgres' host='localhost' password='qwerty'")
            >>> db
            <pgSQL.PgSQL object at 0xb740e5ec>
            >>> db.conn
            <connection object at 0xb718a72c; dsn: 'dbname='test009' user='postgres' host='localhost' password=xxxxxxxx', closed: 0>
            >>> dir(db.conn)
            ['DataError', 'DatabaseError', 'Error', 'IntegrityError', 'InterfaceError', 'InternalError', 'NotSupportedError', \
            'OperationalError', 'ProgrammingError', 'Warning', '__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', \
            '__hash__', '__init__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', \
            '__subclasshook__', 'async', 'binary_types', 'close', 'closed', 'commit', 'cursor', 'dsn', 'encoding', 'fileno', 'get_backend_pid', \
            'get_parameter_status', 'get_transaction_status', 'isexecuting', 'isolation_level', 'lobject', 'notices', 'notifies', 'poll', \
            'protocol_version', 'reset', 'rollback', 'server_version', 'set_client_encoding', 'set_isolation_level', 'status', 'string_types']
            >>>
            >>> db.cur
            <cursor object at 0x83916bc; closed: 0>
            >>> 

    """
    def __init__(self, args=None):
        if args is not None: self.conn = connection(args)  
        else: self.conn = connection()  
              
        self.status = self.conn.status # Status
        self.procpid = self.conn.get_backend_pid() # Get backend process id.

        self.cur = self.conn.cursor() # Return a new cursor.

        #print "procpid:", self.procpid#(Print de Prueba) # process id (Print de Prueba)


    def exe(self, query, data=None):
        """
            query, debe ser una cadena que contenga la Query SQL, así:
            "SELECT * FROM gps"

            data, debe ser una tupla o diccionario que cotenga los datos a 
            pasar a la Query, así:
            "INSERT INTO test (num, data) VALUES (%s, %s)", (42, 'bar')

            usage:
            >>> import pgSQL

            >>> db = pgSQL.PgSQL("dbname='test009' user='postgres' host='localhost' password='qwerty'")
            >>> db.exe("SELECT * FROM gps")
            >>> db.cur.fetchall()
            [(11, 'GPS0003', 2, False, datetime.datetime(2012, 6, 10, 8, 11, 31, 945952, \
            tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=1140, name=None))), (14, 'ANT051', \
            1, False, datetime.datetime(2012, 7, 13, 9, 5, 42, 747214, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=1140, name=None)))]
            >>> 

            >>> db = pgSQL.PgSQL("dbname='test009' user='postgres' host='localhost' password='qwerty'")
            >>> db.exe("SELECT * FROM gps WHERE id=14")
            >>> db.cur.fetchone()
            (14, 'ANT051', 1, False, datetime.datetime(2012, 7, 13, 9, 5, 42, 747214, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=1140, name=None)))
            >>> 
            >>> db.cur.fetchall()
            [(14, 'ANT051', 1, False, datetime.datetime(2012, 7, 13, 9, 5, 42, 747214, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=1140, name=None)))]
            >>> 
            
            >>> db = pgSQL.PgSQL("dbname='test009' user='postgres' host='localhost' password='qwerty'")
            >>> db.exe("INSERT INTO gps (name, type) VALUES (%s, %s)", ('GPS0004', 2))
            'INSERT 0 1'
            >>>

            # Si no, existen datos en una consoulta se puede manajar así:
            >>> db = pgSQL.PgSQL("dbname='test009' user='postgres' host='localhost' password='qwerty'")
            >>> r = db.exe("SELECT * FROM gps WHERE id=10")
            Actualizando y Cerranda la conexión
            >>> if r is not None: print "Record: ", r
            ... else: "No existen datos"
            ... 
            'No existen datos'
            >>>
        """
        record = None

        if data is not None:
            try:
                self.cur.execute(query, data)
                return self.cur.statusmessage # Deberia retornar 1, si el insert se realizo 
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print >> sys.stderr, traceback.format_exc(exc_type)
                #return self.conn.status
                return self.conn.get_transaction_status() # Deberia retornar 0, si el insert no se realizo 
            finally: 
                print >> sys.stderr, "Actualizando y Cerranda la conexión"
                # Realizamos los cambios en la DB
                self.conn.commit()
                # Cerramos la comunicación
                self.cur.close()
                self.conn.close()
                
        else:
            try:
                self.cur.execute(query) # Execute the Query
                record = self.cur.fetchall() or record 
                return record  # Retornamo una lista con los resultados 
                               # de la consulta o None si no obtine nada
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                #print >> sys.stderr, traceback.format_exc(exc_type)
                print >> sys.stderr, "".join(traceback.format_exception_only(exc_type, exc_value))
                #return self.conn.status
                return self.conn.get_transaction_status() # Deberia retornar -1, si sucede un Error. 
            finally:
                print >> sys.stderr, "Actualizando y Cerranda la conexión"
                # Realizamos los cambios en la DB
                self.conn.commit()
                # Cerramos la comunicación
                self.cur.close()
                self.conn.close()


                

    def exemany(self): pass



