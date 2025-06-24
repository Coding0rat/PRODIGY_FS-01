from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '12345'

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="user_auth_1"
)
cursor = db.cursor()

@app.route('/')
def home():
    return redirect(url_for('signin'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password before storing it
        hashed_password = generate_password_hash(password)
        
        # Insert user into database
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        db.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('signin'))

    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            session['user'] = user[1]
            flash('Logged in successfully!', 'success')
            # ✅ This redirects to index page
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('signin.html')


@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)