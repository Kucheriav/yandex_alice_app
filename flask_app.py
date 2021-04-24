from flask import Flask, request
import logging
import json
import os
from random import sample
from data import db_session
from data.players import Player


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

logging.basicConfig(filename='example.log')
logging.basicConfig(level=logging.INFO)

sessionStorage = {}

db_session.global_init("db/game.db")

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

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        db_sess = db_session.create_session()
        player = db_sess.query(Player).filter(Player.id == user_id).first()
        db_sess.close()
        if player:
            sessionStorage['player'] = player
            sessionStorage['state'] = "SHOW_MENU"
            res['response']['text'] = f'Привет, {player.name}'
            res['response']['buttons'] = [
                {'title': 'Играть', 'hide': False},
                {'title': 'Правила', 'hide': False},
                {'title': 'Статистика', 'hide': False},
                {'title': 'Рекорды', 'hide': False},
                {'title': 'Завершить', 'hide': False}
            ]
            return
        else:
            sessionStorage['state'] = "NEW_PLAYER"
            res['response']['text'] = 'Привет, представься, пожалуйста'
            return
    if sessionStorage['state'] == "NEW_PLAYER":
        try:
            db_sess = db_session.create_session()
            player = Player()
            player.id = user_id
            player.name = req['request']['original_utterance']
            db_sess.add(player)
            db_sess.commit()
            db_sess.close()
        except Exception as ex:
            logging.critical(ex)
            res['response']['text'] = ex
            return
        else:
            sessionStorage['player'] = player
            sessionStorage['state'] = "SHOW_MENU"
            res['response']['text'] = f'Привет, {player.name}'
            res['response']['buttons'] = [
                {'title': 'Играть', 'hide': False},
                {'title': 'Правила', 'hide': False},
                {'title': 'Статистика', 'hide': False},
                {'title': 'Рекорды', 'hide': False},
                {'title': 'Завершить', 'hide': False}
            ]
            return

    if sessionStorage['state'] == "SHOW_MENU":
        if req['request']['original_utterance'] == 'Играть':
            sessionStorage['state'] = "GAME"
            sessionStorage['round'] = 0
            #sessionStorage['secret_number'] = ''.join(map(str, sample(range(10), 4)))
            sessionStorage['secret_number'] = '1234'
            res['response']['text'] = 'Привет! Я загадала число из 4 неповторяющихся цифр. Попробуй угадать!'
            return
        if req['request']['original_utterance'] == 'Правила':
            res['response']['text'] = 'Нужно отгадать число из четырех разных цифр. Ты пишешь число, а я говорю ' \
                                      'сколько там "быков" и "коров". "Бык" - цифра встала на свое место. "Корова" -' \
                                      'цифра где-то есть, не обязательно на своем месте'
            res['response']['buttons'] = [
                {'title': 'Играть', 'hide': False},
                {'title': 'Правила', 'hide': False},
                {'title': 'Статистика', 'hide': False},
                {'title': 'Рекорды', 'hide': False},
                {'title': 'Завершить', 'hide': False}
            ]
            return
        if req['request']['original_utterance'] == 'Статистика':
            pl = sessionStorage['player']
            try:
                res['response']['text'] = f'Игрок - {pl.name}\n' \
                                      f'Создан - {pl.created_date}\n' \
                                      f'Игр проведено - {pl.played.games}\n' \
                                      f'Игр выиграно - {pl.score}'
            except Exception as ex:
                logging.critical(ex)
                res['response']['text'] = ex
                return
            else:
                res['response']['buttons'] = [
                    {'title': 'Играть', 'hide': False},
                    {'title': 'Правила', 'hide': False},
                    {'title': 'Статистика', 'hide': False},
                    {'title': 'Рекорды', 'hide': False},
                    {'title': 'Завершить', 'hide': False}
                ]
                return
        if req['request']['original_utterance'] == 'Рекорды':
            res['response']['text'] = 'Раздел в разработке'
            res['response']['buttons'] = [
                {'title': 'Играть', 'hide': False},
                {'title': 'Правила', 'hide': False},
                {'title': 'Статистика', 'hide': False},
                {'title': 'Рекорды', 'hide': False},
                {'title': 'Завершить', 'hide': False}
            ]
            return
        if req['request']['original_utterance'] == 'Завершить':
            res['response']['text'] = 'До новых встреч!'
            res['response']['end_session'] = True
            return
        res['response']['text'] = 'Я вас не поняла'
        return

    if sessionStorage['state'] == "GAME":
        sessionStorage['round'] += 1
        res['response']['buttons'] = [{'title': 'Сдаюсь', 'hide': True}]
        guess = str(req['request']['original_utterance'])
        bulls = cows = 0
        if req['request']['original_utterance'] == 'Сдаюсь':
            res['response']['text'] = f'Ну ты даешь! Это было число {sessionStorage["secret_number"]}'
            sessionStorage['state'] = "SHOW_MENU"
            res['response']['buttons'] = [
                {'title': 'Играть', 'hide': False},
                {'title': 'Правила', 'hide': False},
                {'title': 'Статистика', 'hide': False},
                {'title': 'Рекорды', 'hide': False},
                {'title': 'Завершить', 'hide': False}
            ]
            sessionStorage['player'].played_games += 1
            db_sess = db_session.create_session()
            try:
                db_sess.merge(sessionStorage['player'])
                db_sess.commit()
                db_sess.close()
            except Exception as ex:
                res['response']['text'] = ex.__str__()
                return
            else:
                return
        if not guess.isdigit():
            res['response']['text'] = 'Не число'
            return
        if not (1000 <= int(guess) <= 9999):
            res['response']['text'] = 'Неподходящее число'
            return
        for i in range(len(guess)):
            if guess[i] == sessionStorage["secret_number"][i]:
                bulls += 1
            if guess[i] in sessionStorage["secret_number"]:
                cows += 1
        if cows == 4 and bulls == 4:
            res['response']['text'] = f'Победа! Ты угадал за {sessionStorage["round"]} попыток'
            sessionStorage['state'] = "SHOW_MENU"
            res['response']['buttons'] = [
                {'title': 'Играть', 'hide': False},
                {'title': 'Правила', 'hide': False},
                {'title': 'Статистика', 'hide': False},
                {'title': 'Рекорды', 'hide': False},
                {'title': 'Завершить', 'hide': False}
            ]
            sessionStorage['player'].played_games += 1
            sessionStorage['player'].score += 1
            db_sess = db_session.create_session()
            try:
                db_sess.merge(sessionStorage['player'])
                db_sess.commit()
                db_sess.close()
            except Exception as ex:
                res['response']['text'] = ex.__str__()
                return
            else:
                return
        res['response']['text'] = f'Коровы - {cows}; быки - {bulls}'
        return

    res['response']['text'] = 'Я вас не поняла'
    return


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

