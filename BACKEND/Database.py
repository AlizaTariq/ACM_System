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
                query="Select usr_email,usr_password from users where usr_email=%s and usr_password=%s;"
                args=(admin1.email,admin1.password)
                cursor.execute(query,args)
                adminData=cursor.fetchall()
                print("Admin data is : ",adminData)
                for admin in adminData:
                     if admin1.email==admin[0] and admin1.password==admin[1] :
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

        length=len(batchRdList)
        i=0
        count1=1
        count2=2
        while(i<length):
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



    def getCollegeCoursesDuties(self,clgId,batchRdSemList,departmentsList,practicalDuties=[]):

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

                    crsCodeList=self.getPracticalCourseCode(batch[1],dept,batch[2])
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
                for crsCode in duty[5]:
                    print("\n\nIn Road Map DataBase")
                    if self.connection!=None:
                        cursor=self.connection.cursor()
                        query="insert into practical_duty(ac_id,rd_dept,rd_year,rd_crs_code) values(%s,%s,%s,%s);"
                        
                        dept1=2
                        if(duty[1]=='cs'):
                            dept1=1

                        args=(duty[0],dept1,duty[3],crsCode)
                        cursor.execute(query,args)
                        self.connection.commit()

                        
        except Exception as e:
            print("Exception in road_map",str(e))
        finally:
            pass
            #if cursor!=None:
                #cursor.close()


        

    def generateDuties(self):
        collegesList=self.getCollegesList();
        print("\n\ncollege List --> ",collegesList)
        roadMapYear=self.getRoadMapYears()
        print("road map years are : ",roadMapYear)
        st=1

        for college in collegesList:
            #college[0] --id -- affiliated_colleges
            #dep----- enrolled_departments
            affYear=college[1]

            departmentsList= self.getCollegeDepartment(college[0])
            print("--->>>>:::",departmentsList)
            batchesList=self.getBatchesList(affYear)
            batchRdList=[]
            for batchYear in batchesList:
                for rdYear in roadMapYear:
                    if(int(batchYear)>=int(rdYear)):
                        list1=[]
                        list1.append(batchYear)
                        list1.append(rdYear)
                        batchRdList.append(list1)
                        break;
            print("batch rd list is --->>>-->> ",batchRdList)


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
            btachRdSem =self.GetSemesters(batchRdList,flagBatchSt)

            print("current sem of clg ",college[0], " batchrdsems =  ", batchRdList ,"  btaches ", batchRdList
             ,"  dept list ",departmentsList)
            
            if(st==1):
                pracDuties=self.getCollegeCoursesDuties(college[0],btachRdSem,departmentsList)
                st=st+1
            else:
                pracDuties=self.getCollegeCoursesDuties(college[0],btachRdSem,departmentsList,pracDuties)
            print("\n\n--->>>.Length of pract duties ",len(pracDuties))
            print("\n\nPracDuties Duties lust ::  \n\n---------------->",pracDuties)



        self.savePracticalDuties(pracDuties)

            # if(st==1):
            #     pracDuties=self.getCollegeCoursesDutiesTheorey(college[0],btachRdSem,departmentsList)
            #     st=st+1
            # else:
            #     pracDuties=self.getCollegeCoursesDutiesTheorey(college[0],btachRdSem,departmentsList,pracDuties)
            # print("\n\ntheerryy Duties lust ::  \n\n---------------->",pracDuties)



        



    def getRoadMapYears(self):
        try:
            print("\n\nIn Road Map DataBase")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="select distinct rd_year from roadmap order by rd_year desc limit 4 ;"
                cursor.execute(query)
                rdList=cursor.fetchall()
                print("rd list -->>" ,rdList)
                rdList1=[]
                for rd in rdList:
                     print(rd)
                     rdList1.append(rd[0])
                print("rd list11-- -->>" ,rdList1)

                return rdList1


        except Exception as e:
            print("Exception in road_map",str(e))
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
