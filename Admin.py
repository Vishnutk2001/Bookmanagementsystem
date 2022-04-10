from flask import Flask, render_template, request
import sqlite3

from werkzeug.utils import redirect

connection = sqlite3.connect("Bookadmin.db", check_same_thread=False)
table = connection.execute("select name from sqlite_master where type='table' and name='Book'").fetchall()

if table!=[]:
    print("table already exists")
else:
    connection.execute('''create table Book(
                             id integer primary key autoincrement,
                             Bookname text,
                             Author text,
                             Category text,
                             Price integer,
                             Publisher text
                             )''')
    print("table created successfully")

app=Flask(__name__)

@app.route("/",methods=["POST","GET"])
def Login():
    if request.method == "POST":
        getUsername=request.form["username"]
        getPassword=request.form["password"]
        print(getUsername)
        print(getPassword)
        if getUsername=="admin" and getPassword=="12345":
            return redirect("/Booksentry")
    return  render_template("login.html")

@app.route("/Booksentry",methods = ["GET","POST"])
def details():
    if request.method == "POST":
        getBookname=request.form["name"]
        getAuthor=request.form["author"]
        getCategory=request.form["category"]
        getPrice=request.form["price"]
        getPublisher=request.form["publisher"]
        print(getBookname)
        print(getAuthor)
        print(getCategory)
        print(getPrice)
        print(getPublisher)
        try:
            connection.execute("insert into Book(Bookname,Author,Category,Price,Publisher)\
                               values('"+getBookname+"','"+getAuthor+"','"+getCategory+"',"+getPrice+",'"+getPublisher+"')")
            connection.commit()
            print("inserted successfully")
        except Exception as e:
            print("Error occured ", e)

    return render_template("Booksentry.html")

@app.route("/search",methods=["POST","GET"])
def search():
    if request.method == "POST":
        getBookname=request.form["name"]
        print(getBookname)
        cursor = connection.cursor()
        count = cursor.execute("select * from Book where Bookname='"+getBookname+"'")
        result = cursor.fetchall()
        return render_template("search.html", searchBook=result)

    return render_template("search.html")

@app.route("/delete",methods=["POST","GET"])
def delete():
    if request.method == "POST":
        getBookname = request.form["name"]
        print(getBookname)

        try:
            connection.execute("delete from Book where Bookname='"+getBookname+"'")
            connection.commit()
            print("deleted successfully")
        except Exception as e:
            print("Error occured ", e)

    return render_template("delete.html")

@app.route("/update",methods = ["GET","POST"])
def update():
    if request.method == "POST":
        getBookname = request.form["name"]
        Author = request.form["author"]
        Category = request.form["category"]
        Price = request.form["price"]
        Publisher = request.form["publisher"]
        try:
            connection.execute("update Book set Author='" + Author + "',Category='" + Category + "',Price=" + Price + ",Publisher='" + Publisher + "' where Bookname='" + getBookname + "'")
            connection.commit()
            print("update successfully")
        except Exception as e:
            print(e)
        cursor = connection.cursor()
        count = cursor.execute("select * from Book where Bookname='" + getBookname + "'")
        result = cursor.fetchall()
        return render_template("update.html", searchBook=result)

    return render_template("update.html")



@app.route("/viewall")
def viewall():
    cursor = connection.cursor()
    count = cursor.execute("select * from Book")
    result = cursor.fetchall()
    return render_template("viewall.html", Book=result)



if __name__=="__main__":
    app.run()