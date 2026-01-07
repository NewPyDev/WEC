from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    company_name = forms.CharField(
        max_length=255, 
        required=False,
        label='Your Company Name',
        help_text='Your business name (will appear on shipping labels)'
    )
    phone_number = forms.CharField(max_length=20, required=False)
    shipping_company_name = forms.CharField(
        max_length=255, 
        required=False,
        label='Preferred Shipping Company',
        help_text='Shipping company you prefer (FedEx, UPS, DHL, etc.) - Optional'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'company_name', 'phone_number', 'shipping_company_name', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'company_name', 'company_logo', 'phone_number', 'shipping_company_name')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'company_logo':
                field.widget.attrs['class'] = 'form-control-file'
