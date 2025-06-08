from abc import ABC, abstractmethod
from typing import Any, Optional, List
from datetime import date
from domain.entities import Task, Priority, TaskStatus
from domain.interfaces import ITaskRepository


class ICommand(ABC):
    """Interface base para todos os comandos - Command Pattern"""
    
    @abstractmethod
    def execute(self) -> Any:
        """Executa o comando"""
        pass
    
    @abstractmethod
    def undo(self) -> Any:
        """Desfaz o comando (opcional)"""
        pass


class CreateTaskCommand(ICommand):
    """Comando para criar uma nova tarefa"""
    
    def __init__(self, task_repository: ITaskRepository, title: str, 
                 description: Optional[str], priority: Priority, 
                 due_date: Optional[date], user_id: int):
        self._task_repository = task_repository
        self._title = title
        self._description = description
        self._priority = priority
        self._due_date = due_date
        self._user_id = user_id
        self._created_task: Optional[Task] = None
    
    def execute(self) -> Task:
        """Executa a criação da tarefa"""
        task = Task(
            title=self._title,
            description=self._description,
            priority=self._priority,
            due_date=self._due_date,
            user_id=self._user_id
        )
        self._created_task = self._task_repository.save(task)
        return self._created_task
    
    def undo(self) -> bool:
        """Desfaz a criação removendo a tarefa"""
        if self._created_task and self._created_task.id:
            return self._task_repository.delete(self._created_task.id)
        return False


class UpdateTaskCommand(ICommand):
    """Comando para atualizar uma tarefa"""
    
    def __init__(self, task_repository: ITaskRepository, task_id: int,
                 title: Optional[str] = None, description: Optional[str] = None,
                 priority: Optional[Priority] = None, due_date: Optional[date] = None):
        self._task_repository = task_repository
        self._task_id = task_id
        self._title = title
        self._description = description
        self._priority = priority
        self._due_date = due_date
        self._original_task: Optional[Task] = None
    
    def execute(self) -> Optional[Task]:
        """Executa a atualização da tarefa"""
        task = self._task_repository.find_by_id(self._task_id)
        if not task:
            return None
        
        # Salva o estado original para undo
        self._original_task = Task(
            title=task.title,
            description=task.description,
            priority=task.priority,
            due_date=task.due_date,
            user_id=task.user_id,
            id=task.id
        )
        
        # Atualiza a tarefa
        task.update(self._title, self._description, self._priority, self._due_date)
        return self._task_repository.update(task)
    
    def undo(self) -> Optional[Task]:
        """Desfaz a atualização restaurando os valores originais"""
        if self._original_task:
            return self._task_repository.update(self._original_task)
        return None


class CompleteTaskCommand(ICommand):
    """Comando para marcar uma tarefa como concluída"""
    
    def __init__(self, task_repository: ITaskRepository, task_id: int):
        self._task_repository = task_repository
        self._task_id = task_id
        self._original_status: Optional[TaskStatus] = None
    
    def execute(self) -> Optional[Task]:
        """Executa a marcação da tarefa como concluída"""
        task = self._task_repository.find_by_id(self._task_id)
        if not task:
            return None
        
        self._original_status = task.status
        task.mark_as_completed()
        return self._task_repository.update(task)
    
    def undo(self) -> Optional[Task]:
        """Desfaz a marcação, restaurando o status original"""
        if self._original_status:
            task = self._task_repository.find_by_id(self._task_id)
            if task:
                task.status = self._original_status
                return self._task_repository.update(task)
        return None


class DeleteTaskCommand(ICommand):
    """Comando para remover uma tarefa"""
    
    def __init__(self, task_repository: ITaskRepository, task_id: int):
        self._task_repository = task_repository
        self._task_id = task_id
        self._deleted_task: Optional[Task] = None
    
    def execute(self) -> bool:
        """Executa a remoção da tarefa"""
        # Salva a tarefa para possível undo
        self._deleted_task = self._task_repository.find_by_id(self._task_id)
        return self._task_repository.delete(self._task_id)
    
    def undo(self) -> Optional[Task]:
        """Desfaz a remoção restaurando a tarefa"""
        if self._deleted_task:
            return self._task_repository.save(self._deleted_task)
        return None


class CommandInvoker:
    """Invoker do padrão Command - gerencia execução e histórico de comandos"""
    
    def __init__(self):
        self._history: List[ICommand] = []
        self._current_position = -1
    
    def execute_command(self, command: ICommand) -> Any:
        """Executa um comando e o adiciona ao histórico"""
        result = command.execute()
        
        # Remove comandos após a posição atual (para redo limpo)
        self._history = self._history[:self._current_position + 1]
        
        # Adiciona o novo comando
        self._history.append(command)
        self._current_position += 1
        
        return result
    
    def undo(self) -> Any:
        """Desfaz o último comando executado"""
        if self._current_position >= 0:
            command = self._history[self._current_position]
            result = command.undo()
            self._current_position -= 1
            return result
        return None
    
    def redo(self) -> Any:
        """Refaz o próximo comando no histórico"""
        if self._current_position < len(self._history) - 1:
            self._current_position += 1
            command = self._history[self._current_position]
            return command.execute()
        return None
    
    def can_undo(self) -> bool:
        """Verifica se é possível desfazer"""
        return self._current_position >= 0
    
    def can_redo(self) -> bool:
        """Verifica se é possível refazer"""
        return self._current_position < len(self._history) - 1 