from flask import Flask, render_template, g, redirect, url_for, request
from flask_login import login_user, LoginManager, login_required, current_user
from flask_uploads import UploadSet,IMAGES, configure_uploads
# from repository import CareerManagerDB as Queries
import os
from werkzeug.security import check_password_hash, generate_password_hash
from onet_api import OnetApi as ONetAPI, username, password
from unsplash_api import UnsplashApi

app = Flask(__name__)
app.secret_key = 'CareewiseProjectApplication'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.getcwd(), 'static', 'images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app,photos)

CareerApi = ONetAPI(username=f"{username}", password=f"{password}")
ImageApi = UnsplashApi()


@app.before_request
def before_request():
  g.user = current_user


def log_report(report):
  with open("report.txt", 'a', encoding='utf-8') as f:
        f.write(f'{report}\n')


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route('/search_results', methods=['POST'])
def search_results():
    keyword = request.form['yut'] #to be changed
    occupation = CareerApi.search_occupations(keyword)#use better names
    if occupation[0] == None:
      occupation = None
    return render_template('search_result.html', occupations=occupation)

def extract_resource(occupation):
  lst =[]
  for items in occupation['career']['resources']['resource']:
    lst.append(items['title'])
  return lst

@app.route('/occupation/<code>')
def occupation_details(code):
    occupation = CareerApi.get_occupation(code)
    extra = extract_resource(occupation)
    title = occupation['career']['title']
    img_src= ImageApi.get_image(title)
    knowledge,education,skills,abilities,technology,personality = None,None,None,None,None,None
    if 'Education' in extra:
      if 'education_usually_needed' in occupation['education']:
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
    
    return render_template('eachcareer.html', occupation=occupation,education=education,knowledge=knowledge,skills=skills, personality=personality,abilities=abilities,technology=technology,img_src=img_src)


@app.route('/careers', methods = ['GET'])
def careers():
  industries = CareerApi.get_industries()
  log_report(industries)
  return render_template('careers.html', industries = industries)


@app.route('/profiler/<start>', methods=["GET", "POST"])
def profiler(start):
  if request.method == "POST" :
    user_answer = request.form.to_dict()
    for i,j in user_answer.items():
      CareerApi.RESULTS[int(i)-1]=j
    log_report(CareerApi.RESULTS)
  questions = CareerApi.get_profiler('questions',start)
  question = questions['question']
  answer = questions['answer_options']['answer_option']
  return render_template('profiler.html',question=question, answer=answer,start=start)

@app.route("/profiler/results",methods=['POST'])
def results():
  user_answer = request.form.to_dict()
  for i,j in user_answer.items():
    CareerApi.RESULTS[int(i)-1]=j
  log_report(CareerApi.RESULTS)
  results = CareerApi.get_profiler_results()
  result  = results['career']
  return render_template('result.html',result = result)