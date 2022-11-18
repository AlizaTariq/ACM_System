import psycopg2
import psycopg2.extras

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

    def checkAdminExist(self,email,pwd):
        try:
            print("In DataBase")
            if self.connection!=None:
                cursor=self.connection.cursor()
                query="Select email,password from users where email=%s and password=%s;"
                args=(email,pwd)
                cursor.execute(query,args)
                emailList=cursor.fetchall()
                print(emailList)
                for e in emailList:
                     print(e)
                     if email==e[0]:
                         return True
                return False
        except Exception as e:
            print("Exception in checkUserExist",str(e))
        finally:
            if cursor!=None:
                cursor.close()