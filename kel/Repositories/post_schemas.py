from pydantic  import BaseModel
from typing import List,Optional
from fastapi import FastAPI, File, UploadFile


class NewPost(BaseModel):
    data: str
    product:str
    brand:str
    price :str
    latitude: float
    longtitute: float
    store_name: str
    imageId:str

class Comment(BaseModel):
    postId:str
    comment:str

class Post(BaseModel):
    data: str
    product: str
    brand: str
    price: str
    latitude: float
    longtitute: float
    store_name: str
    time: str
    usernameId:str
    comments:List[Comment]=[]
    like_count:int =0
    dislike_count:int=0
    imageId:str

class ResponsePost(BaseModel):
    data: str
    product: str
    brand: str
    price: str
    latitude: float
    longtitute: float
    store_name: str
    time: str
    usernameId: str
    like_count: int = 0
    dislike_count: int = 0
    imageId: str
    key:str


class filterOptions(BaseModel):
    data:Optional[str]
    product:Optional[str]
    brand:Optional[str]
    price:Optional[str]
    latitude: float
    longtitute: float
    store_name:Optional[str]
    time :Optional[str]


class SepettekiUrun(BaseModel):
    data: str
    product: str
    brand: str
    userId:str


class Sepetim(BaseModel):
    urunler:List[SepettekiUrun]


class UpDown(BaseModel):
    postId:str
    op:int #+1 -1




