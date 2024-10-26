from django.core.management.base import BaseCommand
from main.models import Food

class Command(BaseCommand):
    help = 'Delete all Food objects from the database'

    def handle(self, *args, **options):
        # Get the count of Food objects
        food_count = Food.objects.count()
        
        self.stdout.write(f'You are about to delete {food_count} Food objects.')
        confirm = input('Are you sure you want to proceed? (y/n): ')
        
        if confirm.lower() == 'y':
            # Delete all Food objects
            Food.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {food_count} Food objects')
            )
        else:
            self.stdout.write(self.style.WARNING('Operation cancelled.'))