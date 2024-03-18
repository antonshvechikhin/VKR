from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'index.html')


def get_data_from_messengers(request):
    if request.method == 'POST':
        print(request.POST)
        vk_token = request.POST.get('vkToken')
        # Далее обработайте vk_token по вашему усмотрению
        return HttpResponse("Данные VK Token получены: {}".format(vk_token))
    else:
        return HttpResponse("Метод запроса должен быть POST.")
