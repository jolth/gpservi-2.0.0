rastree=# \df fn_ingresar_vehicle_state
                                                                                   List of functions
 Schema |           Name            | Result data type |                                                 Argument data types                                                  |  Type
--------+---------------------------+------------------+----------------------------------------------------------------------------------------------------------------------+--------
 public | fn_ingresar_vehicle_state | record           | gps_id_ integer, motor_ boolean, car_ boolean, doors_ boolean, battery_gps_ boolean, fecha_ timestamp with time zone | normal
(1 row)


# Event 6/7:

\ef fn_ingresar_vehicle_state


CREATE OR REPLACE FUNCTION public.fn_ingresar_vehicle_state(gps_id_ integer, motor_ boolean, car_ boolean, doors_ boolean, battery_gps_ boolean, fecha_ timestamp with time zone)
 RETURNS record
 LANGUAGE plpgsql
AS $function$
DECLARE
vehiculo_id integer;
retorno record;
BEGIN

 -- Obtenemos vehiculos.id
 SELECT INTO vehiculo_id id FROM vehiculos WHERE gps_id=gps_id_;
 IF NOT FOUND THEN
  RETURN NULL;
 END IF;

 UPDATE vehicle_state SET(
                vehicle_id,
                motor,
                car,
                doors,
                battery_gps, fecha) = ( vehiculo_id, motor_, car_, doors_, battery_gps_, fecha_)
        WHERE (vehicle_id = vehiculo_id) RETURNING vehiculo_id INTO retorno;

 IF not found THEN
  INSERT INTO vehicle_state VALUES (vehiculo_id, motor_, car_, doors_, battery_gps_, fecha_) RETURNING vehiculo_id INTO retorno;
 END IF;

 IF found THEN
  INSERT INTO vehicle_state_history (vehicle_id,
                motor,
                car,
                doors,
                battery_gps, fecha)
  VALUES (vehiculo_id, motor_, car_, doors_, battery_gps_, fecha_) RETURNING vehiculo_id INTO retorno;
 END IF;

-- retornamos vehiculo_id
RETURN retorno;

END;
$function$



-------------------------------------------------------------------------------------------------------------------------------



rastree=# \df fn_insert_ingnition_state
                                                                                   List of functions
 Schema |           Name            | Result data type |                                                 Argument data types                                                  |  Type
--------+---------------------------+------------------+----------------------------------------------------------------------------------------------------------------------+--------
 public | fn_insert_ingnition_state | record           | gps_id_ integer, motor_ boolean, car_ boolean, doors_ boolean, battery_gps_ boolean, fecha_ timestamp with time zone | normal
(1 row)


# Event 5:


\ef fn_insert_ingnition_state


CREATE OR REPLACE FUNCTION public.fn_insert_ingnition_state(gps_id_ integer, motor_ boolean, car_ boolean, doors_ boolean, battery_gps_ boolean, fecha_ timestamp with time zone)
 RETURNS record
 LANGUAGE plpgsql
AS $function$
DECLARE
vehiculo_id integer;
retorno record;
BEGIN

 -- Obtenemos vehiculos.id
 SELECT INTO vehiculo_id id FROM vehiculos WHERE gps_id=gps_id_;
 IF NOT FOUND THEN
  RETURN NULL;
 END IF;

 UPDATE vehicle_state SET(
                vehicle_id,
                motor,
                car,
                doors,
                battery_gps, fecha) = ( vehiculo_id, motor_, car_, doors_, battery_gps_, fecha_)
        WHERE (vehicle_id = vehiculo_id) RETURNING vehiculo_id INTO retorno;

 IF not found THEN
  INSERT INTO vehicle_state VALUES (vehiculo_id, motor_, car_, doors_, battery_gps_, fecha_) RETURNING vehiculo_id INTO retorno;
 END IF;

-- retornamos vehiculo_id
RETURN retorno;

END;
$function$


