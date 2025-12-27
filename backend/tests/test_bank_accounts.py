"""Tests for bank accounts routes."""

import pytest
from decimal import Decimal
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, BankAccount


class TestBankAccountCRUD:
    """Tests for bank account CRUD operations."""

    @pytest.mark.asyncio
    async def test_create_bank_account(self, client: AsyncClient, auth_headers: dict):
        """Test creating a new bank account."""
        response = await client.post(
            "/api/bank-accounts",
            headers=auth_headers,
            json={
                "name": "Compte Courant",
                "account_type": "checking",
                "initial_balance": 1500.00,
                "currency": "EUR"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Compte Courant"
        assert data["account_type"] == "checking"
        assert float(data["initial_balance"]) == 1500.00
        assert float(data["current_balance"]) == 1500.00  # Auto-initialisé
        assert data["currency"] == "EUR"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_bank_account_with_optional_fields(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test creating bank account with all optional fields."""
        response = await client.post(
            "/api/bank-accounts",
            headers=auth_headers,
            json={
                "name": "Livret A",
                "account_type": "savings",
                "initial_balance": 5000.00,
                "currency": "EUR",
                "color": "#00FF00",
                "icon": "piggy-bank"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["color"] == "#00FF00"
        assert data["icon"] == "piggy-bank"

    @pytest.mark.asyncio
    async def test_list_bank_accounts(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test listing all bank accounts."""
        # Créer quelques comptes
        accounts = [
            BankAccount(
                user_id=test_user.id,
                name="Compte Courant",
                account_type="checking",
                initial_balance=Decimal("1000.00"),
                current_balance=Decimal("1000.00"),
                currency="EUR"
            ),
            BankAccount(
                user_id=test_user.id,
                name="Livret A",
                account_type="savings",
                initial_balance=Decimal("5000.00"),
                current_balance=Decimal("5000.00"),
                currency="EUR"
            ),
        ]
        db_session.add_all(accounts)
        await db_session.commit()

        response = await client.get("/api/bank-accounts", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        # Vérifie le tri par nom
        assert data[0]["name"] == "Compte Courant"
        assert data[1]["name"] == "Livret A"

    @pytest.mark.asyncio
    async def test_get_bank_account_by_id(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test getting a specific bank account."""
        account = BankAccount(
            user_id=test_user.id,
            name="Test Account",
            account_type="checking",
            initial_balance=Decimal("2000.00"),
            current_balance=Decimal("2000.00"),
            currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)

        response = await client.get(f"/api/bank-accounts/{account.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == account.id
        assert data["name"] == "Test Account"

    @pytest.mark.asyncio
    async def test_get_bank_account_not_found(self, client: AsyncClient, auth_headers: dict):
        """Test getting non-existent account returns 404."""
        response = await client.get("/api/bank-accounts/9999", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_bank_account(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test updating a bank account."""
        account = BankAccount(
            user_id=test_user.id,
            name="Old Name",
            account_type="checking",
            initial_balance=Decimal("1000.00"),
            current_balance=Decimal("1000.00"),
            currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)

        response = await client.put(
            f"/api/bank-accounts/{account.id}",
            headers=auth_headers,
            json={
                "name": "New Name",
                "account_type": "savings"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"
        assert data["account_type"] == "savings"
        # Les soldes ne doivent pas changer via PUT
        assert float(data["initial_balance"]) == 1000.00
        assert float(data["current_balance"]) == 1000.00

    @pytest.mark.asyncio
    async def test_delete_bank_account(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test deleting a bank account."""
        account = BankAccount(
            user_id=test_user.id,
            name="To Delete",
            account_type="checking",
            initial_balance=Decimal("100.00"),
            current_balance=Decimal("100.00"),
            currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)

        response = await client.delete(f"/api/bank-accounts/{account.id}", headers=auth_headers)
        assert response.status_code == 204

        # Vérifier suppression
        get_response = await client.get(
            f"/api/bank-accounts/{account.id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404


class TestBankAccountAdjustBalance:
    """Tests for balance adjustment endpoint."""

    @pytest.mark.asyncio
    async def test_adjust_balance_success(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test adjusting account balance."""
        account = BankAccount(
            user_id=test_user.id,
            name="Test Account",
            account_type="checking",
            initial_balance=Decimal("1000.00"),
            current_balance=Decimal("1000.00"),
            currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)

        response = await client.post(
            f"/api/bank-accounts/{account.id}/adjust",
            headers=auth_headers,
            json={
                "new_balance": 1523.45,
                "reason": "Ajustement après relevé bancaire"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert float(data["current_balance"]) == 1523.45
        # initial_balance ne change jamais
        assert float(data["initial_balance"]) == 1000.00

    @pytest.mark.asyncio
    async def test_adjust_balance_without_reason(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test adjusting balance without reason (optional)."""
        account = BankAccount(
            user_id=test_user.id,
            name="Test Account",
            account_type="checking",
            initial_balance=Decimal("1000.00"),
            current_balance=Decimal("1000.00"),
            currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)

        response = await client.post(
            f"/api/bank-accounts/{account.id}/adjust",
            headers=auth_headers,
            json={"new_balance": 900.00}
        )
        assert response.status_code == 200
        data = response.json()
        assert float(data["current_balance"]) == 900.00

    @pytest.mark.asyncio
    async def test_adjust_balance_negative(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test adjusting balance to negative value (allowed for overdraft)."""
        account = BankAccount(
            user_id=test_user.id,
            name="Test Account",
            account_type="checking",
            initial_balance=Decimal("1000.00"),
            current_balance=Decimal("1000.00"),
            currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)

        response = await client.post(
            f"/api/bank-accounts/{account.id}/adjust",
            headers=auth_headers,
            json={
                "new_balance": -150.00,
                "reason": "Découvert autorisé"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert float(data["current_balance"]) == -150.00


class TestBankAccountFilters:
    """Tests for bank account filtering."""

    @pytest.mark.asyncio
    async def test_filter_by_account_type(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test filtering by account type."""
        accounts = [
            BankAccount(
                user_id=test_user.id, name="Checking", account_type="checking",
                initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
            ),
            BankAccount(
                user_id=test_user.id, name="Savings", account_type="savings",
                initial_balance=Decimal("5000"), current_balance=Decimal("5000"), currency="EUR"
            ),
        ]
        db_session.add_all(accounts)
        await db_session.commit()

        response = await client.get(
            "/api/bank-accounts?account_type=savings",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["account_type"] == "savings"

    @pytest.mark.asyncio
    async def test_filter_by_currency(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
    ):
        """Test filtering by currency."""
        accounts = [
            BankAccount(
                user_id=test_user.id, name="EUR Account", account_type="checking",
                initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
            ),
            BankAccount(
                user_id=test_user.id, name="USD Account", account_type="checking",
                initial_balance=Decimal("500"), current_balance=Decimal("500"), currency="USD"
            ),
        ]
        db_session.add_all(accounts)
        await db_session.commit()

        response = await client.get(
            "/api/bank-accounts?currency=USD",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["currency"] == "USD"


class TestBankAccountIsolation:
    """Tests for user isolation."""

    @pytest.mark.asyncio
    async def test_cannot_access_other_user_account(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, second_user: User
    ):
        """Test that users cannot access other users' accounts."""
        other_account = BankAccount(
            user_id=second_user.id,
            name="Other User Account",
            account_type="checking",
            initial_balance=Decimal("1000"),
            current_balance=Decimal("1000"),
            currency="EUR"
        )
        db_session.add(other_account)
        await db_session.commit()
        await db_session.refresh(other_account)

        response = await client.get(
            f"/api/bank-accounts/{other_account.id}",
            headers=auth_headers
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_cannot_adjust_other_user_balance(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, second_user: User
    ):
        """Test that users cannot adjust other users' account balances."""
        other_account = BankAccount(
            user_id=second_user.id,
            name="Other User Account",
            account_type="checking",
            initial_balance=Decimal("1000"),
            current_balance=Decimal("1000"),
            currency="EUR"
        )
        db_session.add(other_account)
        await db_session.commit()
        await db_session.refresh(other_account)

        response = await client.post(
            f"/api/bank-accounts/{other_account.id}/adjust",
            headers=auth_headers,
            json={"new_balance": 5000.00}
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_only_own_accounts(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User, second_user: User
    ):
        """Test that listing accounts only returns own accounts."""
        own_account = BankAccount(
            user_id=test_user.id, name="Own Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        other_account = BankAccount(
            user_id=second_user.id, name="Other Account", account_type="checking",
            initial_balance=Decimal("2000"), current_balance=Decimal("2000"), currency="EUR"
        )
        db_session.add_all([own_account, other_account])
        await db_session.commit()

        response = await client.get("/api/bank-accounts", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Own Account"
