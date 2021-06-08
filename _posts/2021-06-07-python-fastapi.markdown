---
categories: blog
date: '2021-06-07 11:50:18'
description: it is so pythonic
layout: post
published: True
title: "fastapi文档阅读（二）"
tags: pythonic fastapi web
---

### form

```python
from fastapi import FastAPI, Form


app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

```

### files

```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File(...)):
	# File是Form的子类，实际上上传文件大都使用form的格式上传的，这里的file已经是字节对象了
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
	# 这里的file是一个类似文件指针
	contens = await file.read()
    return {"filename": file.filename}

```

关于await的执行的，可以参考这个文章,[fastapi的async](https://blog.csdn.net/qq_29518275/article/details/109360617)

### errors

单个接口中的异常可以使用HTTPException处理

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}

@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}
```

一般在项目中，往往需要统一处理异常，使用exception_handler，这个和flask就写法上很像啊

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse



class UnicornException(Exception):

    def __init__(self, name: str):

        self.name = name

app = FastAPI()


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

```

### 中间件

```python
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    response.headers["X-Process-Time"] = str(process_time)

    return response

```

