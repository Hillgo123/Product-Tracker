from django.core.mail import send_mail
from django.conf import settings
from bs4 import BeautifulSoup
import requests
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'}


def get_price(link: str):
        soup = BeautifulSoup(requests.get(link, headers=headers).text, 'html.parser')
        try:
            if link.startswith('https://www.netonnet.se'):
                return int(soup.find('div', class_='price-big').text.strip().removesuffix(':-'))

            elif link.startswith('https://www.mediamarkt.se/'):
                return soup.find('div', class_='price small').text.strip()

            elif link('https://www.elgiganten.se/'):
                return soup.find(class_="product-price-container").get_text()

        except Exception as e:
            print(e)
            return 0

def update_price(product):
    if product.price != 0:
        send_mail(
            f'Price update of {product.name}',
            f'The price of {product.name} has changed to {get_price(product.link)} :- from {product.price} :-',
            settings.EMAIL_HOST_USER,
            [product.author.email],
            fail_silently=False,
        )
        

        product.price = get_price(product.link)
        product.save()


if __name__ == '__main__':
    print(get_price('https://www.netonnet.se/art/hem-fritid/personvard/harborttagning-rakning/nastrimmer/andersson-oron-och-nastrimmer-net-1-3/247047.9140/'))