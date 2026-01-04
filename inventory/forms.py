from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'picture', 'color', 'pieces_bought', 
                 'buying_price_per_piece', 'selling_price_per_piece']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'pieces_bought': forms.NumberInput(attrs={'class': 'form-control'}),
            'buying_price_per_piece': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'selling_price_per_piece': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
