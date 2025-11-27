import psycopg2

def create_connection():
    connection = psycopg2.connect(
        dbname="bvent",
        user="postgres",
        password="byte",
        host="localhost",
        port="5432"
    )

    return connection