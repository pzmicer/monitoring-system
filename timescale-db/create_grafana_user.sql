 CREATE USER grafanauser WITH PASSWORD 'grafanauser';
 GRANT USAGE ON SCHEMA schema TO grafanauser;
 GRANT SELECT ON schema.table TO grafanauser;