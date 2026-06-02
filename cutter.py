from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from groq import Groq

app = Flask(__name__)
load_dotenv()

client = Groq(
    api_key=os.environ.get("groq_api_key"),
)


def scrape(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.select_one('h1').text if soup.select_one('h1') else "No title available"
    
    paragraphs = soup.select('p')
    text = " ".join([p.text for p in paragraphs]) if paragraphs else "No content available"

    return f"Title: {title}\nContent: {text}"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    user_link = data.get('link')

    scraped_content = scrape(user_link)
    
    max_characters = 20000 
    if len(scraped_content) > max_characters:
        print(f"Warning: Content truncated from {len(scraped_content)} to {max_characters} characters.")
        scraped_content = scraped_content[:max_characters] + "\n[im way too broke for u to be asking this much. im only cheesecutting the first 20k characters]"

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful, concise summary assistant. Summarize the content provided by the user accurately."
                },
                {
                    "role": "user",
                    "content": f"Summarize this content: {scraped_content}"
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None
        )


        full_summary = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_summary += chunk.choices[0].delta.content

        return jsonify({"summary": full_summary})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)