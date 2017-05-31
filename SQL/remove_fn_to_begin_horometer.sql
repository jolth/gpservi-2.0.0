-- Before of update fn_insert_ingnition_state and fn_ingresar_vehicle_state
DROP FUNCTION public.fn_insert_ingnition_state(integer, boolean, boolean, boolean, boolean, timestamp with time zone);
DROP FUNCTION public.fn_ingresar_vehicle_state(integer, boolean, boolean, boolean, boolean, timestamp with time zone);

BEGIN;
ALTER TABLE vehicle_state_history ADD COLUMN horometer bigint default 0;
--ALTER TABLE vehicle_state_history ADD COLUMN horometer float default 0;
COMMIT;

BEGIN;
ALTER TABLE vehicle_state ADD COLUMN horometer bigint default 0;
--ALTER TABLE vehicle_state ADD COLUMN horometer float default 0;
COMMIT;
