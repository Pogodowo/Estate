

from django.urls import path
from .views import ogl_list

urlpatterns = [
    path('ogloszenia/', ogl_list),
]
