from django.contrib import admin
from django.urls import path,include
from .views import home,PageUpdateUrl

urlpatterns = [
    path('',home,name='home'),
    path('PageUpdateUrl' , PageUpdateUrl, name='PageUpdateUrl')
]