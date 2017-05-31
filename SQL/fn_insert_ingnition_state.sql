CREATE OR REPLACE FUNCTION public.fn_insert_ingnition_state(gps_id_ integer, motor_ boolean, car_ boolean, doors_ boolean, battery_gps_ boolean, fecha_ timestamp with time zone)
 RETURNS record
 LANGUAGE plpgsql
AS $function$
DECLARE
vehiculo_id integer;
retorno record;
last_state_ign boolean; -- last state of IGN
current_horometer bigint;
horometer_ bigint;
current_datetime timestamp with time zone;
BEGIN

 -- Obtenemos vehiculos.id
 SELECT INTO vehiculo_id id FROM vehiculos WHERE gps_id=gps_id_;
 IF NOT FOUND THEN
  RETURN NULL;
 END IF;

 -- select last state IGN
 SELECT INTO last_state_ign motor FROM vehicle_state WHERE vehicle_id=vehiculo_id;
 IF found THEN
  SELECT INTO current_horometer horometer FROM vehicle_state WHERE vehicle_id=vehiculo_id;
  SELECT INTO current_datetime fecha FROM vehicle_state WHERE vehicle_id=vehiculo_id;
  IF last_state_ign='t' THEN
      --SELECT (((extract (epoch from (now()::timestamp with time zone - vs.fecha))))::integer) FROM vehiculos v, vehicle_state vs WHERE vs.vehicle_id=v.id AND v.placa=lower('RJM270');
      SELECT INTO horometer_ (((extract (epoch from fecha_::timestamp - current_datetime::timestamp)))::integer) FROM vehicle_state WHERE vehicle_id=vehiculo_id;
      --SELECT INTO horometer_ EXTRACT(SECOND FROM fecha_-current_datetime) FROM public.vehicle_state WHERE vehicle_id=vehiculo_id;
      horometer_ = horometer_ + current_horometer;
  ELSE
    horometer_ = current_horometer;
  END IF;
 END IF;

 UPDATE vehicle_state SET(
                vehicle_id,
                motor,
                car,
                doors,
                battery_gps, fecha, horometer) = ( vehiculo_id, motor_, car_, doors_, battery_gps_, fecha_, horometer_)
        WHERE (vehicle_id = vehiculo_id) RETURNING vehiculo_id INTO retorno;

 IF not found THEN
  INSERT INTO vehicle_state VALUES (vehiculo_id, motor_, car_, doors_, battery_gps_, fecha_) RETURNING vehiculo_id INTO retorno;
 END IF;

-- retornamos vehiculo_id
RETURN retorno;

END;
$function$;

