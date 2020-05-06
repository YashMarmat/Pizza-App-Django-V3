from django.db import models
from django.urls import reverse

class Pizza(models.Model):
    name = models.CharField(max_length = 120)

    def __str__(self):
        return self.name

class Topping(models.Model):
    pizza = models.OneToOneField(Pizza, on_delete = models.CASCADE, default = False)
    cheese = models.BooleanField(default = False, verbose_name = "Extra Cheese")
    onion = models.BooleanField(default = False, verbose_name = "Extra onion")
    tomato = models.BooleanField(default = False, verbose_name = "Extra tomato")
    quantity = models.PositiveIntegerField(default = 1)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image_url = models.CharField(max_length = 2083, blank = True)
    
    def __str__(self):
        return str(self.pizza)

    def get_absolute_url(self):
        return reverse('detail', args = [str(self.id)])