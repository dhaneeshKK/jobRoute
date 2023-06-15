from flask import Flask, render_template, request
from dotenv import load_dotenv
import openai
import os
load_dotenv()
openai.organization = os.getenv("ORG_ID")
openai.api_key = os.getenv("JOB_ROUTE_KEY")

app = Flask(__name__)

prompt_example = "I am doing research on transferable skills between similar occupations. My primary reference is the National Occupation Classification (NOC) developed by the Government of Canada. Based on a given NOC code, I want you to identify 5 similar jobs with a percentage similarity estimate based on overlapping skills and education requirements. The job I need you to analyze is "


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
def get_prompt():
    if request.method == "POST":
        recent_job = request.form.get("recentjob")
        print(recent_job)
        prompt_text = prompt_example + recent_job
        print(prompt_text)
        answer = callChatGpt(prompt_text)
    return render_template('home.html', answer=answer)


# callChatGpt("How many bones do a shark have?")
# print(callChatGpt("Who is the creator of Tesla car company?"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
