-- Add columns

BEGIN;
ALTER TABLE last_positions_gps ADD COLUMN odometer character varying(20);
COMMIT;

BEGIN;
ALTER TABLE positions_gps ADD COLUMN odometer character varying(20);
COMMIT;

----- New:
DROP FUNCTION public.fn_save_event_position_gps(character varying, point, text, real, real, real, smallint, character varying, timestamp with time zone);

CREATE OR REPLACE FUNCTION public.fn_save_event_position_gps(name_gps character varying, position_ point, ubicacion_ text, velocidad_ real, altura_ real, grados_ real, satelites_ smallint, address_ character varying, fecha_ timestamp with time zone, odometer_ character varying)
 RETURNS record
 LANGUAGE plpgsql
AS $function$
DECLARE
        gps_id_ integer;
        retorno record;
BEGIN

        -- Buscamos el gps.id en la tabla gps;
        SELECT INTO gps_id_ id FROM gps WHERE name=name_gps;
        IF NOT FOUND THEN
         RETURN NULL;
        END IF;

        INSERT INTO positions_gps
        (
          gps_id,
          position,
          ubicacion,
          velocidad,
          altura,
          grados,
          satelites,
          address,
          fecha,
          odometer
        )
        VALUES (
          gps_id_,
          position_,
          ubicacion_,
          velocidad_,
          altura_,
          grados_,
          satelites_,
          address_,
          fecha_,
          odometer_
        )RETURNING id, gps_id_ INTO retorno;

        RETURN retorno;
END;
$function$;

----- New:
--DROP TRIGGER ingresar_last_positions_gsp ON positions_gps;

CREATE OR REPLACE FUNCTION public.ingresar_last_positions_gsp()
 RETURNS trigger
 LANGUAGE plpgsql
AS $positions_gps$
DECLARE
result boolean;
BEGIN

 SELECT INTO result active FROM gps WHERE id=NEW.gps_id and active='t';
 IF NOT FOUND THEN
  RETURN NULL;
 END IF;

 UPDATE last_positions_gps SET(
                id,
                position,
                ubicacion,
                velocidad,
                altura,
                grados,
                satelites,
                address,
                fecha,
                odometer) = ( NEW.id, NEW.position, NEW.ubicacion, NEW.velocidad, NEW.altura, NEW.grados, NEW.satelites, NEW.address, NEW.fecha, NEW.odometer)
        WHERE gps_id = NEW.gps_id;

 IF not found THEN
  INSERT INTO last_positions_gps VALUES (NEW.*);
 END IF;

RETURN NEW;

END;
$positions_gps$;
