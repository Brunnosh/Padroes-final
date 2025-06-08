from abc import ABC, abstractmethod
from datetime import datetime, date
from enum import Enum
from typing import Optional
from dataclasses import dataclass


class Priority(Enum):
    """Enum para prioridades das tarefas"""
    LOW = "baixa"
    MEDIUM = "media"
    HIGH = "alta"
    URGENT = "urgente"


class TaskStatus(Enum):
    """Enum para status das tarefas"""
    PENDING = "pendente"
    IN_PROGRESS = "em_progresso"
    COMPLETED = "concluida"
    CANCELLED = "cancelada"


@dataclass
class Task:
    """Entidade Task - representa uma tarefa no sistema"""
    id: Optional[int]
    title: str
    description: Optional[str]
    priority: Priority
    due_date: Optional[date]
    status: TaskStatus
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: int
    
    def __init__(self, title: str, description: Optional[str], priority: Priority, 
                 due_date: Optional[date], user_id: int, id: Optional[int] = None):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.updated_at = None
        self.user_id = user_id
    
    def mark_as_completed(self) -> None:
        """Marca a tarefa como concluída"""
        if self.status != TaskStatus.COMPLETED:
            self.status = TaskStatus.COMPLETED
            self.updated_at = datetime.now()
    
    def mark_as_pending(self) -> None:
        """Marca a tarefa como pendente"""
        if self.status != TaskStatus.PENDING:
            self.status = TaskStatus.PENDING
            self.updated_at = datetime.now()
    
    def mark_as_in_progress(self) -> None:
        """Marca a tarefa como em progresso"""
        if self.status != TaskStatus.IN_PROGRESS:
            self.status = TaskStatus.IN_PROGRESS
            self.updated_at = datetime.now()
    
    def is_completed(self) -> bool:
        """Verifica se a tarefa está concluída"""
        return self.status == TaskStatus.COMPLETED
    
    def is_overdue(self) -> bool:
        """Verifica se a tarefa está atrasada"""
        if self.due_date is None:
            return False
        return self.due_date < date.today() and not self.is_completed()
    
    def update(self, title: Optional[str] = None, description: Optional[str] = None, 
              priority: Optional[Priority] = None, due_date: Optional[date] = None) -> None:
        """Atualiza os dados da tarefa"""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if priority is not None:
            self.priority = priority
        if due_date is not None:
            self.due_date = due_date
        self.updated_at = datetime.now()


@dataclass
class User:
    """Entidade User - representa um usuário do sistema"""
    id: Optional[int]
    email: str
    password_hash: str
    created_at: datetime
    
    def __init__(self, email: str, password_hash: str, id: Optional[int] = None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.now() 