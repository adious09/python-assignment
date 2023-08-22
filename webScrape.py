import requests
from bs4 import BeautifulSoup
import csv
import time


base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
headers = {
    "User-Agent": "Your User Agent String"
}
csv_file = open('product_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])

num_pages = 20

for page in range(1, num_pages + 1):
    url = base_url + str(page)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    for product in products:
        product_url = product.find('a', {'class': 'a-link-normal'})['href']
        product_name = product.find('span', {'class': 'a-text-normal'}).text.strip()
        product_price = product.find('span', {'class': 'a-offscreen'}).text.strip()
        
        rating = product.find('span', {'class': 'a-icon-alt'})
        if rating:
            rating = rating.text.split()[0]
        else:
            rating = 'N/A'
        
        num_reviews_elem = product.find('span', {'class': 'a-size-base', 'dir': 'auto'})
        if num_reviews_elem:
            num_reviews = num_reviews_elem.text.split()[0]
        else:
            num_reviews = 'N/A'
        
        csv_writer.writerow([product_url, product_name, product_price, rating, num_reviews])

    time.sleep(2)  

csv_file.close()

