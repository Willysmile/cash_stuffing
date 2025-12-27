"""
Tests pour les routes API des transactions
"""
import pytest
from decimal import Decimal
from datetime import date, timedelta
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.bank_account import BankAccount
from app.models.category import Category
from app.models.envelope import Envelope
from app.models.transaction import Transaction


class TestTransactionCRUD:
    """Tests CRUD pour les transactions."""

    @pytest.mark.asyncio
    async def test_create_transaction(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test creating a new transaction."""
        # Créer les dépendances
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        category = Category(
            user_id=test_user.id, name="Food"
        )
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)

        response = await client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "bank_account_id": account.id,
                "category_id": category.id,
                "amount": 50.00,
                "transaction_type": "expense",
                "date": str(date.today()),
                "description": "Groceries",
                "payee": "Supermarket",
                "priority": "vital"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["amount"] == "50.00"
        assert data["transaction_type"] == "expense"
        assert data["description"] == "Groceries"
        assert data["payee"] == "Supermarket"
        assert data["priority"] == "vital"

    @pytest.mark.asyncio
    async def test_create_transaction_with_envelope(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test creating a transaction with an envelope."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        category = Category(
            user_id=test_user.id, name="Food"
        )
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        
        envelope = Envelope(
            user_id=test_user.id, name="Groceries", bank_account_id=account.id,
            monthly_budget=Decimal("300"), current_balance=Decimal("200")
        )
        db_session.add(envelope)
        await db_session.commit()
        await db_session.refresh(envelope)

        response = await client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "bank_account_id": account.id,
                "envelope_id": envelope.id,
                "category_id": category.id,
                "amount": 25.00,
                "transaction_type": "expense",
                "date": str(date.today())
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["envelope_id"] == envelope.id

    @pytest.mark.asyncio
    async def test_create_transaction_invalid_account(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test creating a transaction with invalid bank account."""
        category = Category(
            user_id=test_user.id, name="Food"
        )
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)

        response = await client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "bank_account_id": 99999,
                "category_id": category.id,
                "amount": 50.00,
                "transaction_type": "expense",
                "date": str(date.today())
            }
        )
        assert response.status_code == 404
        assert "account" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_create_transaction_invalid_category(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test creating a transaction with invalid category."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)

        response = await client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "bank_account_id": account.id,
                "category_id": 99999,
                "amount": 50.00,
                "transaction_type": "expense",
                "date": str(date.today())
            }
        )
        assert response.status_code == 404
        assert "category" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_list_transactions(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test listing all transactions."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        category = Category(
            user_id=test_user.id, name="Food"
        )
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        
        transaction1 = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("50"), transaction_type="expense", date=date.today()
        )
        transaction2 = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("100"), transaction_type="income", date=date.today()
        )
        db_session.add_all([transaction1, transaction2])
        await db_session.commit()

        response = await client.get("/api/transactions", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    @pytest.mark.asyncio
    async def test_get_transaction_by_id(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test getting a transaction by ID."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        category = Category(
            user_id=test_user.id, name="Food"
        )
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        
        transaction = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("75"), transaction_type="expense", date=date.today(),
            description="Test transaction"
        )
        db_session.add(transaction)
        await db_session.commit()
        await db_session.refresh(transaction)

        response = await client.get(f"/api/transactions/{transaction.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == transaction.id
        assert data["description"] == "Test transaction"

    @pytest.mark.asyncio
    async def test_get_transaction_not_found(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test getting a non-existent transaction."""
        response = await client.get("/api/transactions/99999", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_transaction(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test updating a transaction."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        category = Category(
            user_id=test_user.id, name="Food"
        )
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        
        transaction = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("50"), transaction_type="expense", date=date.today(),
            description="Original"
        )
        db_session.add(transaction)
        await db_session.commit()
        await db_session.refresh(transaction)

        response = await client.put(
            f"/api/transactions/{transaction.id}",
            headers=auth_headers,
            json={
                "description": "Updated",
                "amount": 75.00,
                "payee": "New Payee"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Updated"
        assert data["amount"] == "75.00"
        assert data["payee"] == "New Payee"

    @pytest.mark.asyncio
    async def test_delete_transaction(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test deleting a transaction."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        category = Category(
            user_id=test_user.id, name="Food"
        )
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        
        transaction = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("50"), transaction_type="expense", date=date.today()
        )
        db_session.add(transaction)
        await db_session.commit()
        await db_session.refresh(transaction)

        response = await client.delete(f"/api/transactions/{transaction.id}", headers=auth_headers)
        assert response.status_code == 204

        # Vérifier suppression
        get_response = await client.get(f"/api/transactions/{transaction.id}", headers=auth_headers)
        assert get_response.status_code == 404


class TestTransactionFilters:
    """Tests pour les filtres de transactions."""

    @pytest.mark.asyncio
    async def test_filter_by_type(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test filtering transactions by type."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        category = Category(
            user_id=test_user.id, name="Food"
        )
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        
        expense = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("50"), transaction_type="expense", date=date.today()
        )
        income = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("100"), transaction_type="income", date=date.today()
        )
        db_session.add_all([expense, income])
        await db_session.commit()

        response = await client.get(
            "/api/transactions?transaction_type=expense",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["transaction_type"] == "expense"

    @pytest.mark.asyncio
    async def test_filter_by_date_range(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test filtering transactions by date range."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        category = Category(
            user_id=test_user.id, name="Food"
        )
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        
        today = date.today()
        old_transaction = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("50"), transaction_type="expense", date=today - timedelta(days=10)
        )
        recent_transaction = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("75"), transaction_type="expense", date=today
        )
        db_session.add_all([old_transaction, recent_transaction])
        await db_session.commit()

        response = await client.get(
            f"/api/transactions?date_from={today - timedelta(days=5)}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["amount"] in ["75.00", "75"]

    @pytest.mark.asyncio
    async def test_filter_by_amount_range(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test filtering transactions by amount range."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        category = Category(
            user_id=test_user.id, name="Food"
        )
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        
        small = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("10"), transaction_type="expense", date=date.today()
        )
        medium = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("50"), transaction_type="expense", date=date.today()
        )
        large = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("200"), transaction_type="expense", date=date.today()
        )
        db_session.add_all([small, medium, large])
        await db_session.commit()

        response = await client.get(
            "/api/transactions?min_amount=25&max_amount=100",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["amount"] in ["50.00", "50"]

    @pytest.mark.asyncio
    async def test_search_by_text(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test searching transactions by description/payee."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        category = Category(
            user_id=test_user.id, name="Food"
        )
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        
        t1 = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("50"), transaction_type="expense", date=date.today(),
            description="Groceries at supermarket"
        )
        t2 = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("30"), transaction_type="expense", date=date.today(),
            payee="Restaurant"
        )
        db_session.add_all([t1, t2])
        await db_session.commit()

        response = await client.get(
            "/api/transactions?search=supermarket",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "supermarket" in data[0]["description"].lower()


class TestTransactionStats:
    """Tests pour les statistiques de transactions."""

    @pytest.mark.asyncio
    async def test_transaction_summary(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User
    ):
        """Test getting transaction summary."""
        account = BankAccount(
            user_id=test_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        category = Category(
            user_id=test_user.id, name="Food"
        )
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        
        expense1 = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("50"), transaction_type="expense", date=date.today()
        )
        expense2 = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("30"), transaction_type="expense", date=date.today()
        )
        income = Transaction(
            user_id=test_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("200"), transaction_type="income", date=date.today()
        )
        db_session.add_all([expense1, expense2, income])
        await db_session.commit()

        response = await client.get("/api/transactions/stats/summary", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["total_income"] == 200.0
        assert data["total_expense"] == 80.0
        assert data["balance"] == 120.0
        assert data["transaction_count"] == 3


class TestTransactionIsolation:
    """Tests pour l'isolation entre utilisateurs."""

    @pytest.mark.asyncio
    async def test_cannot_access_other_user_transaction(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, second_user: User
    ):
        """Test that users cannot access other users' transactions."""
        account = BankAccount(
            user_id=second_user.id, name="Account", account_type="checking",
            initial_balance=Decimal("1000"), current_balance=Decimal("1000"), currency="EUR"
        )
        db_session.add(account)
        await db_session.commit()
        await db_session.refresh(account)
        
        category = Category(
            user_id=second_user.id, name="Food"
        )
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        
        transaction = Transaction(
            user_id=second_user.id, bank_account_id=account.id, category_id=category.id,
            amount=Decimal("50"), transaction_type="expense", date=date.today()
        )
        db_session.add(transaction)
        await db_session.commit()
        await db_session.refresh(transaction)

        response = await client.get(f"/api/transactions/{transaction.id}", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_only_own_transactions(
        self, client: AsyncClient, auth_headers: dict,
        db_session: AsyncSession, test_user: User, second_user: User
    ):
        """Test that listing transactions only returns own transactions."""
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
        
        category1 = Category(
            user_id=test_user.id, name="Food"
        )
        category2 = Category(
            user_id=second_user.id, name="Food"
        )
        db_session.add_all([category1, category2])
        await db_session.commit()
        await db_session.refresh(category1)
        await db_session.refresh(category2)
        
        own_transaction = Transaction(
            user_id=test_user.id, bank_account_id=account1.id, category_id=category1.id,
            amount=Decimal("50"), transaction_type="expense", date=date.today()
        )
        other_transaction = Transaction(
            user_id=second_user.id, bank_account_id=account2.id, category_id=category2.id,
            amount=Decimal("100"), transaction_type="expense", date=date.today()
        )
        db_session.add_all([own_transaction, other_transaction])
        await db_session.commit()

        response = await client.get("/api/transactions", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["amount"] in ["50.00", "50"]
