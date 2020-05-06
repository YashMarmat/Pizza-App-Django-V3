from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PizzaCreate
from .models import Pizza, Topping


class Homepage(ListView):
    model = Topping
    template_name = 'home.html' 

class Detailpage(DetailView):
    model = Topping
    template_name = 'detail.html'

class Createpage(LoginRequiredMixin, CreateView):
    model = Topping
    template_name = 'create.html'
    form_class = PizzaCreate
    success_url = reverse_lazy('home')

class Createpizza(LoginRequiredMixin, CreateView):
    model = Pizza
    template_name = 'create_pizza.html'
    success_url = reverse_lazy('create')
    fields = '__all__'

class UpdatePizza(UpdateView):
    model = Topping
    template_name = 'update.html'
    from_class = PizzaCreate
    fields = ['cheese', 'onion', 'tomato', 'quantity']

class AdminUpdatePizza(LoginRequiredMixin, UpdateView):
    model = Topping
    template_name = 'admin_update.html'
    from_class = PizzaCreate
    fields = '__all__'

class Confirmpage(DetailView):
    model = Topping
    template_name = 'confirm.html'

class DeletePizza(LoginRequiredMixin, DeleteView):
    model = Pizza
    template_name = 'delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'


class Buypage(DetailView):
    model = Topping
    template_name = 'buy.html'