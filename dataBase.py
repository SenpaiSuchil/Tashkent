#import mariadb
import mysql.connector
import datetime

class myDataBase():
    connector=mysql.connector.connect(
        user="senpaisuchil",
        password="1234",
        host="172.17.0.2", #ip del docker
        database="tashkent",
        port=3306
        )
    connector.autocommit=False
    cursor=connector.cursor()

    def __init__(self):
        super().__init__()

    def insert(self, id, time_start, time_stamp, status):
        #insert values into the database
        sql="INSERT INTO reminders (user_id, time_start, time_stamp, reminder_status) VALUES (%s, %s, %s, %s)"
        values=(f"{id}", f"{time_start}", f"{time_stamp}", status)
        self.cursor.execute(sql, values)
        self.connector.commit()

    def get(self):
        #get the list of people who activated the reminder to check them in the loop task
        self.cursor.execute("SELECT time_stamp, user_id, time_start FROM reminders WHERE reminder_status=1")
        result=self.cursor.fetchall()
        return result

    def verify(self, id):
        #verify if the user has already an active reminder or is already in de database
        #1.- if the user are already on the database and has an active rimender return 1
        #2.- if the user are already on the database but the reminder is off, will update the value and activate the reminder and return 2
        # 3.-if is not in the database will return 0 
        self.cursor.execute(f"SELECT * FROM reminders WHERE user_id={id}")
        result=self.cursor.fetchall()
        if len(result)>0:
            status=result[0][2]
            if status==1:
                
                return 1
            if status==0:

                time=str(datetime.datetime.now())
                sql=f"UPDATE reminders SET reminder_status=1, time_start=%s WHERE user_id=%s"
                values=(f"{time}", f"{id}")
                self.cursor.execute(sql, values)
                self.connector.commit()
                return 2
        else:
            return 0

    def changeDate(self, newDate, id):
        sql=f"UPDATE reminders SET time_stamp=%s WHERE user_id=%s"
        values=(f"{newDate}", f"{id}")
        self.cursor.execute(sql, values)
        self.connector.commit()
    
    def changeStatus(self, id, value):
        sql=f"UPDATE reminders SET reminder_status=%s WHERE user_id=%s"
        values=(value, id)
        self.cursor.execute(sql, values)
        self.connector.commit()