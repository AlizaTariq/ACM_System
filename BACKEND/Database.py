import psycopg2
import psycopg2.extras
import datetime
from Classes import UserAdmin

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
                query="select a.admin_id from admin a where a.usr_id IN(Select u.usr_id from users u "\
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
            print("Exception in checkAdminUserExist",str(e))
        finally:
            if cursor!=None:
                cursor.close()


    #Function-2
    def getAdminNotifications(self):
        try:
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select ac_id,rd_crs_code,examiner_id from practical_duty where prac_ntf_status=1"
                cursor.execute(query)
                adminNotifications=cursor.fetchall()
                print("Admin Notifications are : ",adminNotifications)
                return adminNotifications
        except Exception as e:
            print("Exception in checkAdminUserExist",str(e))
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


    def getPracticalCourseCode(self,rdYear,dept,sem):
        try:
            print("\n\nIn Road Map DataBase")
            if self.connection!=None:
                cursor=self.connection.cursor()
                print(rdYear,"  ",dept," --  ",sem)
                query="select rd_crs_code from roadmap where rd_year=%s and rd_dept=%s and rd_semester=%s and rd_prac_status=1;"
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
                query="select rd_crs_code from roadmap where rd_year=%s and rd_dept=%s and rd_semester=%s and rd_prac_status=0;"
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
                        query="insert into practical_duty(ac_id,rd_dept,rd_year,rd_crs_code,prac_batch_num,prac_duty_status) values(%s,%s,%s,%s,%s,0);"
                        
                        dept1=2
                        if(duty[1]=='cs'):
                            dept1=1

                        args=(duty[0],dept1,duty[3],crsCode,duty[5])
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


            # if(st==1):
            #     pracDuties=self.getCollegeCoursesDutiesTheorey(college[0],btachRdSem,departmentsList)
            #     st=st+1
            # else:
            #     pracDuties=self.getCollegeCoursesDutiesTheorey(college[0],btachRdSem,departmentsList,pracDuties)
            # print("\n\ntheerryy Duties lust ::  \n\n---------------->",pracDuties)



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
                query="select distinct rd_year from roadmap where rd_dept=%s order by rd_year desc limit 4;"
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
                query="select ac_id,rd_dept,rd_year,rd_crs_code,prac_batch_num,prac_duty_status from practical_duty"
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
                
                query="select rd_semester,rd_crs_name from roadmap where rd_year=%s and rd_crs_code=%s and rd_dept=%s and rd_prac_status=1; "
                
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
                query="select prac_duty_id from practical_duty where ac_id=%s and rd_dept=%s and rd_crs_code=%s;"
                dept1='1'
                if dept=="it":
                    dept1='2'
                
                args=(acId,dept1,crsCode)
                cursor.execute(query,args)
                practId=cursor.fetchall()
                print("practId Id list -->",practId)
                return practId[0]
        except Exception as e:
                print("Exception in  get practical duty id ",str(e))
        finally:
                if cursor!=None:
                    cursor.close()




    def getCollegeCourses(self,clgId):
        try:
            print("In get All college")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select distinct rd_crs_code from practical_duty where ac_id=%s"

                args=(clgId,)
                cursor.execute(query,args)
                courses=cursor.fetchall()
                #print("courses list -->",courses)
                return courses
        except Exception as e:
                print("Exception in getting clgName",str(e))
        finally:
                if cursor!=None:
                    cursor.close()

    def getCollegeCourseInfo(self,rdYear,dept,crs_code):
        try:
            print("In get All college")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select rd_crs_name,rd_crs_code from roadmap where rd_year=%s and rd_dept=%s and rd_crs_code=%sand rd_prac_status=1"

                args=(rdYear,dept,crs_code)
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
                query="select distinct rd_year from practical_duty where ac_id=%s and rd_dept=%s"
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


    def getAdminNotifications(self):
        try:
            print("In get admin ntfs")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select examiner_id,prac_duty_id,prac_duty_status,prac_info,ac_id,rd_crs_code from practical_duty where prac_duty_status in(2,3) and prac_ntf_status=2"
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


        



