import requests
import re
from bs4 import BeautifulSoup


def get_product_details(product_link) -> dict:
    detail = {}
    response = requests.get(product_link)
    soup = BeautifulSoup(response.text, 'lxml')
    detail['images'] = [image.a['href'] for image in soup.find_all('div', {'class': 'item'})]
    price = {}
    temp_price = soup.find('div', {'class': 'product-price-wrapper'}).find('div', {'class': 'discounts'})
    if temp_price is not None:
        price['off'], price['old_price'], price['new_price'] = (
            temp_price.find('span', {'class': 'off-badge'}).text, temp_price.find('span', {'class': 'amount-fig'}).text.replace(',', ''),
            temp_price.find('span', {'class': 'product-price'}).text.replace(',', ''))
        detail['price'] = price
    else:
        price['real_price'] = soup.find('span', {'class', 'product-price'}).text.replace(',', '')
        detail['price'] = price
    soup = soup.find("div", {'class': 'atrribute-col'})
    for row in soup.find_all('div', {'class': 'atrribute-wrapp'}):
        for field in row.find_all('div', re.compile("atrribute-items")):
            detail[field.find('div', {'class': 'attribute-item-name'}).text.strip()] = field.find('div', {
                'class': "attribute-item-value"}).text.strip()
    detail['Link'] = product_link
    return detail


def find_products(page_number) -> list:
    URL_MICROLESS = f'https://uae.microless.com/graphic_cards/?page={page_number}'
    response = requests.get(URL_MICROLESS)

    soup = BeautifulSoup(response.text, 'lxml')
    products = soup.find("div", {'id': 'search-results-products'}).find_all("div", {
        'class': 'product product-carousel grid-list'})
    products = [product for product in products if product.text.find("Currently Unavailable") == -1]
    return [product.find('a')['href'] for product in products]

