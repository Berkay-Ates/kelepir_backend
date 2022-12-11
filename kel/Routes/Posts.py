from fastapi import APIRouter
from typing import List,Optional
from fastapi.responses import FileResponse,StreamingResponse
from Repositories import post_schemas
from deta import Deta
from  Hashing.oath2 import get_current_user
from Repositories.user_schemas import User
from fastapi import APIRouter, Depends
from fastapi import FastAPI, File, UploadFile,status
deta=Deta()
posts=deta.Base("posts")
sepetler=deta.Base("sepetim")
router=APIRouter(tags=['Posts'],prefix="/post")
drive = deta.Drive("images") # access to your drive
from datetime import datetime
import uuid


router=APIRouter()

@router.post("/newPost",status_code=status.HTTP_201_CREATED)#request: post_schemas.NewPost,
async def newPost(request: post_schemas.NewPost,get_current_user : User =Depends(get_current_user)):
    #Imagename = str(uuid.uuid1().hex)  # file.filename

    post=post_schemas.Post(data=request.data
                           ,product=request.product
                           ,brand=request.brand
                           ,price=request.price
                           ,latitude=request.latitude #X
                           ,longtitute=request.longtitute #Y
                           ,store_name=request.store_name
                           ,time=str(datetime.utcnow())
                           ,usernameId=get_current_user['key']
                           ,imageId=request.imageId)


    posts.put(post.dict())
    return request

@router.post("/uploadFile",status_code=status.HTTP_201_CREATED)#request: post_schemas.NewPost,
async def uploadImage(file : UploadFile =File(...),get_current_user : User =Depends(get_current_user)):# ):#,get_current_user : User =Depends(get_current_user)):
    Imagename = str(uuid.uuid1().hex)  # file.filename

    f = file.file
    res = drive.put(Imagename+".png", f)

    return {"image_name":Imagename}


@router.get("/getPostsUsingLocation/")
async def getPosts(X: float , Y:float , product:str ,get_current_user : User =Depends(get_current_user)):
    genislik=0.01
    q=[{"latitude?gte":X-genislik,"latitude?lte":X+genislik,"longtitute?gte":Y-genislik,"longtitute?lte":Y+genislik}]

    if product!="":
        q = [{"latitude?gte": X - genislik, "latitude?lte": X + genislik, "longtitute?gte": Y - genislik,
          "longtitute?lte": Y + genislik,"product?contains":product}]

    item_list=posts.fetch(query=q).items
    a=PostToResponsePost(item_list)


    return a


@router.get("/getImage/")
async def getImage(imageId:str ):#,get_current_user : User =Depends(get_current_user)):

    #image=drive.get(imageId+".png")
    f="https://drive.deta.sh/v1/a0tzl87y/images/files/download?name=1944059f783511ed97823db069e62abf.png"
    #return StreamingResponse(image.iter_chunks(1024), media_type="form-data")
    return f

    """ a=image.read()
    image.close()
    return a.decode("utf-8")"""



@router.post("/addComment")
async def addComment(comment : post_schemas.Comment , get_current_user : User =Depends(get_current_user)):
    a={}

    post=posts.get(comment.postId)

    post["comments"].append({
        "username":get_current_user["username"],
        "comment":comment.comment
        })

    posts.put(post ,key=comment.postId)

    return post


@router.get("/getAll")
async def getAll(get_current_user : User =Depends(get_current_user)):
    l=posts.fetch().items
    l=sorted(l,key=lambda x: int(x["like_count"]),reverse=True)
    l=sorted(l,key=lambda x:float(x["price"]))

    #return PostToResponsePost(posts.fetch().items)
    return PostToResponsePost(l)

@router.get("/getComments/")
async def getSelectedCommment(postKey:str, get_current_user : User =Depends(get_current_user)):
    return posts.get(postKey)["comments"]


@router.post("/AppSepetim")
async def Sepetim(sepetim:post_schemas.Sepetim):
    sepetler.put(sepetim.dict())


    return 0





@router.post("/upDown")
def UpDown(upDown:post_schemas.UpDown ):#,get_current_user : User =Depends(get_current_user)):

        post=posts.get(upDown.postId)
        a = post['like_count']
        b = post['dislike_count']

        a+=1
        b+=1
        if upDown.op==1 :
            post['like_count']=a

        elif upDown.op==-1:
            post['dislike_count']=b

        else:
            return post

        posts.put(post,post['key'])

        return post





def PostToResponsePost(l : list):
    a = []

    for i in l:
        p = post_schemas.ResponsePost( data=i["data"]
                                      ,product=i["product"]
                                      , brand=i["brand"]
                                      , price=i["price"]
                                      , latitude=i["latitude"] # X
                                      , longtitute=i["longtitute"]  # Y
                                      , store_name=i["store_name"]
                                      , time=i["time"]
                                      , usernameId=i['usernameId']
                                      ,key=i['key']
                                      , like_count=i["like_count"]
                                      , dislike_count=i["dislike_count"]
                                      , imageId=i["imageId"])
        a.append(p)

    return a




