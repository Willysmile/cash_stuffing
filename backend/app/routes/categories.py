"""
Routes API pour la gestion des catégories
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.database import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryRead,
    CategoryWithChildren
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/options", response_class=HTMLResponse)
async def get_categories_options(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retourne les options HTML pour le select des catégories"""
    query = select(Category).where(Category.user_id == current_user.id).order_by(Category.name)
    result = await db.execute(query)
    categories = result.scalars().all()
    
    html = '<option value="">Aucune</option>\n'
    for cat in categories:
        html += f'<option value="{cat.id}">{cat.name}</option>\n'
    
    return HTMLResponse(content=html)


@router.get("", response_model=List[CategoryRead])
async def get_categories(
    parent_id: Optional[int] = Query(None, description="Filtrer par catégorie parente (None = racines)"),
    search: Optional[str] = Query(None, description="Recherche par nom"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Liste toutes les catégories de l'utilisateur connecté
    
    Paramètres:
    - **parent_id**: Filtrer par parent (omis = toutes, null = racines uniquement)
    - **search**: Recherche partielle dans le nom de la catégorie
    
    Returns:
        Liste des catégories triées par sort_order
    """
    # Construction de la requête de base
    query = select(Category).where(Category.user_id == current_user.id)
    
    # Filtre parent_id
    if parent_id is not None:
        query = query.where(Category.parent_id == parent_id)
    
    # Filtre recherche
    if search:
        query = query.where(Category.name.ilike(f"%{search}%"))
    
    # Tri par sort_order puis nom
    query = query.order_by(Category.sort_order, Category.name)
    
    result = await db.execute(query)
    categories = result.scalars().all()
    
    return categories


@router.get("/tree", response_model=List[CategoryWithChildren])
async def get_categories_tree(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère l'arbre complet des catégories (avec sous-catégories imbriquées)
    
    Returns:
        Liste des catégories racines avec leurs enfants récursifs
    """
    # Récupérer toutes les catégories de l'utilisateur
    result = await db.execute(
        select(Category)
        .where(Category.user_id == current_user.id)
        .order_by(Category.sort_order, Category.name)
    )
    all_categories = result.scalars().all()
    
    # Construire l'arbre manuellement (sans relation SQLAlchemy)
    categories_by_id = {cat.id: cat for cat in all_categories}
    root_categories = [cat for cat in all_categories if cat.parent_id is None]
    
    # Fonction récursive pour construire les enfants
    def build_tree(category):
        children_models = [c for c in all_categories if c.parent_id == category.id]
        
        # Convertir en dict pour éviter les problèmes de lazy loading
        category_dict = {
            "id": category.id,
            "name": category.name,
            "parent_id": category.parent_id,
            "color": category.color,
            "icon": category.icon,
            "is_default": category.is_default,
            "sort_order": category.sort_order,
            "user_id": category.user_id,
            "created_at": category.created_at,
            "children": [build_tree(child) for child in children_models]
        }
        return category_dict
    
    return [build_tree(cat) for cat in root_categories]


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les détails d'une catégorie spécifique
    
    Paramètres:
    - **category_id**: ID de la catégorie
    
    Returns:
        Détails de la catégorie
    """
    result = await db.execute(
        select(Category).where(
            and_(
                Category.id == category_id,
                Category.user_id == current_user.id
            )
        )
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category {category_id} not found"
        )
    
    return category


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crée une nouvelle catégorie
    
    Paramètres:
    - **name**: Nom de la catégorie (requis)
    - **parent_id**: ID de la catégorie parente (optionnel, null = racine)
    - **color**: Couleur hex (ex: #FF5733)
    - **icon**: Icône (ex: 'shopping-cart', 'home')
    - **sort_order**: Ordre d'affichage (défaut: 0)
    
    Returns:
        Catégorie créée
    """
    # Vérifier que le parent existe et appartient à l'utilisateur si spécifié
    if category_data.parent_id is not None:
        parent_result = await db.execute(
            select(Category).where(
                and_(
                    Category.id == category_data.parent_id,
                    Category.user_id == current_user.id
                )
            )
        )
        parent = parent_result.scalar_one_or_none()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent category {category_data.parent_id} not found"
            )
    
    # Créer la catégorie
    new_category = Category(
        **category_data.model_dump(),
        user_id=current_user.id
    )
    
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    
    return new_category


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Met à jour une catégorie existante
    
    Paramètres:
    - **category_id**: ID de la catégorie à modifier
    - Champs modifiables: name, parent_id, color, icon, sort_order
    
    Returns:
        Catégorie mise à jour
    """
    # Récupérer la catégorie
    result = await db.execute(
        select(Category).where(
            and_(
                Category.id == category_id,
                Category.user_id == current_user.id
            )
        )
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category {category_id} not found"
        )
    
    # Vérifier que le parent existe si modifié
    if category_data.parent_id is not None:
        # Éviter les boucles infinies (une catégorie ne peut pas être son propre parent)
        if category_data.parent_id == category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A category cannot be its own parent"
            )
        
        parent_result = await db.execute(
            select(Category).where(
                and_(
                    Category.id == category_data.parent_id,
                    Category.user_id == current_user.id
                )
            )
        )
        parent = parent_result.scalar_one_or_none()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent category {category_data.parent_id} not found"
            )
    
    # Mettre à jour les champs
    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    await db.commit()
    await db.refresh(category)
    
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Supprime une catégorie
    
    Paramètres:
    - **category_id**: ID de la catégorie à supprimer
    
    Note:
    - La suppression échoue si la catégorie a des sous-catégories (intégrité)
    - La suppression échoue si la catégorie est utilisée par des enveloppes
    
    Returns:
        204 No Content si succès
    """
    # Récupérer la catégorie
    result = await db.execute(
        select(Category).where(
            and_(
                Category.id == category_id,
                Category.user_id == current_user.id
            )
        )
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category {category_id} not found"
        )
    
    # Vérifier s'il y a des sous-catégories
    children_result = await db.execute(
        select(Category).where(Category.parent_id == category_id)
    )
    children = children_result.scalars().all()
    
    if children:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category with {len(children)} subcategories. Delete or reassign them first."
        )
    
    # Vérifier s'il y a des enveloppes liées
    # Note: On ne peut pas importer Envelope ici (circular import)
    # La contrainte FK en base empêchera la suppression
    
    try:
        await db.delete(category)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category: {str(e)}"
        )
    
    return None
