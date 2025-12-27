"""Tests for envelopes routes."""

import pytest
from decimal import Decimal
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Envelope, BankAccount, Category


class TestEnvelopeCRUD:
    """Tests for envelope CRUD operations."""

    @pytest.mark.asyncio
    async def test_create_envelope(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test creating a new envelope."""
        # Créer un compte bancaire
        account = BankAccount(
            user_id=test_user.id, name="Test Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)

        response = await client.post(
            "/api/envelopes",
            headers=auth_headers,
            json={
                "name": "Alimentation",
                "bank_account_id": account.id,
                "monthly_budget": 300.00
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Alimentation"
        assert data["bank_account_id"] == account.id
        assert float(data["monthly_budget"]) == 300.00
        assert float(data["current_balance"]) == 0.00

    @pytest.mark.asyncio
    async def test_create_envelope_with_category(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test creating envelope with category."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        category = Category(user_id=test_user.id, name="Food")
        db_session.add_all([account, category])
        await db_session.commit()
        await db_session.refresh(account)
        await db_session.refresh(category)

        response = await client.post(
            "/api/envelopes",
            headers=auth_headers,
            json={
                "name": "Groceries",
                "bank_account_id": account.id,
                "category_id": category.id,
                "monthly_budget": 250.00,
                "color": "#FF5733"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["category_id"] == category.id
        assert data["color"] == "#FF5733"

    @pytest.mark.asyncio
    async def test_create_envelope_invalid_account(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test creating envelope with non-existent account fails."""
        response = await client.post(
            "/api/envelopes",
            headers=auth_headers,
            json={
                "name": "Test",
                "bank_account_id": 9999,
                "monthly_budget": 100.00
            }
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_envelopes(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test listing all envelopes."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)

        envelopes = [
            Envelope(
                user_id=test_user.id, name="Alimentation", bank_account_id=account.id,
                monthly_budget=Decimal("300"), current_balance=Decimal("0")
            ),
            Envelope(
                user_id=test_user.id, name="Transport", bank_account_id=account.id,
                monthly_budget=Decimal("150"), current_balance=Decimal("0")
            ),
        ]
        db_session.add_all(envelopes)
        await db_session.commit()

        response = await client.get("/api/envelopes", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        # Tri par nom
        assert data[0]["name"] == "Alimentation"
        assert data[1]["name"] == "Transport"

    @pytest.mark.asyncio
    async def test_get_envelope_by_id(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test getting a specific envelope."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        envelope = Envelope(
            user_id=test_user.id, name="Loisirs", bank_account_id=account.id,
            monthly_budget=Decimal("200"), current_balance=Decimal("50")
        )
        db_session.add(envelope)
        await db_session.commit()
        await db_session.refresh(envelope)

        response = await client.get(f"/api/envelopes/{envelope.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == envelope.id
        assert data["name"] == "Loisirs"
        assert float(data["current_balance"]) == 50.00

    @pytest.mark.asyncio
    async def test_get_envelope_not_found(self, client: AsyncClient, auth_headers: dict):
        """Test getting non-existent envelope returns 404."""
        response = await client.get("/api/envelopes/9999", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_envelope(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test updating an envelope."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        envelope = Envelope(
            user_id=test_user.id, name="Old Name", bank_account_id=account.id,
            monthly_budget=Decimal("100"), current_balance=Decimal("0")
        )
        db_session.add(envelope)
        await db_session.commit()
        await db_session.refresh(envelope)

        response = await client.put(
            f"/api/envelopes/{envelope.id}",
            headers=auth_headers,
            json={
                "name": "New Name",
                "monthly_budget": 200.00,
                "color": "#00FF00"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"
        assert float(data["monthly_budget"]) == 200.00
        assert data["color"] == "#00FF00"

    @pytest.mark.asyncio
    async def test_delete_envelope(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test deleting an envelope."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        envelope = Envelope(
            user_id=test_user.id, name="To Delete", bank_account_id=account.id,
            monthly_budget=Decimal("100"), current_balance=Decimal("0")
        )
        db_session.add(envelope)
        await db_session.commit()
        await db_session.refresh(envelope)

        response = await client.delete(f"/api/envelopes/{envelope.id}", headers=auth_headers)
        assert response.status_code == 204

        # Vérifier suppression
        get_response = await client.get(f"/api/envelopes/{envelope.id}", headers=auth_headers)
        assert get_response.status_code == 404


class TestEnvelopeReallocation:
    """Tests for envelope fund reallocation."""

    @pytest.mark.asyncio
    async def test_reallocate_funds_success(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test successful fund reallocation between envelopes."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        envelope1 = Envelope(
            user_id=test_user.id, name="Source", bank_account_id=account.id,
            monthly_budget=Decimal("300"), current_balance=Decimal("200")
        )
        envelope2 = Envelope(
            user_id=test_user.id, name="Destination", bank_account_id=account.id,
            monthly_budget=Decimal("100"), current_balance=Decimal("50")
        )
        db_session.add_all([envelope1, envelope2])
        await db_session.commit()
        await db_session.refresh(envelope1)
        await db_session.refresh(envelope2)

        response = await client.post(
            f"/api/envelopes/{envelope1.id}/reallocate",
            headers=auth_headers,
            json={
                "from_envelope_id": envelope1.id,
                "to_envelope_id": envelope2.id,
                "amount": 100.00,
                "description": "Réallocation test"
            }
        )
        assert response.status_code == 200
        data = response.json()
        # L'enveloppe source doit avoir 100 de moins
        assert float(data["current_balance"]) == 100.00

        # Vérifier l'enveloppe destination
        dest_response = await client.get(f"/api/envelopes/{envelope2.id}", headers=auth_headers)
        dest_data = dest_response.json()
        assert float(dest_data["current_balance"]) == 150.00

    @pytest.mark.asyncio
    async def test_reallocate_insufficient_funds(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test reallocation fails with insufficient funds."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        envelope1 = Envelope(
            user_id=test_user.id, name="Source", bank_account_id=account.id,
            monthly_budget=Decimal("100"), current_balance=Decimal("50")
        )
        envelope2 = Envelope(
            user_id=test_user.id, name="Dest", bank_account_id=account.id,
            monthly_budget=Decimal("100"), current_balance=Decimal("0")
        )
        db_session.add_all([envelope1, envelope2])
        await db_session.commit()
        await db_session.refresh(envelope1)
        await db_session.refresh(envelope2)

        response = await client.post(
            f"/api/envelopes/{envelope1.id}/reallocate",
            headers=auth_headers,
            json={
                "from_envelope_id": envelope1.id,
                "to_envelope_id": envelope2.id,
                "amount": 100.00  # Plus que disponible
            }
        )
        assert response.status_code == 400
        assert "insufficient" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_reallocate_same_envelope(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test reallocation fails with same source and destination."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        envelope = Envelope(
            user_id=test_user.id, name="Test", bank_account_id=account.id,
            monthly_budget=Decimal("100"), current_balance=Decimal("50")
        )
        db_session.add(envelope)
        await db_session.commit()
        await db_session.refresh(envelope)
        
        db_session.add(envelope)
        await db_session.commit()
        await db_session.refresh(envelope)

        response = await client.post(
            f"/api/envelopes/{envelope.id}/reallocate",
            headers=auth_headers,
            json={
                "from_envelope_id": envelope.id,
                "to_envelope_id": envelope.id,
                "amount": 10.00
            }
        )
        assert response.status_code == 400
        assert "different" in response.json()["detail"].lower()


class TestEnvelopeFilters:
    """Tests for envelope filtering."""

    @pytest.mark.asyncio
    async def test_filter_by_bank_account(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test filtering envelopes by bank account."""
        account1 = BankAccount(
            user_id=test_user.id, name="Account 1", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        account2 = BankAccount(
            user_id=test_user.id, name="Account 2", account_type="savings",
            initial_balance=Decimal("5000"), current_balance=Decimal("5000"), currency="EUR"
        )
        db_session.add_all([account1, account2])
        await db_session.commit()
        await db_session.refresh(account1)
        await db_session.refresh(account2)

        envelopes = [
            Envelope(
                user_id=test_user.id, name="Env1", bank_account_id=account1.id,
                monthly_budget=Decimal("100"), current_balance=Decimal("0")
            ),
            Envelope(
                user_id=test_user.id, name="Env2", bank_account_id=account2.id,
                monthly_budget=Decimal("200"), current_balance=Decimal("0")
            ),
        ]
        db_session.add_all(envelopes)
        await db_session.commit()

        response = await client.get(
            f"/api/envelopes?bank_account_id={account1.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["bank_account_id"] == account1.id

    @pytest.mark.asyncio
    async def test_filter_by_active_status(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test filtering by active status."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)

        envelopes = [
            Envelope(
                user_id=test_user.id, name="Active", bank_account_id=account.id,
                monthly_budget=Decimal("100"), current_balance=Decimal("0"), is_active=True
            ),
            Envelope(
                user_id=test_user.id, name="Inactive", bank_account_id=account.id,
                monthly_budget=Decimal("100"), current_balance=Decimal("0"), is_active=False
            ),
        ]
        db_session.add_all(envelopes)
        await db_session.commit()

        response = await client.get(
            "/api/envelopes?is_active=true",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["is_active"] is True


class TestEnvelopeIsolation:
    """Tests for user isolation."""

    @pytest.mark.asyncio
    async def test_cannot_access_other_user_envelope(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, second_user: User
    ):
        """Test that users cannot access other users' envelopes."""
        account = BankAccount(
            user_id=second_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        envelope = Envelope(
            user_id=second_user.id, name="Other Envelope", bank_account_id=account.id,
            monthly_budget=Decimal("100"), current_balance=Decimal("0")
        )
        db_session.add(envelope)
        await db_session.commit()
        await db_session.refresh(envelope)

        response = await client.get(f"/api/envelopes/{envelope.id}", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_only_own_envelopes(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User, second_user: User
    ):
        """Test that listing envelopes only returns own envelopes."""
        account1 = BankAccount(
            user_id=test_user.id, name="My Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        account2 = BankAccount(
            user_id=second_user.id, name="Other Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add_all([account1, account2])
        await db_session.commit()
        await db_session.refresh(account1)
        await db_session.refresh(account2)
        
        own_envelope = Envelope(
            user_id=test_user.id, name="My Envelope", bank_account_id=account1.id,
            monthly_budget=Decimal("100"), current_balance=Decimal("0")
        )
        other_envelope = Envelope(
            user_id=second_user.id, name="Other Envelope", bank_account_id=account2.id,
            monthly_budget=Decimal("100"), current_balance=Decimal("0")
        )
        db_session.add_all([own_envelope, other_envelope])
        await db_session.commit()

        response = await client.get("/api/envelopes", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "My Envelope"
