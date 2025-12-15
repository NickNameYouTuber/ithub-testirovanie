from typing import List, Optional
from datetime import datetime
from app.models import ItemCreate, ItemResponse


class ItemService:
    def __init__(self):
        self.items = []
        self.next_id = 1

    def create_item(self, item_data: ItemCreate) -> ItemResponse:
        new_item = ItemResponse(
            id=self.next_id,
            name=item_data.name,
            description=item_data.description,
            price=item_data.price,
            created_at=datetime.now()
        )
        self.items.append(new_item)
        self.next_id += 1
        return new_item

    def get_item_by_id(self, item_id: int) -> Optional[ItemResponse]:
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def get_all_items(self) -> List[ItemResponse]:
        return self.items.copy()

    def delete_item(self, item_id: int) -> bool:
        for index, item in enumerate(self.items):
            if item.id == item_id:
                self.items.pop(index)
                return True
        return False

