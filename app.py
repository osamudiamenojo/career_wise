from flask import Flask, render_template, g, redirect, url_for, request
import os
from onet_api import OnetApi as ONetAPI, username, password
from unsplash_api import UnsplashApi

app = Flask(__name__)
app.secret_key = 'CareewiseProjectApplication'

CareerApi = ONetAPI(username=f"{username}", password=f"{password}")
ImageApi = UnsplashApi()

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
  return render_template('careers.html', industries = industries)

@app.route('/industry/<code>', methods = ['GET'])
def careers_in_industry(code):
  careers = CareerApi.get_career(code)
  return render_template('industry.html', occupations = careers)

@app.route('/profiler/<question>/<int:start>', methods=["GET", "POST"])
def profiler(question,start):
  
  if request.method == "POST" :
    user_answer = request.form.to_dict()
    for i,j in user_answer.items():
      CareerApi.result[int(i)-1]=j
    # log_report(CareerApi.result)
  questions = CareerApi.get_profiler(question,start)
  quest = questions['question']
  answer = questions['answer_options']['answer_option']
  return render_template('profiler.html',question=quest, answer=answer,start=start,type=question,max=CareerApi.profiler)

@app.route("/profiler/results",methods=['POST'])
def results():
  user_answer = request.form.to_dict()
  for i,j in user_answer.items():
    CareerApi.result[int(i)-1]=j
  # log_report(CareerApi.result)
  results = CareerApi.get_profiler_results()
  result  = results['career']
  return render_template('result.html',result = result)

@app.route("/about", methods=["GET"])
def about():
  return render_template("about.html")

@app.route("/project_team", methods=["GET"])
def project_team():
  return render_template("project_team.html")

@app.route("/contact", methods=["GET"])
def contact():
  return render_template("contact.html")