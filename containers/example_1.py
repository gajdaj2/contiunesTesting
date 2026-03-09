from testcontainers.postgres import PostgresContainer
import sqlalchemy

with PostgresContainer("postgres:16") as container:
    engine = sqlalchemy.create_engine(container.get_connection_url())
    with engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("SELECT 1"))
        print(result.fetchone())