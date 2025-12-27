from flask import Flask, render_template, request, redirect
import pymysql
import psutil
import logging

logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(message)s',
        force=True
        )

def log_server_metrics(action_name=""):
    cpu = psutil.cpu_percent(interval=0)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    logging.info(f"[{action_name}] CPU:{cpu}%, Memory:{memory}%, Disk:{disk}%")

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
    log_server_metrics("home")  # 조회 시 서버 상태 기록

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()  # 결과 가져오기

    finally:
        conn.close()

    return render_template("index.html", users=users);

# 추가
@app.route("/add", methods=["GET", "POST"])
def add():
    log_server_metrics("add")  # 조회 시 서버 상태 기록

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

# 삭제
@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM users WHERE id = %s"
            cursor.execute(sql, (user_id,))
        conn.commit()
    finally:
        conn.close()

    return redirect("/")

# 수정
@app.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    log_server_metrics("edit")  # 조회 시 서버 상태 기록

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == "POST":
                # 폼에서 받은 데이터로 업데이트
                name = request.form["name"]
                email = request.form["email"]
                sql = "UPDATE users SET name=%s, email=%s WHERE id=%s"
                cursor.execute(sql, (name, email, user_id))
                conn.commit()
                return redirect("/")

            # GET: 기존 사용자 정보 가져오기
            sql = "SELECT * FROM users WHERE id=%s"
            cursor.execute(sql, (user_id,))
            user = cursor.fetchone()
            if not user:
                return "User not found", 404
    finally:
        conn.close()

    return render_template("comify.html", user=user)

