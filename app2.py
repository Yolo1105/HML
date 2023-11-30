from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Use MySQL configuration for phpMyAdmin
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Use SQLAlchemy for database ORM
db = SQLAlchemy(app)

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return 'Username already exists', 400

    # Create a new user
    new_user = User(username=username, password=password)

    # Save the user to the database
    db.session.add(new_user)
    db.session.commit()

    return 'User registered successfully'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Find the user in the database
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return 'Invalid username or password', 401

    return 'Login successful'

if __name__ == '__main__':
    db.create_all()  # Create tables before running the app
    app.run(debug=True)
