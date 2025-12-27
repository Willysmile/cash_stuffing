"""
Tests pour les routes API des wish lists
"""
import pytest
from decimal import Decimal
from datetime import date
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.wish_list import WishList
from app.models.wish_list_item import WishListItem


class TestWishListCRUD:
    """Tests CRUD pour les wish lists."""

    @pytest.mark.asyncio
    async def test_create_wish_list(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test creating a new wish list."""
        response = await client.post(
            "/api/wish-lists",
            headers=auth_headers,
            json={
                "name": "Christmas 2025",
                "description": "Gift ideas for Christmas",
                "list_type": "to_receive",
                "target_date": "2025-12-25",
                "budget_allocated": 500.00,
                "status": "active"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Christmas 2025"
        assert data["list_type"] == "to_receive"
        assert data["status"] == "active"

    @pytest.mark.asyncio
    async def test_list_wish_lists(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test listing all wish lists."""
        wish_list1 = WishList(
            user_id=test_user.id, name="List 1", list_type="to_receive", status="active"
        )
        wish_list2 = WishList(
            user_id=test_user.id, name="List 2", list_type="to_give", status="active"
        )
        db_session.add_all([wish_list1, wish_list2])
        await db_session.commit()

        response = await client.get("/api/wish-lists", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    @pytest.mark.asyncio
    async def test_get_wish_list_by_id(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test getting a wish list by ID with items."""
        wish_list = WishList(
            user_id=test_user.id, name="My List", list_type="to_receive", status="active"
        )
        db_session.add(wish_list)
        await db_session.commit()
        await db_session.refresh(wish_list)
        
        item = WishListItem(
            wish_list_id=wish_list.id, name="Item 1", price=Decimal("50"), quantity=1
        )
        db_session.add(item)
        await db_session.commit()

        response = await client.get(f"/api/wish-lists/{wish_list.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "My List"
        assert len(data["items"]) == 1
        assert "total_cost" in data
        assert "purchased_cost" in data
        assert "remaining_cost" in data

    @pytest.mark.asyncio
    async def test_get_wish_list_not_found(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test getting a non-existent wish list."""
        response = await client.get("/api/wish-lists/99999", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_wish_list(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test updating a wish list."""
        wish_list = WishList(
            user_id=test_user.id, name="Original", list_type="to_receive", status="active"
        )
        db_session.add(wish_list)
        await db_session.commit()
        await db_session.refresh(wish_list)

        response = await client.put(
            f"/api/wish-lists/{wish_list.id}",
            headers=auth_headers,
            json={
                "name": "Updated",
                "status": "archived"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated"
        assert data["status"] == "archived"

    @pytest.mark.asyncio
    async def test_delete_wish_list(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test deleting a wish list."""
        wish_list = WishList(
            user_id=test_user.id, name="To Delete", list_type="to_receive", status="active"
        )
        db_session.add(wish_list)
        await db_session.commit()
        await db_session.refresh(wish_list)

        response = await client.delete(f"/api/wish-lists/{wish_list.id}", headers=auth_headers)
        assert response.status_code == 204

        # Vérifier suppression
        get_response = await client.get(f"/api/wish-lists/{wish_list.id}", headers=auth_headers)
        assert get_response.status_code == 404


class TestWishListItems:
    """Tests pour les articles de wish lists."""

    @pytest.mark.asyncio
    async def test_create_item(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test creating a wish list item."""
        wish_list = WishList(
            user_id=test_user.id, name="My List", list_type="to_receive", status="active"
        )
        db_session.add(wish_list)
        await db_session.commit()
        await db_session.refresh(wish_list)

        response = await client.post(
            f"/api/wish-lists/{wish_list.id}/items",
            headers=auth_headers,
            json={
                "wish_list_id": wish_list.id,
                "name": "Nintendo Switch",
                "description": "Gaming console",
                "price": 299.99,
                "quantity": 1,
                "priority": "wanted",
                "status": "to_buy"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Nintendo Switch"
        assert data["price"] in ["299.99", "299"]

    @pytest.mark.asyncio
    async def test_create_item_invalid_wish_list(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test creating an item for non-existent wish list."""
        response = await client.post(
            "/api/wish-lists/99999/items",
            headers=auth_headers,
            json={
                "wish_list_id": 99999,
                "name": "Item",
                "price": 10.00,
                "quantity": 1
            }
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_items(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test listing items of a wish list."""
        wish_list = WishList(
            user_id=test_user.id, name="My List", list_type="to_receive", status="active"
        )
        db_session.add(wish_list)
        await db_session.commit()
        await db_session.refresh(wish_list)
        
        item1 = WishListItem(
            wish_list_id=wish_list.id, name="Item 1", price=Decimal("50"), quantity=1
        )
        item2 = WishListItem(
            wish_list_id=wish_list.id, name="Item 2", price=Decimal("75"), quantity=1
        )
        db_session.add_all([item1, item2])
        await db_session.commit()

        response = await client.get(f"/api/wish-lists/{wish_list.id}/items", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    @pytest.mark.asyncio
    async def test_update_item(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test updating a wish list item."""
        wish_list = WishList(
            user_id=test_user.id, name="My List", list_type="to_receive", status="active"
        )
        db_session.add(wish_list)
        await db_session.commit()
        await db_session.refresh(wish_list)
        
        item = WishListItem(
            wish_list_id=wish_list.id, name="Original", price=Decimal("50"), quantity=1
        )
        db_session.add(item)
        await db_session.commit()
        await db_session.refresh(item)

        response = await client.put(
            f"/api/wish-lists/items/{item.id}",
            headers=auth_headers,
            json={
                "name": "Updated",
                "price": 75.00
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated"
        assert data["price"] in ["75.00", "75"]

    @pytest.mark.asyncio
    async def test_delete_item(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test deleting a wish list item."""
        wish_list = WishList(
            user_id=test_user.id, name="My List", list_type="to_receive", status="active"
        )
        db_session.add(wish_list)
        await db_session.commit()
        await db_session.refresh(wish_list)
        
        item = WishListItem(
            wish_list_id=wish_list.id, name="To Delete", price=Decimal("50"), quantity=1
        )
        db_session.add(item)
        await db_session.commit()
        await db_session.refresh(item)

        response = await client.delete(f"/api/wish-lists/items/{item.id}", headers=auth_headers)
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_mark_item_as_purchased(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test marking an item as purchased."""
        wish_list = WishList(
            user_id=test_user.id, name="My List", list_type="to_receive", status="active"
        )
        db_session.add(wish_list)
        await db_session.commit()
        await db_session.refresh(wish_list)
        
        item = WishListItem(
            wish_list_id=wish_list.id, name="Item", price=Decimal("50"), quantity=1, status="to_buy"
        )
        db_session.add(item)
        await db_session.commit()
        await db_session.refresh(item)

        response = await client.post(
            f"/api/wish-lists/items/{item.id}/mark-purchased",
            headers=auth_headers,
            params={"purchased_date": str(date.today())}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "purchased"
        assert data["purchased_date"] is not None


class TestWishListFilters:
    """Tests pour les filtres de wish lists."""

    @pytest.mark.asyncio
    async def test_filter_by_type(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test filtering wish lists by type."""
        to_receive = WishList(
            user_id=test_user.id, name="To Receive", list_type="to_receive", status="active"
        )
        to_give = WishList(
            user_id=test_user.id, name="To Give", list_type="to_give", status="active"
        )
        db_session.add_all([to_receive, to_give])
        await db_session.commit()

        response = await client.get(
            "/api/wish-lists?list_type=to_receive",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["list_type"] == "to_receive"

    @pytest.mark.asyncio
    async def test_filter_by_status(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test filtering wish lists by status."""
        active = WishList(
            user_id=test_user.id, name="Active", list_type="to_receive", status="active"
        )
        archived = WishList(
            user_id=test_user.id, name="Archived", list_type="to_receive", status="archived"
        )
        db_session.add_all([active, archived])
        await db_session.commit()

        response = await client.get(
            "/api/wish-lists?status=active",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "active"

    @pytest.mark.asyncio
    async def test_filter_items_by_status(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test filtering items by status."""
        wish_list = WishList(
            user_id=test_user.id, name="My List", list_type="to_receive", status="active"
        )
        db_session.add(wish_list)
        await db_session.commit()
        await db_session.refresh(wish_list)
        
        to_buy = WishListItem(
            wish_list_id=wish_list.id, name="To Buy", price=Decimal("50"), 
            quantity=1, status="to_buy"
        )
        purchased = WishListItem(
            wish_list_id=wish_list.id, name="Purchased", price=Decimal("75"), 
            quantity=1, status="purchased"
        )
        db_session.add_all([to_buy, purchased])
        await db_session.commit()

        response = await client.get(
            f"/api/wish-lists/{wish_list.id}/items?item_status=to_buy",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "to_buy"


class TestWishListIsolation:
    """Tests pour l'isolation entre utilisateurs."""

    @pytest.mark.asyncio
    async def test_cannot_access_other_user_wish_list(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, second_user: User
    ):
        """Test that users cannot access other users' wish lists."""
        wish_list = WishList(
            user_id=second_user.id, name="Other List", list_type="to_receive", status="active"
        )
        db_session.add(wish_list)
        await db_session.commit()
        await db_session.refresh(wish_list)

        response = await client.get(f"/api/wish-lists/{wish_list.id}", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_only_own_wish_lists(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User, second_user: User
    ):
        """Test that listing wish lists only returns own wish lists."""
        own_list = WishList(
            user_id=test_user.id, name="My List", list_type="to_receive", status="active"
        )
        other_list = WishList(
            user_id=second_user.id, name="Other List", list_type="to_receive", status="active"
        )
        db_session.add_all([own_list, other_list])
        await db_session.commit()

        response = await client.get("/api/wish-lists", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "My List"


class TestWishListCalculations:
    """Tests pour les calculs de coûts."""

    @pytest.mark.asyncio
    async def test_cost_calculations(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test that cost calculations are correct."""
        wish_list = WishList(
            user_id=test_user.id, name="My List", list_type="to_receive", status="active"
        )
        db_session.add(wish_list)
        await db_session.commit()
        await db_session.refresh(wish_list)
        
        # 2 items to buy
        item1 = WishListItem(
            wish_list_id=wish_list.id, name="Item 1", price=Decimal("50"), 
            quantity=2, status="to_buy"
        )
        item2 = WishListItem(
            wish_list_id=wish_list.id, name="Item 2", price=Decimal("30"), 
            quantity=1, status="to_buy"
        )
        # 1 item purchased
        item3 = WishListItem(
            wish_list_id=wish_list.id, name="Item 3", price=Decimal("20"), 
            quantity=1, status="purchased"
        )
        db_session.add_all([item1, item2, item3])
        await db_session.commit()

        response = await client.get(f"/api/wish-lists/{wish_list.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        # total_cost = (50*2) + (30*1) + (20*1) = 150
        # purchased_cost = 20
        # remaining_cost = 130
        assert float(data["total_cost"]) == 150.0
        assert float(data["purchased_cost"]) == 20.0
        assert float(data["remaining_cost"]) == 130.0
