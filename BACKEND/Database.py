import psycopg2
import psycopg2.extras
import datetime
from Classes import UserAdmin

import smtplib, ssl
from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP
from email.mime.multipart import MIMEMultipart
from asyncio.windows_events import NULL
from xml.etree.ElementTree import tostring


class DatabaseModel:
    def __init__(self,database,user,password,host):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
        self.connection=None
        try:
           self.connection=psycopg2.connect(dbname=self.database,
           host=self.host,user=self.user,password=self.password)
        except Exception as e:
            print("There is error in connection",str(e))


    def __del__(self):

        if self.connection!=None:
            self.connection.close()

    #Function-1
    def checkAdminExist(self,admin1):
        try:
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select a.admin_id from admin a where a.usr_id "\
                " IN(Select u.usr_id from users u "\
					 " where u.usr_id=a.usr_id and u.usr_email "\
				" =%s and u.usr_password=%s);"

                args=(admin1.email,admin1.password)
                cursor.execute(query,args)
                adminData=cursor.fetchall()
                print("Admin data is : ",adminData)
                if(len(adminData)>0):
                    return True
                return False
        except Exception as e:
            print("Exception in --checkAdminUserExist",str(e))
        finally:
            if cursor!=None:
                cursor.close()


    #Function-2
    def getAdminNotifications(self):
        try:
            if self.connection!=None:
                print("addddddddddddddmin ntffffffffffff")
                cursor=self.connection.cursor()
                query="select ac_id,rd_crs_code,examiner_id from practical_duty "\
               " where prac_ntf_status=1"
                cursor.execute(query)
                adminNotifications=cursor.fetchall()
                print("Admin Notifications are : ",adminNotifications)
                return adminNotifications
        except Exception as e:
            print("Exception in getAdminNotifications",str(e))
        finally:
            if cursor!=None:
                cursor.close()



    def getCollegesList(self):
        try:
            print("\n\nIn Road Map DataBase")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select * from affiliated_colleges;"
                cursor.execute(query)
                clgList=cursor.fetchall()
                print("clgList --> ",clgList)
                return clgList

        except Exception as e:
            print("Exception in road_map",str(e))
        finally:
            if cursor!=None:
                cursor.close()

    def GetSemesters(self,batchRdList,status):
#4 8(4cs 4it)

        print("list of getting smesters is : ",batchRdList,"----",len(batchRdList))
        length=len(batchRdList)
        i=0
        count1=1
        count2=2
        flag=False
        while(i<length):
            if(batchRdList[i][2]=='it'and flag==False):
                count1=1
                count2=2
                flag=True

            if(status==True):
                batchRdList[i].append(str(count1))
                count1=count1+2
            elif(status==False):
                 batchRdList[i].append(str(count2))
                 count2=count2+2
            i=i+1
        
        print("final rd batch list is :: >>",batchRdList)
        return batchRdList


   
    #2020
    def getBatchesList(self,affClgYear):
        batches=[]
        today = datetime.date.today()
        currYear = int(today.strftime("%Y"))
        month = int(today.strftime("%M"))

        # 2022-2020-1
        # 2021-2020-2
        # 2020-2020-3
        # 2019-2020
        # #fall -- 8, 9,10,11,1,2,
        #spring -- 3,4,5,6,7

        flagBatchSt=False
        i=0
        sems=[]
        #and ((currYear-i)- (int)affClgYear)>=0
        # 2022 -- 2020
        # 2021 --2016
        # 2020 -- 2016
        # 2019 --2016
        while(i!=4 and (int(currYear)-i >= int(affClgYear))):
            batches.append(str(int(currYear)-i))
            if(month in (8,9,10,11,1,2)):
                flagBatchSt=True
            i=i+1
            print("in while")
        print("after while")

       # sems=self.GetSemesters(currYear,affClgYear,flagBatchSt)
        #print("after sems ",sems)
        return batches

#******************************************************
#******************************************************

    def getPracticalCourseCode(self,rdYear,dept,sem):
        try:
            print("\n\nIn Road Map DataBase")
            if self.connection!=None:
                cursor=self.connection.cursor()
                print(rdYear,"  ",dept," --  ",sem)
                query="select rd_crs_code from roadmap where rd_year=%s and "\
               " rd_dept=%s and rd_semester=%s and rd_prac_status=1;"
                args=(rdYear,dept,sem)
                cursor.execute(query,args)

                pracCrsList=cursor.fetchall()
                print("pracCrsList -->>" ,pracCrsList)
                return pracCrsList
        except Exception as e:
            print("Exception in pracCrsList",str(e))
        finally:
            if cursor!=None:
                cursor.close()

    def getTheoreticalCourseCode(self,rdYear,dept,sem):
        try:
            print("\n\nIn Road Map DataBase")
            if self.connection!=None:
                cursor=self.connection.cursor()
                print(rdYear,"  ",dept," --  ",sem)
                query="select rd_crs_code from roadmap where rd_year=%s and "\
                " rd_dept=%s and rd_semester=%s and rd_prac_status=0;"
                args=(rdYear,dept,sem)
                cursor.execute(query,args)

                pracCrsList=cursor.fetchall()
                print("theorey--CrsList -->>" ,pracCrsList)
                return pracCrsList
        except Exception as e:
            print("Exception in pracCrsList",str(e))
        finally:
            if cursor!=None:
                cursor.close()

#******************************************************
#******************************************************

    def getCollegeDepartment(self,acId):
        try:
            print("\n\nIn Road Map DataBase")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select edept_id from enrolled_department where ac_id=%s"
                args=(str(acId))

                cursor.execute(query,args)
                dep1List=cursor.fetchall()
                print(dep1List)
                depList=[]
                print("dep1 -- list ",dep1List)

                for dep in dep1List:
                    if(dep[0]==1):
                        depList.append('cs')
                    elif(dep[0]==2):
                        depList.append('it')
                    print("dep--> ",dep)
                return depList

        except Exception as e:
            print("Exception in road_map",str(e))
        finally:
            if cursor!=None:
                cursor.close()



#brdcs

    def getCollegeCoursesDuties(self,batchRddepClgSemList,practicalDuties=[]):

        #(batch,rodpyaer,dept,clg,bachtsizenum,sem)
        #---(clgId,rdyear,dept,sem,crs code)
        #rd yead,sem,dep
        try:
            print("Hello world")
           
            for batch in batchRddepClgSemList:  #1-rdyear 2-sem
                    list1=[]
                    list1.append(batch[3]) #clg
                    list1.append(batch[2]) #dept
                    list1.append(batch[0]) #batch
                    list1.append(batch[1]) #rd year
                    list1.append(batch[5]) #sem
                    list1.append(batch[4]) #batchsizenum

                    #rdyear, dept, sem (in one sem multiple practical courses)
                    crsCodeList=self.getPracticalCourseCode(batch[1],batch[2],batch[5])
                    list1.append(crsCodeList)
                    practicalDuties.append(list1)
                    #self.getTheoreticalCourseCode(batch[1],dept,batch[2])
            
            print("Practical Duties are : --->> ",practicalDuties)
            return practicalDuties
        except Exception as e:
            print("Exception in road_map",str(e))
       
       
    def getCollegeCoursesDutiesTheorey(self,clgId,batchRdSemList,departmentsList,theoreyDuties=[]):

        #(clgId,rdyear,dept,sem,crs code)
        #rd yead,sem,dep
        try:
            print("Hello world")
            for dept in departmentsList:
                for batch in batchRdSemList:  #1-rdyear 2-sem
                    list1=[]
                    list1.append(clgId)
                    list1.append(dept) #dept
                    list1.append(batch[0]) #batch
                    list1.append(batch[1]) #rd year
                    list1.append(batch[2]) #sem

                    crsCodeList=self.getTheoreticalCourseCode(batch[1],dept,batch[2])
                    list1.append(crsCodeList)
                    theoreyDuties.append(list1)
                    #self.getTheoreticalCourseCode(batch[1],dept,batch[2])
            
            print("Practical Duties are : --->> ",theoreyDuties)
            return theoreyDuties



        except Exception as e:
            print("Exception in road_map",str(e))
       

    def savePracticalDuties(self,practDuties):  #clgId,rdId,rd_dept,rd_year,rd_crscode
        #0-clgId, 1 dept, 2 batchyear,rdyear,sem,list crscode
        try:
            print("duties is :",practDuties)

            for duty in practDuties:
                print("duty is :",duty)
                for crsCode in duty[6]: #courses
                    print("\n\nIn Road Map DataBase")
                    if self.connection!=None:
                        cursor=self.connection.cursor()
                        query="insert into practical_duty(ac_id,rd_dept,rd_year,rd_crs_code, " \
                        "prac_batch_num,prac_duty_status) values(%s,%s,%s,%s,%s,0);"
                        
                        # dept1=2
                        # if(duty[1]=='cs'):
                        #     dept1=1

                        args=(duty[0],duty[1],duty[3],crsCode,duty[5])
                        cursor.execute(query,args)
                        self.connection.commit()

                        
        except Exception as e:
            print("Exception in road_map",str(e))
        finally:
            if cursor!=None:
                cursor.close()

    def calculateBatchSizeNum(self,batchsize,totalSize):
       return round(float(batchsize)/float(totalSize))
        

    def generateDuties(self):
        collegesList=self.getCollegesList();
        print("\n\ncollege List --> ",collegesList)
        #---------------------------------------------
        roadMapYearCS=self.getRoadMapYears('cs')
        roadMapYearIT=self.getRoadMapYears('it')

        #roadMapYear=self.getRoadMapYears(dept)
        #print("road map years are : ",roadMapYearCS, "  ",roadMapYearIT)
        st=1

        for college in collegesList:
            #college[0] --id -- affiliated_colleges
            #dep----- enrolled_departments
            affYear=college[1]

            departmentsList= self.getCollegeDepartment(college[0])
            print("--->>>>:::",departmentsList)
            batchesList=self.getBatchesList(affYear)
            batchRdDepList=[]
            batchSizeList=self.getBatchSize(int(college[0]))
            
            #calculate Batch Size
            batchSize=batchSizeList[0][2]
            batchSizeDepCS=0
            batchSizeDepIT=0

            for batchSize in batchSizeList:
                print("\n\nbatch list -->> ",batchSize)
                if batchSize[0]==1:  #CS
                    batchSizeDepCS= self.calculateBatchSizeNum(batchSize[3],batchSize[2])
                if batchSize[0]==2:  #IT
                    batchSizeDepIT=self.calculateBatchSizeNum(batchSize[3],batchSize[2])
                    
            print("batchsize num cs it : ",batchSizeDepCS,"---",batchSizeDepIT)
           

            for batchYear in batchesList:
                if('cs' in departmentsList):
                    for rdYear in roadMapYearCS:
                        if(int(batchYear)>=int(rdYear)):
                            list1=[]
                            list1.append(batchYear)
                            list1.append(rdYear)
                            list1.append('cs')
                            list1.append(college[0])
                            list1.append(batchSizeDepCS)
                            batchRdDepList.append(list1)
                            break
                if('it' in departmentsList):   
                    for rdYear in roadMapYearIT:
                        if(int(batchYear)>=int(rdYear)):
                            list1=[]
                            list1.append(batchYear)
                            list1.append(rdYear)
                            list1.append('it')
                            list1.append(college[0])
                            list1.append(batchSizeDepIT)
                            batchRdDepList.append(list1)
                            break
                
            #batchRdDepList.append(batchRdDepList1[0])
            #batchRdDepList.append(batchRdDepList2[0])


            #(batchyear,rdyeyear,dept)
            #batchRdDepList.sort()

            batchRdDepList= sorted(batchRdDepList, key=lambda x: x[2])

            print("batch rd list is --->>>-->> ",batchRdDepList)


            print("batches List --> ",batchesList)
            print("back in loop")


            flagBatchSt=False
            today = datetime.date.today()
            month = int(today.strftime("%m"))
            currYear = int(today.strftime("%Y"))
            print("Month is : ",month,"   ",currYear)

            if(int(month) in (8,9,10,11,12,1,2)):
                print("status is going to be true ")
                flagBatchSt=True
           # sems=self.GetSemesters(batchRdList,currYear,affYear,flagBatchSt)
            btachRdSem =self.GetSemesters(batchRdDepList,flagBatchSt)

            print("current sem of clg ",college[0], " batchrdsems =  ", 
            batchRdDepList ,"  btaches ", batchesList
             ,"  dept list ",departmentsList)
            
            if(st==1):
                pracDuties=self.getCollegeCoursesDuties(batchRdDepList)
                st=st+1
            else:
                pracDuties=self.getCollegeCoursesDuties(batchRdDepList,pracDuties)
            print("\n\n--->>>.Length of pract duties ",len(pracDuties))
            print("\n\nPracDuties Duties lust ::  \n\n---------------->",pracDuties)
        #save duties in DB
        self.savePracticalDuties(pracDuties)


    def checkDutyGenerateStatus(self):
        try:
            print("\n\ncheckDutyGenerateStatus")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select prac_duty_id from practical_duty where prac_duty_status !=2"
                cursor.execute(query)
                listSt=cursor.fetchall()
                if listSt==None or len(listSt)==0:
                    return True
                return False
        except Exception as e:
            print("Exception in checkDutyGenerateStatus",str(e))
        finally:
            if cursor!=None:
                cursor.close()

    def getBatchSize(self,clgId):
        try:
            print("\n\nIn Road Map DataBase")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select * from enrolled_department where ac_id=%s"
                args=(clgId,)
                cursor.execute(query,args)

                batchSizeList=cursor.fetchall()
               
                print("batch size list  is --->" ,batchSizeList)

                # rdbatchSizeList=[]
                # for rd in batchSizeList:
                #      print(rd)
                #      rdList1.append(rd[0])
                # print("rd list11-- -->>" ,rdList1)

                return batchSizeList
        except Exception as e:
            print("Exception in batchsize ",str(e))
        finally:
            if cursor!=None:
                cursor.close()




    def getRoadMapYears(self,dept):
        try:
            print("\n\nIn Road Map DataBase")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select distinct rd_year from roadmap where rd_dept=%s "\
                "  order by rd_year desc limit 4;"
                args=(dept,)
               
                cursor.execute(query,args)

                rdList=cursor.fetchall()
               
                print("rd list --->" ,rdList)

                rdList1=[]
                for rd in rdList:
                     print(rd)
                     rdList1.append(rd[0])
                print("rd list11-- -->>" ,rdList1)

                return rdList1


        except Exception as e:
            print("Exception in --getroad_mapyears",str(e))
        finally:
            if cursor!=None:
                cursor.close()

    
    
    def GetCurrentYear(self):
        import datetime
        today = datetime.date.today()
        year = today.strftime("%Y")
        print(year)
        return year


    def GetRoadMapInfo(self):
        try:
            print("In Roadmap calc")
            if self.connection!=None:
                cursor=self.connection.cursor()
                currYear = self.GetCurrentYear()
                print(type(currYear))

                lastYear=int(currYear)-3
                
                print(str(lastYear))
                query="Select batch_rd_year from batch_enrollment"
                # where YEAR(batch_year_date) BETWEEN %s and %s;"
               
                args=(currYear,str(lastYear))
                cursor.execute(query,args)
                roadmapList=cursor.fetchall()
                print(roadmapList)
                return roadmapList

        except Exception as e:
                print("Exception in getting roadmap",str(e))
        finally:
                if cursor!=None:
                    cursor.close()


    def getAllPraticalDuty(self):
        try:
            print("\n\nIn Road Map DataBase")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select ac_id,rd_dept,rd_year,rd_crs_code,prac_batch_num,prac_duty_status "\
                " from practical_duty"
                cursor.execute(query)
                pracDutyList=cursor.fetchall()
               
                print("All Pract duty list --->" ,pracDutyList)                
                return pracDutyList
        except Exception as e:
            print("Exception in get All Practical duty list",str(e))
        finally:
            if cursor!=None:
                cursor.close()



    def getTypeDutiesList(self,status):
        try:
            print("\n\nget type duties")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select ac_id,rd_dept,rd_year,rd_crs_code,prac_batch_num,prac_duty_status "\
                " from practical_duty where prac_duty_status=%s"
                args=(status,)
                cursor.execute(query,args)
                dutyList=cursor.fetchall()
               
                print("DB All Pract duty list --->" ,dutyList)                
                return dutyList

        except Exception as e:
            print("Exception in get All Practical duty list",str(e))
        finally:
            if cursor!=None:
                cursor.close()




    def getSemInfo(self,rd_year,crs_code,rd_dept):
        try:
            print("In Roadmap calc")
            if self.connection!=None:
                cursor=self.connection.cursor()
                
                query="select rd_semester,rd_crs_name from roadmap where rd_year=%s and "\
                    " rd_crs_code=%s and rd_dept=%s and rd_prac_status=1; "
                
                args=(str(rd_year),str(crs_code),str(rd_dept))
                cursor.execute(query,args)
                
                print("get sem of ",rd_year,crs_code,rd_dept)
                SemCrsList=cursor.fetchall()
                print("Sem---->",SemCrsList)
                return SemCrsList[0]
        except Exception as e:
                print("Exception in getting semcrs",str(e))
        finally:
                if cursor!=None:
                    cursor.close()

    def getCollegeInfo(self,clgId):
        try:
            print("In Roadmap calc")
            if self.connection!=None:
                cursor=self.connection.cursor()
                
                query="select * from affiliated_colleges where ac_id=%s"
                args=(clgId,)
                cursor.execute(query,args)
                clgInfo=cursor.fetchall()
                print("clgName-->",clgInfo)
                return clgInfo[0]

        except Exception as e:
                print("Exception in getting clgName",str(e))
        finally:
                if cursor!=None:
                    cursor.close()
    

    def getAllCollege(self):
        try:
            print("In get All college")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select ac_name from affiliated_colleges"
                cursor.execute(query)
                clgInfo=cursor.fetchall()
                #print("college list -->",clgInfo)
                return clgInfo
        except Exception as e:
                print("Exception in getting clgName",str(e))
        finally:
                if cursor!=None:
                    cursor.close()

    def getCollegeId(self,clgName):
        try:
            print("In get All college is ",clgName)
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select distinct ac_id from affiliated_colleges where ac_name=%s"
                args=(clgName,)
                cursor.execute(query,args)
                acId=cursor.fetchall()
                print("college Id list -->",acId)
                return acId[0]
        except Exception as e:
                print("Exception in getting college Id",str(e))
        finally:
                if cursor!=None:
                    cursor.close()

    def getPracticalDutyId(self,acId,dept,crsCode):
        try:
            print("In get practical duty id ",acId,dept,crsCode)
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select prac_duty_id from practical_duty where "\
               " ac_id=%s and rd_dept=%s and rd_crs_code=%s;"
                # dept1='1'
                # if dept=="it":
                #     dept1='2'
                
                args=(acId,dept,crsCode)
                cursor.execute(query,args)
                practId=cursor.fetchall()
                print("practId Id list -->",practId)
                return practId[0]
        except Exception as e:
                print("Exception in  get practical duty id ",str(e))
        finally:
                if cursor!=None:
                    cursor.close()


    def getTeacherId(self,acId,dept,crsCode):
        try:
            print("In get practical duty id ",acId,dept,crsCode)
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select examiner_id from practical_duty where "\
               " ac_id=%s and rd_dept=%s and rd_crs_code=%s;"
                
                args=(acId,dept,crsCode)
                cursor.execute(query,args)
                exmId=cursor.fetchall()
                print("examId Id list -->",exmId)
                return exmId[0]
        except Exception as e:
                print("Exception in  get examiner id ",str(e))
        finally:
                if cursor!=None:
                    cursor.close()

    
    def getTeacherDetail(self,examinerId):
        try:
            print("In get teacher detail  ",examinerId)
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select e.examiner_id,u.usr_name,u.usr_email,e.institution, "\
                    " u.usr_profile_pic from users u , examiner e where "\
                    "e.user_id=u.usr_id and e.examiner_id=%s"
                
                args=(examinerId,)
                cursor.execute(query,args)
                teacher=cursor.fetchall()
                print("teacher detail list -->",teacher)
                return teacher[0]
        except Exception as e:
                print("Exception in  get examiner id ",str(e))
        finally:
                if cursor!=None:
                    cursor.close()



    def getCollegeCourses(self,clgId,dept):
        try:
            print("In get getCollegeCourses ",clgId,dept)
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select rd_crs_code from practical_duty "\
                    " where ac_id=%s and rd_dept=%s and prac_duty_status in (0,3) "

                args=(clgId,dept)
                cursor.execute(query,args)
                courses=cursor.fetchall()
                print("courses list -->",courses)
                return courses
        except Exception as e:
                print("Exception in getting clgName",str(e))
        finally:
                if cursor!=None:
                    cursor.close()

    def getCollegeCourseInfo(self,rdYear,dept,crs_code):
        try:
            print("In get All college====>",rdYear,dept,crs_code)
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select rd_crs_name,rd_crs_code from roadmap where"\
                    " rd_dept=%s and rd_crs_code=%s and rd_prac_status=1"

                args=(dept,crs_code)
                cursor.execute(query,args)
                coursesInfo=cursor.fetchall()
                print("coursesInfo list -->",coursesInfo)
                return coursesInfo[0]
        except Exception as e:
                print("Exception in getting courseInfo",str(e))
        finally:
                if cursor!=None:
                    cursor.close()



    def getCollegeRoadMapYear(self,clgId,dept):
        try:
            print("In get All college")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select distinct rd_year from practical_duty where ac_id=%s and "\
                " rd_dept=%s"
                args=(clgId,dept)
                cursor.execute(query,args)
                year=cursor.fetchall()
                print("year list -->",year)
                return year[0]
        except Exception as e:
                print("Exception in getting college year",str(e))
        finally:
                if cursor!=None:
                    cursor.close()

    
    def getRankedExaminer(self,courseName):
        try:
            print("In get getRankedExaminer")
            if self.connection!=None:
                cursor=self.connection.cursor()
                courseName='%'+courseName+'%'
                query="select distinct u.usr_id,usr_name,usr_email,e.examiner_id,e.ranking "\
                " from users u,examiner_courses ec,examiner e where "\
            " e.examiner_id=ec.examiner_id and u.usr_id=e.user_id and usr_active_status=true "\
            " and lower(examiner_crs_name) like lower(concat(%s)) "\
            " order by e.ranking desc"
                args=(courseName,)
                cursor.execute(query,args)
                rankedExaminers=cursor.fetchall()
                print("getRankedExaminer -->",rankedExaminers)
                return rankedExaminers
        except Exception as e:
                print("Exception in getRankedExaminer",str(e))
        finally:
                if cursor!=None:
                    cursor.close()


    
    def savePracticalDuty(self,practDutyId,examinerId,moreInfo):  
        try:
            print("practDutyId insertion is :",practDutyId)
            if self.connection!=None:
                cursor=self.connection.cursor()
                date1=datetime.date.today()
                query="UPDATE public.practical_duty"\
	" SET prac_duty_status=1, prac_ntf_status=1, examiner_id=%s, prac_ass_date=%s,prac_info=%s "\
	" WHERE prac_duty_id=%s;"                    
                args=(examinerId,date1,moreInfo,practDutyId)                    
                cursor.execute(query,args)
                self.connection.commit()
                        
        except Exception as e:
            print("Exception in insert practical duty examiner",str(e))
        finally:
            if cursor!=None:
                cursor.close()


    def getAdminNotificationsPrac(self):
        try:
            print("In get admin ntfs")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select examiner_id,prac_duty_id,prac_duty_status,prac_info,ac_id, "\
                    " rd_crs_code from practical_duty where prac_duty_status in(2,3) and "\
                        " prac_ntf_status=1"
                cursor.execute(query)
                ntfs=cursor.fetchall()
                print("notification list -->",ntfs)
                return ntfs
        except Exception as e:
                print("Exception in getting admin notifications",str(e))
        finally:
                if cursor!=None:
                    cursor.close()


    def getExaminerName(self,exm_id):
        try:
            print("In get admin ntfs")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select u.usr_name from users u where "\
                " u.usr_id=(select e.user_id from examiner e where "\
								"	e.examiner_id=%s)"
                args=(exm_id,)
                cursor.execute(query,args)
                examiner=cursor.fetchall()
                print("Examinr name list -->",examiner)
                return examiner[0]
        except Exception as e:
                print("Exception in getting Examinr name",str(e))
        finally:
                if cursor!=None:
                    cursor.close()

#getExmProfilePic
    def getExmProfilePic(self,exm_id):
        try:
            print("In get profile pic exam")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select u.usr_profile_pic from users u where "\
                " u.usr_id=(select e.user_id from examiner e where "\
								"	e.examiner_id=%s)"
                args=(exm_id,)
                cursor.execute(query,args)
                examiner=cursor.fetchall()
                print("Examiner profile pic -->",examiner)
                return examiner[0]
        except Exception as e:
                print("Exception in getting Examiner profile pic : ",str(e))
        finally:
                if cursor!=None:
                    cursor.close()

    def updateAdminNotifications(self,practDutyId):
        try:
            print("practDutyId insertion is :",practDutyId)
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="UPDATE public.practical_duty"\
	            " SET prac_ntf_status=0 "\
	            " WHERE prac_duty_id=%s;"                    
                args=(practDutyId,)                    
                cursor.execute(query,args)
                self.connection.commit()
                        
        except Exception as e:
            print("Exception in update practical duty admin notifications",str(e))
        finally:
            if cursor!=None:
                cursor.close()

    
    ############################################3###################################

    def onDutyExaminers(self):
        try:
            if self.connection!=None:
                cursor=self.connection.cursor()
                # where u.usr_active_status=true and
                cursor.execute("select examiner_id from exam_duty;")
                onDutyExmnrs=cursor.fetchall()
                return onDutyExmnrs
        except Exception as e:
                print("Exception in onDutyExaminers",str(e))
        finally:
                if cursor!=None:
                    cursor.close()
    
    def getExaminerNameAccordingToCourseSelection(self,courseName):
        
        try:
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select u.usr_name AS name,u.usr_email,e.examiner_id from users u "\
                "JOIN public.examiner e ON u.usr_id=e.user_id JOIN "\
				"public.examiner_courses ec ON ec.examiner_id=e.examiner_id " \
				"where u.usr_active_status=true and  e.availability=true and ec.examiner_crs_name=%s "\
				"order by e.ranking desc;"
                args=(courseName,)
                # where u.usr_active_status=true and
                cursor.execute(query,args)
                rankedExaminers=cursor.fetchall()
                onDutyExmnrs = self.onDutyExaminers()
                NameList = []
                for re in rankedExaminers:
                    if onDutyExmnrs.__len__() != 0:
                        for tup in onDutyExmnrs:
                            if re[2] not in tup:
                                NameList.append(str(re[2])+"_"+re[0])
                    else:
                         NameList.append(str(re[2])+"_"+re[0])

                print("Name list : ",NameList)
                return NameList
        except Exception as e:
                print("Exception in getRankedExaminer",str(e))
        finally:
                if cursor!=None:
                    cursor.close()
    
    def findCrsDetail(self,id):
        try:
            if self.connection!=None:
                self.cursor=self.connection.cursor()
                query ="Select * from roadmap where rd_id = %s;"
                arg =(id,)
                self.cursor.execute(query,arg)
                crs_code=self.cursor.fetchone()
                return crs_code
        except Exception as e:
                print("Exception in getting findCrsDetail",str(e))
        finally:
                if self.cursor!=None:
                    self.cursor.close()

    def CreateDuty(self,List):
        try:
            if self.connection!=None:
                cursor=self.connection.cursor()
                # exam_id=List[0], rd_id = List[4],rd_dept=List[2],rd_year=List[3]
                # deadline = datetime.date.today() + datetime.timedelta(days=15)
                query="INSERT INTO public.exam_duty( "\
                      "examiner_id,  status_req, rd_id, rd_dept, rd_year, rd_crs_code) "\
                      "VALUES (%s, %s, %s, %s, %s, %s);"
                # duty_status =  0 for notAssigned, 1 for assigned, 2 for accepted, 3 for rejected
                args=(List[0], 0,List[4],List[2],List[3],self.findCrsDetail(List[4])[4])
                cursor.execute(query,args)
                self.connection.commit()
                query = "select exam_duty_id from exam_duty where rd_id = %s;"
                args = (List[4],)
                cursor.execute(query,args)
                id = cursor.fetchone()
                return id[0]
        except Exception as e:
                print("Exception in Creating Duty",str(e))
        finally:
                if cursor!=None:
                    cursor.close()

    def SendDuty(self,id):
        try:
            if self.connection!=None:
                cursor=self.connection.cursor()
                # exam_id=List[0], rd_id = List[4],rd_dept=List[2],rd_year=List[3]
                deadline = datetime.date.today() + datetime.timedelta(days=15)
                query= "UPDATE exam_duty SET status_req = 1, request_date = %s, paper_upload_deadline = %s, result_upload_deadline = %s WHERE exam_duty_id = %s;"
                # duty_status =  0 for notAssigned, 1 for assigned, 2 for accepted, 3 for rejected
                args=(datetime.date.today(),(datetime.date.today() + datetime.timedelta(days=30)), (datetime.date.today() + datetime.timedelta(days=35)), id)
                cursor.execute(query,args)
                self.connection.commit()
                self.SendReqforDuty(id)
                return "True"
        except Exception as e:
                print("Exception in Sending Duty",str(e))
        finally:
                if cursor!=None:
                    cursor.close()

    def GetCurrentYear(self):
        import datetime
        today = datetime.date.today()
        year = today.strftime("%Y")
        return year
    
    def GetCurrentMonth(self):
        import datetime
        today = datetime.date.today()
        month = today.strftime("%M")
        return month
    
    def GetCurrentFollowedRoadMapYear(self):
        try:
            if self.connection!=None:
                self.cursor=self.connection.cursor()
                currYear = self.GetCurrentYear()
                print(currYear)
                lastYear=int(currYear)-3
                strLastYear=str(lastYear)

                print(lastYear)
                self.cursor.execute("""Select DISTINCT batch_rd_year from batch_enrollment where date_part('year', to_date(batch_year_date, 'DD/MM/YYYY')) BETWEEN %s and %s; """, (strLastYear,currYear))
                roadmapList=self.cursor.fetchall()
                return roadmapList

        except Exception as e:
                print("Exception in getting roadmap",str(e))
        finally:
                if self.cursor!=None:
                    self.cursor.close()

    def GetCurrentBatchesXyear(self):
        try:
            # print("In GetCurrentBatchesXyear calc")
            if self.connection!=None:
                self.cursor=self.connection.cursor()
                currYear = self.GetCurrentYear()
                # print(type(currYear))
                lastYear=int(currYear)-3
                # print(str(lastYear))
                self.cursor.execute("""Select date_part('year', to_date(batch_year_date, 'DD/MM/YYYY')) from batch_enrollment where date_part('year', to_date(batch_year_date, 'DD/MM/YYYY')) BETWEEN %s and %s; """, (lastYear,currYear))
                currentBatches=self.cursor.fetchall()
                # print(roadmapList)
                return currentBatches

        except Exception as e:
                print("Exception in getting roadmap",str(e))
        finally:
                if self.cursor!=None:
                    self.cursor.close()

    def GetDepartments(self):
        try:
            if self.connection!=None:
                self.cursor=self.connection.cursor()
                self.cursor.execute("Select dep_name from departments;")
                deptList=self.cursor.fetchall()
                return deptList
        except Exception as e:
                print("Exception in getting departments",str(e))
        finally:
                if self.cursor!=None:
                    self.cursor.close()

    def getFollowedRoadMapByCurrentBatches(self):
        # print("In getFollowedRoadMapByCurrentBatches")
        #2020
        CurrentFollowedRoadMapYear = self.GetCurrentFollowedRoadMapYear()
        #(6,4,2)
        CurrentSemester = self.getSemester()
        #(cs,it)
        CurrentDept = self.GetDepartments()

        years_string = ", ".join("'" + str(x[0]) + "'"for x in CurrentFollowedRoadMapYear)
        departments_string = ", ".join("'{}'".format(x[0].lower()) for x in CurrentDept)
        semesters_string = ", ".join("{}".format(int(x)) for x in CurrentSemester)
        # print(years_string)
        # print(departments_string)
        # print(semesters_string)
        # RoadMapIDList = None
        try:
            if self.connection!=None:
                self.cursor=self.connection.cursor()
                self.cursor.execute("SELECT * FROM roadmap WHERE rd_year IN ({}) AND rd_dept IN ({}) AND rd_semester IN ({}) and rd_prac_status = 0;".format(years_string, departments_string, semesters_string))
                RoadMapIDList=self.cursor.fetchall()
                return RoadMapIDList
        except Exception as e:
            print("Exception in getting roadmapID",str(e))
        finally:
                if self.cursor!=None:
                    self.cursor.close()
        
    def getSemester(self):
        CurrentBatch = self.GetCurrentBatchesXyear()
        CurrentYear = self.GetCurrentYear()
        CurrentMonth = int(self.GetCurrentMonth())
        CurrentSemesters = []
        listCompletedYearXsems = []
        for year in CurrentBatch:
            listCompletedYearXsems.append(2*(int(CurrentYear) - int(year[0])))
        if(CurrentMonth >= 10 or CurrentMonth == 1):
            for sem in listCompletedYearXsems:
                CurrentSemesters.append(int(sem)-1)
        elif(CurrentMonth > 1 or CurrentMonth <= 7):
            CurrentSemesters = listCompletedYearXsems
        return CurrentSemesters
 
    def getNotAssignedDuties(self):
        try:
            if self.connection!=None:
                self.cursor=self.connection.cursor()
                self.cursor.execute("select ed.exam_duty_id, u.usr_name,u.usr_email,rd.rd_crs_name,rd.rd_semester,rd.rd_dept from users u "\
                    "JOIN examiner e ON u.usr_id=e.user_id JOIN exam_duty ed "\
                    "ON e.examiner_id=ed.examiner_id JOIN roadmap rd ON "\
                    "rd.rd_id = ed.rd_id where ed.status_req = 0;")
                dutyList=self.cursor.fetchall()
                print("Duty list : ",dutyList)
                return dutyList
        except Exception as e:
                print("Exception in getting duties",str(e))
        finally:
                if self.cursor!=None:
                    self.cursor.close()
    
    def getAllDuties(self):
        try:
            if self.connection!=None:
                self.cursor=self.connection.cursor()
                self.cursor.execute("select ed.exam_duty_id, u.usr_name,u.usr_email,rd.rd_crs_name,rd.rd_semester,rd.rd_dept,ed.status_req from users u "\
                    "JOIN examiner e ON u.usr_id=e.user_id JOIN exam_duty ed "\
                    "ON e.examiner_id=ed.examiner_id JOIN roadmap rd ON "\
                    "rd.rd_id = ed.rd_id where ed.status_req != 0;")
                dutyList=self.cursor.fetchall()
                return dutyList
        except Exception as e:
                print("Exception in getting duties",str(e))
        finally:
                if self.cursor!=None:
                    self.cursor.close()

    def getCoursesName(self,department,year):
        
        List = self.getFollowedRoadMapByCurrentBatches()
        CoursesList = []
        try:
            if self.connection!=None:
                cursor=self.connection.cursor()
                cursor.execute("select rd_id from exam_duty;")
                RoadMapIDList=cursor.fetchall()
                for rd in List:
                    if rd[1] == department and rd[3] == year:
                        if RoadMapIDList.__len__() != 0:
                            for tup in RoadMapIDList:
                                if rd[0] not in tup:
                                    CoursesList.append(str(rd[0])+"_"+rd[5])
                        else:
                            CoursesList.append(str(rd[0])+"_"+rd[5])
                return CoursesList
        except Exception as e:
                print("Exception in getAlreadySentCourses",str(e))
        finally:
                if cursor!=None:
                    cursor.close()
    
    #Password==lenwtfhxccnpghlt

    def SendReqforDuty(self,examDutyid):
        try:
            cursor = self.connection.cursor()
            query = ("select u.usr_name,u.usr_email,rd.rd_crs_name,rd_crs_code,rd_dept"\
                ",rd_semester from users u "\
                    "JOIN examiner e ON u.usr_id=e.user_id JOIN exam_duty ed "\
                    "ON e.examiner_id=ed.examiner_id JOIN roadmap rd ON "\
                    "rd.rd_id = ed.rd_id  where ed.exam_duty_id = %s;")
            arg=(examDutyid,)
            cursor.execute(query,arg)
            exam_duty_one = cursor.fetchone()
            self.connection.commit()
            #Construct the HTML email content
            html_content = f"""\
            <html>
             <body>
                    <p>Hi <b>{exam_duty_one[0]}</b>,<br><br>
                    Congratulations you are selected for the Exam Duty. Details are given below
                    <br><b>Course</b> : {exam_duty_one[2]} - {exam_duty_one[3]}
                    <br><b>Department</b> : {exam_duty_one[4]}
                    <br><b>Semester</b> : {exam_duty_one[3]}
                    <br>
                   
                    Thanks,<br><br>
                    Show Your willingness by replying.<br><br>
                    <a href="https://www.w3schools.com/">
                        <button style="background-color: green; color: white; padding: 10px 20px;">Accepted!</button>
                    </a>
                      <a href="https://www.w3schools.com/">
                        <button style="background-color: red; color: white; padding: 10px 20px;">Rejected!</button>
                    </a>
                    </p>
                </body>
            </html>
        """

            # Create the email message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Exam Duty Assignment"
            message["From"] = "acms.duty@gmail.com"  # Replace with your email address
            message["To"] =   exam_duty_one[1]# Replace with the recipient's email address

            # Attach the HTML content to the message
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)

            # Send the email using Gmail SMTP
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login("acms.duty@gmail.com", "lenwtfhxccnpghlt")  # Replace with your Gmail credentials
                server.sendmail(message["From"], message["To"], message.as_string())

            print("Email sent successfully.")
            return True
        except Exception as e:
            print("Exception in SendReqforDuty:", str(e))
            return False

   
    def getExaminerNameAgainstId(self,examinerid):
            try:
                if self.connection != None:
                    cursor = self.connection.cursor()
                    query = f'''select * from users u JOIN examiner e ON u.usr_id=e."user_id " where  e.examiner_id= %s;'''
                    arg=(examinerid,)
                    cursor.execute(query,arg)
                    exam_duty_one = cursor.fetchone()
                    self.connection.commit()
                    return exam_duty_one[1]
                else:
                    return False
            except Exception as e:
                print("Exception in message: ", str(e))
                return False
            finally:
                if cursor:
                    cursor.close()

#     # def mail(self,receiver_email,txt):
#     #     sender_email = "elite.express243@gmail.com"
#     #     # receiver_email = "bitf19a027@pucit.edu.pk"
#     #     print(receiver_email)
#     #     # password = 'fnwxynvngtjesidi'
#     #     password = "njsopxyyzkkssixt"
#     #     # message = txt
#     #     message = MIMEMultipart("alternative")
#     #     message.attach(txt)
#     #     message = message.as_string()
#     #     try:
#     #         server = smtplib.SMTP("smtp.gmail.com", 587)
#     #         server.ehlo()
#     #         server.starttls()
#     #         server.login(sender_email, password)
#     #         server.sendmail(sender_email, receiver_email, message)
#     #         print("Email sent successfully")
#     #     except Exception as e:
#     #         print("Failed to send email")
#     #         print(e)
#     #     finally:
#     #         server.quit()

    def mail(self, receiver_email, txt):
        sender_email = "elite.express243@gmail.com"
        # receiver_email = "bitf19a027@pucit.edu.pk"
        print(receiver_email)
        # password = 'fnwxynvngtjesidi'
        password = "njsopxyyzkkssixt"
        # message = txt
        message = MIMEMultipart("alternative")
        message.attach(txt)
        message = message.as_string()
        server = None  # Initialize server to None
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            print("Email sent successfully")
        except Exception as e:
            print("Failed to send email")
            print(e)
        finally:
            if server is not None:  # Check if server has a value before calling server.quit()
                server.quit()

    def ExaminerDetailForDuty(self,examinerid):
            try:
                if self.connection != None:
                    cursor = self.connection.cursor()
                    query = f'''select u.usr_name,u.usr_email, e.institution  from users u JOIN examiner e ON u.usr_id=e.user_id where  e.examiner_id= %s;'''
                    arg=(examinerid,)
                    cursor.execute(query,arg)
                    examiner = cursor.fetchone()
                    self.connection.commit()
                    return examiner
                else:
                    return False
            except Exception as e:
                print("Exception in ExaminerDetailForDuty: ", str(e))
                return False
            finally:
                if cursor:
                    cursor.close()
  
    def deadlines(self, crs_id, exam_id):
        try:
            if self.connection!=None:
                self.cursor=self.connection.cursor()
                query = "Select exam_duty_id, deadline from exam_duty where examiner_id = %s and rd_id = %s;"
                args = (exam_id, crs_id)
                self.cursor.execute(query,args)
                deptList=self.cursor.fetchone()
                return deptList
        except Exception as e:
                print("Exception in fetching Deadlines",str(e))
        finally:
                if self.cursor!=None:
                    self.cursor.close()
    
    def getDuty(self,id):
        try:
            if self.connection!=None:
                self.cursor=self.connection.cursor()
                query = "Select examiner_id, rd_id from exam_duty where exam_duty_id = %s;"
                args = (id,)
                self.cursor.execute(query,args)
                dList=self.cursor.fetchone()
                print("getDuty: ",dList)
                return dList
        except Exception as e:
                print("Exception in fetching Duty",str(e))
        finally:
                if self.cursor!=None:
                    self.cursor.close()
    
    def fetchDutyDetail(self, List):
        #List = [examinerId,Name,dept,roadmapyr,rd_id,courseName]
        DataList = []
        examiner = self.ExaminerDetailForDuty(List[0])
        courseDetail= self.findCrsDetail(List[1])
        for item in examiner:
             DataList.append(item)
        DataList.append(courseDetail[1].upper() +"-"+ str(courseDetail[2])) # dept-semester
        DataList.append(courseDetail[4] +"-"+ courseDetail[5]) #courseCode-Name
        print(DataList)
        return DataList
        
    def getRoadMapList(self):
        
        if self.connection != None:
            cursor = self.connection.cursor()
            try:
                cursor.execute('select * from public."roadmap"')
                roadMapList = cursor.fetchall()
                return roadMapList
            except Exception as e:
                print("Exception in checkUserExist", str(e))
                return NULL
            finally:
                if cursor != None:
                    cursor.close()
        else:
            return NULL
    
    def getcourse(self, id):
        
        if self.connection != None:
            cursor = self.connection.cursor()
            try:
                cursor.execute("select * from public.roadmap where rd_id =  %s;",[id["id"]])
                course = cursor.fetchone()
                return course
            except Exception as e:
                print("Exception in Fetching Course", str(e))
                return NULL
            finally:
                if cursor != None:
                    cursor.close()
        else:
            return NULL
# Open a cursor to perform database operations
    def insertRoadmap(self, roadmap):
        if self.connection != None:
                cursor = self.connection.cursor()
                try:
                    query = 'INSERT INTO public."roadmap" (rd_dept,rd_semester,rd_year,rd_crs_code,rd_crs_name,rd_prac_status,rd_crs_hr,rd_crs_book,rd_crs_outline) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    args = ('usma', '12345', '32202-3561801-6', 'xyz.png', 'lahore', 'usma@gmail.com', 'true', 'xyzz', 'male')
                    cursor.execute(query, args)
                    self.connection.commit()
                    return True
                except Exception as e:
                    print("Exception in insertRoadmap", str(e))
                    return False
                finally:
                    if cursor != None:
                        cursor.close()
        else:
                return False
    
    def updateRoadmap(self, dept, course_name, course_code, ID=240):
        if self.connection != None:
            cursor = self.connection.cursor()
            try:
                query = f'''update public."roadmap" set rd_dept = {dept}, rd_crs_name = {course_name}, rd_crs_code = '{course_code}' where  rd_id = {ID};'''
                cursor.execute(query)
                self.connection.commit()
                return True
                
            except Exception as e:
                print("Exception in updateRoadmap", str(e))
                return False
            finally:
                if cursor:
                    cursor.close()
        else:
            return False
    
    def deleteCourse(self, ID=240):
        if self.connection != None:
            cursor = self.connection.cursor()
            try:
                query = f'delete from public."roadmap" where rd_id = {ID};'
                cursor.execute(query)
                self.connection.commit()
                return True
            except Exception as e:
                print("Exception in deleteRoadmap", str(e))
                return False
            finally:
                if cursor:
                    cursor.close()
        else:
            return False

# dbModel= DatabaseModel("ACMS","postgres","aat","localhost");
# dbModel.GetCurrentFollowedRoadMapYear();

        



