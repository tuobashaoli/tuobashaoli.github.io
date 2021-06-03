---
categories: blog
date: '2021-06-02 15:41:18'
description: it is so pythonic
layout: post
published: False
title: "fastapi文档阅读"
tags: pythonic fastapi web
---

### 路径传参数

```python
from fastapi import FastAPI

app = FastAPI()

# 按照顺序匹配路径，如果/users/{user_id}放在/users/me前面，会将/users/me匹配给/users/{user_id}

@app.get("/users/me")

async def read_user_me():
    return {"user_id": "the current user"}



@app.get("/users/{user_id}")

async def read_user(user_id: str):
    return {"user_id": user_id}

```

### 预设值/枚举值

```python
from enum import Enum


from fastapi import FastAPI


class ModelName(str, Enum):

    alexnet = "alexnet"

    resnet = "resnet"

    lenet = "lenet"

app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

```

### 可选参数

```python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}/items/{item_id}")

async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
```