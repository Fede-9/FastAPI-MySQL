from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import engine, meta_data



users = Table('users', meta_data,
              Column('id', Integer, primary_key=True),
              Column('name', String(100), nullable=False),
              Column('username', String(100), nullable=False),
              Column('password', String(100), nullable=False))


meta_data.create_all(engine)