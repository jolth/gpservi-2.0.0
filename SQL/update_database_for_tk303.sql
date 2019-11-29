insert into type_gps (codigo, name, descrip) values (5, 'TK', 'Coban');

ALTER TABLE gps ADD COLUMN aka varchar(10); 
ALTER TABLE gps ALTER COLUMN name TYPE varchar(20);
ALTER TABLE log_gps ALTER COLUMN name TYPE varchar(20);

--- Test:
-- insert into gps (name, type, active, aka) VALUES ('864180038790106', 5, 't', 'TK001');
