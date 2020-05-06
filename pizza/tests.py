from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Pizza, Topping
from django.urls import reverse


class TestPizza(TestCase):

    def setUp(self):
        
        self.user = get_user_model().objects.create_user(
            username = 'admin',
            email = 'forexample.com',
            password = 'secret',
        )

        self.pizza_data = Pizza.objects.create(
            name = 'Veg Pizza',   
        )

        self.topping_data = Topping.objects.create(
            pizza = self.pizza_data,
            cheese = True,
            onion = True,
            tomato = True,
            quantity = 2,
            price = 5, 
        )

    def test_string_representation(self):           # testing __str__(self) of models.py 
        pizza = Pizza(name='sample pizza')
        self.assertEqual(str(pizza), pizza.name)
        
    def test_get_absolute_url(self):
        self.assertEqual(self.topping_data.get_absolute_url(), '/1/')
    
    def test_topping_model_content(self):
        self.assertEqual(f'{self.topping_data.pizza}', 'Veg Pizza')
        self.assertEqual(f'{self.topping_data.cheese}', 'True')
        self.assertEqual(f'{self.topping_data.onion}', 'True')
        self.assertEqual(f'{self.topping_data.tomato}', 'True')
        self.assertEqual(f'{self.topping_data.quantity}', '2')
        self.assertEqual(f'{self.topping_data.price}', '5')

    def test_hompage_view(self):
        self.request = self.client.get(reverse('home'))
        self.assertEqual(self.request.status_code, 200)
        self.assertContains(self.request, 'Homepage')
        self.assertTemplateUsed(self.request, 'home.html')

    def test_detailpage_view(self):
        self.request = self.client.get(reverse('detail', args = '1'))
        self.assertEqual(self.request.status_code, 200)
        self.assertContains(self.request, 'Extra Cheese')
        self.assertContains(self.request, 'Extra Onion')
        self.assertContains(self.request, 'Extra Tomato')
        self.assertContains(self.request, 'Total Pizzas: 2')    # pizza quantity in setUp is 2        
        self.assertTemplateUsed(self.request, 'detail.html')

    def test_confirmpage_view_price_calculation(self):
        self.request = self.client.get(reverse('confirm', args = '1'))
        self.assertEqual(self.request.status_code, 200)
        self.assertContains(self.request, 'Product Summary')
        self.assertContains(self.request, 'Bill Detail: 5.00 $ (pizza price) + 2 $(topping charge) x 2(total pizza) = 14 $')
        self.assertContains(self.request, 'Total Amount Payable: 14 $')
        self.assertContains(self.request, 'Total Pizzas: 2')

    def test_confirmpage_view_with_wrong_price_calculation(self):
        self.request = self.client.get(reverse('confirm', args = '1'))
        self.assertEqual(self.request.status_code, 200)
        self.assertContains(self.request, 'Product Summary')
        self.assertNotContains(self.request, 'Bill Detail: 5.00 $ (pizza price) + 2 $(topping charge) x 2(total pizza) = 7 $')
        self.assertNotContains(self.request, 'Total Amount Payable: 7 $')
        self.assertNotContains(self.request, 'Total Pizzas: 1')

    def test_updatepage_view(self):   
        self.request = self.client.get(reverse('update', args = '1'), {
            'Extra Cheese': 'True', 
            'Extra onion': 'True',
            'Extra tomato': 'True',
            'Quantity': '2',
        })
        self.assertEqual(self.request.status_code, 200)
        self.assertNotContains(self.request, 'False')
        self.assertContains(self.request, 'Pizza Selected: Veg Pizza')
        self.assertNotContains(self.request, 'Pizza Selected: Non Veg Pizza')
        
    def test_buypage_view(self):
        self.request = self.client.get(reverse('buy', args = '1'))
        self.assertEqual(self.request.status_code, 200)
        self.assertContains(self.request, 'Your Veg Pizza is on the way :)')
        self.assertNotContains(self.request, 'Your Non Veg Pizza is on the way :)')
        self.assertTemplateUsed(self.request, 'buy.html')

    # admin privilages tests

    def test_createpage_view_for_logged_in_user(self):
        self.client.login(username = 'admin', email = 'forexample.com', password = 'secret')
        self.request = self.client.get(reverse('create'))
        self.assertEqual(self.request.status_code, 200)
        self.assertContains(self.request, 'Change Pizza Name')
        self.assertTemplateUsed(self.request, 'create.html')
    
    def test_createpage_view_when_logged_out(self):
        self.client.logout()
        self.request = self.client.get(reverse('create'))
        self.assertEqual(self.request.status_code, 302)
        self.assertRedirects(self.request, '%s?next=/createpage/' % (reverse('login'))) 

    def test_createpizza_view_for_logged_in_user(self):
        self.client.login(username = 'admin', email = 'forexample.com', password = 'secret')
        self.request = self.client.get(reverse('create_pizza'))
        self.assertEqual(self.request.status_code, 200)
        self.assertContains(self.request, 'Create Pizza Name')
        self.assertTemplateUsed(self.request, 'create_pizza.html')

    def test_createpizza_view_when_logged_out(self):
        self.client.logout()
        self.request = self.client.get(reverse('create_pizza'))
        self.assertEqual(self.request.status_code, 302)
        self.assertRedirects(self.request, '%s?next=/createpage/createpizza/' % (reverse('login'))) 

    def test_deletepage_view_for_logged_in_user(self):
        self.client.login(username = 'admin', email = 'forexample.com', password = 'secret')
        self.request = self.client.get(reverse('delete', args = '1'))
        self.assertEqual(self.request.status_code, 200)
        self.assertContains(self.request, 'Delete')
        self.assertTemplateUsed(self.request, 'delete.html')

    def test_deletepage_view_when_logged_out(self):
        self.client.logout()
        self.request = self.client.get(reverse('delete', args = '1'))
        self.assertEqual(self.request.status_code, 302)
        self.assertRedirects(self.request, '%s?next=/1/delete/' % (reverse('login'))) 

        
