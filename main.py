from flask import Flask, render_template, request, redirect
import pymysql


app = Flask(__name__)

def get_connection():
    connection = pymysql.connect(
        host='my-mysql',
        user='flaskuser',
        password='flaskpass',
        database='testdb',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor  # <-- 여기가 핵심
    )
    return connection


@app.route("/")
def home():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()  # 결과 가져오기

    finally:
        conn.close()

    return render_template("index.html", users=users);