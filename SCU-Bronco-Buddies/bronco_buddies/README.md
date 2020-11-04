## Structure of Bronco Buddies

### This directory contains the content for the flask app. The structure is as follows: 

```bash
.
├── README.md
├── bronco_buddies
│   ├── __init__.py
│   ├── forms.py
│   ├── broncoBuddies.db
│   ├── models.py
│   ├── routes.py
│   ├── static
│   │   ├── iamges
│   │   └── main.css
│   └── templates
│       ├── README.md
│       ├── about.html
│       ├── form.html
│       ├── home.html
│       ├── layout.html
│       ├── login.html
│       ├── profile.html
│       ├── register.html
├── requirements.txt
└── run.py
```

* models.py - contains classes for app's databases
* routes - all website urls 
* run.py - main python file, used to run the app 
* forms.py - where all user forms are configured
* templates - the html files that can have embedded jinja (language to connect with flask app data)
* static - images and css files
* images - all logos, images 

## To Run Application 

1. Make sure Flask and all dependencies are installed 
 - Flask 
 - Flask-SQLAlchemy (pip install -U Flask-SQLAlchemy)
   - database ORM
 - Flask login (pip install flask-login)
   - for login validation
 - Flask-Bcrypt (pip install bcrypt)  
   - for password encryption 
 - Flask-WTF (pip install Flask-WTF)
   - for login, registration, and preference forms 
2. In terminal: 
```bash
export FLASK_APP=run.py
export export FLASK_DEBUG=1 
flask run -h localhost -p (port you want to run application on)
```
Or you can do: 
```bash
python run.py
```

