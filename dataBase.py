import mariadb

class myDataBase():
    connector=mariadb.connect(
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

        self.cursor.execute("INSERT INTO reminders (user_id, time_stamp, reminder_status) VALUES (?, ?, ?)",
        (f"{id}", f"{hour}", status)) 
        self.connector.commit()

    def get(self):
        self.cursor.execute("SELECT HOUR(time_stamp), id FROM reminders WHERE status=1")
        print(f"{self.cursor}")
        pass
