from fastapi import FastAPI
from routers import item

app = FastAPI()
app.include_router(item.router) # routers/item.pyを読み込み
