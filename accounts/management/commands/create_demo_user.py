from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from inventory.models import Product
from clients.models import Client
from orders.models import Order, OrderItem
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a secure "test" demo account with sample data'

    def handle(self, *args, **options):
        username = 'test'
        password = 'test'
        email = 'demo@example.com'

        # 1. Create or Reset User
        try:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists. Resetting password and data...'))
            user.set_password(password)
            user.company_name = "Demo Store Inc."
            user.save()
            
            # Wipe existing data for clean slate
            Product.objects.filter(user=user).delete()
            Client.objects.filter(user=user).delete()
            Order.objects.filter(user=user).delete()
            
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.company_name = "Demo Store Inc."
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user "{username}"'))

        # 2. Add Sample Products
        products_data = [
            ("Premium Cotton T-Shirt", "Navy Blue", "M", 15.00, 35.00, 50),
            ("Urban Cargo Pants", "Khaki", "32", 25.00, 65.00, 30),
            ("Signature Hoodie", "Black", "L", 20.00, 55.00, 40),
            ("Running Sneakers", "White/Red", "42", 40.00, 120.00, 15),
            ("Denim Jacket", "Faded Blue", "L", 35.00, 89.99, 20),
        ]

        created_products = []
        for name, color, size, buy, sell, stock in products_data:
            p = Product.objects.create(
                user=user,
                name=name,
                color=color,
                size=size, # Assuming choices match or loose matching if char field
                buying_price_per_piece=Decimal(str(buy)),
                selling_price_per_piece=Decimal(str(sell)),
                pieces_bought=stock,
                pieces_sold=0
            )
            created_products.append(p)
        
        self.stdout.write(f'Created {len(created_products)} sample products.')

        # 3. Add Sample Clients
        clients_data = [
            ("Alice Smith", "555-0101", "123 Main St, New York, NY"),
            ("Bob Jones", "555-0102", "456 Market Ave, San Francisco, CA"),
            ("Charlie Brown", "555-0103", "789 Broadway, Seattle, WA"),
        ]

        created_clients = []
        for name, phone, addr in clients_data:
            c = Client.objects.create(
                user=user,
                name=name,
                phone=phone,
                address=addr,
                email=f"{name.lower().replace(' ', '.')}@example.com"
            )
            created_clients.append(c)
            
        self.stdout.write(f'Created {len(created_clients)} sample clients.')

        # 4. Create a Sample Order
        if created_products and created_clients:
            order = Order.objects.create(
                user=user,
                client=created_clients[0],
                status='done',
                total_amount=Decimal('0')
            )
            
            # Add items
            p1 = created_products[0]
            qty = 2
            price = p1.selling_price_per_piece
            OrderItem.objects.create(order=order, product=p1, quantity=qty, price=price)
            
            # Update product stock (manual since we created raw)
            p1.pieces_sold += qty
            p1.save()
            
            # Update order total
            order.total_amount = qty * price
            order.save()
            
            self.stdout.write(f'Created sample finished order #{order.id}')

        self.stdout.write(self.style.SUCCESS(f'Successfully setup demo account: {username} / {password}'))
