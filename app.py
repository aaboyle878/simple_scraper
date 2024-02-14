import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

page = requests.get('https://quotes.toscrape.com')
headers=headers
soup = BeautifulSoup(page.text, 'html.parser')

quotes = []
quote_elements = soup.find_all('div', class_='quote')

for quote_element in quote_elements:
    #extract text from quote
    text = quote_element.find('span', class_='text').text
    #extract author name
    author = quote_element.find('small', class_='author').text
    #extract <a> element N.B. .find is not suitable as it expects a single entry to be returned
    tag_elements = quote_element.select('.tags .tag')
    #store multiple tag entries in a list of tags 
    tags = []
    for tag_element in tag_elements:
        tags.append(tag_element.text)
    quotes.append(
        {
            'text': text,
            'author': author,
            'tags': ','.join(tags)
        }
    )