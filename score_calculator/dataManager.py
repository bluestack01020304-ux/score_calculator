import mysql.connector as connector

import os
from dotenv import load_dotenv

load_dotenv()

conn = None
cursor = None

def initialize_data_manager():
    global conn, cursor

    conn = connector.connect(
        host="localhost",
        user=os.getenv("DB_ADMIN_ID"),
        password=os.getenv("DB_ADMIN_PW"),
        database="calculator_db",
        use_pure=True
    )

    cursor = conn.cursor()

    if conn.is_connected():
        print("Connected to MySQL database")
        cursor.execute("USE calculator_db")

def executeQuery(query): #조회
    cursor.execute(query)
    return cursor.fetchall()

def executeCommit(query): #추가, 수정, 삭제
    cursor.execute(query)
    conn.commit()

def close_database():
    if cursor: cursor.close()
    if conn and conn.is_connected(): conn.close()