# personal info and all imp cant be null 
class User:
    def _init_(self, usr_name, usr_password, usr_phoneno, usr_cnic, usr_profile_pic, usr_address,
    usr_email, usr_active_status, usr_bio, usr_gender):
        self.usr_name = usr_name
        self.usr_password = usr_password
        self.usr_phoneno = usr_phoneno
        self.usr_cnic = usr_cnic
        self.usr_profile_pic = usr_profile_pic
        self.usr_address = usr_address
        self.usr_email = usr_email
        self.usr_active_status = usr_active_status
        self.usr_bio = usr_bio
        self.usr_gender = usr_gender

class examiner :
    def __init__(self, user_id, institution, availability, ranking, resume, acceptance_count, rejection_count,verified) -> None:
        self.user_id = user_id
        self.institution = institution
        self.availability = availability
        self.ranking = ranking
        self.resume = resume
        self.acceptance_count = acceptance_count
        self.rejection_count = rejection_count
        self.verified = verified

class admin:
    def __init__(self, usr_id, admin_role) -> None:
        self.usr_id = usr_id
        self.admin_role = admin_role
        
class affiliated_colleges:
    def __init__(self, ac_year, ac_address, ac_student_count, ac_incharge, ac_name) -> None:
        self.ac_year = ac_year
        self.ac_address = ac_address
        self.ac_student_count = ac_student_count
        self.ac_incharge = ac_incharge
        self.ac_name = ac_name
        
class roadmap:
    def __init__(self, rd_dept, rd_semester, rd_year, rd_crs_code, rd_crs_name, rd_prac_status, rd_crs_hr, rd_crs_book, rd_crs_outlline) -> None:
        self.rd_dept = rd_dept
        self.rd_semester = rd_semester
        self.rd_year = rd_year
        self.rd_crs_code = rd_crs_code
        self.rd_crs_name = rd_crs_name
        self.rd_prac_status = rd_prac_status
        self.rd_crs_hr = rd_crs_hr
        self.rd_crs_book = rd_crs_book
        self.rd_crs_outlline = rd_crs_outlline

class practical_duty:
    def __init__(self, admin_id, prac_date, prac_time, ac_id, prac_duty_status, prac_ntf_status, 
                 request_date, paper_upload_deadline, result_upload_deadline, 
                 examiner_id, rd_id, rd_dept, rd_year, rd_crs_code, paper, result) -> None:
        self.prac_date = prac_date
        self.prac_time = prac_time
        self.prac_duty_status = prac_duty_status
        self.prac_ntf_status = prac_ntf_status
        self.admin_id = admin_id
        self.examiner_id = examiner_id
        self.ac_id = ac_id
        self.rd_id = rd_id
        self.rd_dept = rd_dept
        self.rd_year = rd_year
        self.rd_crs_code = rd_crs_code
        self.paper_upload_deadline = paper_upload_deadline
        self.result_upload_deadline = result_upload_deadline
        self.paper = paper
        self.result = result
        self.request_date = request_date

class exam_duty:
    def __init__(self , examiner_id, request_date, paper_upload_deadline, paper_date, result_upload_deadline,
                 paper, result, status_req, rd_id, rd_dept, rd_year, rd_crs_code) -> None:
        self.examiner_id = examiner_id
        self.paper_upload_deadline = paper_upload_deadline
        self.status_req = status_req
        self.rd_id = rd_id
        self.rd_dept = rd_dept
        self.rd_year = rd_year
        self.rd_crs_code = rd_crs_code   
        self.paper_date = paper_date
        self.result_upload_deadline = result_upload_deadline
        self.paper = paper
        self.result = result
        self.request_date = request_date
'''
SELECT exam_duty.examiner_id, exam_duty.deadline, exam_duty.status_req, roadmap.rd_dept, roadmap.rd_year, roadmap.rd_crs_code
    exam_duty INNER JOIN roadmap
    ON  exam_duty.rd_id=roadmap.rd_id; 
'''

class batch_enrollment:
    def __init__(self, batch_rd_year, batch_year_date, batch_type) -> None:
        self.batch_rd_year = batch_rd_year
        self.batch_year_date = batch_year_date
        self.batch_type = batch_type

class departments:
    def __init__(self, dep_name) -> None:
        self.dep_name = dep_name
        
class enrolled_department:
    def __init__(self, ac_id, edept_batch_size, edept_std_count) -> None:
        self.ac_id = ac_id
        self.edept_batch_size = edept_batch_size
        self.edept_std_count = edept_std_count
        
class examiner_courses:
    def __init__(self, examiner_id, rd_id) -> None:
        self.examiner_id = examiner_id
        self.rd_id = rd_id

class qualification:
    def __init__(self, examiner_id, degree_title, transcript, institution, starting_date, ending_date) -> None:
        self.examiner_id = examiner_id
        self.degree_title = degree_title
        self.transcript = transcript
        self.institution = institution
        self.starting_date = starting_date
        self.ending_date = ending_date
        self.transcript = transcript
    
    def to_dic(self):
        return {
            "examiner_id" : self.examiner_id,
            "degree_title" : self.degree_title,
            "transcript" : self.transcript,
            "institution" : self.institution,
            "starting_date" : self.starting_date,
            "ending_date" : self.ending_date
            }

class experience:
    def __init__(self, examiner_id, job_title, ExperianceLetter, organization, reference_email, starting_date, ending_date) -> None:
        self.examiner_id = examiner_id
        self.job_title =job_title
        self.organization = organization
        self.ExperianceLetter = ExperianceLetter
        self.reference_email = reference_email
        self.starting_date = starting_date
        self.ending_date = ending_date
        
    def to_dic(self):
        return {
        "examiner_id" : self.examiner_id,
        "job_title" : self.job_title,
        "organization" : self.organization,
        "ExperianceLetter" : self.ExperianceLetter,
        "reference_email" : self.reference_email,
        "starting_date" : self.starting_date,
        "ending_date" : self.ending_date
        }
class college_review:
    def __init__(self, examiner_id, cr_complain, ac_id) -> None:
        self.examiner_id = examiner_id
        self.cr_complain = cr_complain
        self.ac_id  = ac_id
       
class teacher_feedback:
    def __init__(self, prac_duty_id, tf_edu_sys, tf_apparatus, tf_teacher_attitude, tf_rate_duty, tf_complain) -> None:
        self.prac_duty_id = prac_duty_id
        self.tf_edu_sys = tf_edu_sys
        self.tf_apparatus = tf_apparatus
        self.tf_teacher_attitude = tf_teacher_attitude
        self.tf_rate_duty = tf_rate_duty
        self.tf_complain = tf_complain 

class duty_details :
    def __init__(self, crs_code, crs_title, requested_date, paper_upload_deadline, books, outline, prac_date, prac_time) -> None:
        self.crs_code = crs_code
        self.crs_title = crs_title
        self.requested_date = requested_date
        self.paper_upload_deadline = paper_upload_deadline
        self.books = books
        self.outline = outline
        self.prac_date = prac_date
        self.prac_time = prac_time