from sqlalchemy import Table, create_engine, MetaData
from sqlalchemy.sql import select, insert
from flask_sqlalchemy import SQLAlchemy
import psycopg2

# db = SQLAlchemy()
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(15), unique=True)
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(80))

# meta = MetaData()

# uri = 'jdbc:postgresql://10.129.0.19:6432/mo'
uri = '10.129.0.19:6432/mo'
dialect = 'postgresql+psycopg2'
db_user = 'moro'
db_pass = 'Yo6aephiCheo0pae'
url = dialect + "://" + (db_user + ':' + db_pass) + '@' + uri
print(url)

# engine = create_engine('sqlite:///users.db', echo=False)
engine = create_engine(url, echo=False)    
metadata = MetaData()

print(engine.table_names())

users = Table('migrations', metadata, autoload=True, autoload_with=engine)
print(users.columns)
connection = engine.connect()

query = select(users)
# print(connection.execute(query).fetchall())
connection.close()