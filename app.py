from flask import Flask, render_template, g, redirect, url_for, request
from flask_login import login_user, LoginManager, login_required, current_user
from forms import LoginForm, SignupForm
from flask_uploads import UploadSet,IMAGES, configure_uploads
from models import AppUser as User
from repository import CareerManagerDB as Queries
import os
from werkzeug.security import check_password_hash, generate_password_hash
from onet_api import OnetApi as ONetAPI
from private import username, password

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///carrers.db'
app.secret_key = 'CareewiseProjectApplication'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.getcwd(), 'static', 'images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app,photos)

api = ONetAPI(username=f"{username}", password=f"{password}")

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


def log_report(report):
  with open("report.txt", 'a', encoding='utf-8') as f:
        f.write(f'{report}\n')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  error = None

  if form.validate_on_submit():
    password_hash = generate_password_hash(form.password.data)
    queries.add_user(form.name.data, form.email.data,
                            password_hash)
    user = queries.find_user_by_email(form.email.data)
    # user = User.query.filter_by(email=form.email.data).first()
    if user:
      login_user(user)
    else:
      error = "unsuccesful"
    return redirect(url_for('dashboard')) 
  if form.errors:
    log_report
  return render_template("signup.html", form=form, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        user = queries.find_user_by_email(email=form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
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


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route('/search_results', methods=['POST'])
def search_results():
    keyword = request.form['yut'] #to be changed
    occupation_codes = api.search_occupations(keyword)#use better namess
    # occupations = []
    # for title in occupation_codes:
    #     # occupation = api.get_occupation(code)
    #     occupations.append(title)
    
    return render_template('search_result.html', occupations=occupation_codes)

def extract_resource(occupation):
  lst =[]
  for items in occupation['resources']['resource']:
    lst.append(items['title'])
  return lst

@app.route('/occupation/<code>')
def occupation_details(code):
    occupation = api.get_occupation(code)
    # resources = occupation['resources']['resource']
    extra = extract_resource(occupation)
    log_report(extra)
    if 'Education' in extra:
      education_info = api.get_extra_info(code,'education')
      education = education_info['education_usually_needed']['category']

    if 'Knowledge' in extra:
      knowledge_info = api.get_extra_info(code,'knowledge')
      knowledge = knowledge_info['group']
    if 'Skills' in extra:
      skill_info = api.get_extra_info(code,'skills')
      skills = skill_info['group']
    # if 'personality' in extra:
    #   log_report(api.get_extra_info('personality'))
    
    return render_template('eachcareer.html', occupation=occupation,education=education,knowledge=knowledge,skills=skills)




@app.route("/search", methods=["GET", "POST"])
def search():

  return render_template('search.html')


@app.route('/careers', methods = ['GET'])
def careers():
    return render_template('careers.html')

@app.route('/eachcareer', methods =['GET'])
def eachcareer():
    return render_template('eachcareer.html')