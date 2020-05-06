
from django.urls import path
from django.conf import settings
from .views import (
    Homepage, 
    Detailpage, 
    Createpage,
    Createpizza, 
    UpdatePizza, 
    AdminUpdatePizza,
    Confirmpage, 
    DeletePizza,
    Buypage,
)

urlpatterns = [
    path('', Homepage.as_view(), name = 'home'),
    path('<int:pk>/', Detailpage.as_view(), name = 'detail'),
    path('createpage/', Createpage.as_view(), name = 'create'),
    path('createpage/createpizza/', Createpizza.as_view(), name = 'create_pizza'),    
    path('<int:pk>/update/', UpdatePizza.as_view(), name = 'update'),
    path('<int:pk>/adminupdate/', AdminUpdatePizza.as_view(), name = 'admin_update'),    
    path('<int:pk>/confirm/', Confirmpage.as_view(), name = 'confirm'),
    path('<int:pk>/delete/', DeletePizza.as_view(), name = 'delete'),
    path('<int:pk>/confirm/buy/', Buypage.as_view(), name = 'buy'),
]
