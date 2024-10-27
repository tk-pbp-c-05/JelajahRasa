import os
from django.conf import settings
from django.core.management.base import BaseCommand
from main.models import Food
import csv

class Command(BaseCommand):
    help = 'Import food items from a CSV file in the static folder into the Food model'

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help='Name of the CSV file in the static folder')

    def handle(self, *args, **options):
        file_name = options['file_name']
        file_path = os.path.join(settings.BASE_DIR, 'static', file_name)

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                food, created = Food.objects.get_or_create(
                    name=row["Nama Food / Beverages"],
                    defaults={
                        'flavor': row["Asin/Manis"],
                        'category': row["Makanan/Minuman"],
                        'vendor_name': row["Restoran"],
                        'price': row["Harga"],
                        'map_link': row["Lokasi (Gmaps)"],
                        'address': row["Alamat"],
                        'image': row["Foto"]
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Successfully added food item: {food.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Food item already exists: {food.name}"))