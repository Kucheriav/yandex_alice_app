from flask import Flask
from data import db_session
from data.players import Player



app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def add_player(info):
    player = Player()
    player.id = info[0]
    player.name = info[1]
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
    user = db_sess.query(Player).filter(Player.id == info[0]).first()
    print(user)


def main():
    db_session.global_init("db/game.db")
    #app.run()
    answ = input('A u new: y/n')
    if answ == 'y':
        id_name = input('id name').split()
        add_player(id_name)
    else:
        id_name = input('id name').split()
        login(id_name)




if __name__ == '__main__':
    main()



