from django.urls import path
from . import views


app_name = 'app'  # here for namespacing of urls.

urlpatterns = [
    path('', views.index, name="home"),
    path('test/', views.test, name="test"),
]

