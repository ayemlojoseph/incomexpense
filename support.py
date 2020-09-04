#if your .env is not working, you need to source it in
#checking if it can be read then source it
ls -la

source.env 

#Using Sendgrid for email
 create api from sendgrid
 https://app.sendgrid.com/settings/api_keys


#settings.py
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = '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'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
#There are also optional settings to deliver emails in debug mode or to send them to standard output:
# Toggle sandbox mode (when running in DEBUG mode)
SENDGRID_SANDBOX_MODE_IN_DEBUG=True

# echo to stdout or any other file-like object that is passed to the backend via the stream kwarg.
SENDGRID_ECHO_TO_STDOUT=True


pip install django-sendgrid-v5


#pdb is a python debugger
import pdb
pdb.set_trace()
#this allows you to pause your program excution and use the terminal to debug


#.env setup using python-decouple

pip3 install python-decouple
from decouple import config
#sample usage
SENDGRID_API_KEY = config('SENDGRID_API_KEY')
SECRET_KEY =#hln71x$utfo^b#4%#9=rfgntlkfv)d*0i*1by8j4d1cowa@qy

#deploying to heroku

pip3 install django-heroku
#import in settings.py

# Configure Django App for Heroku.
import django_heroku
django_heroku.settings(locals())


# normally we use locahost but in order to host on heroku
#we need an http server
#we will be using gunicorn
pip3 install gunicorn

pip3 freeze > requirements.txt

#defining our heroku should run our application
#setup a web proccess using Procfile
#  create Procfile

#isntlall heroku cli on your machine
$ apt-get update
$ wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
$ heroku update


heroku login on terminal
provide your login credentials


#push to github
git init
git add .
git commit -m "incomeexpenseapi" -m"This is an api for income and expense for user"
git push
git remote add origin git@github.com:ayemlojoseph/incomexpense.git
git remote -v
git push -f origin master


#creating app on heroku cli

heroku create appname

git push heroku master

