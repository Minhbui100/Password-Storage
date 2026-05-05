from config import master_password, secret_key, db_host, db_port, db_name, db_user, db_password
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import hmac
from functools import wraps
import psycopg2
from psycopg2 import IntegrityError


app=Flask(__name__)
app.secret_key=secret_key

def get_db_connection():
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("get_website"))
    error=None
    if request.method=="POST":
        submitted=request.form.get("password", "")
        if hmac.compare_digest(submitted, master_password):
            session["logged_in"]=True
            return redirect(url_for("get_website"))
        error="Incorrect password"
    return render_template("login.html", error=error)

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def get_website():
    try:
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute("select distinct website from account order by website")
        websites=cur.fetchall()
        website_list=[website[0] for website in websites]
        cur.close()
        conn.close()
        return render_template("index.html", websites=website_list)
    except Exception as e:
        print(e)
        return jsonify({"error": "Error fetching websites"}), 500


@app.route("/add", methods=["POST"])
@login_required
def add_account():
    website=request.form.get("website")
    username=request.form.get("username")
    password=request.form.get("password")
    url=request.form.get("url")
    if not website or not username or not password:
        return jsonify({"error": "Missing required fields"}), 400
    try:
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute("insert into account (website, username, password, url) values (%s, %s, %s, %s)", (website, username, password, url))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True})
    except IntegrityError:
        conn.rollback()
        return jsonify({"error": f"Account {username} already exists for this website {website}"}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "Error adding account"}), 500
    
@app.route("/website/<website>")    
@login_required
def get_accounts(website):
    try: 
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute("select * from account where website=%s order by username", (website,))
        accounts=cur.fetchall()
        accounts_list=[{"id": account[0], "website": account[1], "username": account[2], "password": account[3], "url": account[4]} for account in accounts]
        cur.close()
        conn.close()
        return render_template("account.html", website=website, accounts=accounts_list)
    except Exception as e:
        print(e)
        return jsonify({"error": "Error fetching accounts"}), 500




if __name__=="__main__":
    app.run(debug=True)