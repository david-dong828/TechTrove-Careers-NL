# used to check programmer jobs of newfoundland tech companies
import json,os
from flask import Flask, render_template
import api.getCompniesCareerPage
import api.for_vercel
import threading
from api.chatBot import chatBot_main

app = Flask(__name__,static_folder='static')

page = """
<|layout|columns=300px 1|
<|part|class_name=sidebar|
# AI Job **Help**{: .color-primary} # {: .logo-text}
<|New Conversation|button|class_name=fullwidth plain|id=reset_app_button|on_action=reset_chat|>
### Previous activities ### {: .h5 .mt2 .mb-half}
<|{selected_conv}|tree|lov={past_conversations}|class_name=past_prompts_list|multiple|adapter=tree_adapter|on_change=select_conv|>
|>

<|part|class_name=p2 align-item-bottom table|
<|{conversation}|table|style=style_conv|show_all|selected={selected_row}|rebuild|>
<|part|class_name=card mt1|
<|{current_user_message}|input|label=Write your message here...|on_action=send_message|class_name=fullwidth|change_delay=-1|>
|>
|>
|>
"""

# aipCompanyfile = "/api/aipCompanies.json"
aipCompanyfile = os.path.join(os.path.dirname(__file__), 'aipCompanies.json')

@app.route("/")
def index():
    return render_template("index_main.html")

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


def run_flask():
    app.run(host='0.0.0.0', port=5005)

def run_chat():
    chatBot_main()

if __name__ == '__main__':
    # app.run(host='0.0.0.0',port=5005)
    # Create threads for Flask and Taipy
    flask_thread = threading.Thread(target=run_flask)
    chat_thread = threading.Thread(target=run_chat)

    # Start both servers
    flask_thread.start()
    chat_thread.start()

    # Wait for both threads to complete (optional, depending on your shutdown strategy)
    flask_thread.join()
    chat_thread.join()


