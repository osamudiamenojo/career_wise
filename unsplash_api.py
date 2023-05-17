import requests
from dotenv import load_dotenv
import os

load_dotenv()


def log_report(report):
  with open("report.txt", 'a', encoding='utf-8') as f:
        f.write(f'{report}\n')

class UnsplashApi():
    # Replace 'YOUR_ACCESS_KEY' with your actual Unsplash access key
    ACCESS_KEY = os.environ['ACCESS_KEY']

    url = f'https://api.unsplash.com/search/photos'

    def make_request(self,endpoint):
        url = UnsplashApi.url+'/'+endpoint
        response = requests.get(url)
        return response

    def get_image(self,keyword):
        endpoint =f'?query={keyword}&client_id={UnsplashApi.ACCESS_KEY}'
    # Process the response
        response = self.make_request(endpoint)
        data = response.json()
        images = data['results']
        log_report(images)
        # Extract the URLs of the images
        for image in images:
            if image['height'] < 4000:
                return image["urls"]['regular']
        return images[0]['urls']['raw']

# api = UnsplashApi()
# img = api.get_image("doctor")
# print(img)
