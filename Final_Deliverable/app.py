from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import asc, desc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secret key for production
# Use MySQL configuration for phpMyAdmin
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for static files

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
def home():
    success_message = request.args.get('success_message')
    return render_template('home.html', success_message=success_message)


@app.route('/index')
def index():
    return render_template('index.html', authenticated=current_user.is_authenticated, username=current_user.username if current_user.is_authenticated else None)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/criminal')
def criminal():
    return render_template('criminal.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/alias_accounts')
@login_required
def alias_accounts():
    users = User.query.all()
    return render_template('alias_accounts.html', users=users)

@app.route('/appeals_accounts')
@login_required
def appeals_accounts():
    users = User.query.all()
    return render_template('appeals_accounts.html', users=users)

@app.route('/crime_charges_accounts')
@login_required
def crime_charges_accounts():
    users = User.query.all()
    return render_template('crime_charges_accounts.html', users=users)

@app.route('/crime_officers_accounts')
@login_required
def crime_officers_accounts():
    users = User.query.all()
    return render_template('crime_officers_accounts.html', users=users)

@app.route('/crime_accounts')
@login_required
def crime_accounts():
    users = User.query.all()
    return render_template('crime_accounts.html', users=users)

@app.route('/criminal_accounts')
@login_required
def criminal_accounts():
    users = User.query.all()
    return render_template('criminal_accounts.html', users=users)

@app.route('/officier_accounts')
@login_required
def officier_accounts():
    users = User.query.all()
    return render_template('officier_accounts.html', users=users)

@app.route('/prob_officer_accounts')
@login_required
def prob_officer_accounts():
    users = User.query.all()
    return render_template('prob_officer_accounts.html', users=users)

@app.route('/sentences_accounts')
@login_required
def sentences_accounts():
    users = User.query.all()
    return render_template('sentences_accounts.html', users=users)

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
        success_message = "Successfully Logged In!"
        # Add the success_message parameter when redirecting to the home page
        return redirect(url_for('home', success_message=success_message))
    else:
        return 'Invalid username or password', 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

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

@app.route('/user-options')
@login_required
def user_options():
    # Check if the current user is an admin
    if current_user.username in ['Hongjie', 'Mohan', 'Lucas']:
        role = 'Admin (View and Edit)'
    else:
        role = 'User (View only)'

    return render_template('user_options.html', role=role)

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

if __name__ == '__main__':
    app.run(debug=True)
