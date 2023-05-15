from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from bs4 import BeautifulSoup
import requests
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'}


def price_to_float(price: str):
    """Converts a price string to a float"""

    numbers = re.findall(r'\d+', price)
    if numbers:
        return float(''.join(numbers))
    else:
        return 0

def get_price(link: str):
        """Returns the price of a product from a link"""
        
        soup = BeautifulSoup(requests.get(link, headers=headers).text, 'html.parser')
        try:
            if link.startswith('https://www.netonnet.se'):
                return price_to_float(soup.find('div', class_='price-big').get_text(strip=True))

            elif link.startswith('https://www.mediamarkt.se/'):
                return price_to_float(soup.find("div", class_="price big").get_text(strip=True) )

            elif link.startswith('https://www.inet.se/'):
                try:
                    return price_to_float(soup.find("span", class_="bp5wbcj c1funyia l1gqmknm").get_text(strip=True))
                except:
                    return price_to_float(soup.find("span", class_="bp5wbcj l1gqmknm").get_text(strip=True))

        except Exception as e:
            print(e)
            return 0

def update_price(product):
    if product.price != get_price(product.link):
        tracking_users = User.objects.filter(producttracking__product=product)

        for user in tracking_users:
            send_mail(
                f'Price update of {product.name}',
                f'The price of {product.name} has changed to {get_price(product.link)} :- from {product.price} :-',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

        product.price = get_price(product.link)
        product.save()


if __name__ == '__main__':
    pass