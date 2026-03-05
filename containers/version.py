import psycopg2
from testcontainers.postgres import PostgresContainer


with PostgresContainer("postgres:16", driver=None) as postgres:
    psql_url = postgres.get_connection_url()
    with psycopg2.connect(psql_url) as connection:
        with connection.cursor() as cursor:
            version = cursor.execute("SELECT version()")

            print("PostgreSQL version:", version)