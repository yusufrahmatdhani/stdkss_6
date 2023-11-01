from cs50 import SQL
import os 
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

db = SQL("sqlite:///score.db")
app.config.update(SECRET_KEY=os.urandom(24))

@app.route("/", methods=["GET", "POST"])
def index():
        if request.method == "POST": 
            name = request.form.get("name")
            score = request.form.get("score")

            db.execute("INSERT INTO score (name, score) VALUES(?, ?)", name, score)

            return redirect("/")
        else:

            students = db.execute("SELECT * FROM score")
            return render_template("index.html", students=students)

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_data(id):
    if request.method == "GET":
        score = db.execute("SELECT * FROM score WHERE id = ?", id)[0]
        print(score)
        return render_template("edit.html", score=score)
    elif request.method == "POST":
        score_name = request.form.get("name")
        score_score = request.form.get("score")
        db.execute('UPDATE score set name = ?, score = ? where id = ?', score_name, score_score, id)
        return redirect("/")

@app.route("/delete/<id>", methods=["GET"])
def delete(id):
    db.execute("delete from score where id = ? ", id)
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register(): 
     session.clear()
     """Register User"""
     #access form data (sesuaikan dengan form register masing-masing)
     if request.method == "POST":
          if not request.form.get("username"):
               return "must providde username"
          elif not request.form.get("password"):
               return "must provide password"
          # baca data username yang sudah terdaftar
          rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
          # baca data isian member baru dari form
          email = request.form.get("email")
          username = request.form.get("username")
          password = request.form.get("password")
          rpassword = request.form.get("repeat_password")
          #enkripsi password
          hash = generate_password_hash(password)
          if len(rows) == 1:
               return "username tidak tersedia"
          if password == rpassword:
               db.execute("INSERT INTO users (email, username, password, repeat_password) VALUES(?, ?, ?, ?) ",email, username, hash, hash)

               registered_user = db.execute("SELECT * FROM users WHERE username = ?", username)
               session["id"] = registered_user[0]["id"]
               flash("Berhasil Registrasi")
               return redirect("/")
          else:
               return "must provide matching password"
     else:
          return render_template("register.html")     
          
