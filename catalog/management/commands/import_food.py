import json
from django.core.management.base import BaseCommand
from main.models import Food  
class Command(BaseCommand):
    help = 'Load food items from a JSON file into the Food model'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file containing food data')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Load JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Parse and save each food item
        for item in data:
            food, created = Food.objects.get_or_create(
                name=item["Nama Makanan / Minuman"],
                flavor=item["Asin/Manis"],
                category=item["Makanan/Minuman"],
                vendor_name=item["Restoran"],
                price=item["Harga"],
                map_link=item["Lokasi (Gmaps)"],
                address=item["Alamat"]
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added food item: {food.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Food item already exists: {food.name}"))