import psycopg2

DB_NAME = 'student_management'
USER = 'postgres'
PASSWORD = '0935109623tn'
HOST = 'localhost'
PORT = '5432'


def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        return conn
    except Exception as e:
        raise Exception(f"Không thể kết nối cơ sở dữ liệu: {e}")
