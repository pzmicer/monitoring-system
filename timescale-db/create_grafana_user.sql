-- Usage: psql --set=user="$DB_GRAFANA_USER" --set=passwd="$DB_GRAFANA_PASSWORD" <conn> -f script.sql
-- \set user `echo "$DB_GRAFANA_USER"`
-- \set passwd `echo "$DB_GRAFANA_PASSWORD"`
CREATE USER :user WITH PASSWORD :'passwd'   ;
GRANT USAGE ON SCHEMA public TO :user;
GRANT SELECT ON public.sensor_data TO :user;
