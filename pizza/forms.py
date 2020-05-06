
from django import forms
from django.forms import ModelForm
from .models import Topping

class PizzaCreate(ModelForm):
    
    class Meta:
        model = Topping
        fields = ('pizza', 'cheese', 'onion', 'tomato', 'price', 'image_url')
