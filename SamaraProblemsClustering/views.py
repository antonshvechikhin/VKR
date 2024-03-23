from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def get_data_from_messengers(request):
    if request.method == 'POST':
        vk_token = request.POST.get('vkToken')
        # # Далее обработайте vk_token по вашему усмотрению
        # vk_data = pd.DataFrame(columns=['Link to post/comment',
        #                                 'Published by',
        #                                 'Datetime',
        #                                 'Post/comment text'])
        #
        # vk_groups = [
        # ]
        #
        # data = get_posts(vk_token, vk_data, vk_groups)

        return HttpResponse("Данные VK Token получены: {}".format(vk_token))

    else:
        return HttpResponse("Метод запроса должен быть POST.")
