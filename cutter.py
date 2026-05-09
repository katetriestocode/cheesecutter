import requests
from bs4 import BeautifulSoup

from openai import OpenAI
import os
client = OpenAI(
    api_key=os.environ.get("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"),
    base_url="https://api.groq.com/openai/v1",
)
# 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

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