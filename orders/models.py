from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

class Order(models.Model):
    """Order model for tracking customer orders"""
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('cancelled', 'Cancelled'),
        ('done', 'Done'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    client = models.ForeignKey('clients.Client', on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    shipping_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Order #{self.id} - {self.client.name} - {self.status}"
    
    @property
    def is_completed(self):
        return self.status in ['done', 'cancelled']
    
    @property
    def grand_total(self):
        return self.total_amount + self.shipping_cost
    
    def update_inventory_on_completion(self):
        """Update product inventory when order is marked as done"""
        if self.status == 'done':
            for item in self.items.all():
                item.product.pieces_sold += item.quantity
                item.product.save()
    
    def restore_inventory_on_cancellation(self):
        """Restore product inventory if order was previously done and now cancelled"""
        # This would be used if we need to handle status reversions
        pass
    
    def save(self, *args, **kwargs):
        # Check if status changed to 'done'
        if self.pk:
            old_order = Order.objects.get(pk=self.pk)
            if old_order.status != 'done' and self.status == 'done':
                # Status changed to done, update inventory
                super().save(*args, **kwargs)
                self.update_inventory_on_completion()
                return
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Order item model for tracking products in orders"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    class Meta:
        unique_together = ('order', 'product')
        
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def subtotal(self):
        return self.quantity * self.price
    
    def save(self, *args, **kwargs):
        # Stock will be updated when order status changes to 'done'
        # Not when order item is created
        super().save(*args, **kwargs)
