-- Add columns

BEGIN;
ALTER TABLE last_positions_gps ADD COLUMN odometer character varying(20);
COMMIT;

BEGIN;
ALTER TABLE positions_gps ADD COLUMN odometer character varying(20);
COMMIT;

