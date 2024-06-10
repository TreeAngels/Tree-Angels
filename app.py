from flask import Flask, render_template, g, request, session, redirect
from flask_session import Session
from sqlite3 import connect, Row
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import *

app = Flask(__name__)

DATABASE_ADRESS = r"data\TreeAngelsDB.db"  # Use raw string to avoid escape sequence issues

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect(DATABASE_ADRESS, check_same_thread=False)
        db.row_factory = Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_request
def before_request():
    g.loggedIn = session.get("username") is not None

@app.context_processor
def inject_is_admin():
    return dict(isAdmin=isAdmin)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html", user_logged_in=g.loggedIn)

@app.route("/account", methods=["GET", "POST"])
def account():
    return render_template("account.html", user_logged_in=g.loggedIn)

@app.route("/about_us", methods=["GET", "POST"])
def about_us():
    return render_template("about_us.html", user_logged_in=g.loggedIn)

@app.route("/cart", methods=["GET", "POST"])
def cart():
    return render_template("cart.html", user_logged_in=g.loggedIn)

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html", user_logged_in=g.loggedIn)

@app.route("/register", methods=["POST"])
def create_account():
    # Number of special characters
    c = sum(1 for char in request.form.get("password") if char in '[@_!#$%^&*()<>?/}{~:]')
    didg = sum(1 for char in request.form.get("password") if char.isdigit())
    pass_len = len(request.form.get("password"))

    if not request.form.get("firstName"):
        return apology("Must Provide First Name", 400)
    if not request.form.get("lastName"):
        return apology("Must Provide Last Name", 400)
    if not request.form.get("email"):
        return apology("Must Provide Email", 400)
    if not request.form.get("username"):
        return apology("Must Provide Username", 400)
    if len(get_db().execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()) > 0:
        return apology("Username is Taken", 400)
    if c < 1 or didg < 1 or pass_len < 8:
        return apology("Password Must Fit Requirements", 400)
    if not request.form.get("password"):
        return apology("Must Provide Password", 400)
    if not request.form.get("confirmation"):
        return apology("Must Confirm Password", 400)
    if request.form.get("confirmation") != request.form.get("password"):
        return apology("Passwords Must Match", 400)

    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    email = request.form.get("email")
    user = request.form.get("username")
    hashed_pass = generate_password_hash(request.form.get("password"))

    loginUserInfo = {"username": user, "hash": hashed_pass, "privilege": 'donor'}
    donorInfo = {"firstName": firstName, "lastName": lastName, "email": email, "username": user}

    db = get_db()
    db.execute("INSERT INTO login (username, hash, privilege) VALUES (:username, :hash, :privilege)", loginUserInfo)
    db.execute("INSERT INTO users (firstName, lastName, email, username) VALUES (:firstName, :lastName, :email, :username)", donorInfo)
    db.commit()

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login_to_account():
    if request.method == "POST":
        session.clear()

        if not request.form.get("username"):
            return apology("must provide username", 403)
        if not request.form.get("password"):
            return apology("must provide password", 403)

        cursor = get_db().execute("SELECT * FROM login WHERE username = ?", (request.form.get("username"),))
        row = cursor.fetchone()

        if row is None:
            return apology("Username Not Found", 403)
        if not check_password_hash(row["hash"], request.form.get("password")):
            return apology("Invalid Password", 403)

        session["username"] = row["username"]
        return redirect("/")

    return render_template("login.html", user_logged_in=g.loggedIn)

@app.route("/donate", methods=["GET", "POST"])
def donate():
    return render_template("donate.html", user_logged_in=g.loggedIn)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    return render_template("admin.html", user_logged_in=g.loggedIn, admin_logged_in=isAdmin())

def isAdmin():
    if g.loggedIn:
        cursor = get_db().execute("SELECT * FROM Login WHERE username = ?", (session["username"],))
        row = cursor.fetchone()
        if row and row["privilege"] == "admin":
            return True
    return False

if __name__ == '__main__':
    app.run(debug=True)