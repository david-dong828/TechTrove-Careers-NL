# used to check programmer jobs of newfoundland tech companies
import json,os

from flask import Flask, render_template
import api.getCompniesCareerPage

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

    if url:
        scraper = api.getCompniesCareerPage.ScraperFactory.get_scraper(company,url)
        if scraper:
            result = scraper.scrape()
            scraper.close_driver()
            return result
    else:
        return -1

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5005)

