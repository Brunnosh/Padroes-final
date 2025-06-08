from typing import List
from datetime import date
from domain.entities import Task, Priority, TaskStatus
from domain.interfaces import ITaskFilterStrategy, ITaskSortStrategy


# ============= FILTROS (Strategy Pattern) =============

class AllTasksFilterStrategy(ITaskFilterStrategy):
    """Estratégia que retorna todas as tarefas sem filtro"""
    
    def filter(self, tasks: List[Task]) -> List[Task]:
        return tasks


class CompletedTasksFilterStrategy(ITaskFilterStrategy):
    """Estratégia que filtra apenas tarefas concluídas"""
    
    def filter(self, tasks: List[Task]) -> List[Task]:
        return [task for task in tasks if task.status == TaskStatus.COMPLETED]


class PendingTasksFilterStrategy(ITaskFilterStrategy):
    """Estratégia que filtra apenas tarefas pendentes"""
    
    def filter(self, tasks: List[Task]) -> List[Task]:
        return [task for task in tasks if task.status == TaskStatus.PENDING]


class InProgressTasksFilterStrategy(ITaskFilterStrategy):
    """Estratégia que filtra apenas tarefas em progresso"""
    
    def filter(self, tasks: List[Task]) -> List[Task]:
        return [task for task in tasks if task.status == TaskStatus.IN_PROGRESS]


class HighPriorityFilterStrategy(ITaskFilterStrategy):
    """Estratégia que filtra tarefas de alta prioridade"""
    
    def filter(self, tasks: List[Task]) -> List[Task]:
        return [task for task in tasks if task.priority in [Priority.HIGH, Priority.URGENT]]


class OverdueTasksFilterStrategy(ITaskFilterStrategy):
    """Estratégia que filtra tarefas atrasadas"""
    
    def filter(self, tasks: List[Task]) -> List[Task]:
        return [task for task in tasks if task.is_overdue()]


class TodayTasksFilterStrategy(ITaskFilterStrategy):
    """Estratégia que filtra tarefas que vencem hoje"""
    
    def filter(self, tasks: List[Task]) -> List[Task]:
        today = date.today()
        return [task for task in tasks if task.due_date == today]


class PriorityFilterStrategy(ITaskFilterStrategy):
    """Estratégia que filtra tarefas por prioridade específica"""
    
    def __init__(self, priority: Priority):
        self._priority = priority
    
    def filter(self, tasks: List[Task]) -> List[Task]:
        return [task for task in tasks if task.priority == self._priority]


# ============= ORDENAÇÃO (Strategy Pattern) =============

class PrioritySortStrategy(ITaskSortStrategy):
    """Estratégia que ordena tarefas por prioridade (urgente → baixa)"""
    
    def sort(self, tasks: List[Task]) -> List[Task]:
        priority_order = {
            Priority.URGENT: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3
        }
        return sorted(tasks, key=lambda task: priority_order[task.priority])


class DueDateSortStrategy(ITaskSortStrategy):
    """Estratégia que ordena tarefas por data de vencimento"""
    
    def sort(self, tasks: List[Task]) -> List[Task]:
        # Tarefas sem data de vencimento vão para o final
        return sorted(tasks, key=lambda task: task.due_date or date.max)


class CreationDateSortStrategy(ITaskSortStrategy):
    """Estratégia que ordena tarefas por data de criação (mais recentes primeiro)"""
    
    def sort(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda task: task.created_at, reverse=True)


class AlphabeticalSortStrategy(ITaskSortStrategy):
    """Estratégia que ordena tarefas alfabeticamente por título"""
    
    def sort(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda task: task.title.lower())


class StatusSortStrategy(ITaskSortStrategy):
    """Estratégia que ordena tarefas por status (pendente → em progresso → concluída)"""
    
    def sort(self, tasks: List[Task]) -> List[Task]:
        status_order = {
            TaskStatus.PENDING: 0,
            TaskStatus.IN_PROGRESS: 1,
            TaskStatus.COMPLETED: 2,
            TaskStatus.CANCELLED: 3
        }
        return sorted(tasks, key=lambda task: status_order[task.status])


# ============= CONTEXT PARA ESTRATÉGIAS =============

class TaskFilterContext:
    """Context para aplicar estratégias de filtro"""
    
    def __init__(self, strategy: ITaskFilterStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: ITaskFilterStrategy) -> None:
        """Altera a estratégia de filtro"""
        self._strategy = strategy
    
    def apply_filter(self, tasks: List[Task]) -> List[Task]:
        """Aplica o filtro usando a estratégia atual"""
        return self._strategy.filter(tasks)


class TaskSortContext:
    """Context para aplicar estratégias de ordenação"""
    
    def __init__(self, strategy: ITaskSortStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: ITaskSortStrategy) -> None:
        """Altera a estratégia de ordenação"""
        self._strategy = strategy
    
    def apply_sort(self, tasks: List[Task]) -> List[Task]:
        """Aplica a ordenação usando a estratégia atual"""
        return self._strategy.sort(tasks)


# ============= FACTORY PARA ESTRATÉGIAS =============

class FilterStrategyFactory:
    """Factory para criar estratégias de filtro"""
    
    @staticmethod
    def create_filter_strategy(filter_type: str, **kwargs) -> ITaskFilterStrategy:
        """Cria uma estratégia de filtro baseada no tipo"""
        strategies = {
            'all': AllTasksFilterStrategy(),
            'completed': CompletedTasksFilterStrategy(),
            'pending': PendingTasksFilterStrategy(),
            'in_progress': InProgressTasksFilterStrategy(),
            'high_priority': HighPriorityFilterStrategy(),
            'overdue': OverdueTasksFilterStrategy(),
            'today': TodayTasksFilterStrategy(),
            'priority': PriorityFilterStrategy(kwargs.get('priority', Priority.MEDIUM))
        }
        
        return strategies.get(filter_type, AllTasksFilterStrategy())


class SortStrategyFactory:
    """Factory para criar estratégias de ordenação"""
    
    @staticmethod
    def create_sort_strategy(sort_type: str) -> ITaskSortStrategy:
        """Cria uma estratégia de ordenação baseada no tipo"""
        strategies = {
            'priority': PrioritySortStrategy(),
            'due_date': DueDateSortStrategy(),
            'creation_date': CreationDateSortStrategy(),
            'alphabetical': AlphabeticalSortStrategy(),
            'status': StatusSortStrategy()
        }
        
        return strategies.get(sort_type, CreationDateSortStrategy()) 