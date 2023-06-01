import random
from flask import Flask, redirect,render_template,jsonify,request,session
import psycopg2
import psycopg2.extras
from Database import DatabaseModel
import json
from Classes import UserAdmin,DisplayDuty
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import os

# Initializing flask app
app = Flask(__name__)

app.config.from_object("config")
app.secret_key=app.config["SECRET_KEY"]
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)


conn=psycopg2.connect(dbname=app.config["DATABASE"],user=app.config["DB_USER"],
password=app.config["DB_PASSWORD"],host=app.config["DB_HOST"])

dbModel= DatabaseModel(app.config["DATABASE"],app.config["DB_USER"],
    app.config["DB_PASSWORD"],app.config["DB_HOST"])

dbModel.getExaminerName(4)




# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/createToken", methods=["POST"])
def createToken():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)




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

    # Creating Access Token

    if(userStatus==True):
        session["uemail"]=adminObj.email
        session["upwd"]=adminObj.password
        access_token = create_access_token(identity=email)
        #return render page
        print("Admin Exist")
        
    else:
        #return render page
        print("Admin Not Exist")
        #return jsonify({'status': 'failure'})
        return jsonify(success=False)

    print("email--- : ",email,"  password = " ,password)

    #return jsonify({'status': 'success'})
    #return redirect('/notifications')
    return jsonify({'success':True,'access_token':access_token})
    #return  render_template('reactView.html')

#()


@app.route('/generatePracDuties', methods=['GET'])
def generatePracDuties():
     try:
        status1=dbModel.checkDutyGenerateStatus()
        print("Hello World")
        return jsonify({'success':True})
        if(status1==True):
            #dbModel.generateDuties();
            return jsonify({'success':True})
        return jsonify({'success':False})
     except Exception as e:
         print("Exception in genrate duties : ",e) 
    # userdata = {
    #     'name': 'John',
    #     'age': '43',
    #     'status': 'Active',
    #     'password': 'ABC123',
    #     'email': 'john@example.com'
    # }
    # return jsonify(userdata)


    #return jsonify(success=True)
   


def makePracDutyObj(list1):
    print("In make prac")
    listShowDuty=[]
    for duty in list1:
      list2=[]
      clgInfo=dbModel.getCollegeInfo(duty[0])
    #   dept='it'
    #   if int(duty[1])==1:
    #     dept='cs'    

      semCrsInfo=dbModel.getSemInfo(duty[2],duty[3],duty[1])
      print("semCrsInfo ---===> ",semCrsInfo)

      #(6, '2 ', '2020', 'CS 302', 5)
      print("obj-->.",clgInfo[0],clgInfo[5],duty[1],duty[3],semCrsInfo[1],semCrsInfo[0],duty[4])
    #   DisplayDutyObj=DisplayDuty(clgInfo[0],clgInfo[5],dept,duty[3],semCrsInfo[1],semCrsInfo[0]
    #   ,duty[4])

      list2.append(clgInfo[0])
      list2.append(clgInfo[5])
      list2.append(duty[1])
      list2.append(duty[3])
      list2.append(semCrsInfo[1]) 
      list2.append(semCrsInfo[0])
      list2.append(duty[4])

      if(int(duty[5])==0):
        list2.append("Not Assigned")
      if(int(duty[5])==1):
        list2.append("Pending")
      if(int(duty[5])==2):
        list2.append("Accepted")
      if(int(duty[5])==3):
        list2.append("Rejected")
    

      print("\n\nlist in getallprac duties ---- > > > : \n\n",list2)

      listShowDuty.append(list2)
    return listShowDuty 


@app.route('/getAllPraticalList')
def getAllPraticalList():
    list2=dbModel.getAllPraticalDuty()
    print("List of pract duty---------------->>>>>",list2)
    list1=makePracDutyObj(list2)
    print("list1 iii--->> ",list1)

    return json.dumps(list1)


@app.route('/getDutiesList',methods=['GET'])
def getDutiesList():
    type=request.args.get("typeduty")
    if int(type)==4:
       list2= dbModel.getAllPraticalDuty()
    else:
       list2=dbModel.getTypeDutiesList(int(type))

    print("type of duty is : ",type)
    print("List of pract duty---------------->>>>>",list2)
    list1=makePracDutyObj(list2)
    print("list1 iii--->> ",list1)
    return json.dumps(list1)


@app.route('/getAdminNtfList')
def getAdminNtfList():
    print("admin admin")
    ntfList=dbModel.getAdminNotificationsPrac()
    notifications=[]
    i=0
    for list2 in ntfList:
        list1=[]
        exm=dbModel.getExaminerName(list2[0])
        for l1 in list2:
            list1.append(l1)
        list1.append(exm[0])
        notifications.append(list1)
        
    print("ntflist-- ",ntfList)
    print("update ntfList -- ",notifications)

    return json.dumps(notifications)

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

@app.route("/getCrsInfo",methods=['POST','GET'])
def getCrsInfo():
    data = request.get_json()
    print("data is : ",data)

    college = data['ClgDropdownValue']
    dept = data['deptValue']
    course=data['courseValue']
    print("College is : ===>>>>>>>> ::: ",college,dept,course)
    courseName=course.split(' - ')
    print("-----course name is : ",courseName)

    #examiners=dbModel.getRankedExaminer('Data Structures and Algorithms Lab')
    examiners=dbModel.getRankedExaminer(courseName[1])
    
    data['examiners']=examiners
    acId=dbModel.getCollegeId(college[0])
    #data['acId']=acId
    data['practicalDutyId']=dbModel.getPracticalDutyId(acId,dept,course[0])

    print("data after exminer is : ",data)
    userdata = {
        'success':True,
        'data':data,
    }
    return jsonify(userdata)

@app.route("/sendPracticalDuty",methods=['POST'])
def sendPracticalDuty():
    print("\n\n\n\tIn send practical function")
    data = request.get_json()
    print("send Practical----pract data send is data is : ",data)
    examiner=data['examiner']
    college=data['college']

    print("\n\n college is : ",college)
    collegeId=dbModel.getCollegeId(college)
    dept=data['deptValue']
    courseInfo=data['courseValue']
    moreInfo=data['moreInfo']

    course=courseInfo.split(" - ");
    print("pract data send is data is : ",data)

    print("CollegeId is : ",collegeId)
    pracId=dbModel.getPracticalDutyId(collegeId,dept,course[0])
    dbModel.savePracticalDuty(pracId,examiner[3],moreInfo)

    print("\n\n-------------->> pract duty id : ",pracId)
    userdata = {
        'success':True,
        'data':data,
    }
    return jsonify(userdata)

@app.route('/updateAdminNtf', methods=['POST'])
def updateAdminNtf():
    print("in notfication updating")
    data = request.get_json()
    practId=data['practId']
    print("Notification data is : ",data)
    print("Practical Id is : ",practId)
    dbModel.updateAdminNotifications(int(practId))
    userdata = {
        'success':True,
        'data':data,
    }
    return jsonify(userdata)



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
    print("data is : ",data)
    username = data['username']
    password = data['password']
    # city = data['city']
    # status = data['status']
    # print(username,password,city,status)
    print(username,password)
    return jsonify({'status': 'success'})


@app.route('/reactView', methods=['GET'])
def reactView():
    data = {'name': 'John', 'age': 30}
    return render_template('reactView.html', data=data)

#form1
@app.route('/api/<num>')
def api(num):
    numbers = random.sample(range(1, int(num)+1), 5)
    return jsonify(numbers)

@app.route("/updateCrs",methods=['GET'])
def updateCrs():
    clgName = request.args.get("clgname")
    dept1=request.args.get("dept")
   
    #if clgName!=None and len(clgName)!=0:
    print("seleected value==========> :","   ",clgName,"  department -->>>",dept1)
    clgId=dbModel.getCollegeId(clgName)
    print("=================clgIg=",clgId)

    rdYear=dbModel.getCollegeRoadMapYear(clgId[0],dept1)
    crsList=dbModel.getCollegeCourses(clgId[0],dept1)
    print("Years are : ",rdYear)
    coursesInfo=[]
    for courseCode in crsList:
        print("Course is : ",courseCode)
        course1=dbModel.getCollegeCourseInfo(rdYear,dept1,courseCode)
        if course1!=None and len(course1)!=0:
            coursesInfo.append(course1[1]+" - "+course1[0])
    
    #print("courses list detail is : ",coursesInfo)
    #return jsonify(crsList)
    return jsonify(coursesInfo)

    
@app.route("/getTeacherDetail",methods=['GET'])
def getTeacherDetail():
    acId=request.args.get("acId")
    dept=request.args.get("dept")
    crsCode=request.args.get("crsCode")
    print("to get teacher ",acId,"--",dept,"--",crsCode)
    exmId=dbModel.getTeacherId(acId,dept,crsCode)
    if(exmId[0]==None or len(exmId)==0):
        print("exm id null")
        return ({"success":"false",
                    "examiner":None})

    print("examiner Id is : ",exmId)
    teacher=dbModel.getTeacherDetail(exmId)
    print("teacher detail is : ",teacher)
    return({"success":"true",
            "examiner":teacher
    })

# #axios    
# @app.route('/updateCrs/<selected_value>/', methods=['GET'])
# def updateCrs(selected_value):
#     print("seleected value==========> :",selected_value,"   ")
#     crsList=dbModel.getCollegeCourses(selected_value)
#     return jsonify(crsList)



@app.route('/randomNumbers', methods=['GET'])
def random_numbers():
    valueOne = request.args.get('valueOne')
    random_numbers = random.sample(range(1, int(valueOne)+1), 5)
    return jsonify({"random_numbers": random_numbers})

@app.route('/randomFruitsOrVegetables', methods=['GET'])
def random_fruits_or_vegetables():
    valueTwo = request.args.get('valueTwo')
    fruits = ["Apple", "Orange", "Banana", "Mango", "Grapes"]
    vegetables = ["Tomato", "Onion", "Carrot", "Potato", "Cucumber"]
    if int(valueTwo)%2 == 0:
        random_fruits_or_vegetables = random.sample(fruits, 5)
    else:
        random_fruits_or_vegetables = random.sample(vegetables, 5)
    return jsonify({"random_fruits_or_vegetables": random_fruits_or_vegetables})

#reactform


#Flask Backend Code
@app.route("/getAllCollegeList")
def getAllCollegeList():
    clgList=dbModel.getAllCollege()
    return json.dumps(clgList)


@app.route('/fetchRandomNumbers/<selected_value>/', methods=['GET'])
def fetchRandomNumbers(selected_value):
    print("seleected value :",selected_value,"   ")

    list_of_numbers = []
    for i in range(1, int(selected_value)+1):
        list_of_numbers.append(i)
    random_numbers = random.sample(list_of_numbers, 5)
    return jsonify(random_numbers)

@app.route('/fetchRandomFruits/', methods=['GET'])
def fetchRandomFruits():
    fruits = ["Apple", "Mango", "Banana", "Strawberry", "Orange"]
    random_fruits = random.sample(fruits, 5)
    return jsonify(random_fruits)

@app.route('/fetchRandomVegetables/', methods=['GET'])
def fetchRandomVegetables():
    vegetables = ["Carrot", "Potato", "Cabbage", "Tomato", "Cucumber"]
    random_vegetables = random.sample(vegetables, 5)
    return jsonify(random_vegetables)


#fetch form

# @app.route('/getRandomNumbers', methods=['GET'])
# def get_random_numbers():
#     num = request.args.get('num')
#     numbers = [random.randint(1, int(num)) for _ in range(5)]
#     return jsonify(numbers)

# @app.route('/getRandomFruits', methods=['GET'])
# def get_random_fruits():
#     fruits = ['apple', 'banana', 'strawberry', 'pear', 'grape']
#     random_fruits = random.choices(fruits, k=5)
#     return jsonify(random_fruits)

# @app.route('/getRandomVegetables', methods=['GET'])
# def get_random_vegetables():
#     vegetables = ['carrot', 'potato', 'pepper', 'cucumber', 'onion']
#     random_vegetables = random.choices(vegetables, k=5)
#     return jsonify(random_vegetables)


#Flask Backend Code
@app.route('/fetchRandomNumbersList', methods=['GET'])
def fetch_random_numbers():
    random_numbers = random.sample(range(1, 10), 5)
    return jsonify({'random_numbers': random_numbers})

@app.route('/fetchRandomFruitsList', methods=['GET'])
def fetch_random_fruits():
    fruits = ['apple', 'banana', 'strawberry', 'pear', 'grape']
    random_fruits = random.choices(fruits, k=5)
    return jsonify({'random_fruits': random_fruits})

@app.route('/fetchRandomVegetablesList', methods=['GET'])
def fetch_random_vegetables():
    vegetables = ['carrot', 'potato', 'pepper', 'cucumber', 'onion']
    random_vegetables = random.choices(vegetables, k=5)
    return jsonify({'random_vegetables': random_vegetables})





###################################################################################


@app.route('/getCourseName',methods = ["GET"])
def getCourseName():
    List = dbModel.getCoursesName()
    # print("posting......")
    # print(List)
    if List != None:
        return jsonify(List)
    return "'key': 'empty'"


@app.route('/getDataFromReact',methods=["POST"])
def setTime():
    if request.method == 'POST':
        FileName=request.form['fileName']
        dataOfFile=request.form['ArrayList']
        DictionaryOfdata=json.loads(dataOfFile)
        
        for e in DictionaryOfdata:
            dbModel.insertRoadmap(json.dumps(e))
        DictionaryOfdata[0]
        # print(f'Posting....{FileName}{DictionaryOfdata[0]}{DictionaryOfdata[0]["rd_crs_code"]}')
        return "Hello"
    print('Wrong')
    return "Hello"

@app.route('/set_data',methods = ["GET"])
def set_data():
    List = dbModel.getRoadMapList()
    print("posting......")
    #print(List)
    if List != None:
        return jsonify(List)
    return "'key': 'empty'"

@app.route('/send_data', methods=["POST","GET"])
def send_data():
    course = None
    id = request.get_json()
    course = dbModel.getcourse(id)
    print(course)
    if request.method == "POST":
        return jsonify(course)
    else:
        return jsonify(course)

@app.route('/put_data', methods=["GET"])
def put_data():
    course = None
    id = request.get_json()
    course = dbModel.getcourse(id)
    print(course)
    return jsonify(course)

@app.route('/getAllCourses',methods = ["GET","POST"])
def getAllCourses():
    department = request.get_json()
    print(department,int((department['roadMapYear']['SelectedRoadMapYear'])))
    NameList  = dbModel.getCoursesName((department['department']['selectedValue']).lower(),(department['roadMapYear']['SelectedRoadMapYear']))
   
    if NameList != None:
        return jsonify(NameList)
    return "'key': 'empty'"


@app.route('/click/Accepted')
def button_click():
    print(f'Button with ID "" was clicked!')
    return 'Button clicked!'

@app.route('/click/Rejected')
def button_reject():
    print(f'Button with ID "" was clicked!')
    return 'Reject Button clicked!'

###################SEND EXAMINER DUTY



@app.route('/sendDuty',methods = ["GET","POST"])
def sendDuty():
    data = request.get_json()
    string = dbModel.SendDuty(data['Id'])
    if string != None:
        return "success"
    return "'key': 'empty'"

@app.route('/createDuty',methods = ["GET","POST"])
def createDuty():
    print("In Create app.py")
    data = request.get_json()
    List=[]
    List.append(int(data[0].split("_")[0]))
    List.append(data[0].split("_")[1])
    List.append((data[1]).lower())
    List.append(data[2])
    List.append(int(data[3].split("_")[0]))
    List.append(data[3].split("_")[1])
    id = dbModel.CreateDuty(List)
    print(id)
    if id != None:
        return jsonify(id)
    return "'key': 'empty'"

@app.route('/getDutyDetail' ,methods = ["GET","POST"])
def getDutyDetail():
    print("In getDutyDetail aap.py")
    data = request.get_json()
    print("DataID: ",data)
    List = dbModel.getDuty(data['Id'])
    print("List: ",List)
    dutyDetail = dbModel.fetchDutyDetail(List)
    if dutyDetail != None:
        return jsonify(dutyDetail)
    return "'key': 'empty'" 

@app.route('/getNotAssignedDuties' ,methods = ["GET"])
def getNotAssignedDuties():
    print("In getAllDuties aap.py")
    List = dbModel.getNotAssignedDuties()
    print("List: ",List)
    if List != None:
        return jsonify(List)
    return "'key': 'empty'" 

@app.route('/getAllDuties' ,methods = ["GET"])
def getAllDuties():
    print("In getAllDuties aap.py")
    List = dbModel.getAllDuties()
    print("List: ",List)
    if List != None:
        return jsonify(List)
    return "'key': 'empty'"

@app.route('/getAllExaminerName',methods = ["GET","POST"])
def getAllExaminerName():
    courseName = request.get_json()
    NameList  = dbModel.getExaminerNameAccordingToCourseSelection(courseName['courseName']['selectedValue'].split("_")[1])
    if NameList != None:
        return jsonify(NameList)
    return "'key': 'empty'"

@app.route('/getAllData', methods =["GET"])
def getAllData():
    List =[] 
    List.append(dbModel.GetCurrentFollowedRoadMapYear())
    List.append(dbModel.GetDepartments())
    if List != None:
        return jsonify(List)
    return "'key': 'empty'" 



# Running app
if __name__ == '__main__':
    app.run(debug=True)