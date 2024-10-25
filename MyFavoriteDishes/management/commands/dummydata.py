# your_app/management/commands/create_dummy_data.py

from django.core.management.base import BaseCommand
from MyFavoriteDishes.models import Food

class Command(BaseCommand):
    help = 'Create dummy data for testing'

    def handle(self, *args, **kwargs):
        dummy_data = [
            {
                "name": "Bakso Malang",
                "flavor": "Asin",
                "category": "Makanan",
                "vendor_name": "Pangsit Mie Bakso M Gendut - Lowokwaru",
                "price": "14290",
                "map_link": "https://maps.app.goo.gl/EHe1nLz1mZGdn4FJA",
                "address": "Jl. Locari No.1, Lowokwaru, Kec. Lowokwaru, Kota Malang, Jawa Timur 65141",
            },
            {
                "name": "Rawon Malang",
                "flavor": "Asin",
                "category": "Makanan",
                "vendor_name": "Rawon Pak Jenggot - Purwantoro",
                "price": "20000",
                "map_link": "https://maps.app.goo.gl/g37EDaUMZvaKoPdH6",
                "address": "Jl. Sulfat No.5, Purwantoro, Kec. Blimbing, Kota Malang, Jawa Timur 65126",
            },
            {
                "name": "Pecel Kawi",
                "flavor": "Asin",
                "category": "Makanan",
                "vendor_name": "Pecel Kawi Hj Musilah Asli 1975 - Klojen",
                "price": "17500",
                "map_link": "https://maps.app.goo.gl/PJva5axgM3KFGgQd9",
                "address": "Jl. Kawi Kios No.43B, Bareng, Kec. Klojen, Kota Malang, Jawa Timur 65116",
            },
            # Add more dummy entries as needed
        ]

        for item in dummy_data:
            food = Food(
                name=item['name'],
                flavor=item['flavor'],
                category=item['category'],
                vendor_name=item['vendor_name'],
                price=item['price'],
                map_link=item['map_link'],
                address=item['address'],
            )
            food.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully added {food.name}'))
