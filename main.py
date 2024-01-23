# used to check programmer jobs of newfoundland aip companies

from flask import Flask,request,render_template,jsonify,Response

app = Flask(__name__,static_folder='assets')

@app.route("/")
def index():
    return render_template("index.html")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0')

