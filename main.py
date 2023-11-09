import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    save_path = "./uploads"  # 현재 디렉토리의 'uploads' 폴더
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open(f"{save_path}/{file.filename}", "wb") as f:
        f.write(contents)
    return {"filename": file.filename}

@app.get("/downloadfile/{filename}")
async def download_file(filename: str):
    return FileResponse(f"./uploads/{filename}")

@app.post("/items/")
async def create_item(item: Item):
    return item


