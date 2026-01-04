from django.db import models
from django.conf import settings

class Client(models.Model):
    """Client model for tracking customers"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ('user', 'phone')
        
    def __str__(self):
        return f"{self.name} - {self.phone}"
    
    @property
    def total_orders(self):
        return self.orders.count()
    
    @property
    def total_spent(self):
        from django.db.models import Sum
        return self.orders.aggregate(total=Sum('total_amount'))['total'] or 0
