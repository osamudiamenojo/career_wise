import requests
import base64
import json
from dotenv import load_dotenv
import os



load_dotenv()
username = os.environ['USERNAME']
password = os.environ['PASSWORD']


def log_report(report):
  with open("report.txt", 'a', encoding='utf-8') as f:
        f.write(f'{report}\n')


class OnetApi:
    # API_BASE_URL = 'https://services.onetcenter.org/ws'
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._headers = {
            'User-Agent': 'python-OnetWebService/1.00 (bot)',
            'Authorization': 'Basic ' + base64.standard_b64encode((self.username + ':' + self.password).encode()).decode(),
            'Accept': 'application/json' }
        self.set_version()
    
    def set_version(self, version = None):
        if version is None:
            self._url_root = 'https://services.onetcenter.org/ws/mnm'
        else:
            self._url_root = 'https://services.onetcenter.org/v' + version + '/ws/'
    
    def _make_request(self, endpoint, params=None,code =None,extra=None):
        if code:
            # if extra:
            #     url = self._url_root+ '/' + endpoint +'/' + code +'/' + extra
            # else:
                url = self._url_root + '/' + endpoint +'/' + code + '/' + 'report'
        else :
            url = self._url_root + '/' + endpoint
        # url = f"{self._url_root}/{endpoint}"
        response = requests.get(url, headers=self._headers, params=params)
        # response = requests.get(url, headers=self._headers)
        response.raise_for_status()
        return response.json()

    def get_extra_info(self,code,extra):
        endpoint = 'careers'
        response_data = self._make_request(endpoint, code=code,extra=extra)
        occupation_data = response_data
        return occupation_data

    def get_occupation(self, code):
        endpoint = '/careers'
        
        response_data = self._make_request(endpoint, code=code)
        # log_report(response_data)
        occupation_data = response_data
        # occupation = Occupation(occupation_data)
        return occupation_data

    def get_education_training(self, code):
        occupation = self.get_occupation(code)
        return occupation.education_training

    def get_career_info(self, code):
        occupation = self.get_occupation(code)
        return occupation.summary

    def search_occupations(self, keyword):
        endpoint = 'search'
        params = {'keyword': keyword}
        response_data = self._make_request(endpoint, params=params)
        # log_report(response_data)
        results = response_data['career']
        return [(result['title'],result['code']) for result in results]

class Occupation:
    def __init__(self, occupation_data):
        self.code = occupation_data['code']
        self.title = occupation_data['title']
        self.description = occupation_data['description']
        self.summary = occupation_data['summary']
        self.education_training = []
        self._set_education_training(occupation_data)

    def _set_education_training(self, occupation_data):
        education_training = occupation_data.get('educationTraining')
        if education_training:
            for item in education_training:
                self.education_training.append(item['value'])

api = OnetApi(username=f"{username}", password=f"{password}")

