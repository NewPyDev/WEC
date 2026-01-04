from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model for the application"""
    is_admin_user = models.BooleanField(default=False)
    company_name = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name='Your Company Name',
        help_text='Your business/company name (appears at top of shipping labels)'
    )
    phone_number = models.CharField(max_length=20, blank=True)
    shipping_company_name = models.CharField(
        max_length=255, 
        blank=True, 
        default='',
        verbose_name='Preferred Shipping Company',
        help_text='Shipping company you prefer to use (FedEx, UPS, DHL, etc.) - Optional'
    )
    
    def __str__(self):
        return self.username
