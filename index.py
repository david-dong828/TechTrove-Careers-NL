# used to check programmer jobs of newfoundland aip companies
import json

from flask import Flask,request,render_template,jsonify,Response
from getCompniesCareerPage import checkVerafin,checkColab
import getCompniesCareerPage

app = Flask(__name__,static_folder='assets')

aipCompanyfile = "aipCompanies.json"

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
            "polyunit": getCompniesCareerPage.checkPolyU,
            "vision33": getCompniesCareerPage.checkVission33,
            "mysa": getCompniesCareerPage.checkMysa,
            "strobel tek":getCompniesCareerPage.checkStrobeltek,
            "other ocean":getCompniesCareerPage.checkOtherOcean,
            "avalon":getCompniesCareerPage.checkAvalonholo
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
    app.run(host='0.0.0.0')

