
from django.urls import path
from .views import redirect_short_url, create_short_url
urlpatterns = [
    path('create/', create_short_url, name='create_short_url'),
    path('<str:short_code>/', redirect_short_url, name='redirect'),
]
