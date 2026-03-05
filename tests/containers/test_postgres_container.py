import psycopg2
import pytest
from testcontainers.postgres import PostgresContainer


@pytest.mark.containers
@pytest.mark.slow
def test_postgres_container_roundtrip():
    print("Start testu: uruchamiam kontener Postgres")
    with PostgresContainer("postgres:16") as container:  # kluczowy krok: start kontenera
        dsn = (
            f"host={container.get_container_host_ip()} "
            f"port={container.get_exposed_port(5432)} "
            f"dbname={container.dbname} user={container.username} password={container.password}"
        )
        print(f"Utworzony DSN: host={container.get_container_host_ip()} port={container.get_exposed_port(5432)}")
        with psycopg2.connect(dsn) as conn:
            print("Polaczono z baza, wykonuje zapytania")
            with conn.cursor() as cursor:
                cursor.execute("CREATE TABLE demo(id serial PRIMARY KEY, name text)")
                cursor.execute("INSERT INTO demo(name) VALUES (%s)", ("CT",))
                cursor.execute("SELECT name FROM demo WHERE id = 1")
                row = cursor.fetchone()
            print(f"Odczytano wiersz: {row}")

    print("Zakonczono test i zatrzymano kontener")
    assert row[0] == "CT"
