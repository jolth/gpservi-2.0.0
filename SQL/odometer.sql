-- Add columns

BEGIN;
ALTER TABLE last_positions_gps ADD COLUMN odometer double precision;
COMMIT;

BEGIN;
ALTER TABLE positions_gps ADD COLUMN odometer double precision;
COMMIT;

