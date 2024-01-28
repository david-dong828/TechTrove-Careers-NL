# Name: Dong Han
# Mail: dongh@mun.ca

import mysql.connector

def connectDB():
    # For local mysql
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="david"
    )

    # db = mysql.connector.connect(
    #     host="https://app.planetscale.com/david-dong828/david",
    #     user="0li99e4aqzrxuj0kpx3o",
    #     password="pscale_pw_1Hpwr3n74cTJdBP4QYcQ9dkbTQx8rMdENDwWWA6FrLw",
    #     database="david"
    # )

    cursor = db.cursor()

    return db, cursor


def createTable(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS NL_TECH_JOBS (
            job_id varchar(100) PRIMARY KEY,
            json_data TEXT
        );
    
        """
    )
    # cursor.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS NL_JOB_DATA (
    #
    #         job_company varchar(100),
    #         job_title varchar(255),
    #         link varchar(255),
    #         job_id varchar(50)
    #     )
    #     """
    # )

def saveTotable(company, title,link,jobid,db,cursor):
    sql = "INSERT INTO NL_JOB_DATA (job_company,job_title,link,job_id) values (%s,%s,%s,%s)"
    val = (company, title,link,jobid)
    cursor.execute(sql,val)
    db.commit()

def saveJsonFileToTable(job_id,json_string,db,cursor):
    sql = "insert into NL_TECH_JOBS (job_id,json_data) values (%s,%s)"
    val = (job_id,json_string)
    cursor.execute(sql,val)
    db.commit()

def main():
    db, cursor = connectDB()


if __name__ == '__main__':
    main()