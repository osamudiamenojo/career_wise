from flask import Flask, render_template, g, redirect, url_for, request
from flask_login import login_user, LoginManager, login_required, current_user
from flask_uploads import UploadSet,IMAGES, configure_uploads
# from repository import CareerManagerDB as Queries
import os
from werkzeug.security import check_password_hash, generate_password_hash
from onet_api import OnetApi as ONetAPI, username, password

app = Flask(__name__)
app.secret_key = 'CareewiseProjectApplication'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.getcwd(), 'static', 'images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app,photos)

api = ONetAPI(username=f"{username}", password=f"{password}")


@app.before_request
def before_request():
  g.user = current_user


def log_report(report):
  with open("report.txt", 'a', encoding='utf-8') as f:
        f.write(f'{report}\n')

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
  if not g.user:
    return redirect(url_for('login'))

  return render_template("dashboard.html")


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("careers"))


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
  # log_report(occupation['resources'])
  for items in occupation['career']['resources']['resource']:
    lst.append(items['title'])
  return lst

@app.route('/occupation/<code>')
def occupation_details(code):
    occupation = api.get_occupation(code)
    extra = extract_resource(occupation)
    # log_report(extra)
    if 'Education' in extra:
      education = occupation['education']['education_usually_needed']['category']
    if 'Knowledge' in extra:
      knowledge = occupation['knowledge']['group']
    if 'Skills' in extra:
      skills = occupation['skills']['group']
    if 'Personality' in extra:
      personality = occupation['personality']
    if 'Abilities' in extra:
      abilities = occupation['abilities']['group']
    if 'Technology' in extra:
      technology = occupation['technology']['category']
    
    return render_template('eachcareer.html', occupation=occupation,education=education,knowledge=knowledge,skills=skills, personality=personality,abilities=abilities,technology=technology)




@app.route("/search", methods=["GET", "POST"])
def search():

  return render_template('search.html')


@app.route('/careers', methods = ['GET'])
def careers():
    return render_template('careers.html')

@app.route('/eachcareer', methods =['GET'])
def eachcareer():
    return render_template('eachcareer.html')

@app.route('/profiler/<start>', methods=["GET", "POST"])
def profiler(start):
  results = ["0"]*60
  if request.method == "POST" :
    user_answer = request.form["options"]
  questions = api.get_profiler('questions')
  # for num in range 

  return render_template('profiler.html',questions)
