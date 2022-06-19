from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import configparser

from server import User, engine


User_tbl = Table('user', User.metadata)

def create_user_table():
    User.metadata.create_all(engine)

def add_user(username, password, email):
    hashed_password = generate_password_hash(password, method='sha256')

    ins = User_tbl.insert().values(
        username=username, email=email, password=hashed_password)

    conn = engine.connect()
    conn.execute(ins)
    conn.close()

def del_user(username):
    delete = User_tbl.delete().where(User_tbl.c.username == username)

    conn = engine.connect()
    conn.execute(delete)
    conn.close()

def show_users():
    select_st = select([User_tbl.c.username, User_tbl.c.email])

    conn = engine.connect()
    rs = conn.execute(select_st)

    for row in rs:
        print(row)

    conn.close()


if __name__ == '__main__':
    show_users()
