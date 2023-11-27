from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from cruds import item as item_cruds
from schemas import itemCreate, ItemUpdate, ItemResponse
from database import get_db

DbDependency = Annotated[Session, Depends(get_db)]

# APIRouterをインスタンス化
router = APIRouter(prefix='/items', tags=['Items'])

# 全建取得は配列のresになるのでresponse_model=list[ItemResponse]
# ステータスコードを明示的に適切に設定
@router.get('', response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
async def find_all(db: DbDependency):
    return item_cruds.find_all(db)

# findは指定されたIDが無く、Noneが返る可能性があるのでresponse_model=Optional[ItemResponse]
@router.get('/{id}', response_model=ItemResponse, status_code=status.HTTP_200_OK)
# パスパラメータのバリデーション
async def find_by_id(db: DbDependency, id: int=Path(gt=0)):
    found_item = item_cruds.find_by_id(db, id)
    # 例外処理
    if not found_item:
        raise HTTPException(status_code=404, detail='Item not found')
    return found_item


@router.get('/', response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
# クエリパラメータのバリデーション
async def find_by_name(db: DbDependency, name: str = Query(min_length=2, max_length=20)):
    return item_cruds.find_by_name(db, name)

# createは201
@router.post('', response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
# db: DbDependency　の記述でdbのセッションを変数として定義
async def create(db: DbDependency, item_create: itemCreate):
    # print(item_create)
    # db変数をitem_cruds.createに渡している
    return item_cruds.create(db, item_create)


@router.put('/{id}', response_model=ItemResponse, status_code=status.HTTP_200_OK)
# パスパラメータのバリデーション 後ろに記述
async def update(db: DbDependency, item_update: ItemUpdate, id: int = Path(gt=0)):
    updated_item = item_cruds.update(db, id, item_update)
    # 例外処理
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not updated")
    return updated_item


@router.delete('/{id}', response_model=ItemResponse, status_code=status.HTTP_200_OK)
# パスパラメータのバリデーション
async def delete (db: DbDependency, id: int = Path(gt=0)):
    deleted_item = item_cruds.delete(db, id)
    # 例外処理
    if not deleted_item:
        raise HTTPException(status_code=404, detail='Item not deleted')
    return deleted_item