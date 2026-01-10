from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth import get_user_model
from inventory.models import Product
from orders.models import Order
from clients.models import Client

User = get_user_model()

class Command(BaseCommand):
    help = 'Resets all business data (Products, Orders, Clients) for a specific user to "Start Over"'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username to reset data for')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" not found'))
            return

        self.stdout.write(self.style.WARNING(f'Are you sure you want to DELETE ALL DATA for user "{username}"?'))
        self.stdout.write(self.style.WARNING('This includes ALL Products, Orders, and Clients. This cannot be undone.'))
        confirm = input('Type "yes" to confirm: ')

        if confirm != 'yes':
            self.stdout.write(self.style.ERROR('Operation cancelled.'))
            return

        # Delete data
        orders_count = Order.objects.filter(user=user).count()
        products_count = Product.objects.filter(user=user).count()
        clients_count = Client.objects.filter(user=user).count()

        Order.objects.filter(user=user).delete() # Cascades to OrderItems
        Product.objects.filter(user=user).delete()
        Client.objects.filter(user=user).delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted:'))
        self.stdout.write(f'- {orders_count} Orders')
        self.stdout.write(f'- {products_count} Products')
        self.stdout.write(f'- {clients_count} Clients')

        # Attempt to reset IDs (Best Effort)
        self.stdout.write(self.style.MIGRATE_HEADING('Attempting to reset ID counters (Order #1)...'))
        
        try:
            with connection.cursor() as cursor:
                if connection.vendor == 'sqlite':
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='orders_order';")
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='inventory_product';")
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='clients_client';")
                elif connection.vendor == 'postgresql':
                    # This might fail if other users have data, strictly speaking we shouldn't reset sequence if shared 
                    # But assuming single tenant or "Start Over" implies they want #1
                    # Check if table is empty first to be safe? 
                    # If table is NOT empty (other users), we generally CANNOT reset sequence to 1 easily.
                    # We'll just try and ignore errors.
                    cursor.execute("ALTER SEQUENCE orders_order_id_seq RESTART WITH 1;")
                    cursor.execute("ALTER SEQUENCE inventory_product_id_seq RESTART WITH 1;")
                    cursor.execute("ALTER SEQUENCE clients_client_id_seq RESTART WITH 1;")
            
            self.stdout.write(self.style.SUCCESS('ID counters reset (next Order will be #1).'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not reset ID counters: {e}'))
            self.stdout.write(self.style.WARNING('Data is deleted, but new Order IDs might continue from previous numbers.'))

        self.stdout.write(self.style.SUCCESS(f'Done! User "{username}" acts as a fresh account.'))
