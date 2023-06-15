# career_wise
Team Software Project For Kibo Developers
Careerwise is a web application that helps secondary school students discover and learn about potential career paths. 
This version will also enable users to view different career options and get a recommendation on best career choice after taking a career test 


## Set Up

To run this application locally, you need make use of the onet api. Read the docs [here](https://services.onetcenter.org/reference/). You will need a username and password to run locally.  Clone the project on your preferred IDE and add your username and password to your .env file as **API_USERNAME** and **PASSWORD** . Also you'll need the unsplash API for images. Read the docs [here](https://unsplash.com/documentation) Add your key to the .env file as **ACCESS_KEY**. 

make sure you are in the project folder on your terminal then create a virtual environment using
```dotnetcli
python3 -m venv env 
```
Activate the environment using
```dotnetcli
.\env\scripts\activate
```
install the dependencies using 
```powershell-interactive
  pip install -r requirements.txt
```
Run the application using
```azurepowershell
  flask run
```
Your app should be running on port 5000

[](http://127.0.0.1:5000)



## Credits
- This projects makes use of two API's from onet and unsplash

## Hosting 
This app is hosted on render and can be accessed from this link [here](https://careerwise.onrender.com/careers)
