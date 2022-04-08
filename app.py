from datetime import datetime
from flask import Flask, render_template, request, session 
import datetime
# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime=datetime.timedelta(days=365)
app.secret_key="super secret key"
#############################################################

@app.route('/')
def home():
    email=None
    if "email" in session:
        email=session["email"]
        return render_template('index.html')
    else :
        return render_template('Login.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    email = None
    if email in session:
        return render_template("index.html", data=session["email"])
    else:
        if (request.method == "GET"):
            return render_template("Login.html", data="email")
        else:
            
            email = request.form["email"]
            password = request.form["password"]
            session["email"]=email
            return render_template("index.html", data=email)


@app.route('/estructuradedatos')
def prueba():
    nombres = []
    nombres.append({"nombre": "ruben",

                    "Semetre01": [{
                        "matematicas": "8",
                        "español": "7"
                    }],
                    "Semetre02": [{
                        "programacion": "5",
                        "basededatos": "9"
                    }]
                    })

    return render_template("home.html", data=nombres)
