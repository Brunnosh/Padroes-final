from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from .entities import Task, User, Priority, TaskStatus


class ITaskRepository(ABC):
    """Interface para repositório de tarefas"""
    
    @abstractmethod
    def save(self, task: Task) -> Task:
        """Salva uma tarefa"""
        pass
    
    @abstractmethod
    def find_by_id(self, task_id: int) -> Optional[Task]:
        """Busca uma tarefa por ID"""
        pass
    
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Task]:
        """Busca todas as tarefas de um usuário"""
        pass
    
    @abstractmethod
    def find_by_status(self, user_id: int, status: TaskStatus) -> List[Task]:
        """Busca tarefas por status"""
        pass
    
    @abstractmethod
    def find_by_priority(self, user_id: int, priority: Priority) -> List[Task]:
        """Busca tarefas por prioridade"""
        pass
    
    @abstractmethod
    def find_by_due_date(self, user_id: int, due_date: date) -> List[Task]:
        """Busca tarefas por data de vencimento"""
        pass
    
    @abstractmethod
    def update(self, task: Task) -> Task:
        """Atualiza uma tarefa"""
        pass
    
    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """Remove uma tarefa"""
        pass


class IUserRepository(ABC):
    """Interface para repositório de usuários"""
    
    @abstractmethod
    def save(self, user: User) -> User:
        """Salva um usuário"""
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Busca um usuário por ID"""
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Busca um usuário por email"""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Atualiza um usuário"""
        pass


class IPasswordHasher(ABC):
    """Interface para hash de senhas"""
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Gera hash da senha"""
        pass
    
    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica se a senha confere com o hash"""
        pass


class ITaskFilterStrategy(ABC):
    """Interface para estratégias de filtro de tarefas"""
    
    @abstractmethod
    def filter(self, tasks: List[Task]) -> List[Task]:
        """Aplica filtro na lista de tarefas"""
        pass


class ITaskSortStrategy(ABC):
    """Interface para estratégias de ordenação de tarefas"""
    
    @abstractmethod
    def sort(self, tasks: List[Task]) -> List[Task]:
        """Ordena a lista de tarefas"""
        pass 