from fastapi import APIRouter, Query, Depends, HTTPException
from app.schemas.demo import CreateItemRequest, ItemResponse
from datetime import datetime

router = APIRouter(prefix="/demo", tags=["测试接口"])


@router.get("/")
async def get_list():
    return {"mes": "woshi jiek"}


@router.get("/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id, "name": f"商品id{item_id}"}


@router.get("/search/list")
async def search(
    keyword: str = Query(default="", description="关键词"),
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=1, ge=1, description="每页数量"),
):
    return {"keyword": keyword, "page": page, "pagesize": page_size}


@router.post("/items", response_model=ItemResponse)
async def create_item(body: CreateItemRequest):
    print(f"收到请求：{body.name}，价格：{body.price}")
    return {
        "id": 1,
        "name": body.name,
        "price": body.price,
        "description": body.description,
        "is_active": body.is_active,
        "create_at": datetime.now(),
    }


def get_current_user_id(x_user_id: str = Query(default=None, alias="X-User-Id")):
    """从请求头或查询参数里提取用户 ID，模拟认证逻辑"""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="缺少用户 ID")
    return x_user_id


@router.get("/protected")
async def protected_route(user_id: str = Depends(get_current_user_id)):
    # Depends(get_current_user_id) 表示调用这个接口前先执行 get_current_user_id
    # user_id 就是 get_current_user_id 的返回值
    return {"message": f"你好，用户 {user_id}"}
