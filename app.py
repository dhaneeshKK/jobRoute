from flask import Flask, render_template, request
from dotenv import load_dotenv
import openai
import os
import json
load_dotenv()
openai.organization = os.getenv("ORG_ID")
openai.api_key = os.getenv("JOB_ROUTE_KEY")
answer = ''
app = Flask(__name__)

prompt_example = "I am doing research on transferable skills between similar occupations. My primary reference is the National Occupation Classification (NOC) developed by the Government of Canada. Based on a given NOC code, I want you to identify 5 similar jobs with a percentage similarity estimate based on overlapping skills and education requirements. The job I need you to analyze is "

prompt_json = "Please provide a response in JSON format only, based on the given NOC code. Include the original job title, and a node called 'similar_jobs' with sub-nodes containing 'job_title', 'noc_code' and 'percent_similarity'"


def callChatGpt(prompt_text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_text,
        max_tokens=3000,
        temperature=0
    )
    answer = response.choices[0].text
    return answer


@app.route("/answer", methods=["GET", "POST"])
def get_prompt():
    if request.method == "POST":
        recent_job = request.form.get("recentjob")
        print(recent_job)
        prompt_text = prompt_example + recent_job + prompt_json
        print(prompt_text)
        answer = json.loads(callChatGpt(prompt_text))
        # return answer
        print(type(answer))
        return render_template('answer.html', answerToHtml=answer)


@app.route("/", methods=["GET", "POST"])
def job_route():
    return render_template('home.html')


# callChatGpt("How many bones do a shark have?")
# print(callChatGpt("Who is the creator of Tesla car company?"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
