import os
import json
import time
import pymysql
import datetime
import requests
import traceback
from components import query as query_sql
from components import parser
from selenium.common.exceptions import WebDriverException

from components.components import Browser, ReviewsTwoGis
from components.exception import ProxyError


def send_message_tg(datetime_work, company_yandex_url, filial_id, company_name):
    """send message to tg"""

    # init tg variables
    token = os.environ.get('TG_BOT')
    chat = os.environ.get('TG_CHAT')

    row_tg = f"Ошибка при получении отзывов \n"

    if company_name is not None:
        row_tg += f"Название комании: {str(company_name)} \n"

    if filial_id is not None:
        row_tg += f"Филиал: {str(filial_id)} \n"

    if company_yandex_url is not None:
        row_tg += f"Ссылка на yandex карты: {str(company_yandex_url)} \n"

    if filial_id is not None:
        url = 'https://test.geoadv.ru/itemcampagin/view?id=' + str(filial_id)
        row_tg += f"Ссылка на профиль: {url} \n"

    row_tg += f"Дата и время: {datetime_work}"
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                  json={"chat_id": chat, "text": row_tg})


def run():
    print('it is start')
    dt_now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print(dt_now)

    # connect to db
    try:
        sql = query_sql.connect()
    except pymysql.err.OperationalError:
        print('Error: failed to connect to the database')
        time.sleep(30)

        return

    two_gis_url = None
    organization = None
    id_filial = None

    if sql:
        sql, queue = query_sql.getFindFilialQueue(sql, query_sql.TYPE['find_two_gis_reviews_in_filial'])
        # queue = {'queue_id': 3290, 'resource_id': 3657}

        if queue:
            id_filial = queue.get('resource_id')
            print(queue)
            try:
                # get proxy
                sql, proxy_dict = query_sql.get_proxy(sql)

                # Если есть задача - присваиваем статус "в работе"
                sql = query_sql.statusInProcess(sql, queue['queue_id'])
                sql, two_gis_url, organization = query_sql.getYandexUrl(sql, queue['resource_id'])

                if two_gis_url:
                    # control count of repeat
                    sql, control_repeat = query_sql.repeat_filial(sql, queue['resource_id'])

                    # Получаем страницу
                    result = parser.load_page(two_gis_url, {'ip': proxy_dict[0], 'port': '1050'}, control_repeat)

                    if result:
                        # make json format
                        json_string = json.dumps(result, ensure_ascii=False)

                        # save result
                        sql = query_sql.statusDone(sql, queue['queue_id'])
                        # Получаем id записи результата
                        sql, result_id = query_sql.add_result(sql, queue['queue_id'], json_string)
                        # Создаём задачу на сохранение отзывов
                        sql, result_id = query_sql.newSaveFilialQueue(sql, entity_id=queue['resource_id'],
                                                                      resource_id=queue['queue_id'])

                        # control count of reviews
                        # sql = query_sql.control_count_json(sql, queue['queue_id'])
                    else:
                        print('Нет результата')
                        sql = query_sql.statusDone(sql, queue['queue_id'])
                else:
                    print('Нет URL филиала')
                    sql = query_sql.statusError(sql, queue['queue_id'], 'Нет URL филиала')

            # Если получили ошибку драйвера, данная задача получает статус новой и делаем паузу 10 минут
            # except WebDriverException:
            #    if queue['queue_id']:
            #        sql = query_sql.statusError(sql, queue['queue_id'], 'hz')

            except ProxyError:
                print('proxy error')
                time.sleep(300)

            except Exception as error:
                print(traceback.format_exc())
                if queue['queue_id']:
                    error_text = "Ошибка:" + str(repr(error))
                    query_sql.statusError(sql, queue['queue_id'], error_text)

                # send message
                send_message_tg(dt_now, two_gis_url, id_filial, organization)

        else:
            print('пауза')
            time.sleep(300)

        try:
            sql.close()
        except pymysql.err.Error:
            pass


run()
