import io

from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from datetime import datetime
from SamaraProblemsClustering.vk_func import get_posts

# Create your views here.


def index(request):
    return render(request, 'index.html')


def get_data_from_messengers(request):
    if request.method == 'POST':
        vk_token = request.POST.get('vkToken')
        vk_data = pd.DataFrame(columns=['Link to post/comment',
                                        'Published by',
                                        'Datetime',
                                        'Post/comment text'])

        vk_groups = [
            81824379, 168133074, 116930,
            150841265, 25647397, 158724912,
            161552339, 74315431, 168244689,
            168132385, 168168058, 159089020,
            168176712, 168255131, 118110564,
            168132792, 169063436, 169576604,
            161663611, 201814802, 168215280,
            174771890, 80382170, 168134633,
            58141452, 211002213, 42949290,
            218628204, 182783442, 60751871,
            28352059, 2579489, 148068601,
            182250209, 113171782, 164170148,
            172005456, 59875474, 168128224,
            167431460, 33344798, 79894688,
            1528722, 40786487
        ]

        data = get_posts(vk_token, vk_data, vk_groups)


        # Объект BytesIO для хранения Excel файла
        csv_buffer = io.BytesIO()

        # Создание модуля записи Pandas Excel (xlsxwriter в качестве движка)
        with pd.ExcelWriter(csv_buffer, engine='xlsxwriter') as writer:
            data.to_excel(writer, index=False, sheet_name='Sheet1')
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

        # Сохраняем модуль записи Pandas Excel в объект BytesIO
        writer._save()

        # Ставим указатель объекта BytesIO в начало
        csv_buffer.seek(0)

        # Создание HttpResponse с CSV файлом в качестве вложения.
        response = HttpResponse(csv_buffer, content_type='text/csv')
        filename = datetime.now().strftime('%Y%m%d-%H%M')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        return response

    else:
        return HttpResponse("Метод запроса должен быть POST.")
