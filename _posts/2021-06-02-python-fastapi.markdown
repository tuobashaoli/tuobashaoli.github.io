---
categories: blog
date: '2021-06-02 15:41:18'
description: it is so pythonic
layout: post
published: True
title: "fastapi文档阅读（一）"
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

### post请求体

默认会将post的请求体使用json格式

```python
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):

    name: str

    description: Optional[str] = None

    price: float
    tax: Optional[float] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
	# 这里的item是Item(BaseModel)类的实例，不是字典，需要调用item.dict()转换成字典
    return item

```

### 参数校验

```python
from typing import Optional

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")
):
	# 如果参数是必须的，去掉Optional就行，并且None改为...
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(..., gt=0, lt=10.5)
):
	# 也可以做数值校验，size是大于0且小于10.5的数值
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

### 综合参数

```python
from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class User(BaseModel):
    username: str
    full_name: Optional[str] = None

@app.put("/items/{item_id}")

async def update_item(
    item_id: int, item: Item, user: User, importance: int = Body(...)
):
	# Body将会使importance传入到请求体中
	#{
	#	"item": {
	#		"name": "Foo",
	#		"description": "The pretender",
	#		"price": 42.0,
	#		"tax": 3.2
	#	},
	#	"user": {
	#		"username": "dave",
	#		"full_name": "Dave Grohl"
	#	},
	#	"importance": 5
	#}
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results
```

### pydantic中的字段校验

这个是使用pydantic中自带的字段校验功能，使用Field

```python
from typing import Optional



from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
```

### 返回值

```python
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []



@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item

```
