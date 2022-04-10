from flask import Flask, render_template, request
import sqlite3

from werkzeug.utils import redirect

connection=sqlite3.connect("BookAdmin.db",check_same_thread=False)
table = connection.execute("select name from sqlite_master where type='table' and name='myuser'").fetchall()

if table!=[]:
    print("Table exist already")
else:
    connection.execute('''create table myuser(
                             ID integer primary key autoincrement,
                             name text,
                             address text,
                             email text,
                             phone integer,
                             password text
                             )''')
    print("table created successfully")

app=Flask(__name__)

@app.route("/",methods=["POST","GET"])
def user_login_details():
    if request.method == "POST":
        getName=request.form["name"]
        getAddress=request.form["address"]
        getEmail=request.form["email"]
        getPhone=request.form["phone"]
        getPassword=request.form["password"]
        print(getName)
        print(getAddress)
        print(getEmail)
        print(getPhone)
        print(getPassword)
        try:
            query=("insert into myuser(name,address,email,phone,password)\
                                   values('" + getName + "','" + getAddress + "','" + getEmail + "'," + getPhone + ",'" + getPassword + "')")
            print(query)
            connection.execute(query)
            connection.commit()
            print("inserted successfully")
        except Exception as e:
            print("Error occured ", e)

    return render_template("userlogin.html")

@app.route("/uselogin",methods=["POST","GET"])
def use_login():
    if request.method=="POST":
        getEmail=request.form["email"]
        getPassword=request.form["password"]
        print(getEmail)
        print(getPassword)
        if getEmail!="1" and getPassword!="0":
            return redirect("/viewbook")
    return render_template("uselogin.html")


@app.route("/viewbook")
def user_viewbook():
    cursor = connection.cursor()
    count = cursor.execute("select * from Book")
    result = cursor.fetchall()
    return render_template("viewbook.html", Book=result)

@app.route("/searchbook",methods=["POST","GET"])
def user_search_book():
    if request.method == "POST":
        getBookname=request.form["name"]
        print(getBookname)
        cursor = connection.cursor()
        count = cursor.execute("select * from Book where Bookname='"+getBookname+"'")
        result = cursor.fetchall()
        return render_template("searchbook.html", searchBook=result)

    return render_template("searchbook.html")

if __name__=="__main__":
    app.run()