from flask import Flask, render_template, g, request, session, redirect
from flask_session import Session
from sqlite3 import connect, Row
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import *

app = Flask(__name__)

DATABASE_ADRESS = "data\TreeAngelsDB.db"


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # The `check_same_thread` flag is set to False to allow the same connection to be used in different threads
        db = g._database = connect(DATABASE_ADRESS, check_same_thread=False)
        db.row_factory = Row  # Optional: This allows you to treat the rows as dictionaries
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html", user_logged_in=True)


@app.route("/account", methods=["GET", "POST"])
def account():
    return render_template("account.html", user_logged_in=True)


@app.route("/about_us", methods=["GET", "POST"])
def about_us():
    return render_template("about_us.html", user_logged_in=True)


@app.route("/cart", methods=["GET", "POST"])
def cart():
    return render_template("cart.html", user_logged_in=True)


@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html", user_logged_in=True)

@app.route("/register", methods=["POST"])
def create_account():
            # # Of special Chars
        c = 0
        s = '[@_!#$%^&*()<>?/}{~:]'  # special character set
        for i in range(len(request.form.get("password"))):
            # checking if any special character is present in given string or not
            if request.form.get("password")[i] in s:
                c += 1
        didg = 0
        # # Of nums
        for i in range(len(request.form.get("password"))):
            if request.form.get("password")[i].isdigit:
                didg += 1
        # Num of chars
        pass_len = len(request.form.get("password"))
        # Ensure firstName was submitted
        if not request.form.get("firstName"):
            return apology("Must Provide First Name", 400)
        # Ensure lastName was submitted
        if not request.form.get("lastName"):
            return apology("Must Provide Last Name", 400)
        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("Must Provide Email", 400)
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must Provide Username", 400)
        # Check if username is taken
        elif len((get_db().execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))).fetchall()) > 0:
            return apology("Username is Taken", 400)
        elif c < 1 or didg < 1 or pass_len < 8:
            return apology("Password Must Fit Reqirements", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must Provide Password", 400)
        # Ensure confirm was submitted
        elif not request.form.get("confirmation"):
            return apology("Must Confirm Password", 400)
        # Make sure passwords match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("Passwords Must Match", 400)
        # Put it in the data base and return to the home page
        elif request.form.get("confirmation") == request.form.get("password"):
            firstName = request.form.get("firstName")
            lastName = request.form.get("lastName")
            email = request.form.get("email")
            user = request.form.get("username")
            # Code for the next two lines is inspired by DinoCoderSaurus at https://cs50.stackexchange.com/questions/34666/finance-pset-register-will-not-insert-user-data
            hashed_pass = generate_password_hash(request.form.get("password"))
            loginUserInfo = ({"username" : user, "hash" : hashed_pass, "privlidges" : 'donor'})
            donorInfo = ({"firstName" : firstName, "lastName" : lastName, "email" : email, "username" : user})
            db = get_db()
            db.execute("INSERT INTO login ('username', 'hash', 'privlidges') VALUES (:username, :hash, :privlidges)", loginUserInfo)
            db.execute("INSERT INTO users ('firstName', 'lastName', 'email', 'username') VALUES (:firstName, :lastName, :email, :username)", donorInfo)
            # Commit the transaction
            db.commit()       
            return render_template("index.html", user_logged_in=True)
        # Final Step if everything fails
        else:
            return render_template("register.html", user_logged_in=True)


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html", user_logged_in=True)


@app.route("/login", methods=["POST"])
def login_to_account():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 403)
    # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 403)
    # Execute the query
    cursor = get_db().execute("SELECT * FROM login WHERE username = ?", (request.form.get("username"),))
    # Fetch one result
    row = cursor.fetchone()
    # Check if the row exists
    if row is None:
        return apology("Username Not Found", 403)
    # Continue with your password check
    if not check_password_hash(row["hash"], request.form.get("password")):
        return apology("Invalid Password", 403)
    # If everything is correct, remember which user has logged in
    session["user_id"] = row["userID"]
    # Redirect user to home page
    return redirect("/")


@app.route("/donate", methods=["GET", "POST"])
def donate():
    return render_template("donate.html", user_logged_in=True)


if __name__ == '__main__':
    app.run(debug=True)