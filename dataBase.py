#import mariadb
import mysql.connector

class myDataBase():
    connector=mysql.connector.connect(
        user="senpaisuchil",
        password="1234",
        host="127.0.0.1",
        port=3306,
        database="duck"
        )
    connector.autocommit=False
    cursor=connector.cursor()

    def __init__(self):
        super().__init__()

    def insert(self, id, hour, status):
        sql="INSERT INTO reminders (user_id, time_stamp, reminder_status) VALUES (%s, %s, %s)"
        values=(f"{id}", f"{hour}", status)
        self.cursor.execute(sql, values)
        self.connector.commit()

    def get(self):
        self.cursor.execute("SELECT user_id, HOUR(time_stamp), MINUTE(time_stamp) FROM reminders WHERE reminder_status=1")
        result=self.cursor.fetchall()
        pass
