from flask import Flask, render_template, request, redirect, session, url_for, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'agrosecret'

# MongoDB Setup
client = MongoClient( "mongodb+srv://username:password@cluster0.9jcddh7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['agrohub']
users = db['users']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']

        user = users.find_one({"username": uname})
        if user and check_password_hash(user['password'], pword):
            session['user'] = uname
            return redirect("/admin")
        else:
            flash("Invalid credentials!", "danger")
            return render_template("login.html")

    return render_template("login.html")


@app.route('/sign-up', methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        uname = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        # Check if the user already exists
        if users.find_one({"username": uname}):
            flash("Username already exists!", "warning")
            return redirect(url_for("signup"))

        # Store in MongoDB
        users.insert_one({
            "username": uname,
            "password": hashed_pw
        })

        flash("Registered successfully! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("sign-up.html")

@app.route('/admin')
def admin():
    if 'user' in session:
        return render_template('admin.html')
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully", "info")
    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

if __name__ == '__main__':
    app.run(debug=True)