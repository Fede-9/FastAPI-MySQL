from fastapi import APIRouter, Response
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED
from schemas.schema import UserSchema, DataUser
from config.db import engine
from models.users import users

from werkzeug.security import check_password_hash
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)


user = APIRouter()



@user.get('/')
def root():
    return 'FasAPI'

# ---  LOGIN ----
@user.post('/users/login')
def login_user(data_user: DataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.username == data_user.username)).first()
        if result != None:
            check_password = check_password_hash(result[3], data_user.password)
            if check_password:
                return 'Correcto'
        return 'Incorrecto'


@user.get('/users')
def get_users():
    with engine.connect() as conn:
        return conn.execute(users.select()).fetchall()

@user.get('/users/{id}')
def get_user(id:str):
    with engine.connect() as conn:
        return conn.execute(users.select().where(users.c.id == id)).first()


@user.post('/users', status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        new_user = {'name':data_user.name, 'username':data_user.username}
        new_user['password'] = f.encrypt(data_user.password.encode('utf-8'))
        result = conn.execute(users.insert().values(new_user))
        # return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()
        return Response(status_code=HTTP_201_CREATED)


@user.delete('/users/{id}', status_code=HTTP_204_NO_CONTENT)
def delete_user(id:str):
    with engine.connect() as conn:
        conn.execute(users.delete().where(users.c.id == id))
        return Response(status_code=HTTP_204_NO_CONTENT)


@user.put('/users/{id}')
def update_user(id: str, data_user:UserSchema):
    with engine.connect() as conn:
        conn.execute(users.update().values(name=data_user.name, 
                                        username=data_user.username,
                                        password=f.encrypt(data_user.password.encode('utf-8'))).where(users.c.id == id))
        return 'actualizadooo'

    