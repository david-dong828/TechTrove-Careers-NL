# used to check programmer jobs of newfoundland tech companies
import json,os
import requests
from flask import Flask, render_template, jsonify
import api.getCompniesCareerPage
import api.for_vercel

app = Flask(__name__,static_folder='static')

# aipCompanyfile = "/api/aipCompanies.json"
aipCompanyfile = os.path.join(os.path.dirname(__file__), 'aipCompanies.json')

@app.route("/")
def index():
    return render_template("index.html")

def readjson(filePath):
    try:
        with open(filePath,"r") as f:
            data = json.load(f)
            return data
    except Exception:
        print("NO SUCH JSON FILE")
        return

def find_value_by_partial_key(data,partial_key):
    for key,value in data.items():
        if partial_key.lower() in key.lower():
            return value
    return

@app.route("/<company>", methods=["POST"])
def get_jobs(company):
    aipCompanies = readjson(aipCompanyfile)
    url = find_value_by_partial_key(aipCompanies, company)

    # For local usage
    if url:
        if os.getenv('VERCEL'):
            return api.for_vercel.getJobData(company)
        scraper = api.getCompniesCareerPage.ScraperFactory.get_scraper(company,url)
        if scraper:
            result = scraper.scrape()
            scraper.close_driver()
            return result
    else:
        return "-1"

    # For work with AWS Lambda which holds the scrappers
    # if url:
    #     # Construct the payload to send to AWS Lambda
    #     payload = {"company": company, "url": url}
    #     # Call the AWS Lambda function through API Gateway
    #     response = requests.post("http://api",json=payload)
    #     print("endpoint...")
    #     if response.status_code == 200:
    #         result = response.json()
    #         return jsonify(result)
    #     else:
    #         print("no 500")
    #         return jsonify({"error": "Failed to scrape data"}), 500
    # else:
    #     return jsonify({"error": "Company not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5005)

