from flask import Flask, render_template, request, redirect, url_for, flash, session
from peewee import SqliteDatabase
from models import User, Peep
from flask_mail import Mail, Message
import bcrypt

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'superstar'

# Flask-Mail configuration
app.config.update(
    MAIL_SERVER='smtp.example.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='your_email@example.com',
    MAIL_PASSWORD='your_email_password'
)
mail = Mail(app)

# Connect to the database
db = SqliteDatabase('chitter.db')

@app.route('/')
def index():
    peeps = Peep.select().order_by(Peep.timestamp.desc())
    return render_template('index.html', peeps=peeps)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        
        print(f"Received data: {username}, {email}, {password}, {name}")
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            with db.transaction():
                user = User.create(username=username, email=email, password=hashed_password, name=name)
                flash('Registration successful!', 'success')
                return redirect(url_for('index'))
        except:
            flash('Error occurred during registration. Please try again.', 'error')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        print(f"User {session['username']} already logged in. Redirecting to home.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f"Attempting to log in with username: {username} and password: {password}")

        try:
            user = User.get(User.username == username)
            print(f"User found: {user.username}, {user.password}")

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                session['username'] = username
                print(f"Password match. Logging in user {username}. Session set.")
                return redirect(url_for('home'))
            else:
                print("Password does not match.")
                flash('Invalid username or password. Please try again.', 'error')
        except User.DoesNotExist:
            print("User does not exist.")
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

def send_email_notification(tagged_user_email, peep_content):
    msg = Message('You were tagged in a peep!', 
                  sender='your_email@example.com', 
                  recipients=[tagged_user_email])
    msg.body = f'You were tagged in a peep: {peep_content}'
    mail.send(msg)

@app.route('/post_peep', methods=['POST'])
def post_peep():
    if 'username' not in session:
        flash('Please login to post a peep.', 'error')
        return redirect(url_for('login'))

    username = session.get('username')
    peep_content = request.form['peep_content']

    try:
        user = User.get(User.username == username)
    except User.DoesNotExist:
        flash('Invalid user. Please login again.', 'error')
        return redirect(url_for('login'))

    try:
        peep = Peep.create(content=peep_content, user=user)
        flash('Peep posted successfully!', 'success')

        # Process tagged users
        tagged_users = [word[1:] for word in peep_content.split() if word.startswith('@')]
        for tagged_username in tagged_users:
            try:
                tagged_user = User.get(User.username == tagged_username)
                send_email_notification(tagged_user.email, peep_content)
            except User.DoesNotExist:
                flash(f'User {tagged_username} does not exist.', 'error')
    except:
        flash('Error occurred while posting peep. Please try again.', 'error')

    return redirect(url_for('home'))

@app.route('/home')
def home():
    if 'username' not in session:
        print("User not logged in. Redirecting to login.")
        return redirect(url_for('login'))

    username = session['username']
    print(f"User {username} logged in. Rendering home page.")
    peeps = Peep.select().order_by(Peep.timestamp.desc())
    return render_template('home.html', username=username, peeps=peeps)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

