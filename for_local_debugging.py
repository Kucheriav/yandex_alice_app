from flask import Flask
from data import db_session
from data.players import Player



app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def add_player(info):
    player = Player()
    player.login = info[0]
    player.hashed_password = hash(info[1])
    db_sess = db_session.create_session()
    try:
        db_sess.add(player)
        db_sess.commit()
    except Exception as ex:
        print(ex)
    else:
        print('ok')


def login(info):
    db_sess = db_session.create_session()
    user = db_sess.query(Player).filter(Player.login == info[0], Player.hashed_password == hash(info[1])).first()
    print(user)


def main():
    db_session.global_init("db/game.db")
    #app.run()
    answ = input('A u new: y/n')
    if answ == 'y':
        log_pasw = input('Login passw').split()
        add_player(log_pasw)
    else:
        log_pasw = input('Login passw').split()
        login(log_pasw)




if __name__ == '__main__':
    main()



