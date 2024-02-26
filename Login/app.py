from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']  # Replace 'mydatabase' with your database name

# Define a collection for users
users_collection = db['users']

@app.route('/')
def login_form():
    return render_template('login.html', error=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', error=None)
    elif request.method == 'POST':
        # Get user data from the login form
        username = request.form['username']
        password = request.form['password']
        
        # Query MongoDB to find user by username and password
        user = users_collection.find_one({'username': username, 'password': password})

        if user:
            # Authentication successful, store user in session and redirect to page.html
            session['username'] = username
            return redirect(url_for('page'))
        else:
            # Authentication failed, redirect back to login page with error message
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear the session and redirect to login page
    session.clear()
    return redirect(url_for('login_form'))

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    # Get user data from the registration form
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # Check if the username already exists
    existing_user = users_collection.find_one({'username': username})
    if existing_user:
        return 'Username already exists!'

    # Insert the user data into the database
    new_user = {
        'username': username,
        'password': password,
        'email': email
    }
    users_collection.insert_one(new_user)

    # Redirect to login page after successful registration
    return redirect(url_for('login_form'))

@app.route('/page.html')
def page():
    # Check if user is logged in
    if 'username' in session:
        return render_template('page.html')
    else:
        # If user is not logged in, redirect to login page
        return redirect(url_for('login_form'))

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
