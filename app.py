from flask import Flask, render_template, request
from dotenv import load_dotenv
from flask_cors import CORS
import openai
import os
import json
import requests
from prompt_variables import prompt_example, prompt_json
app = Flask(__name__, template_folder="templates")
cors = CORS(app)
load_dotenv()
openai.organization = os.getenv("ORG_ID")
openai.api_key = os.getenv("JOB_ROUTE_KEY")
captcha_site_key_v2 = os.getenv("CAPTCHA_SITE_KEY_V2")
captcha_secret_key_v2 = os.getenv("CAPTCHA_SECRET_KEY_V2")
captcha_verify_url = 'https://www.google.com/recaptcha/api/siteverify'
answer = ''


def callChatGpt(prompt_text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_text,
        max_tokens=3000,
        temperature=0
    )
    answer = response.choices[0].text
    return answer


@app.route("/", methods=["GET", "POST"])
def job_route():
    return render_template('home.html', site_key=captcha_site_key_v2)


@app.route("/answer", methods=["GET", "POST"])
def get_prompt():
    if request.method == "POST":
        recent_job = request.form.get("recentJob")
        captcha_response = request.form['g-recaptcha-response']
        captcha_verify_response = requests.post(url=f'{captcha_verify_url}?secret={captcha_secret_key_v2}&response={captcha_response}').json()
        print(captcha_verify_response)
        print(captcha_verify_response["success"])
        if captcha_verify_response["success"] is True:
            prompt_text = prompt_example + recent_job + prompt_json
            answer = json.loads(callChatGpt(prompt_text))
            print(type(answer))
            print(answer)
            return render_template('answer.html', answerToHtml=answer)
        else:
            print("Wrong Captcha")
            return render_template('wrong_captcha.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
