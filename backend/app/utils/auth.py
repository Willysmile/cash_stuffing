"""
Utilitaires d'authentification - JWT et hash de mots de passe
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
from jose import JWTError, jwt
from app.config import get_settings

settings = get_settings()


# === Hash des mots de passe ===

def hash_password(password: str) -> str:
    """
    Hash un mot de passe avec bcrypt
    
    Args:
        password: Mot de passe en clair
        
    Returns:
        Hash du mot de passe
    
    Note:
        Bcrypt limite les mots de passe à 72 bytes maximum
    """
    # Convertir en bytes et limiter à 72 bytes
    password_bytes = password.encode('utf-8')[:72]
    # Générer le hash avec bcrypt
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Retourner en string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie qu'un mot de passe correspond à son hash
    
    Args:
        plain_password: Mot de passe en clair
        hashed_password: Hash du mot de passe
        
    Returns:
        True si le mot de passe correspond, False sinon
    """
    password_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# === JWT Tokens ===

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un token JWT d'accès
    
    Args:
        data: Données à encoder dans le token (user_id, email, etc.)
        expires_delta: Durée de validité personnalisée (optionnel)
        
    Returns:
        Token JWT encodé
    """
    to_encode = data.copy()
    
    # Définir l'expiration
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({
        "exp": expire,
        "type": "access"
    })
    
    # Encoder le token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Crée un token JWT de rafraîchissement
    
    Args:
        data: Données à encoder dans le token (généralement user_id)
        
    Returns:
        Token JWT encodé
    """
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    Décode et vérifie un token JWT
    
    Args:
        token: Token JWT à décoder
        
    Returns:
        Payload du token si valide, None sinon
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def verify_token_type(payload: dict, expected_type: str) -> bool:
    """
    Vérifie que le token est du bon type (access ou refresh)
    
    Args:
        payload: Payload décodé du token
        expected_type: Type attendu ("access" ou "refresh")
        
    Returns:
        True si le type correspond, False sinon
    """
    token_type = payload.get("type")
    return token_type == expected_type
