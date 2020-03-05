import os
#api

import requests
from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#sqlalchameny is a library to conncet python a sql 

app = Flask(__name__)


# Check for environment variable

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#GETTING review counts FROM API 
# res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "2T78BJ2F7Pz0DqSFkAUWg", "isbns": "1632168146"})
# print(res.json())


@app.route("/index") # to do a log in
def index():
    #return "Project 1: TODO"
    return render_template("index.html")

@app.route("/signup") # to do a sign up
def signup():
    #return "Project 1: TODO"
    return render_template("signup.html")



#REGISTER A USER
@app.route("/sign", methods=["POST"])
def sign():
    """Sign up a user."""

    # Get form information.
    name = request.form.get("name")
    password = request.form.get("password")


    if db.execute("SELECT * FROM users WHERE name = :name AND password = :password", {"name": name, "password": password}).rowcount == 0:
        db.execute("INSERT INTO users (name, password) VALUES (:name, :password)",
                {"name": name, "password": password})
        db.commit()
        return render_template("success.html")
    else:
        return render_template("error.html", message="Try Again, user or password are incorrect.")

#LOGIN A USER

@app.route("/signIn", methods=["POST"])
def signIn():
    """Signin a user."""

    name = request.form.get("name")
    password = request.form.get("password")

    if db.execute("SELECT name FROM users WHERE name = :name AND password = :password", {"name": name, "password": password}):
        return render_template("bookpage.html")

    else:
        return render_template("error.html", message="No such user with name or password.")

#LOG OUT

@app.route('/logout')
def logout():
    return redirect('/index')
    #this redirect is to the page of flask

#SEACRH A BOOK
# <isbn>,<title>, <author>

@app.route("/search", methods=["POST"])
def search():
    """search a book."""
    isbn = '%' + request.form.get("isbn") + '%'
    title = '%' + request.form.get("title") + '%'
    author = '%' + request.form.get ("author") + '%'

    books = db.execute("SELECT id, isbn, title, author, year FROM books WHERE isbn LIKE :isbn AND title LIKE :title AND author LIKE :author",
                                {"isbn": isbn, "title": title, "author": author}).fetchall()

    if books:
        return render_template("showbooks.html", books=books)
    else:
        return render_template("error.html", message="No such book.")



@app.route("/showbooks/<int:id>")
def showbooks(id):
    """Lists details about a single book."""

    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": id}).fetchone()
    print(book)
    if book:
        return render_template("showdetailbook.html", book=book)
    return render_template("error.html", message="No such book.")
    

