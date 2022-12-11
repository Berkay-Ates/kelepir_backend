from fastapi import FastAPI
from Routes import Posts,Users
"""from Database import models
from Database.database import engine"""


app = FastAPI()

app.include_router(Users.router)
app.include_router(Posts.router)

#models.Base.metadata.create_all(engine)


"""@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
"""