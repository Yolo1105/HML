from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import asc, desc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secret key for production
# Use MySQL configuration for phpMyAdmin
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define a User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Check if the app successfully connects to the database
try:
    with app.app_context():
        db.create_all()
    print("Successfully connected to the database!")
except Exception as e:
    print(f"Failed to connect to the database. Error: {e}")

@app.route('/')
def index():
    return render_template('index.html', authenticated=current_user.is_authenticated, username=current_user.username if current_user.is_authenticated else None)

# New route to fetch and display user accounts
@app.route('/user_accounts')
@login_required
def user_accounts():
    users = User.query.all()
    return render_template('user_accounts.html', users=users)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return 'Username already exists', 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return 'User registered successfully'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        login_user(user)
        return redirect(url_for('index'))
    else:
        return 'Invalid username or password', 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)

    if request.method == 'POST':
        # Update user information
        user.username = request.form['username']
        user.password = request.form['password']
        db.session.commit()
        return redirect(url_for('user_accounts'))

    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user_accounts'))

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists', 400

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('user_accounts'))

    return render_template('add_user.html')

