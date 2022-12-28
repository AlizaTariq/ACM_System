import random
from flask import Flask, redirect,render_template,jsonify,request,session
import psycopg2
import psycopg2.extras
from Database import DatabaseModel
import json
from Classes import UserAdmin,DisplayDuty


# Initializing flask app
app = Flask(__name__)

app.config.from_object("config")
app.secret_key=app.config["SECRET_KEY"]

conn=psycopg2.connect(dbname=app.config["DATABASE"],user=app.config["DB_USER"],
password=app.config["DB_PASSWORD"],host=app.config["DB_HOST"])

dbModel= DatabaseModel(app.config["DATABASE"],app.config["DB_USER"],
    app.config["DB_PASSWORD"],app.config["DB_HOST"])

dbModel.getSemInfo('2020','CS 302','it')
dbModel.getCollegeInfo(3)
#dbModel.getAllCollege()
dbModel.getCollegeCourses(1)
dbModel.getRankedExaminer('Data Structures and Algorithms Lab')
dbModel.getPracticalDutyId(1,"cs","CS 103")
#dbModel.getBatchSize(2)
#dbModel.getCollegeRoadMapYear(1,'1')

#dbModel.getCollegeCourseInfo('2020','cs','CS 103')

#dbModel.getRoadMapYears('it')
#dbModel.generateDuties()

# print("Roadmap year is")
# dbModel1.getCollegesList();

# dbModel1.generateDuties();

# dbModel1.GetRoadMapInfo();

#dbModel.getAdminNotifications()
#dbModel.updateAdminNotifications(859)
#dbModel.getAdminNotifications()


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

    print("email--- : ",email,"  password = " ,password)

    #return jsonify({'status': 'success'})
    #return redirect('/notifications')
    return jsonify(success=True)
    #return  render_template('reactView.html')

#()
def makePracDutyObj(list1):
    print("In make prac")
    listShowDuty=[]
    for duty in list1:
      list2=[]
      clgInfo=dbModel.getCollegeInfo(duty[0])
      dept='it'
      if int(duty[1])==1:
        dept='cs'    

      semCrsInfo=dbModel.getSemInfo(duty[2],duty[3],dept)
      print("semCrsInfo ---===> ",semCrsInfo)

      #(6, '2 ', '2020', 'CS 302', 5)
      print("obj-->.",clgInfo[0],clgInfo[5],dept,duty[3],semCrsInfo[1],semCrsInfo[0],duty[4])
    #   DisplayDutyObj=DisplayDuty(clgInfo[0],clgInfo[5],dept,duty[3],semCrsInfo[1],semCrsInfo[0]
    #   ,duty[4])

      list2.append(clgInfo[0])
      list2.append(clgInfo[5])
      list2.append(dept)
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
    examiners=dbModel.getRankedExaminer('Data Structures and Algorithms Lab')
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
    data = request.get_json()
    examiner=data['examiner']
    college=data['college']
    print("\n\n college is : ",college)
    collegeId=dbModel.getCollegeId(college[0])
    dept=data['deptValue']
    courseInfo=data['courseValue']
    moreInfo=data['moreInfo']

    course=courseInfo.split(" - ");
    print("pract data send is data is : ",data)

    print("CollegeId is : ",collegeId)
    pracId=dbModel.getPracticalDutyId(collegeId,dept,course[0])
    dbModel.savePracticalDuty(pracId,examiner[3],moreInfo)

    print("\n\n-------------->> pract duty id : ",pracId)



    #examinerId = data['examinerId']
    #name = data['teacherName']
    #rank=data['teacherRank']
    #email=data['teacherEmail']
    
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
    city = data['city']
    status = data['status']
    print(username,password,city,status)
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
    dept=''
    if(dept1=="cs"):
        dept='1'
    else:
        dept='2'

    #if clgName!=None and len(clgName)!=0:
    print("seleected value==========> :","   ",clgName,"  department -->>>",dept)
    clgId=dbModel.getCollegeId(clgName)
    print("=================clgIg=",clgId)
    rdYear=dbModel.getCollegeRoadMapYear(clgId[0],dept)
    crsList=dbModel.getCollegeCourses(clgId[0])
    coursesInfo=[]
    for courseCode in crsList:
        course1=dbModel.getCollegeCourseInfo(rdYear,dept1,courseCode)
        if course1!=None and len(course1)!=0:
            coursesInfo.append(course1[1]+" - "+course1[0])
    
    #print("courses list detail is : ",coursesInfo)

    #return jsonify(crsList)
   


    return jsonify(coursesInfo)

    

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



# Running app
if __name__ == '__main__':
    app.run(debug=True)