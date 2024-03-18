from django.urls import path
from .views import index, get_data_from_messengers

urlpatterns = [
    path('', index, name='index'),
    path('get-data/', get_data_from_messengers, name='get_data_from_messengers'),

]
