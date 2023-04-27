from flask import Flask, render_template, g, redirect, url_for
from flask_login import login_user, LoginManager, login_required, current_user
from forms import LoginForm, SignupForm
from flask_uploads import UploadSet,IMAGES, configure_uploads
from models import AppUser as User
from repository import CareerManagerDB as Queries
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///carrers.db'
app.secret_key = 'CareewiseProjectApplication'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.getcwd(), 'static', 'images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app,photos)


queries = Queries()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
  return queries.session.get(User, int(user_id))

@app.before_request
def before_request():
  g.user = current_user

@app.get("/")
def index():
  return render_template("index.html")

def log_report(report):
  with open("report.txt", 'a', encoding='utf-8') as f:
        f.write(f'{report}\n')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  error = None

  if form.validate_on_submit():
    password_hash = generate_password_hash(form.password.data)
    log_report("validated")
    queries.add_user(form.name.data, form.email.data,
                            password_hash)
    log_report("not sure add_user worked")
    user = queries.find_user_by_email(form.email.data)
    # user = User.query.filter_by(email=form.email.data).first()
    if user:
      login_user(user)
    else:
      error = "unsuccesful"
    return redirect(url_for('dashboard')) 
  if form.errors:
    log_report(form.errors)
  return render_template("signup.html", form=form, error=error)

# def validate_user(email, password):
#     user = Queries.find_user_by_email(email=email)
#     if user and check_password_hash(user.password, password):
#         login_user(user)
#         return True
#     else:
#         return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        user = queries.find_user_by_email(email=form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
        #     return True
        # else:
        #     return False
            return redirect(url_for('dashboard'))
        else:
            error = "invalid password / user"

    return render_template("login.html", form=form, error=error)

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
  if not g.user:
    return redirect(url_for('login'))

  return render_template("dashboard.html")