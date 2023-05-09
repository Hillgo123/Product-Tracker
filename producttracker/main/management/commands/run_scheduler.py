from django.core.management.base import BaseCommand
import schedule
from main.product_price import update_price
from main.models import Product

def update_price_wrapper(product: Product):
    def inner():
        update_price(product)
    return inner

class Command(BaseCommand):
    help = "Runs the scheduler for updating prices."

    def handle(self, *args, **options):
        for product in Product.objects.all():
            schedule.every(10).minutes.do(update_price_wrapper(product))

        while True:
            schedule.run_pending()
