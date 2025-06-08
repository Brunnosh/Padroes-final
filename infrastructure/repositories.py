from typing import List, Optional
from datetime import date
from domain.entities import Task, User, Priority, TaskStatus
from domain.interfaces import ITaskRepository, IUserRepository
from .database import db, TaskModel, UserModel, PriorityEnum, TaskStatusEnum


class TaskRepositoryImpl(ITaskRepository):
    """Implementação concreta do repositório de tarefas usando SQLAlchemy"""
    
    def _to_domain_entity(self, task_model: TaskModel) -> Task:
        """Converte modelo do banco para entidade do domínio"""
        # Mapear enums do banco para enums do domínio
        priority_map = {
            PriorityEnum.LOW: Priority.LOW,
            PriorityEnum.MEDIUM: Priority.MEDIUM,
            PriorityEnum.HIGH: Priority.HIGH,
            PriorityEnum.URGENT: Priority.URGENT
        }
        
        status_map = {
            TaskStatusEnum.PENDING: TaskStatus.PENDING,
            TaskStatusEnum.IN_PROGRESS: TaskStatus.IN_PROGRESS,
            TaskStatusEnum.COMPLETED: TaskStatus.COMPLETED,
            TaskStatusEnum.CANCELLED: TaskStatus.CANCELLED
        }
        
        task = Task(
            title=task_model.title,
            description=task_model.description,
            priority=priority_map[task_model.priority],
            due_date=task_model.due_date,
            user_id=task_model.user_id,
            id=task_model.id
        )
        
        # Definir campos que não são definidos no construtor
        task.status = status_map[task_model.status]
        task.created_at = task_model.created_at
        task.updated_at = task_model.updated_at
        
        return task
    
    def _to_database_model(self, task: Task) -> TaskModel:
        """Converte entidade do domínio para modelo do banco"""
        # Mapear enums do domínio para enums do banco
        priority_map = {
            Priority.LOW: PriorityEnum.LOW,
            Priority.MEDIUM: PriorityEnum.MEDIUM,
            Priority.HIGH: PriorityEnum.HIGH,
            Priority.URGENT: PriorityEnum.URGENT
        }
        
        status_map = {
            TaskStatus.PENDING: TaskStatusEnum.PENDING,
            TaskStatus.IN_PROGRESS: TaskStatusEnum.IN_PROGRESS,
            TaskStatus.COMPLETED: TaskStatusEnum.COMPLETED,
            TaskStatus.CANCELLED: TaskStatusEnum.CANCELLED
        }
        
        if task.id:
            # Atualizar tarefa existente
            task_model = TaskModel.query.get(task.id)
            if task_model:
                task_model.title = task.title
                task_model.description = task.description
                task_model.priority = priority_map[task.priority]
                task_model.due_date = task.due_date
                task_model.status = status_map[task.status]
                task_model.updated_at = task.updated_at
                return task_model
        
        # Criar nova tarefa
        return TaskModel(
            title=task.title,
            description=task.description,
            priority=priority_map[task.priority],
            due_date=task.due_date,
            status=status_map[task.status],
            user_id=task.user_id
        )
    
    def save(self, task: Task) -> Task:
        """Salva uma tarefa no banco de dados"""
        task_model = self._to_database_model(task)
        
        if not task.id:
            db.session.add(task_model)
        
        db.session.commit()
        
        # Atualizar o ID da entidade se for nova
        if not task.id:
            task.id = task_model.id
        
        return task
    
    def find_by_id(self, task_id: int) -> Optional[Task]:
        """Busca uma tarefa por ID"""
        task_model = TaskModel.query.get(task_id)
        if task_model:
            return self._to_domain_entity(task_model)
        return None
    
    def find_by_user_id(self, user_id: int) -> List[Task]:
        """Busca todas as tarefas de um usuário"""
        task_models = TaskModel.query.filter_by(user_id=user_id).all()
        return [self._to_domain_entity(tm) for tm in task_models]
    
    def find_by_status(self, user_id: int, status: TaskStatus) -> List[Task]:
        """Busca tarefas por status"""
        status_map = {
            TaskStatus.PENDING: TaskStatusEnum.PENDING,
            TaskStatus.IN_PROGRESS: TaskStatusEnum.IN_PROGRESS,
            TaskStatus.COMPLETED: TaskStatusEnum.COMPLETED,
            TaskStatus.CANCELLED: TaskStatusEnum.CANCELLED
        }
        
        task_models = TaskModel.query.filter_by(
            user_id=user_id, 
            status=status_map[status]
        ).all()
        
        return [self._to_domain_entity(tm) for tm in task_models]
    
    def find_by_priority(self, user_id: int, priority: Priority) -> List[Task]:
        """Busca tarefas por prioridade"""
        priority_map = {
            Priority.LOW: PriorityEnum.LOW,
            Priority.MEDIUM: PriorityEnum.MEDIUM,
            Priority.HIGH: PriorityEnum.HIGH,
            Priority.URGENT: PriorityEnum.URGENT
        }
        
        task_models = TaskModel.query.filter_by(
            user_id=user_id, 
            priority=priority_map[priority]
        ).all()
        
        return [self._to_domain_entity(tm) for tm in task_models]
    
    def find_by_due_date(self, user_id: int, due_date: date) -> List[Task]:
        """Busca tarefas por data de vencimento"""
        task_models = TaskModel.query.filter_by(
            user_id=user_id, 
            due_date=due_date
        ).all()
        
        return [self._to_domain_entity(tm) for tm in task_models]
    
    def update(self, task: Task) -> Task:
        """Atualiza uma tarefa"""
        if not task.id:
            raise ValueError("Não é possível atualizar tarefa sem ID")
        
        task_model = self._to_database_model(task)
        db.session.commit()
        return task
    
    def delete(self, task_id: int) -> bool:
        """Remove uma tarefa"""
        task_model = TaskModel.query.get(task_id)
        if task_model:
            db.session.delete(task_model)
            db.session.commit()
            return True
        return False


class UserRepositoryImpl(IUserRepository):
    """Implementação concreta do repositório de usuários usando SQLAlchemy"""
    
    def _to_domain_entity(self, user_model: UserModel) -> User:
        """Converte modelo do banco para entidade do domínio"""
        user = User(
            email=user_model.email,
            password_hash=user_model.password_hash,
            id=user_model.id
        )
        user.created_at = user_model.created_at
        return user
    
    def _to_database_model(self, user: User) -> UserModel:
        """Converte entidade do domínio para modelo do banco"""
        if user.id:
            # Atualizar usuário existente
            user_model = UserModel.query.get(user.id)
            if user_model:
                user_model.email = user.email
                user_model.password_hash = user.password_hash
                return user_model
        
        # Criar novo usuário
        return UserModel(
            email=user.email,
            password_hash=user.password_hash
        )
    
    def save(self, user: User) -> User:
        """Salva um usuário no banco de dados"""
        user_model = self._to_database_model(user)
        
        if not user.id:
            db.session.add(user_model)
        
        db.session.commit()
        
        # Atualizar o ID da entidade se for nova
        if not user.id:
            user.id = user_model.id
        
        return user
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Busca um usuário por ID"""
        user_model = UserModel.query.get(user_id)
        if user_model:
            return self._to_domain_entity(user_model)
        return None
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Busca um usuário por email"""
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            return self._to_domain_entity(user_model)
        return None
    
    def update(self, user: User) -> User:
        """Atualiza um usuário"""
        if not user.id:
            raise ValueError("Não é possível atualizar usuário sem ID")
        
        user_model = self._to_database_model(user)
        db.session.commit()
        return user 