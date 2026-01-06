from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

class Product(models.Model):
    """Product model for inventory management"""
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', '2X Large'),
        ('OS', 'One Size'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='products/', blank=True, null=True)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, default='M')
    pieces_bought = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    pieces_sold = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    pieces_left = models.IntegerField(default=0, editable=False)
    buying_price_per_piece = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    selling_price_per_piece = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} ({self.size}) - {self.color}" if self.color else f"{self.name} ({self.size})"
    
    def save(self, *args, **kwargs):
        # Auto-calculate pieces left
        self.pieces_left = self.pieces_bought - self.pieces_sold
        super().save(*args, **kwargs)
    
    @property
    def total_buying_cost(self):
        return self.pieces_bought * self.buying_price_per_piece
    
    @property
    def total_revenue(self):
        return self.pieces_sold * self.selling_price_per_piece
    
    @property
    def profit(self):
        return self.total_revenue - (self.pieces_sold * self.buying_price_per_piece)
