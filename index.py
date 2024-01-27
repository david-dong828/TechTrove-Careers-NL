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

@app.route("/verafin", methods=["POST"])
def getVerafinJobs():
    aipCompanies = readjson(aipCompanyfile)
    url = find_value_by_partial_key(aipCompanies,"verafin")

    if url:
        data = checkVerafin(url)
        return data
    else: return "-1"

@app.route("/colab", methods=["POST"])
def getColab():
    aipCompanies = readjson(aipCompanyfile)
    url = find_value_by_partial_key(aipCompanies, "colab")

    if url:
        data = checkColab(url)
        return data
    else:
        return "-1"

@app.route("/polyu", methods=["POST"])
def getPolyU():
    aipCompanies = readjson(aipCompanyfile)
    url = find_value_by_partial_key(aipCompanies, "polyunit")

    if url:
        data = getCompniesCareerPage.checkPolyU(url)
        return data
    else:
        return "-1"

@app.route("/vission33", methods=["POST"])
def getVission33():
    aipCompanies = readjson(aipCompanyfile)
    url = find_value_by_partial_key(aipCompanies, "vision33")

    if url:
        data = getCompniesCareerPage.checkVission33(url)
        return data
    else:
        return "-1"

@app.route("/mysa", methods=["POST"])
def getMysa():
    aipCompanies = readjson(aipCompanyfile)
    url = find_value_by_partial_key(aipCompanies, "mysa")

    if url:
        data = getCompniesCareerPage.checkMysa(url)
        return data
    else:
        return "-1"

@app.route("/strobeltek", methods=["POST"])
def getStrobeltek():
    aipCompanies = readjson(aipCompanyfile)
    url = find_value_by_partial_key(aipCompanies, "strobel tek")

    if url:
        data = getCompniesCareerPage.checkStrobeltek(url)
        return data
    else:
        return "-1"

@app.route("/otherocean", methods=["POST"])
def getOtherOcean():
    aipCompanies = readjson(aipCompanyfile)
    url = find_value_by_partial_key(aipCompanies, "other ocean")

    if url:
        data = getCompniesCareerPage.checkOtherOcean(url)
        return data
    else:
        return "-1"

@app.route("/avalonholo", methods=["POST"])
def getAvalonholo():
    aipCompanies = readjson(aipCompanyfile)
    url = find_value_by_partial_key(aipCompanies, "avalon")

    if url:
        data = getCompniesCareerPage.checkAvalonholo(url)
        return data
    else:
        return "-1"

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

if __name__ == '__main__':
    app.run(host='0.0.0.0')

