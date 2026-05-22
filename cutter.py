from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
import os

app = Flask(__name__)
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("groq_api_key"),
    base_url="https://api.groq.com/openai/v1",
)

def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.select_one('h1').text if soup.select_one('h1') else "No title available"
    text = soup.select_one('p').text if soup.select_one('p') else "No content available"

    return f"Title: {title}\nContent: {text}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    user_link = data.get('link')

    scraped_content = scrape(user_link)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"summarize this content: {scraped_content}"
            }
        ]
    )

    summary = chat_completion.choices[0].message.content
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)