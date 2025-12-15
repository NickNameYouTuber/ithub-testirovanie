import pytest
from app.services import ItemService
from app.models import ItemCreate


class TestItemService:
    def test_create_item_success(self):
        service = ItemService()
        item_data = ItemCreate(
            name="Test Item", description="Test", price=10.0
        )
        
        result = service.create_item(item_data)
        
        assert result.id == 1
        assert result.name == "Test Item"
        assert result.description == "Test"
        assert result.price == 10.0
        assert result.created_at is not None

    def test_get_item_by_id_existing(self):
        service = ItemService()
        item_data = ItemCreate(name="Test Item", price=10.0)
        created_item = service.create_item(item_data)
        
        result = service.get_item_by_id(created_item.id)
        
        assert result is not None
        assert result.id == created_item.id
        assert result.name == "Test Item"

    def test_get_item_by_id_nonexistent(self):
        service = ItemService()
        
        result = service.get_item_by_id(999)
        
        assert result is None

    def test_get_all_items_empty(self):
        service = ItemService()
        
        result = service.get_all_items()
        
        assert result == []

    def test_get_all_items_multiple(self):
        service = ItemService()
        item1 = service.create_item(ItemCreate(name="Item 1", price=10.0))
        item2 = service.create_item(ItemCreate(name="Item 2", price=20.0))
        
        result = service.get_all_items()
        
        assert len(result) == 2
        assert result[0].id == item1.id
        assert result[1].id == item2.id

    def test_delete_item_existing(self):
        service = ItemService()
        created_item = service.create_item(
            ItemCreate(name="Test Item", price=10.0)
        )
        
        result = service.delete_item(created_item.id)
        
        assert result is True
        assert service.get_item_by_id(created_item.id) is None

    def test_delete_item_nonexistent(self):
        service = ItemService()
        
        result = service.delete_item(999)
        
        assert result is False

    def test_item_ids_increment(self):
        service = ItemService()
        item1 = service.create_item(ItemCreate(name="Item 1", price=10.0))
        item2 = service.create_item(ItemCreate(name="Item 2", price=20.0))
        item3 = service.create_item(ItemCreate(name="Item 3", price=30.0))
        
        assert item1.id == 1
        assert item2.id == 2
        assert item3.id == 3

