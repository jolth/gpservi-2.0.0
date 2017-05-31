CREATE OR REPLACE FUNCTION public.fn_ingresar_vehicle_state(gps_id_ integer, motor_ boolean, car_ boolean, doors_ boolean, battery_gps_ boolean, fecha_ timestamp with time zone)
 RETURNS record
 LANGUAGE plpgsql
AS $function$
DECLARE
--variable:
 vehiculo_id integer;
 retorno record; 
 last_state_ign boolean; -- last state of IGN
 current_horometer bigint;
 last_datetime timestamp with time zone;
 horometer_ bigint;
 id_ integer;
BEGIN

 -- Obtenemos vehiculos.id
 SELECT INTO vehiculo_id id FROM vehiculos WHERE gps_id=gps_id_;
 IF NOT FOUND THEN
  RETURN NULL;
 END IF;

 --select max(vsh.id) FROM vehiculos v, vehicle_state_history vsh WHERE vsh.vehicle_id=v.id AND v.placa=lower('RJM270');
 SELECT INTO id_ max(id) FROM vehicle_state_history WHERE vehicle_id=vehiculo_id;
 -- select last state of IGN:
 SELECT INTO last_state_ign motor FROM vehicle_state_history WHERE id=id_;--vehicle_id=vehiculo_id;
 IF found THEN
  SELECT INTO current_horometer horometer FROM vehicle_state_history WHERE id=id_;--vehicle_id=vehiculo_id;
  --SELECT INTO current_datetime fecha FROM vehicle_state WHERE vehicle_id=vehiculo_id;
  IF (last_state_ign='t') AND (motor_='f') THEN
      SELECT INTO last_datetime fecha FROM vehicle_state_history WHERE id=id_;--vehicle_id=vehiculo_id;
      --SELECT INTO horometer_ EXTRACT(MINUTE FROM fecha_-last_datetime) FROM public.vehicle_state_history WHERE id=id_;--vehicle_id=vehiculo_id;
      SELECT INTO horometer_ (((extract (epoch from fecha_::timestamp - last_datetime::timestamp)))::integer) FROM vehicle_state_history WHERE id=id_;
      horometer_ = horometer_ + current_horometer;
  ELSE
    horometer_ = current_horometer;
  END IF;
 END IF;

 /*UPDATE vehicle_state SET(
                vehicle_id,
                motor,
                car,
                doors,
                battery_gps, fecha) = ( vehiculo_id, motor_, car_, doors_, battery_gps_, fecha_)
        WHERE (vehicle_id = vehiculo_id) RETURNING vehiculo_id INTO retorno;*/
 -- update state IGN and horometer:
 SELECT fn_insert_ingnition_state(gps_id_, motor_, car_, doors_, battery_gps_, fecha_) INTO retorno;
 --PERFORM fn_insert_ingnition_state(gps_id_, motor_, car_, doors_, battery_gps_, fecha_);

 IF not found THEN
  INSERT INTO vehicle_state VALUES (vehiculo_id, motor_, car_, doors_, battery_gps_, fecha_) RETURNING vehiculo_id INTO retorno;
 END IF;

 IF found THEN
  INSERT INTO vehicle_state_history (vehicle_id,
                motor,
                car,
                doors,
                battery_gps, fecha, horometer)
  VALUES (vehiculo_id, motor_, car_, doors_, battery_gps_, fecha_, horometer_) RETURNING vehiculo_id INTO retorno;
 END IF;

-- retornamos vehiculo_id
RETURN retorno;

END;
$function$;
