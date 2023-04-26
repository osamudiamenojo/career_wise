from flask import Flask, render_template, g, redirect, url_for
from flask_login import login_user, LoginManager, login_required, current_user
from forms import LoginForm, SignupForm
from flask_uploads import UploadSet,IMAGES, configure_uploads
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///carrers.db'
app.config["SECRET_KEY"] = "tspproject"
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.getcwd(), 'static', 'images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app,photos)

db.init_app(app)
queries = Queries(db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
  return db.session.get(User, int(user_id))

@app.before_request
def before_request():
  g.user = current_user

@app.get("/")
def index():
  return render_template("index.html")

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
  form = SignupForm()
  error = None

  if form.validate_on_submit():
    queries.create_new_user(form.name.data, form.email.data,
                            form.password.data)
    user = User.query.filter_by(email=form.email.data).first()
    if user:
      login_user(user)
    else:
      error = "unsuccesful"
    return redirect(url_for('dashboard'))
  return render_template("signup.html", form=form, error=error)

def validate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and queries.validate_password(email, password):
        login_user(user)
        return True
    else:
        return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        if validate_user(form.email.data, form.password.data):
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