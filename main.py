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

    return render_template("index.html");

# 추가
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        firstname = request.form.get("Firstname")
        lastname = request.form.get("Lastname")
        email = request.form.get("email")  # 이제 에러 없이 가져옵니다.

        print(f"데이터 수신: {firstname}, {lastname}, {email}")

        name = f"{firstname}{lastname}"
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
                cursor.execute(sql, (name, email))
            conn.commit()
        finally:
            conn.close()

        return redirect("/")  # INSERT 후 목록으로 이동

    return render_template("register.html")


