class UserAdmin:
    def __init__(self,email1="",password1="",name1="",role1="",activeStatus1="",cnic1=""):

        self.email=email1
        self.password=password1
        self.name=name1
        self.role=role1
        self.activeStatus=activeStatus1
        self.cnic=cnic1

class DisplayDuty:
    def __init__(self,clg_id="",clg_name="",dept="",crs_code="",crs_name="",
    sem=0,batchSizeNum=0,clgAddress="",desc="",date="",time="",status=""):
        self.crs_code=crs_code
        self.crs_name=crs_name
        self.clg_id=clg_id
        self.clg_name=clg_name
        self.sem=sem
        self.dept=dept
        self.desc=desc
        self.date=date
        self.time=time
        self.batchSizeNum=batchSizeNum
        self.status=status
        self.clgAddress=clgAddress

