from Hashing.hashing import Hash
from sqlalchemy.orm import  Session
from passlib.context import CryptContext
from Repositories.user_schemas  import NewUser,User,Login
#from Database import models
from deta import Deta
crypt_cntxt=CryptContext(schemes=["bcrypt"] ,deprecated="auto")




def login(request: Login, users : Deta):
    #user=db.query(models.Users).filter(models.Users.username==request.username).first()

    #user=users.fetch(query={"username":request.username} , limit=3)
    user=users.fetch()
    print(user)

    if not user:
        return "User not found"
    """
    if Hash.veify(user.password,request.password):
        print("logging in")
        return "giris yapıldı"
    """
    return "cc" #Hash.veify(user.password,request.password)




def addUser(user: NewUser ,users : Deta):
    user.password=Hash.hash(user.password)
    return users.put(user.dict())