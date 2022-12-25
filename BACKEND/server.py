from flask import Flask, redirect,render_template,jsonify,request,session
import psycopg2
import psycopg2.extras
from Database import DatabaseModel
import json
from Classes import UserAdmin


# Initializing flask app
app = Flask(__name__)

app.config.from_object("config")
app.secret_key=app.config["SECRET_KEY"]

conn=psycopg2.connect(dbname=app.config["DATABASE"],user=app.config["DB_USER"],
password=app.config["DB_PASSWORD"],host=app.config["DB_HOST"])

dbModel= DatabaseModel(app.config["DATABASE"],app.config["DB_USER"],
    app.config["DB_PASSWORD"],app.config["DB_HOST"])


# print("Roadmap year is")
# dbModel1.getCollegesList();

# dbModel1.generateDuties();

# dbModel1.GetRoadMapInfo();

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


@app.route('/loginData', methods=['POST','GET'])
def loginData():
    print("hey")
    data = request.get_json()
    email = data['username']
    password = data['password']
    adminObj=UserAdmin(email,password)
    print("admin obj is : ",adminObj)
    userStatus=False;
    userStatus=dbModel.checkAdminExist(adminObj)
    if(userStatus==True):
        session["uemail"]=adminObj.email
        session["upwd"]=adminObj.password
        #return render page
        print("Admin Exist")
        
    else:
        #return render page
        print("Admin Not Exist")
        #return jsonify({'status': 'failure'})
        return jsonify(success=False)

    print("email : ",email,"  password = " ,password)

    #return jsonify({'status': 'success'})
    #return redirect('/notifications')
    return jsonify(success=True)
    #return  render_template('reactView.html')



@app.route('/data')
def get_time():
    #uList = GetAdminUserInfo()
   # print(uList)
    #jsonString = json.dumps(uList)
    # Returning an api for showing in  reactjs
    return {
        'Name':"geek", 
        "Age":"22",
        "Date":"88/9/0", 
        "programming":"python"
        }
    #return jsonString


@app.route('/')
@app.route('/members')
def members():
    
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

@app.route('/userdata', methods=['GET'])
def userdata():
    userdata = {
        'name': 'John',
        'age': '43',
        'status': 'Active',
        'password': 'ABC123',
        'email': 'john@example.com'
    }
    return jsonify(userdata)


@app.route('/data', methods=['POST'])
def fetchData():
    data = request.get_json()
    username = data['username']
    password = data['password']
    city = data['city']
    status = data['status']
    print(username,password,city,status)
    return jsonify({'status': 'success'})


@app.route('/reactView', methods=['GET'])
def reactView():
    data = {'name': 'John', 'age': 30}
    return render_template('reactView.html', data=data)


# Running app
if __name__ == '__main__':
    app.run(debug=True)