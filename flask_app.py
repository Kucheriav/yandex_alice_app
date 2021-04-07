from flask import Flask, request
import logging
import json
import os
from random import randint


app = Flask(__name__)

logging.basicConfig(filename='example.log')
logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
# Функция получает тело запроса и возвращает ответ.
# Внутри функции доступен request.json - это JSON,
# который отправила нам Алиса в запросе POST
def main():
    logging.info(f'Request: {request.json!r}')

    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом при помощи
    # библиотеки json преобразуем в JSON и отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    # Отправляем request.json и response в функцию handle_dialog.
    # Она сформирует оставшиеся поля JSON, которые отвечают
    # непосредственно за ведение диалога
    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        # Запишем подсказки, которые мы ему покажем в первый раз
        sessionStorage[user_id] = str(randint(1000, 9999))
        # Заполняем текст ответа
        res['response']['text'] = 'Привет! Угадай число!'
        # Получим подсказки
        return
    res['response']['buttons'] = [{'title': 'Сдаюсь', 'hide': True}]
    # Сюда дойдем только, если пользователь не новый,
    # и разговор с Алисой уже был начат
    # Обрабатываем ответ пользователя.
    # В req['request']['original_utterance'] лежит весь текст,
    # что нам прислал пользователь
    # Если он написал 'ладно', 'куплю', 'покупаю', 'хорошо',
    # то мы считаем, что пользователь согласился.
    # Подумайте, всё ли в этом фрагменте написано "красиво"?
    user = str(req['request']['original_utterance'])
    bulls = cows = 0
    if req['request']['original_utterance'] == 'Сдаюсь':
        res['response']['text'] = f'Слабак! Это было число {sessionStorage[user_id]}'
        res['response']['end_session'] = True
        return
    if not user.isdigit():
        res['response']['text'] = 'Ne chislo'
        return
    if not (1000 <= int(user) <= 9999):
        res['response']['text'] = 'неподходящее число'
        return
    for i in range(len(user)):
        if user[i] == sessionStorage[user_id][i]:
            bulls += 1
        if user[i] in sessionStorage[user_id]:
            cows += 1
    if cows == 4 and bulls == 4:
        res['response']['text'] = 'Ugadal!'
        res['response']['end_session'] = True
        return
    res['response']['text'] = f'cows - {cows}; bulls - {bulls}'
    return



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

