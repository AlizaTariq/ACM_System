from flask import *
from flask import Flask, request, session, jsonify, redirect
#  pip install flask_session
from flask_session import Session
from werkzeug.wrappers import response
from Model import model
from datetime import datetime
# pip install flask_cors
from flask_cors import CORS
from fileinput import filename
import os
from pathlib import Path
import smtplib
import ssl
import random
import string
# pip install flask_mail
from flask_mail import Mail, Message
from BusinessObjects import *
from werkzeug.security import generate_password_hash, check_password_hash
# pip install flask_jwt_extended
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config['SECRET_KEY'] = "MYSECRETKEY"
# Initialize Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object("config")
app.config['JWT_SECRET_KEY'] = 'super-secret'


jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'elite.express243@gmail.com'
app.config['MAIL_PASSWORD'] = 'njsopxyyzkkssixt'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config['MAIL_DEFAULT_SENDER'] = "elite.express243@gmail.com"
mail = Mail(app) 
verification_code = "".join(random.choices(string.ascii_letters+string.digits,k=10))

# m = model()

@app.route('/SignUpPersonalInfo', methods=["POST"])
def SignUpPersonalInfo():
    # get data from form
    usr_name = request.json.get("usr_name")
    usr_cnic = request.json.get("usr_cnic")
    usr_email = request.json.get("usr_email")
    usr_address = request.json.get("usr_address")
    usr_bio = request.json.get("usr_bio")
    usr_gender = request.json.get("usr_gender")
    usr_password = request.json.get("usr_password")
    usr_phone = request.json.get("usr_phone")
    usr_profile_pic = "Static\Resumes\ProfilePics\empty.png"
    usr_active_status = True
    _hashed_password = generate_password_hash(usr_password)

    # insert data into db
    data = User()
    data.usr_name = usr_name
    data.usr_password = _hashed_password
    data.usr_cnic = usr_cnic
    data.usr_profile_pic = usr_profile_pic
    data.usr_address = usr_address
    data.usr_email = usr_email
    data.usr_active_status = usr_active_status
    data.usr_bio = usr_bio
    data.usr_gender = usr_gender
    data.usr_phoneno = usr_phone
    
    # Insertion in database
    m = model()
    if m.checkEmailExist(usr_email):
        return jsonify({"error": "Email exists"}), 401
    user_id = m.InsertUser(data)  # insertion function return userid
    if user_id != False:
        session['user_id'] = user_id
        session["usr_email"] = usr_email
        session["usr_name"] = usr_name
        access_token = create_access_token(identity=usr_email)
        # sending email
        verification_code = "".join(random.choices(
            string.ascii_letters+string.digits, k=10))
        session["verification_code"] = verification_code
        verification_link = request.url_root + 'verify?code=' + verification_code
        message = Message('Verify your email', recipients=[
                          session.get("usr_email")])
        message.html = f'<div style="background-color: #221e1e; border-radius: 20px; color: wheat; font-family: Tahoma, Verdana, sans-serif; padding: 10px;"><h1 style="text-align: center;"><strong>ٱلسَّلَامُ عَلَيْكُمْ <br /></strong></h1><h2 style="text-align: center;"><span style="color: brown;"> {session.get("usr_name")} </span></h2><hr/><p>Welcome to Exam Portal, before being able to use your account you need to verify that this is your email address by clicking here: {verification_link}</p><p style="text-align: left;"><span style="color: brown;">If you do not recognize this activity simply ignore this mail.&nbsp;</span></p><p>Kind Regards,<br /><span style="color: brown;"><strong>PUCIT Exam Portal</strong></span></p></div>'
        # message.body = f'Click the link to verify your email: {verification_link}'
        mail.send(message)
        # sending email
        verification_code = "".join(random.choices(string.ascii_letters+string.digits,k=10))
        session["verification_code"] = verification_code 
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Error in insertion"}), 401
    
    # session['user_id'] = "29"
    # return "200"

@app.route('/SignUpExaminerInfo', methods=["POST", "GET"])
def SignUpExaminerInfo(): 
    # get data from form 
    institution = request.form.get("institution")
    user_id = session.get('user_id')

    # Get File and Save in a directory
    f = request.files.get("resume")
    resume = f"Static\Resumes\{user_id}.pdf"
    if Path(resume).is_file():
        os.remove(resume)
    f.save(resume)

    # Set by default values
    availability = True
    ranking = 0
    acceptance_count = 0
    rejection_count = 0
    verified = False
    data = examiner(user_id, institution, availability, ranking,
                    resume, acceptance_count, rejection_count,verified)
    
    # insertion in DataBase
    m = model()
    examiner_id = m.InsertExaminer(data)
    if examiner_id != False:
        session["examiner_id"] = examiner_id
        access_token = create_access_token(identity=user_id)
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Error in insertion"}), 401

@app.route('/ExaminerQualification', methods=["POST", "GET"])
def ExaminerQualification():
    examiner_id = session.get("examiner_id")

    # Fetch data from form
    degree_title = request.form.get("degree_title")
    institution = request.form.get("institution")
    starting_date = request.form.get("starting_date")
    ending_date = request.form.get("ending_date")
    f = request.files.get("transcript")

    # Strore file in local directory
    transcript = f"Static\\transcripts\{examiner_id}.pdf"
    if Path(transcript).is_file():
        os.remove(transcript)
    f.save(transcript)

    data = qualification(examiner_id, degree_title, transcript,
                         institution, starting_date, ending_date)
    
    # Insertion in DataBase
    m = model()
    if m.InsertExaminerQualification(data) != False:
        access_token = create_access_token(identity=examiner_id)
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Error in insertion"}), 401

@app.route('/ExaminerExperience', methods=["POST", "GET"])
def ExaminerExperience():
    examiner_id = session.get("examiner_id")

    # fetch data from form
    job_title = request.form.get("job_title")
    organization = request.form.get("organization")
    reference_email = request.form.get("reference_email")
    starting_date = request.form.get("starting_date")
    ending_date = request.form.get("ending_date")
    f = request.files.get("ExperianceLetter")
    
    # Strore file in local directory
    ExperianceLetters = f"Static\\ExperianceLetters\\{examiner_id}.pdf"
    print(ExperianceLetters)
    if Path(ExperianceLetters).is_file():
        os.remove(ExperianceLetters)
    f.save(ExperianceLetters)

    data = experience(examiner_id, job_title, ExperianceLetters,
                      organization, reference_email, starting_date, ending_date)
    verification_link = request.url_root + 'verify?code=' + verification_code

    # Insertion in dataBase
    m = model
    email = session.get('usr_email')
    message = Message('Verify your email', recipients=email) 
    message.html = f'<div style="background-color: #221e1e; border-radius: 20px; color: wheat; font-family: Tahoma, Verdana, sans-serif; padding: 10px;"><h1 style="text-align: center;"><strong>ٱلسَّلَامُ عَلَيْكُمْ <br /></strong></h1><h2 style="text-align: center;"><span style="color: brown;"> {session.get("usr_name")} </span></h2><hr/><p>Welcome to Exam Portal, before being able to use your account you need to verify that this is your email address by clicking here: {verification_link}</p><p style="text-align: left;"><span style="color: brown;">If you do not recognize this activity simply ignore this mail.&nbsp;</span></p><p>Kind Regards,<br /><span style="color: brown;"><strong>PUCIT Exam Portal</strong></span></p></div>'
    mail.send(message)

    if m.InsertExaminerExperience(data) != False:
        # Email = session.get("usr_email")
		#email sent should be here
        access_token = create_access_token(identity=examiner_id)
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Error in insertion"}), 401

@app.route('/verify')
def verify():
    code = request.args.get('code')
    m = model()
    if verification_code == code:
        m.setUserVerified(session.get("examiner_id"))
        return redirect("http://localhost:3000")
    else:
        return 'Invalid verification code!'

@app.route('/ExaminerLogin', methods=["POST"])
def ExaminerLogin():
    # Fetch data from form
    email = request.json.get("email")
    password = request.json.get("password")

    # Verification
    m = model()
    examiner_id = m.getExaminerID(m.getUserID(email))

    if not (m.checkExaminerVerified(examiner_id)):
        return jsonify({"error": "Verify email first"}), 401
    
    if not (m.checkEmailExist(email)) :
        return jsonify({"error": "Email does not exist"}), 401 
    
    usr_pass = m.getUserPassword(email)
    if not (check_password_hash(usr_pass, password)):
        return jsonify({"error": "Invalid Password"}), 401
    
    examiner_id = m.ValidatePassword(email, usr_pass)
    if (examiner_id > 0):
        session["examiner_id"] = examiner_id
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid Password"}), 401
    
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    examiner_id = session.get("examiner_id")
    user_ = m.getDataofUser(24)
    examiner_ = m.getDataofExaminer("examiner", examiner_id)
    data = {
        "usr_name": user_.usr_name,
        "usr_phoneno": user_.usr_phoneno,
        "usr_cnic": user_.usr_cnic,
        "usr_address": user_.usr_address,
        "usr_email": user_.usr_email,
        "usr_profile_pic": user_.usr_profile_pic,
        "usr_bio": user_.usr_bio,
        "usr_gender": user_.usr_gender,
        "usr_active_status": user_.usr_active_status,
        "institution": examiner_.institution,
        "availability": examiner_.availability,
        "ranking": examiner_.ranking,
        "resume": examiner_.resume,
        "acceptance_count": examiner_.acceptance_count,
        "rejection_count": examiner_.rejection_count,
        "qualification": m.getDataofExaminer("qualification", examiner_id),
        "experience": m.getDataofExaminer("experience", examiner_id)
    }
    print(data)
    return jsonify(data)

@app.route('/notifications')
def notifications():
    examiner_id = session.get("examiner_id")
    examiner_id = 14
    m = model()
    data = []

    # Fetch data from database
    pracDuties = m.getRecievedPracRequests(examiner_id)
    examDuties = m.getRecievedTheoryRequests(examiner_id)
    
    for i in pracDuties:
        i = list(i)
        i.append("Practicle Exam")
        data.append(i)
    
    for i in examDuties:
        i = list(i)
        i.append("Theory Paper")
        data.append(i)

    data.sort(key=lambda x: x[0], reverse=True)

    return jsonify(data)

@app.route('/getRequestRecievedId', methods=['POST'])
def getRequestRecievedId() :                
    examiner_id = session.get("examiner_id")
    duty = request.form.get('duty_id')
    print("duty: ", duty)
    data = duty.split(",")
    session["duty_id"] = str(data[0])
    session["duty_Type"] = str(data[data.__len__() - 1])
    access_token = create_access_token(identity=examiner_id)
    return jsonify(access_token=access_token), 200

@app.route("/DutyDetails", methods=['POST', 'GET'])
def DutyDetails():                  # moving from request page to duty details
    duty_id = session.get("duty_id")
    m = model()
    # => using course code get crs code, crs title,
    # => request date, paper upload deadline from exam/duty table
    # => using rd_id get crs_book and crs_outline from both tables
    # => get prac_date, time and institute by using ac_id get name and location of
    # institute from affiliated_colleges table
    dutyDetails = m.getDutyDetails(duty_id)
    print("dutyDetails:: ", dutyDetails)
    return jsonify(dutyDetails)

@app.route('/home')
def home():
    m = model()
    examiner_id = session.get("examiner_id")
    examiner_id = 14
    # return requested received and status is true and 
    # paper upload deadline is after today
    duties = []
    pracDuties = m.getAcceptedPracDuties(examiner_id)  # 2 for accepted status
    examDuties = m.getAcceptedTheoryDuties(examiner_id)
    
    for i in pracDuties:
        i = list(i)
        i.append("Practicle Exam")
        duties.append(i)
    
    for i in examDuties:
        i = list(i)
        i.append("Theory Paper")
        duties.append(i)
        
    duties.sort(key=lambda x: x[1], reverse=True)
    return jsonify(duties)

@app.route('/PaperPendingDuty', methods=['GET'])
def PaperPendingDuty():						# accepted and uploaded paper and paper is not taken yet
    examiner_id = session.get("examiner_id")
    examiner_id = 14
    m = model()
    # paper table has the entity has the same duty id
    # and paper_date in exam_duty table is after today
    duties = []
    pracDuties = m.getPracPaper_Pending(examiner_id)
    examDuties = m.getTheoryPaper_Pending(examiner_id)
    
    for i in pracDuties:
        i = list(i)
        i.append("Practicle Exam")
        duties.append(i)
    
    for i in examDuties:
        i = list(i)
        i.append("Theory Paper")
        duties.append(i)
        
    duties.sort(key=lambda x: x[1], reverse=True)
    return jsonify(duties)

@app.route('/ResultUploadPending', methods=['GET'])
def ResultUploadPending():					# paper done upload paper now
    examiner_id = session.get("examiner_id")
    examiner_id = 14
    m = model()
    # paper table has the entity has the same duty id has null result column
    # and result_date in exam_duty table is after today
    duties = []
    pracDuties = m.getPracResult_Pending(examiner_id)
    examDuties = m.getTheoryResult_Pending(examiner_id)
    
    for i in pracDuties:
        i = list(i)
        i.append("Practicle Exam")
        duties.append(i)
    
    for i in examDuties:
        i = list(i)
        i.append("Theory Paper")
        duties.append(i)
        
    duties.sort(key=lambda x: x[1], reverse=True)
    return jsonify(duties)

@app.route("/GetPaper", methods=['GET'])
def GetPaper():
    d_id = session.get('duty_id')
    paper = request.files["Paper"]
    # Store paper in local directory
    papers = f"Static\papers\{d_id}.pdf"
    if Path(papers).is_file():
        os.remove(papers)
    paper.save(papers)
    # store nme of the paper in the DataBase
    m = model()
    if m.InsertUploadedPaper(d_id, papers, session.get("duty_type")) :
        return jsonify({"status": "success", "message": "Paper Uploaded Successfully"})
    return jsonify({"status": "failed", "message": "Failed to Upload Paper"})

@app.route("/GetResult", methods=['GET'])
def GetResult():
    d_id = session.get('duty_id')
    result = request.files["result"]
    # Store file in local directory
    results = f"Static\results\{d_id}.pdf"
    if Path(results).is_file():
        os.remove(results)
    result.save(results)
    # Store file name in DataBase
    m = model()
    if m.InsertUploadedResult(d_id, results, session.get("duty_type")) :
        return jsonify({"status": "success", "message": "Result Uploaded Successfully"})
    return jsonify({"status": "failed", "message": "Failed to Upload Result"})

@app.route('/NewQualifications')
def NewQualifications():
    examiner_id = session.get("examiner_id")
    qualifications = m.getDataofExaminer("qualification",examiner_id)
    return jsonify(qualifications)

@app.route('/NewExperience')
def NewExperience():
    examiner_id = session.get("examiner_id")
    experiences = m.getDataofExaminer("experience",examiner_id)
    return jsonify(experiences)

@app.route('/UpdateStatus') 
def UpdateStatus():
    d_id = session.get('duty_id')
    d_type = session.get("duty_Type")
    d_type = "Practicle Exam"
    # get Status
    status = "get"
    m = model()
    if m.UpdateStatus(d_id, status, d_type) :
        return jsonify({"status": "success", "message": "Status Updated Successfully"})
    return jsonify({"status": "fail", "message": "Status has not Updated Successfully"})
# Running app
if __name__ == '__main__':
    app.run(debug=True)