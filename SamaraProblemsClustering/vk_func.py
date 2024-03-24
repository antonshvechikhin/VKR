import pandas as pd
import requests
from datetime import datetime, timedelta
import time


def get_comments(vk_token, dataframe, post, time_delta, v, from_threads=False, comment_id=None):
    wall_comments_url = 'https://api.vk.com/method/wall.getComments'
    offset = 0
    from_what_date = int(time.mktime((datetime.now() - timedelta(days=time_delta)).timetuple()))
    time_condition = True

    while time_condition:

        wall_comments_params = {
            'access_token': vk_token,
            'owner_id': post['from_id'],
            'post_id': post['id'],
            'count': 100,
            'offset': offset,
            'v': v,
            'sort': 'desc'
        }

        # Если выгружаем комментарии из тредов (выгружаем ответы на комментарии), то добавляем
        # параметр comment_id. Он указывает для какого комментария нам нужно выгрузить ответы.
        if from_threads:
            wall_comments_params['comment_id'] = comment_id

        time.sleep(0.2)
        comments = requests.get(wall_comments_url, wall_comments_params).json()['response']['items']

        # Если комментариев нет
        if not comments:
            break

        for comment in comments:

            comment_link = 'https://vk.com/wall' + str(post['from_id']) + '_' + str(post['id']) + '?reply=' + str(
                comment['id'])
            comment_date = pd.to_datetime(comment['date'], unit='s')
            if str(comment['from_id']).startswith('-'):
                username = 'https://vk.com/public' + str(comment['from_id'])[1:]
            else:
                username = 'https://vk.com/id' + str(comment['from_id'])
            comment_text = comment['text']

            if comment['date'] < from_what_date:
                time_condition = False
                break

            # Если пост подходит - заносим данные в таблицу
            else:
                # Получаем комментарии из треда
                if 'thread' in comment:
                    if comment['thread']['count']:
                        dataframe = get_comments(vk_token, dataframe, post, time_delta, v, True, comment['id'])

                # Получаем обычный комментарий
                if comment_text:
                    dataframe = dataframe._append({
                        'Link to post/comment': comment_link,
                        'Datetime': comment_date,
                        'Published by': username,
                        'Post/comment text': comment_text
                    }, ignore_index=True)

            # Чтобы получать более старые комментарии, после записи последнего комментария из пачки, увеличиваем
            # срез на то же количество, что и количество постов в пачке
            if comment == comments[-1]:
                offset += 100

    return dataframe


def get_posts(vk_token, dataframe, groups, time_delta=31, v=5.131) -> pd.DataFrame:
    wall_url = 'https://api.vk.com/method/wall.get'

    for group in groups:
        # Дата, начиная с которой нам нужны посты/комментарии
        from_what_date = int(time.mktime((datetime.now() - timedelta(days=time_delta)).timetuple()))
        # Сдвиг по постам
        offset = 0
        # Условие времени
        time_condition = True

        while time_condition:

            wall_params = {
                'access_token': vk_token,
                'owner_id': -group,
                'count': 100,
                'offset': offset,
                'v': v
            }

            posts = requests.get(wall_url, wall_params).json()['response']['items']

            # Если постов нет
            if not posts:
                break

            for post in posts:
                post_link = 'https://vk.com/wall' + str(post['from_id']) + '_' + str(post['id'])
                post_date = pd.to_datetime(post['date'], unit='s')
                username = 'https://vk.com/public' + str(group)
                post_text = post['text']

                if 'is_pinned' in post:
                    if post['is_pinned'] and post['date'] < from_what_date:
                        continue

                # Если из пачки постов (100 постов) следующий пост не подходит к дате, начиная с которой
                # нам нужны посты, то выходим из циклов и переходим к следующей группе
                if post['date'] < from_what_date:
                    time_condition = False
                    break
                # Если пост подходит - заносим данные в таблицу
                else:
                    if post_text:
                        dataframe = dataframe._append({
                            'Link to post/comment': post_link,
                            'Datetime': post_date,
                            'Published by': username,
                            'Post/comment text': post_text
                        }, ignore_index=True)

                    if post['comments']['count']:
                        dataframe = get_comments(vk_token, dataframe, post, time_delta, v)

                # Чтобы получать более старые посты, после записи последнего поста из пачки, увеличиваем срез
                # на то же количество, что и количество постов в пачке
                if post == posts[-1]:
                    offset += 100

    return dataframe
