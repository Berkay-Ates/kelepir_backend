import json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends,status
from fastapi.responses import RedirectResponse,HTMLResponse

from Repositories.user_schemas import NewUser,User,Login
from Repositories import UserOperations
from Hashing.hashing  import Hash
from deta import Deta
from JWT_Token import token
from  Hashing.oath2 import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
deta=Deta()
users=deta.Base("users")
router=APIRouter(tags=['User'],prefix="/user")



@router.post("/newUser",status_code=status.HTTP_201_CREATED)
async def newUser(request : NewUser):
    if request.surname!="" and request.name!="" and request.password!="" and request.username!="" and request.email!="":
          if users.fetch({"email":request.email}).count==0:

            user=UserOperations.addUser(request, users)

            acces_token = token.create_access_token({"sub": user['key']})

            return{"accessToken":acces_token,"token_type":"bearer"}

          return {"Bu mail adresi Kullanılmaktadır"}

    return {"Bos alan girdiniz"}


@router.post("/login")
async def login(request: Login): #:OAuth2PasswordRequestForm = Depends(Login)):

    try:

        first_fetch=users.fetch({"username": request.username})
        s_fetch=users.fetch({"username": request.username})



        key=s_fetch.items[0]['key']


        password=s_fetch.items[0]['password']



        if Hash.verify(password, request.password):

            acces_token=token.create_access_token({"sub":key})

            return {"accessToken":acces_token,"token_type":"bearer"}
        else:
            return {"parola hatalı"}



    except :
        return {"kullanıcı adıo hatalı"}




    #return UserOperations.login(request,users)




@router.get("/")
async def allUsers(get_current_user : User =Depends(get_current_user)):
    return users.fetch().items

