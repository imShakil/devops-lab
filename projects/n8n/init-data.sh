#!/bin/bash
# Creates the non-root user n8n connects as.
# Runs only once, on an empty PGDATA (Docker entrypoint behaviour).
#
# Postgres 15+ revoked CREATE on schema public from PUBLIC, so granting
# privileges on the DATABASE alone leaves n8n unable to create its tables.
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER "$POSTGRES_NON_ROOT_USER" WITH PASSWORD '$POSTGRES_NON_ROOT_PASSWORD';

    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_NON_ROOT_USER";

    ALTER SCHEMA public OWNER TO "$POSTGRES_NON_ROOT_USER";
    GRANT ALL ON SCHEMA public TO "$POSTGRES_NON_ROOT_USER";
EOSQL
