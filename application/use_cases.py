from typing import List, Optional
from datetime import date
from domain.entities import Task, User, Priority, TaskStatus
from domain.interfaces import ITaskRepository, IUserRepository, IPasswordHasher
from .commands import (
    CreateTaskCommand, UpdateTaskCommand, CompleteTaskCommand, 
    DeleteTaskCommand, CommandInvoker
)
from .strategies import (
    TaskFilterContext, TaskSortContext, 
    FilterStrategyFactory, SortStrategyFactory
)


class CreateTaskUseCase:
    """Caso de uso para criar uma nova tarefa"""
    
    def __init__(self, task_repository: ITaskRepository, command_invoker: CommandInvoker):
        self._task_repository = task_repository
        self._command_invoker = command_invoker
    
    def execute(self, title: str, description: Optional[str], priority: Priority,
                due_date: Optional[date], user_id: int) -> Task:
        """Executa a criação de uma nova tarefa"""
        if not title or len(title.strip()) == 0:
            raise ValueError("Título da tarefa é obrigatório")
        
        if due_date and due_date < date.today():
            raise ValueError("Data de vencimento não pode ser no passado")
        
        command = CreateTaskCommand(
            self._task_repository, title.strip(), description, 
            priority, due_date, user_id
        )
        
        return self._command_invoker.execute_command(command)


class UpdateTaskUseCase:
    """Caso de uso para atualizar uma tarefa"""
    
    def __init__(self, task_repository: ITaskRepository, command_invoker: CommandInvoker):
        self._task_repository = task_repository
        self._command_invoker = command_invoker
    
    def execute(self, task_id: int, user_id: int, title: Optional[str] = None,
                description: Optional[str] = None, priority: Optional[Priority] = None,
                due_date: Optional[date] = None) -> Optional[Task]:
        """Executa a atualização de uma tarefa"""
        # Verificar se a tarefa existe e pertence ao usuário
        existing_task = self._task_repository.find_by_id(task_id)
        if not existing_task:
            raise ValueError("Tarefa não encontrada")
        
        if existing_task.user_id != user_id:
            raise ValueError("Você não tem permissão para editar esta tarefa")
        
        if title is not None and len(title.strip()) == 0:
            raise ValueError("Título da tarefa não pode estar vazio")
        
        if due_date and due_date < date.today():
            raise ValueError("Data de vencimento não pode ser no passado")
        
        command = UpdateTaskCommand(
            self._task_repository, task_id, 
            title.strip() if title else None, description, priority, due_date
        )
        
        return self._command_invoker.execute_command(command)


class CompleteTaskUseCase:
    """Caso de uso para marcar uma tarefa como concluída"""
    
    def __init__(self, task_repository: ITaskRepository, command_invoker: CommandInvoker):
        self._task_repository = task_repository
        self._command_invoker = command_invoker
    
    def execute(self, task_id: int, user_id: int) -> Optional[Task]:
        """Executa a marcação da tarefa como concluída"""
        # Verificar se a tarefa existe e pertence ao usuário
        existing_task = self._task_repository.find_by_id(task_id)
        if not existing_task:
            raise ValueError("Tarefa não encontrada")
        
        if existing_task.user_id != user_id:
            raise ValueError("Você não tem permissão para alterar esta tarefa")
        
        if existing_task.is_completed():
            raise ValueError("Tarefa já está concluída")
        
        command = CompleteTaskCommand(self._task_repository, task_id)
        return self._command_invoker.execute_command(command)


class DeleteTaskUseCase:
    """Caso de uso para remover uma tarefa"""
    
    def __init__(self, task_repository: ITaskRepository, command_invoker: CommandInvoker):
        self._task_repository = task_repository
        self._command_invoker = command_invoker
    
    def execute(self, task_id: int, user_id: int) -> bool:
        """Executa a remoção de uma tarefa"""
        # Verificar se a tarefa existe e pertence ao usuário
        existing_task = self._task_repository.find_by_id(task_id)
        if not existing_task:
            raise ValueError("Tarefa não encontrada")
        
        if existing_task.user_id != user_id:
            raise ValueError("Você não tem permissão para remover esta tarefa")
        
        command = DeleteTaskCommand(self._task_repository, task_id)
        return self._command_invoker.execute_command(command)


class ListTasksUseCase:
    """Caso de uso para listar tarefas com filtros e ordenação"""
    
    def __init__(self, task_repository: ITaskRepository):
        self._task_repository = task_repository
    
    def execute(self, user_id: int, filter_type: str = 'all', 
                sort_type: str = 'creation_date', priority_filter: Optional[Priority] = None) -> List[Task]:
        """Executa a listagem de tarefas com filtros e ordenação"""
        # Buscar todas as tarefas do usuário
        tasks = self._task_repository.find_by_user_id(user_id)
        
        # Aplicar filtro
        filter_strategy = FilterStrategyFactory.create_filter_strategy(
            filter_type, priority=priority_filter
        )
        filter_context = TaskFilterContext(filter_strategy)
        filtered_tasks = filter_context.apply_filter(tasks)
        
        # Aplicar ordenação
        sort_strategy = SortStrategyFactory.create_sort_strategy(sort_type)
        sort_context = TaskSortContext(sort_strategy)
        sorted_tasks = sort_context.apply_sort(filtered_tasks)
        
        return sorted_tasks


class GetTaskStatsUseCase:
    """Caso de uso para obter estatísticas das tarefas"""
    
    def __init__(self, task_repository: ITaskRepository):
        self._task_repository = task_repository
    
    def execute(self, user_id: int) -> dict:
        """Executa o cálculo de estatísticas das tarefas"""
        tasks = self._task_repository.find_by_user_id(user_id)
        
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.is_completed()])
        pending_tasks = len([t for t in tasks if t.status == TaskStatus.PENDING])
        in_progress_tasks = len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS])
        overdue_tasks = len([t for t in tasks if t.is_overdue()])
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Tarefas por prioridade
        priority_stats = {
            'urgent': len([t for t in tasks if t.priority == Priority.URGENT]),
            'high': len([t for t in tasks if t.priority == Priority.HIGH]),
            'medium': len([t for t in tasks if t.priority == Priority.MEDIUM]),
            'low': len([t for t in tasks if t.priority == Priority.LOW])
        }
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'in_progress_tasks': in_progress_tasks,
            'overdue_tasks': overdue_tasks,
            'completion_rate': round(completion_rate, 2),
            'priority_stats': priority_stats
        }


class RegisterUserUseCase:
    """Caso de uso para registrar um novo usuário"""
    
    def __init__(self, user_repository: IUserRepository, password_hasher: IPasswordHasher):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
    
    def execute(self, email: str, password: str) -> User:
        """Executa o registro de um novo usuário"""
        if not email or '@' not in email:
            raise ValueError("Email inválido")
        
        if not password or len(password) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")
        
        # Verificar se o email já existe
        existing_user = self._user_repository.find_by_email(email)
        if existing_user:
            raise ValueError("Email já está em uso")
        
        # Criar usuário com senha hash
        password_hash = self._password_hasher.hash_password(password)
        user = User(email=email, password_hash=password_hash)
        
        return self._user_repository.save(user)


class AuthenticateUserUseCase:
    """Caso de uso para autenticar um usuário"""
    
    def __init__(self, user_repository: IUserRepository, password_hasher: IPasswordHasher):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
    
    def execute(self, email: str, password: str) -> Optional[User]:
        """Executa a autenticação do usuário"""
        if not email or not password:
            raise ValueError("Email e senha são obrigatórios")
        
        user = self._user_repository.find_by_email(email)
        if not user:
            return None
        
        if not self._password_hasher.verify_password(password, user.password_hash):
            return None
        
        return user


class UndoActionUseCase:
    """Caso de uso para desfazer a última ação"""
    
    def __init__(self, command_invoker: CommandInvoker):
        self._command_invoker = command_invoker
    
    def execute(self) -> bool:
        """Executa o undo da última ação"""
        if not self._command_invoker.can_undo():
            return False
        
        self._command_invoker.undo()
        return True


class RedoActionUseCase:
    """Caso de uso para refazer uma ação"""
    
    def __init__(self, command_invoker: CommandInvoker):
        self._command_invoker = command_invoker
    
    def execute(self) -> bool:
        """Executa o redo de uma ação"""
        if not self._command_invoker.can_redo():
            return False
        
        self._command_invoker.redo()
        return True 