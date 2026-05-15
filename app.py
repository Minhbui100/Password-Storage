from config import master_password, secret_key, db_host, db_port, db_name, db_user, db_password, salt
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import hmac
from functools import wraps
import psycopg2
from psycopg2 import IntegrityError

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64

app=Flask(__name__)
app.secret_key=secret_key

def _make_fernet():
    kdf=PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    key=base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return Fernet(key)

fernet = _make_fernet()

def encrypt(plaintext):
    return fernet.encrypt(plaintext.encode()).decode()

def decrypt(token):
    return fernet.decrypt(token.encode()).decode()


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


@app.route("/delete/<account_id>", methods=["POST"])
@login_required
def delete_account(account_id):
    try:
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute("select website from account where id=%s", (account_id,))
        row=cur.fetchone()
        if not row:
            return jsonify({"error": "Account not found"}), 404
        website=row[0]
        cur.execute("delete from account where id=%s", (account_id,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("get_accounts", website=website))
    except Exception as e:
        print(e)
        return jsonify({"error": "Error deleting account"}), 500
    
@app.route("/edit/<account_id>", methods=["POST"])
@login_required
def edit_account(account_id):
    try:
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute("update account set website=%s, username=%s, password=%s, url=%s where id=%s",
                    (request.form["website"].lower(), request.form["username"].lower(), request.form["password"], request.form["url"], account_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"redirect": url_for("get_accounts", website=request.form["website"].lower())})
    except IntegrityError:
        conn.rollback()
        
        return jsonify({"error": f"Account {request.form['username']} already exists for website {request.form['website']}"}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "Error editing account"}), 500

if __name__=="__main__":
    app.run(debug=True)