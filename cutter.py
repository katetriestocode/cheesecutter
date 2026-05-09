import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

client = OpenAI(
    api_key=os.environ.get(""),
    base_url="https://api.groq.com/openai/v1",
)


response = client.responses.create(
    input="Explain the importance of fast language models",
    model="openai/gpt-oss-20b",
)
print(response.output_text)


def scrape():
    url = 'https://example.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)

    title = soup.select_one('h1').text
    text = soup.select_one('p').text
    link = soup.select_one('a').get('href')

    print(title)
    print(text)
    print(link)

if __name__ == '__main__':
    scrape()