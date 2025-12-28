"""
Script de seeding pour créer des données de test
"""
import asyncio
from datetime import date, timedelta
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.user import User
from app.models.bank_account import BankAccount
from app.models.category import Category
from app.models.envelope import Envelope
from app.models.payee import Payee
from app.models.transaction import Transaction


async def seed_data():
    """Crée des données de test complètes"""
    async with AsyncSessionLocal() as session:
        # Récupérer ou créer l'utilisateur test
        result = await session.execute(select(User).where(User.email == "test@test.com"))
        user = result.scalar_one_or_none()
        
        if user is None:
            from app.utils.auth import hash_password
            user = User(
                email="test@test.com",
                password_hash=hash_password("test"),
                is_active=True
            )
            session.add(user)
            await session.flush()
        
        print(f"✓ Utilisateur: {user.email}")
        
        # 1. COMPTES BANCAIRES
        print("\n📊 Création des comptes bancaires...")
        compte_courant = BankAccount(
            user_id=user.id,
            name="Compte Courant",
            account_type="checking",
            initial_balance=2500.00,
            current_balance=2500.00,
            color="#3273dc",
            icon="wallet"
        )
        session.add(compte_courant)
        
        livret_a = BankAccount(
            user_id=user.id,
            name="Livret A",
            account_type="savings",
            initial_balance=8000.00,
            current_balance=8000.00,
            color="#48c774",
            icon="piggy-bank"
        )
        session.add(livret_a)
        
        pel = BankAccount(
            user_id=user.id,
            name="PEL",
            account_type="savings",
            initial_balance=15000.00,
            current_balance=15000.00,
            color="#ffdd57",
            icon="chart-line"
        )
        session.add(pel)
        
        await session.flush()
        print(f"  ✓ {compte_courant.name} - {compte_courant.current_balance}€")
        print(f"  ✓ {livret_a.name} - {livret_a.current_balance}€")
        print(f"  ✓ {pel.name} - {pel.current_balance}€")
        
        # 2. CATÉGORIES
        print("\n📁 Création des catégories...")
        categories_data = [
            {"name": "Salaire", "color": "#48c774", "icon": "money-bill-wave"},
            {"name": "Alimentation", "color": "#f14668", "icon": "shopping-cart"},
            {"name": "Transport", "color": "#3273dc", "icon": "car"},
            {"name": "Loisirs", "color": "#ffdd57", "icon": "film"},
            {"name": "Logement", "color": "#ff3860", "icon": "home"},
            {"name": "Santé", "color": "#00d1b2", "icon": "heartbeat"},
            {"name": "Épargne", "color": "#209cee", "icon": "piggy-bank"},
            {"name": "Autres revenus", "color": "#48c774", "icon": "plus"},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat = Category(
                user_id=user.id,
                name=cat_data["name"],
                color=cat_data.get("color"),
                icon=cat_data.get("icon")
            )
            session.add(cat)
            await session.flush()
            categories[cat_data["name"]] = cat
            print(f"  ✓ {cat.name}")
        
        # 3. ENVELOPPES
        print("\n💰 Création des enveloppes...")
        env_courses = Envelope(
            user_id=user.id,
            bank_account_id=compte_courant.id,
            name="Courses du mois",
            category_id=categories["Alimentation"].id,
            target_amount=400.00,
            current_balance=185.20,
            description="Budget courses alimentaires mensuel",
            color="#f14668",
            icon="shopping-basket"
        )
        session.add(env_courses)
        
        env_essence = Envelope(
            user_id=user.id,
            bank_account_id=compte_courant.id,
            name="Essence & Carburant",
            category_id=categories["Transport"].id,
            target_amount=150.00,
            current_balance=105.80,
            description="Budget carburant mensuel",
            color="#3273dc",
            icon="gas-pump"
        )
        session.add(env_essence)
        
        env_loisirs = Envelope(
            user_id=user.id,
            bank_account_id=compte_courant.id,
            name="Sorties & Loisirs",
            category_id=categories["Loisirs"].id,
            target_amount=200.00,
            current_balance=56.98,
            description="Budget sorties, restaurants et divertissements",
            color="#ffdd57",
            icon="theater-masks"
        )
        session.add(env_loisirs)
        
        await session.flush()
        print(f"  ✓ {env_courses.name} - Objectif: {env_courses.target_amount}€")
        print(f"  ✓ {env_essence.name} - Objectif: {env_essence.target_amount}€")
        print(f"  ✓ {env_loisirs.name} - Objectif: {env_loisirs.target_amount}€")
        
        # 4. BÉNÉFICIAIRES
        print("\n👥 Création des bénéficiaires...")
        payees_data = [
            "Auchan",
            "Carrefour",
            "Leclerc",
            "Total",
            "Shell",
            "Netflix",
            "Amazon",
            "EDF",
            "Employeur"
        ]
        
        payees = {}
        for payee_name in payees_data:
            payee = Payee(
                user_id=user.id,
                name=payee_name
            )
            session.add(payee)
            await session.flush()
            payees[payee_name] = payee
            print(f"  ✓ {payee.name}")
        
        # 5. TRANSACTIONS
        print("\n💳 Création des transactions...")
        today = date.today()
        
        transactions_data = [
            # Salaire du mois
            {
                "date": today - timedelta(days=25),
                "type": "income",
                "amount": 2500.00,
                "account": compte_courant,
                "category": categories["Salaire"],
                "payee": payees["Employeur"],
                "description": "Salaire décembre"
            },
            # Courses
            {
                "date": today - timedelta(days=20),
                "type": "expense",
                "amount": 89.50,
                "account": compte_courant,
                "category": categories["Alimentation"],
                "payee": payees["Auchan"],
                "description": "Courses semaine"
            },
            {
                "date": today - timedelta(days=15),
                "type": "expense",
                "amount": 125.30,
                "account": compte_courant,
                "category": categories["Alimentation"],
                "payee": payees["Carrefour"],
                "description": "Courses + produits ménagers"
            },
            {
                "date": today - timedelta(days=7),
                "type": "expense",
                "amount": 67.80,
                "account": compte_courant,
                "category": categories["Alimentation"],
                "payee": payees["Leclerc"],
                "description": "Courses semaine"
            },
            # Transport
            {
                "date": today - timedelta(days=18),
                "type": "expense",
                "amount": 65.00,
                "account": compte_courant,
                "category": categories["Transport"],
                "payee": payees["Total"],
                "description": "Plein essence"
            },
            {
                "date": today - timedelta(days=10),
                "type": "expense",
                "amount": 58.50,
                "account": compte_courant,
                "category": categories["Transport"],
                "payee": payees["Shell"],
                "description": "Plein essence"
            },
            # Loisirs
            {
                "date": today - timedelta(days=22),
                "type": "expense",
                "amount": 13.99,
                "account": compte_courant,
                "category": categories["Loisirs"],
                "payee": payees["Netflix"],
                "description": "Abonnement Netflix"
            },
            {
                "date": today - timedelta(days=12),
                "type": "expense",
                "amount": 45.90,
                "account": compte_courant,
                "category": categories["Loisirs"],
                "payee": payees["Amazon"],
                "description": "Livre + film"
            },
            # Logement
            {
                "date": today - timedelta(days=23),
                "type": "expense",
                "amount": 850.00,
                "account": compte_courant,
                "category": categories["Logement"],
                "description": "Loyer décembre"
            },
            {
                "date": today - timedelta(days=16),
                "type": "expense",
                "amount": 78.20,
                "account": compte_courant,
                "category": categories["Logement"],
                "payee": payees["EDF"],
                "description": "Facture électricité"
            },
            # Épargne
            {
                "date": today - timedelta(days=24),
                "type": "expense",
                "amount": 500.00,
                "account": compte_courant,
                "category": categories["Épargne"],
                "description": "Virement épargne"
            },
            {
                "date": today - timedelta(days=24),
                "type": "income",
                "amount": 500.00,
                "account": livret_a,
                "category": categories["Épargne"],
                "description": "Virement depuis compte courant"
            },
            # Transactions récentes
            {
                "date": today - timedelta(days=3),
                "type": "expense",
                "amount": 32.50,
                "account": compte_courant,
                "category": categories["Alimentation"],
                "payee": payees["Auchan"],
                "description": "Courses express"
            },
            {
                "date": today - timedelta(days=1),
                "type": "expense",
                "amount": 25.00,
                "account": compte_courant,
                "category": categories["Loisirs"],
                "description": "Cinéma"
            },
        ]
        
        for trans_data in transactions_data:
            trans = Transaction(
                user_id=user.id,
                bank_account_id=trans_data["account"].id,
                category_id=trans_data["category"].id,
                payee_id=trans_data.get("payee").id if trans_data.get("payee") else None,
                transaction_type=trans_data["type"],
                amount=trans_data["amount"],
                date=trans_data["date"],
                description=trans_data.get("description")
            )
            session.add(trans)
            print(f"  ✓ {trans.date} - {trans.description} - {trans.amount}€")
        
        await session.commit()
        
        print("\n" + "="*60)
        print("✅ SEEDING TERMINÉ AVEC SUCCÈS!")
        print("="*60)
        print(f"📊 Comptes bancaires: 3")
        print(f"📁 Catégories: {len(categories)}")
        print(f"💰 Enveloppes: 3")
        print(f"👥 Bénéficiaires: {len(payees)}")
        print(f"💳 Transactions: {len(transactions_data)}")
        print("="*60)


if __name__ == "__main__":
    print("\n🌱 Démarrage du seeding de la base de données...\n")
    asyncio.run(seed_data())
