from datetime import datetime
from flask import Flask, render_template, request, session, url_for, redirect
import datetime
#from numpy import array
import pymongo
from twilio.rest import Client
from decouple import config

# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime=datetime.timedelta(days=365)
app.secret_key="super secret key"
#############################################################

#Conectarnos a la base de datos
#############################################################
mongodb_key =config('mongodb_key')
client=pymongo.MongoClient(mongodb_key, tls=True, tlsAllowInvalidCertificates=True) #crea un cliente
db=client.Escuela #conecta a la base de datos escuela
cuentas=db.alumno

#############################################################
# Twilio
#############################################################
account_sid = config('account_sid')
auth_token = config('auth_token')
TwilioClient = Client(account_sid, auth_token)
#############################################################

@app.route('/')
def home():
    email=None
    if "email" in session:
        email=session["email"]
        return render_template('index.html')
    else :
        return render_template('Login.html')

@app.route('/signup', methods=["POST"])
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    return render_template('index.html', data=email)########

@app.route("/login", methods=["GET", "POST"])
def login():
    email = None
    if "email" in session:
        return render_template('index.html', data=session["email"])
    else:
        if (request.method == "GET"):
            return render_template("Login.html", data="email")
        else:
            email2 = request.form["email"]
            password = request.form["password"]
            session["email"] = email

        mail = cuentas.find_one({"email": (email2)})
        passw = cuentas.find_one({"password": (password)})
        if (mail==None or passw==None):
            return render_template("Login.html", data=True)
        elif (mail==passw):
            return render_template("index.html", data=email)
        else:
            return "<p> No existe email</p>"



@app.route('/logout')
def logout():
    if "email" in session:
        session.clear()
        return redirect(url_for("home"))
    else :
        return redirect(url_for("home"))


@app.route("/usuarios")
def usuarios():
    cursor=cuentas.find({})     #nos permite encontrar todo lo que haya en el documento (Alumnos)
    #for para indagar
    users=[]
    for doc in cursor:
        users.append(doc)
    return render_template("/Usuarios.html", data=users)    #crea template

@app.route("/insert", methods=["POST"])
def insertUsers():
    user = {
        #"matricula": request.form["matricula"],
        "name": request.form["name"],
        "email": request.form["email"],
        "password": request.form["password"],
    }
    try:
        cuentas.insert_one(user)
        print("se agregó usuario")
        comogusten = TwilioClient.messages.create(
            from_="whatsapp:+14155238886",
            body="El usuario %s se agregó a tu pagina web" % (
                request.form["name"]),
            to="whatsapp:+5215543898573"
        )
        print(comogusten.sid)
        return redirect(url_for("usuarios"))
    except Exception as e:
        return "<p>El servicio no esta disponible =>: %s %s" % type(e), e



@app.route("/find_one/<matricula>")
def find_one(matricula):
    try:
        user = cuentas.find_one({"matricula": (matricula)})
        if user == None:
            return "<p>La matricula %s nó existe</p>" % (matricula)
        else:
            return "<p>Encontramos: %s </p>" % (user)
    except Exception as e:
        return "%s" % e


@app.route("/delete/<matricula>")
def delete_one(matricula):
    try:
        user = cuentas.delete_one({"matricula": (matricula)})
        if user.deleted_count == None:
            return "<p>La matricula %s nó existe</p>" % (matricula)
        else:
            return redirect(url_for("usuarios"))    
    except Exception as e:
        return "%s" % e


@app.route("/update", methods=["POST"])
def update():
    try:
        filter = {"matricula": request.form["matricula"]}
        user = {"$set": {
            "nombre": request.form["nombre"]
        }}
        cuentas.update_one(filter, user)
        return redirect(url_for("usuarios"))

    except Exception as e:
        return "error %s" % (e)
@app.route('/create')
def create():
    return render_template('Create.html')