from fastapi import APIRouter
from schemas.schema import UserSchema


user = APIRouter()



@user.get('/')
def root():
    return {'message':'CRUD CON FASTAPI'}


@user.post('/api/user')
def create_user(data_user: UserSchema):
    print(data_user)
    