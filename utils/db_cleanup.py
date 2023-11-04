import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os
def create_connection():
    try:
        # Database credentials are typically stored as environment variables for security reasons
        db_host = os.getenv('PROD_ECO_HOST')
        db_name = os.getenv('PROD_ECO_DB')
        db_user = os.getenv('PROD_ECO_USER')
        db_password = os.getenv('PROD_ECO_PASS')
        db_port = os.getenv('PROD_ECO_DB_PORT')

        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        return conn
    except psycopg2.Error as e:
        # If an error occurs, print it and rollback the transaction
        print(f"An error occurred: {e}")
        conn.rollback()
        return None


# Function to create a table (if it doesn't exist)
def drop_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                DROP TABLE IF EXISTS library_search;
                DROP SEQUENCE IF EXISTS library_search_id_seq;
            """)
            conn.commit()
    except psycopg2.Error as e:
        # If an error occurs, print it and rollback the transaction
        print(f"An error occurred: {e}")
        conn.rollback()
        return None
    

conn = create_connection()
drop_table(conn)



