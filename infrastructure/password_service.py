from werkzeug.security import generate_password_hash, check_password_hash
from domain.interfaces import IPasswordHasher


class BcryptPasswordHasher(IPasswordHasher):
    """Implementação concreta do hasher de senhas usando Werkzeug (Bcrypt)"""
    
    def hash_password(self, password: str) -> str:
        """Gera hash da senha usando bcrypt"""
        return generate_password_hash(password, method='pbkdf2:sha256')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica se a senha confere com o hash"""
        return check_password_hash(hashed_password, password) 