import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(soup, quotes):
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

#target url for scrapping
base_url= 'https://quotes.toscrape.com'

#defifing the user agent for the GET request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
page = requests.get(base_url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

#initialising variable to contain scrapped quotes
quotes = []

#scrapping home page
scrape_page(soup, quotes)
 
#check for multiple pages by retrieve the <li> element
next_element_li = soup.find('li', class_='next')
#if there is more than one page
while next_element_li is not None:
    next_page_url = next_element_li.find('a', href=True)['href']
    #load  and parse new page
    page = requests.get(base_url + next_page_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    scrape_page(soup, quotes)
    #look for <li> element 
    next_element_li = soup.find('li', class_='next')

#reads quotes.csv if it already exist else will create the file
csv_file = open('quotes.csv', 'w', encoding='utf-8', newline='')

#initialising the writer to add content to the file 
writer = csv.writer(csv_file)

#creating header fields 
writer.writerow(['Text', 'Author', 'Tags'])

#writing quote content to the csv file
for quote in quotes:
    writer.writerow(quote.values())

#releaseing resources
csv_file.close()