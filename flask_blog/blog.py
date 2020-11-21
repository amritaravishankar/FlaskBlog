from flask import Flask, render_template, request, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '735d0d18695bfe32c861a12bcde8497f'
app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    image_file=db.Column(db.String(20), nullable=False, default='default.jpg')
    password=db.Column(db.String(60), nullable=False) #hashing creates a 60 character string
    posts=db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}') "

posts = [
    {
        "author": "Amrita",
        "title": "Blog 1",
        "content": 'Blog Post 1 content',
        "date": "Septemeber 30, 2020"
    },
    {   "author": "Suchi",
        "title": "Blog 2",
        "content": 'Blog Post 2 content',
        "date": "October 1, 2020"
    }    
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title = "About")

@app.route("/register", methods = ['GET', 'POST'])
def register():
   form = RegistrationForm()
   if form.validate_on_submit():
       flash(f'Account created for {form.username.data}!', 'success') 
       return redirect(url_for('home'))
   return render_template('register.html', title = 'Register', form = form)

@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)
