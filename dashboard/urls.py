from django import urls
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('', views.home, name='home'),
    path('edit', views.edit, name='edit'),
    path('addauction', views.addauction, name='addauction'),
    path('auction/<int:pk>', views.auctionpage, name='auctionpage'),
    path('report', views.report, name='report'),
]
