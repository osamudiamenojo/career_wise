import requests
import base64
import json
import os
from dotenv import load_dotenv

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
    
    def _make_request(self, endpoint, params=None,code =None):
        if code:
                url = self._url_root + '/' + endpoint +'/' + code + '/' + 'report'
        else :
            url = self._url_root + '/' + endpoint
        # url = f"{self._url_root}/{endpoint}"
        response = requests.get(url, headers=self._headers, params=params)
        # response = requests.get(url, headers=self._headers)
        response.raise_for_status()
        return response.json()

    def get_occupation(self, code):
        endpoint = '/careers'    
        response_data = self._make_request(endpoint, code=code)
        # log_report(response_data)
        occupation_data = response_data
        # occupation = Occupation(occupation_data)
        return occupation_data  

    def search_occupations(self, keyword):
        endpoint = 'search'
        params = {'keyword': keyword}
        response_data = self._make_request(endpoint, params=params)
        # log_report(response_data)
        results = response_data['career']
        return [(result['title'],result['code']) for result in results]
    
    def get_profiler(self,questions,start=1):
        endpoint = f"interestprofiler/{questions}?start={start}&end={start+11}"
        response_data = self._make_request(endpoint)
        
        return response_data  

