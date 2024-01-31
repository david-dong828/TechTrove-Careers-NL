# used to check programmer jobs of newfoundland aip companies
import json,os

from flask import Flask, render_template,current_app
from api.getCompniesCareerPage import checkVerafin,checkColab
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

def get_company_jobs(company):
    aipCompanies = readjson(aipCompanyfile)
    url = find_value_by_partial_key(aipCompanies, company)

    if url:
        function_map = {
            "verafin": checkVerafin,
            "colab": checkColab,
            "polyunit": api.getCompniesCareerPage.checkPolyU,
            "vision33": api.getCompniesCareerPage.checkVission33,
            "mysa": api.getCompniesCareerPage.checkMysa,
            "strobel tek": api.getCompniesCareerPage.checkStrobeltek,
            "other ocean": api.getCompniesCareerPage.checkOtherOcean,
            "avalon": api.getCompniesCareerPage.checkAvalonholo,
            "enaimco":api.getCompniesCareerPage.checkEnamco
        }
        scraping_function = function_map.get(company)
        if scraping_function:
            return scraping_function(url)
    else:
        return "-1"

@app.route("/<company>", methods=["POST"])
def get_jobs(company):
    return get_company_jobs(company)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5005)

