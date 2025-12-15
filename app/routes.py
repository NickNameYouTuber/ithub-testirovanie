from fastapi import APIRouter, HTTPException, status
from app.models import ItemCreate, ItemResponse
from app.services import ItemService

router = APIRouter(prefix="/api/items", tags=["items"])

item_service = ItemService()


@router.get("/", response_model=list[ItemResponse])
async def get_all_items():
    return item_service.get_all_items()


@router.post(
    "/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED
)
async def create_item(item: ItemCreate):
    return item_service.create_item(item)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    item = item_service.get_item_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    deleted = item_service.delete_item(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )