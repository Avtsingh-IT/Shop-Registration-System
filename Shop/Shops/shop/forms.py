from django import forms
from .models import Shop
from django import forms

class ShopRegistrationForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'latitude', 'longitude']

class UserLocationForm(forms.Form):
    latitude = forms.FloatField(label='Your Latitude', required=True)
    longitude = forms.FloatField(label='Your Longitude', required=True)
