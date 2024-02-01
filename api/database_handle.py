# Name: Dong Han
# Mail: dongh@mun.ca
import json
import os
import mysql.connector

def get_planetscale_params(file ='planetscale.json'):
    # To check if in CI env
    if os.environ.get("host") and os.environ.get("user") and os.environ.get("passwd"):
        return {
            "host": os.environ.get("HOST"),
            "user": os.environ.get("USER"),
            "passwd": os.environ.get("PASSWD"),
            "database": os.environ.get("DB")
        }
    else:
        params = {}
        planetScale_paramsfile = os.path.join(os.path.dirname(__file__), file)
        with open(planetScale_paramsfile,"r") as f:
            d= json.load(f)
            params["host"] = d.get("host")
            params["user"] = d.get("user")
            params["passwd"] = d.get("passwd")
            params["database"] = d.get("db")
        return params

def connectDB():
    ## For local mysql
    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="1234",
    #     database="david"
    # )

    # # For Vercel, using PlanetScale
    # db = mysql.connector.connect(
    #     host=os.getenv("PLANETSCALE_DB_HOST"),
    #     user=os.getenv("PLANETSCALE_DB_USERNAME"),
    #     passwd=os.getenv("PLANETSCALE_DB_PASSWORD"),
    #     db=os.getenv("PLANETSCALE_DB"),
    #     autocommit=True,
    #     # ssl_mode="VERIFY_IDENTITY",
    #     # ssl={
    #     #     "ca": "/etc/ssl/cert.pem"
    #     # }
    # )

    # For local but, using PlanetScale
    planetsclae_params = get_planetscale_params()
    db = mysql.connector.connect(
        host=planetsclae_params.get("host"),
        user=planetsclae_params.get("user"),
        passwd=planetsclae_params.get("passwd"),
        db=planetsclae_params.get("database"),
        autocommit=True
    )
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
    sql = "select * from NL_TECH_JOBS limit 1"
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)


if __name__ == '__main__':
    main()