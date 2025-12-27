"""Tests for categories routes."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Category


class TestCategoryCRUD:
    """Tests for category CRUD operations."""

    @pytest.mark.asyncio
    async def test_create_category(self, client: AsyncClient, auth_headers: dict):
        """Test creating a new category."""
        response = await client.post(
            "/api/categories",
            headers=auth_headers,
            json={
                "name": "Alimentation",
                "color": "#FF5733",
                "icon": "shopping-cart"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Alimentation"
        assert data["color"] == "#FF5733"
        assert data["icon"] == "shopping-cart"
        assert data["parent_id"] is None
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_subcategory(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test creating a subcategory."""
        # Créer une catégorie parent
        parent = Category(
            user_id=test_user.id,
            name="Alimentation",
            color="#FF5733",
            icon="shopping-cart"
        )
        db_session.add(parent)
        await db_session.commit()
        await db_session.refresh(parent)

        # Créer une sous-catégorie
        response = await client.post(
            "/api/categories",
            headers=auth_headers,
            json={
                "name": "Courses",
                "parent_id": parent.id
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Courses"
        assert data["parent_id"] == parent.id

    @pytest.mark.asyncio
    async def test_create_category_invalid_parent(self, client: AsyncClient, auth_headers: dict):
        """Test creating category with non-existent parent fails."""
        response = await client.post(
            "/api/categories",
            headers=auth_headers,
            json={
                "name": "Test",
                "parent_id": 9999  # N'existe pas
            }
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_categories(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test listing all categories."""
        # Créer quelques catégories
        categories = [
            Category(user_id=test_user.id, name="Alimentation", sort_order=1),
            Category(user_id=test_user.id, name="Loisirs", sort_order=2),
        ]
        db_session.add_all(categories)
        await db_session.commit()

        response = await client.get("/api/categories", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Alimentation"
        assert data[1]["name"] == "Loisirs"

    @pytest.mark.asyncio
    async def test_get_category_by_id(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test getting a specific category."""
        category = Category(user_id=test_user.id, name="Transport", color="#0000FF")
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)

        response = await client.get(f"/api/categories/{category.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == category.id
        assert data["name"] == "Transport"
        assert data["color"] == "#0000FF"

    @pytest.mark.asyncio
    async def test_get_category_not_found(self, client: AsyncClient, auth_headers: dict):
        """Test getting non-existent category returns 404."""
        response = await client.get("/api/categories/9999", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_category(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test updating a category."""
        category = Category(user_id=test_user.id, name="Old Name", color="#000000")
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)

        response = await client.put(
            f"/api/categories/{category.id}",
            headers=auth_headers,
            json={
                "name": "New Name",
                "color": "#FFFFFF",
                "icon": "new-icon"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"
        assert data["color"] == "#FFFFFF"
        assert data["icon"] == "new-icon"

    @pytest.mark.asyncio
    async def test_delete_category(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test deleting a category."""
        category = Category(user_id=test_user.id, name="To Delete")
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)

        response = await client.delete(f"/api/categories/{category.id}", headers=auth_headers)
        assert response.status_code == 204

        # Vérifier que la catégorie a été supprimée
        get_response = await client.get(f"/api/categories/{category.id}", headers=auth_headers)
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_category_with_children_fails(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test deleting category with subcategories fails."""
        parent = Category(user_id=test_user.id, name="Parent")
        db_session.add(parent)
        await db_session.commit()
        await db_session.refresh(parent)

        child = Category(user_id=test_user.id, name="Child", parent_id=parent.id)
        db_session.add(child)
        await db_session.commit()

        response = await client.delete(f"/api/categories/{parent.id}", headers=auth_headers)
        assert response.status_code == 400
        detail = response.json()["detail"].lower()
        assert "subcategor" in detail or "sous-catégories" in detail


class TestCategoryTree:
    """Tests for category tree endpoint."""

    @pytest.mark.asyncio
    async def test_get_category_tree(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test getting hierarchical category tree."""
        # Créer une structure hiérarchique
        parent1 = Category(user_id=test_user.id, name="Parent 1", sort_order=1)
        parent2 = Category(user_id=test_user.id, name="Parent 2", sort_order=2)
        db_session.add_all([parent1, parent2])
        await db_session.commit()
        await db_session.refresh(parent1)
        await db_session.refresh(parent2)

        child1 = Category(user_id=test_user.id, name="Child 1", parent_id=parent1.id)
        child2 = Category(user_id=test_user.id, name="Child 2", parent_id=parent1.id)
        db_session.add_all([child1, child2])
        await db_session.commit()

        response = await client.get("/api/categories/tree", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        # Doit avoir 2 catégories racines
        assert len(data) == 2
        assert data[0]["name"] == "Parent 1"
        assert data[1]["name"] == "Parent 2"
        
        # Parent 1 doit avoir 2 enfants
        assert len(data[0]["children"]) == 2
        assert data[1]["children"] == []


class TestCategoryFilters:
    """Tests for category filtering."""

    @pytest.mark.asyncio
    async def test_filter_by_parent_id(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test filtering categories by parent_id."""
        parent = Category(user_id=test_user.id, name="Parent")
        db_session.add(parent)
        await db_session.commit()
        await db_session.refresh(parent)

        children = [
            Category(user_id=test_user.id, name="Child 1", parent_id=parent.id),
            Category(user_id=test_user.id, name="Child 2", parent_id=parent.id),
        ]
        db_session.add_all(children)
        await db_session.commit()

        response = await client.get(
            f"/api/categories?parent_id={parent.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        for item in data:
            assert item["parent_id"] == parent.id

    @pytest.mark.asyncio
    async def test_search_categories(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test searching categories by name."""
        categories = [
            Category(user_id=test_user.id, name="Alimentation"),
            Category(user_id=test_user.id, name="Transport"),
            Category(user_id=test_user.id, name="Loisirs"),
        ]
        db_session.add_all(categories)
        await db_session.commit()

        response = await client.get(
            "/api/categories?search=ali",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Alimentation"


class TestCategoryIsolation:
    """Tests for user isolation."""

    @pytest.mark.asyncio
    async def test_cannot_access_other_user_category(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, second_user: User
    ):
        """Test that users cannot access other users' categories."""
        # Créer une catégorie pour l'autre utilisateur
        other_category = Category(user_id=second_user.id, name="Other User Category")
        db_session.add(other_category)
        await db_session.commit()
        await db_session.refresh(other_category)

        # Essayer d'accéder avec le premier utilisateur
        response = await client.get(
            f"/api/categories/{other_category.id}",
            headers=auth_headers
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_only_own_categories(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User, second_user: User
    ):
        """Test that listing categories only returns own categories."""
        # Créer des catégories pour chaque utilisateur
        own_cat = Category(user_id=test_user.id, name="Own Category")
        other_cat = Category(user_id=second_user.id, name="Other Category")
        db_session.add_all([own_cat, other_cat])
        await db_session.commit()

        response = await client.get("/api/categories", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        # Doit voir seulement sa propre catégorie
        assert len(data) == 1
        assert data[0]["name"] == "Own Category"
