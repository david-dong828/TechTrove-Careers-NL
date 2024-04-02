# Name: Dong Han
# Mail: dongh@mun.ca
import json
import os
import psycopg2

def get_planetscale_params(file ='vercel_postgres.json'):
    # To check if in CI env
    if os.getenv("POSTGRES_HOST") and os.getenv("POSTGRES_USER") and os.getenv("POSTGRES_PASSWORD"):
        return {
            "host": os.getenv("POSTGRES_HOST"),
            "user": os.getenv("POSTGRES_USER"),
            "passwd": os.getenv("POSTGRES_PASSWORD"),
            "database": os.getenv("POSTGRES_DATABASE")
        }
    else:
        params = {}
        planetScale_paramsfile = os.path.join(os.path.dirname(__file__), file)
        with open(planetScale_paramsfile,"r") as f:
            d= json.load(f)
            params["host"] = d.get("POSTGRES_HOST")
            params["user"] = d.get("POSTGRES_USER")
            params["passwd"] = d.get("POSTGRES_PASSWORD")
            params["database"] = d.get("POSTGRES_DATABASE")
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

    # # For local but, using PlanetScale
    planetsclae_params = get_planetscale_params()
    db = psycopg2.connect(
        host=planetsclae_params.get("host"),
        user=planetsclae_params.get("user"),
        password=planetsclae_params.get("passwd"),
        database=planetsclae_params.get("database"),
        # autocommit=True
    )
    cursor = db.cursor()
    return db, cursor

    # For Vercel postgreSql


def createTable(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS nl_tech_jobs (
            job_id varchar(100) PRIMARY KEY,
            json_data TEXT
        );
    
        """
    )

def saveTotable(company, title,link,jobid,db,cursor):
    sql = "INSERT INTO nl_tech_jobs (job_company,job_title,link,job_id) values (%s,%s,%s,%s)"
    val = (company, title,link,jobid)
    cursor.execute(sql,val)
    db.commit()

def saveJsonFileToTable(job_id,json_string,db,cursor):
    sql = "insert into nl_tech_jobs (job_id,json_data) values (%s,%s)"
    val = (job_id,json_string)
    cursor.execute(sql,val)
    db.commit()

def main():
    db, cursor = connectDB()
    sql = "select * from nl_tech_jobs "
    # sql = "select * from NL_TECH_JOBS where job_id = 'verafin_2024-03-17' "
    # sql = "delete from NL_TECH_JOBS where job_id = 'verafin_2024-03-17'"
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)


if __name__ == '__main__':
    main()