from datetime import datetime
from flask import Flask, render_template, request, session, url_for, redirect
import datetime
import pymongo
# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime=datetime.timedelta(days=365)
app.secret_key="super secret key"
#############################################################

#Conectarnos a la base de datos
#############################################################
mongodb_key="mongodb+srv://desarrollowebuser:<password>@cluster0.x11il.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client=pymongo.MongoClient(mongodb_key, tls=True, tlsAllowInvalidCertificates=True) #crea un cliente
db=client.Escuela #conecta a la base de datos escuela
cuentas=db.Alumno

#############################################################



@app.route('/')
def home():
    email=None
    if "email" in session:
        email=session["email"]
        return render_template('index.html')
    else :
        return render_template('Login.html')

@app.route('/signup')
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    return render_template('index.html', data=email)

@app.route("/login", methods=["GET", "POST"])
def login():
    email = None
    if "email" in session:
        return render_template('index.html', data=session["email"])
    else:
        if (request.method == "GET"):
            return render_template("Login.html", data="email")
        else:
            email = request.form["email"]
            password = request.form["password"]
            session["email"] = email
            return render_template("index.html", data=email)


@app.route('/logout')
def logout():
    if "email" in session:
        session.clear()
        return redirect(url_for("home"))
    else :
        return redirect(url_for("home"))


@app.route("\datos")
def usuarios():
    cursor=cuentas.find({})     #nos permite encontrar todo lo que haya en el documento (Alumnos)
    #for para indagar
    users=[]
    for doc in cursor:
        users.append(doc)
    return render_template("\usuarios.html", data=users)    #crea template
