from flask import Flask,render_template,jsonify,request,session
import psycopg2
import psycopg2.extras
from Database import DatabaseModel
import json

# Initializing flask app
app = Flask(__name__)

app.config.from_object("config")
app.secret_key=app.config["SECRET_KEY"]

conn=psycopg2.connect(dbname=app.config["DATABASE"],user=app.config["DB_USER"],
password=app.config["DB_PASSWORD"],host=app.config["DB_HOST"])

@app.route('/listData')
def listData():
    #cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur=conn.cursor()
    query="Select * from users"
    cur.execute(query)
    list_users=cur.fetchall()
    #list_users=json.dumps(list_users[0])
    #return render_template("user.html",list_users=list_users)
    #return  {"list_users":["Member11","Member22","Member33"]}
    row=json.dumps(list_users)
   # return row
    return {"list_users":[row]}


@app.route('/')
@app.route('/members')
def members():
    return {"members":["Member1","Member2","Member3"]}
    
@app.route("/loginAdmin", methods=["POST"])
def loginAdmin():

    username=request.json['username']
    password=request.json['password']
    print("user name = ",username)
    print("password = ",password)
    return {"members":["Member1","Member2","Member3"]}


@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    if request.method=="POST":
        email = request.form["emailId"]
        pwd = request.form["pwdId"]
    else:
        email = request.args.get("emailId")
        pwd = request.args.get("pwd")

    session["uemail"]=email
    session["upwd"]=pwd

    print("email= ", email, "pwd=", pwd)
    dbModel= DatabaseModel(app.config["DATABASE"],app.config["DB_USER"],
    app.config["DB_PASSWORD"],app.config["DB_HOST"])

    status=dbModel.checkAdminExist(email,pwd)
    print(status)

    print(email)
    print(pwd)
    #print(sd)
    row=json.dumps(email)
    return row
    #return {"members":["Member1","Member2","Member3"]}


# Running app
if __name__ == '__main__':
    app.run(debug=True)