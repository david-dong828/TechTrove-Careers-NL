# Name: Dong Han
# Mail: dongh@mun.ca

import json
from datetime import datetime,timedelta
import os
import mysql.connector

def connectDB():
    # For Vercel, using PlanetScale
    db = mysql.connector.connect(
        host=os.getenv("PLANETSCALE_DB_HOST"),
        user=os.getenv("PLANETSCALE_DB_USERNAME"),
        passwd=os.getenv("PLANETSCALE_DB_PASSWORD"),
        db=os.getenv("PLANETSCALE_DB"),
        autocommit=True
    )
    cursor = db.cursor()
    return db, cursor

def is_job_json_existed_in_mysql(job_file_id,cursor,tableName="NL_TECH_JOBS"):
    try:
        sql = f"select json_data from {tableName} where job_id = %s"
        cursor.execute(sql,(job_file_id,))

        result = cursor.fetchone()

        if result and result[0]: # also check the json_data is not empty
            json_data = json.loads(result[0])
            return json_data
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error in is_job_json_existed_in_mysql: {err}")
        return None

def getJobData(company):
    job_file_id = company + "_" + datetime.now().strftime("%Y-%m-%d")
    db, cursor = connectDB()
    json_data = is_job_json_existed_in_mysql(job_file_id, cursor)
    if not json_data:
        yesterday_job_file_id =  company + "_" +  (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        json_data = is_job_json_existed_in_mysql(yesterday_job_file_id, cursor)
        if not json_data:
            return "4"
    return json_data
