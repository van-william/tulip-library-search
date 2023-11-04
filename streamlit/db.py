import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os

# Function to connect to the AWS RDS database
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
def create_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS library_search (
                    id SERIAL PRIMARY KEY,
                    query_text TEXT NOT NULL,
                    feedback TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
    except psycopg2.Error as e:
        # If an error occurs, print it and rollback the transaction
        print(f"An error occurred: {e}")
        conn.rollback()
        return None

# Function to insert a new query into the table
def insert_query(conn, query_text):
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO library_search (query_text) VALUES (%s) RETURNING id", (query_text,))
            query_id = cur.fetchone()[0]
            conn.commit()
            return query_id
    except psycopg2.Error as e:
        # If an error occurs, print it and rollback the transaction
        print(f"An error occurred: {e}")
        conn.rollback()
        return None
    
def update_feedback(conn, feedback, query_id):
    try:
        with conn.cursor() as cur:
            update_query = """
            UPDATE library_search
            SET feedback = %s
            WHERE id = %s;
            """
            cur.execute(update_query, (feedback, query_id))
            conn.commit()
    except psycopg2.Error as e:
        # If an error occurs, print it and rollback the transaction
        print(f"An error occurred: {e}")
        conn.rollback()
    return None

