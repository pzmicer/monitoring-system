 CREATE USER grafanareader WITH PASSWORD 'grafanareader';
 GRANT USAGE ON SCHEMA schema TO grafanareader;
 GRANT SELECT ON schema.table TO grafanareader;