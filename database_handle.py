# Name: Dong Han
# Mail: dongh@mun.ca

import mysql.connector
import json

def connectDB():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="david"
    )

    cursor = db.cursor()

    return db, cursor


def createTable(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS NL_JOB_DATA (
            job_company varchar(100),
            job_title varchar(255),
            link varchar(255),
            job_id varchar(50) primary key
        )
        """
    )

def saveTotable(company, title,link,jobid,db,cursor):
    sql = "INSERT INTO NL_JOB_DATA (job_company,job_title,link,job_id) values (%s,%s,%s,%s)"
    val = (company, title,link,jobid)
    cursor.execute(sql,val)
    db.commit()

def main():
    db, cursor = connectDB()


if __name__ == '__main__':
    main()