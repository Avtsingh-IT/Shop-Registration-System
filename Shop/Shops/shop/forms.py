from django import forms
from .models import Shop

class ShopRegistrationForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'latitude', 'longitude']
