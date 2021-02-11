from django.urls import path

import mainapp.views as mainapp
from django.views.decorators.cache import cache_page


app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='index'),
    path('category/<int:pk>/', mainapp.products, name='category'),
    path('category/<int:pk>/page/<int:page>/',
         cache_page(3600)(mainapp.products), name='page'),
    path('product/<int:pk>/', mainapp.product, name='product'),
]
