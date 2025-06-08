# TaskFlow - Sistema de Gerenciamento de Tarefas

## Descrição

Este projeto foi desenvolvido aplicando os conceitos de **Clean Architecture**, **Princípios SOLID**, **Clean Code** e **Padrões de Projeto GoF**. O TaskFlow é um sistema web moderno para gerenciamento de tarefas que demonstra a aplicação prática desses conceitos fundamentais da engenharia de software.

## Funcionalidades

-  **Autenticação segura** de usuários com hash de senhas
-  **Criação de tarefas** com título, descrição, prioridade e prazo
-  **Filtros avançados** (todas, pendentes, concluídas, por prioridade, atrasadas)
-  **Ordenação inteligente** (data, prioridade, status, alfabética)
-  **Marcação de tarefas** como concluídas
-  **Sistema de Undo/Redo** para operações
-  **Interface responsiva** com design moderno
-  **Estatísticas** de produtividade
-  **Atalhos de teclado** para navegação rápida

## Arquitetura: Clean Architecture

O projeto segue rigorosamente os princípios da Clean Architecture:

```
📁 domain/           # Camada de Domínio
├── entities.py      # Entidades de negócio (Task, User)
└── interfaces.py    # Contratos/Interfaces

📁 application/      # Camada de Aplicação  
├── commands.py      # Padrão Command
├── strategies.py    # Padrão Strategy  
└── use_cases.py     # Casos de uso

📁 infrastructure/   # Camada de Infraestrutura
├── database.py      # Configuração do banco (Singleton)
├── repositories.py  # Implementações concretas
└── password_service.py

📁 presentation/     # Camada de Apresentação
└── controllers.py   # Controladores Flask

📁 templates/        # Interface de usuário
└── static/         # Recursos estáticos
```

## Padrões de Projeto GoF Implementados

### 1. **Command Pattern**
- **Localização**: `application/commands.py`
- **Propósito**: Encapsula operações como objetos, permitindo undo/redo
- **Classes**: `CreateTaskCommand`, `UpdateTaskCommand`, `CompleteTaskCommand`, `DeleteTaskCommand`, `CommandInvoker`

### 2. **Strategy Pattern**
- **Localização**: `application/strategies.py`
- **Propósito**: Define família de algoritmos de filtro e ordenação
- **Classes**: `FilterStrategy`, `SortStrategy`, `TaskFilterContext`, `TaskSortContext`

### 3. **Singleton Pattern**
- **Localização**: `infrastructure/database.py`
- **Propósito**: Garante uma única instância da conexão com banco
- **Classe**: `DatabaseConnection`

### 4. **Factory Pattern**
- **Localização**: `application/strategies.py`
- **Propósito**: Cria estratégias baseadas em tipos
- **Classes**: `FilterStrategyFactory`, `SortStrategyFactory`

## Princípios SOLID Aplicados

### **S - Single Responsibility Principle**
- Cada classe tem uma única responsabilidade bem definida
- `TaskController` apenas gerencia requisições HTTP
- `TaskRepository` apenas persiste dados
- `CreateTaskUseCase` apenas cria tarefas

### **O - Open/Closed Principle**
- Sistema aberto para extensão, fechado para modificação
- Novos filtros podem ser adicionados sem alterar código existente
- Novas estratégias de ordenação são facilmente implementáveis

### **L - Liskov Substitution Principle**
- Implementações podem ser substituídas sem quebrar o sistema
- `ITaskRepository` pode ter implementações SQLite, PostgreSQL, etc.
- Estratégias são intercambiáveis

### **I - Interface Segregation Principle**
- Interfaces específicas para cada responsabilidade
- `ITaskRepository`, `IUserRepository`, `IPasswordHasher` são separadas
- Clientes dependem apenas das interfaces que usam

### **D - Dependency Inversion Principle**
- Dependência de abstrações, não implementações
- `UseCase` → `IRepository` (não implementação concreta)
- Injeção de dependência via `DependencyContainer`


## Tecnologias Utilizadas

- **Backend**: Python 3.8+, Flask 3.0+
- **Banco de Dados**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, JavaScript ES6+, Bootstrap 5.3
- **Arquitetura**: Clean Architecture
- **Padrões**: Command, Strategy, Singleton, Factory
- **Princípios**: SOLID, Clean Code

## Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Método 1: Instalação Automática (Recomendado)

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/Brunnosh/Padroes-final.git
   cd Padroes-final
   ```

2. **Execute o setup automático**:
   ```bash
   ./setup.sh
   ```

3. **Inicie a aplicação**:
   ```bash
   ./start.sh
   ```

### Método 2: Instalação Manual

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/Brunnosh/Padroes-final.git
   cd Padroes-final
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python3 -m venv venv
   ```

3. **Ative o ambiente virtual**:
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```

4. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute a aplicação**:
   ```bash
   python3 main.py
   ```

### Acesso à Aplicação
Abra seu navegador e acesse: `http://localhost:5000`

### Solução de Problemas

**Problema: Aplicação para instantaneamente**
-  **Solução**: Use um ambiente virtual (venv) e execute o script principal.
-  **Comando**: `./setup.sh` seguido de `./start.sh`

**Problema: Dependências não encontradas**
-  **Solução**: Instale as dependências no ambiente virtual
-  **Comando**: `pip install -r requirements.txt`

**Problema: Python não encontrado**
-  **Solução**: Use `python3` em vez de `python`
-  **Comando**: `python3 main.py`

## Como Usar

### 1. **Cadastro e Login**
- Acesse a página inicial
- Clique em "Cadastrar" para criar uma conta
- Faça login com suas credenciais

### 2. **Gerenciar Tarefas**
- **Criar**: Clique em "Nova Tarefa" e preencha os campos
- **Visualizar**: Use os filtros no dashboard para organizar suas tarefas
- **Completar**: Marque o checkbox ao lado da tarefa
- **Editar**: Clique no ícone de edição
- **Excluir**: Clique no ícone de lixeira

### 3. **Atalhos de Teclado**
- `Ctrl + N`: Nova tarefa
- `Ctrl + F`: Buscar
- `Ctrl + Z`: Desfazer última ação
- `1, 2, 3`: Filtros rápidos

##  Clean Code Aplicado

### **Nomenclatura Clara**
```python
# ❌ Ruim
def calc(t, p):
    return t * p

# ✅ Bom  
def calculate_task_priority_score(task: Task, priority_weight: float) -> float:
    return task.complexity * priority_weight
```

### **Funções Pequenas e Focadas**
```python
# ✅ Cada função tem uma única responsabilidade
def create_task(self, title: str, description: str, priority: Priority, due_date: date, user_id: int) -> Task:
    self._validate_task_data(title, due_date)
    task = Task(title, description, priority, due_date, user_id)
    return self._task_repository.save(task)

def _validate_task_data(self, title: str, due_date: date) -> None:
    if not title or len(title.strip()) == 0:
        raise ValueError("Título da tarefa é obrigatório")
    if due_date and due_date < date.today():
        raise ValueError("Data de vencimento não pode ser no passado")
```

### **Evitando Duplicação (DRY)**
```python
# ✅ Factory centraliza a criação de estratégias
class FilterStrategyFactory:
    @staticmethod
    def create_filter_strategy(filter_type: str) -> ITaskFilterStrategy:
        strategies = {
            'all': AllTasksFilterStrategy(),
            'completed': CompletedTasksFilterStrategy(),
            'pending': PendingTasksFilterStrategy()
        }
        return strategies.get(filter_type, AllTasksFilterStrategy())
```

##  Benefícios da Arquitetura

### **Testabilidade**
- Dependências injetadas facilitam mocks e testes unitários
- Lógica de negócio isolada de frameworks

### **Manutenibilidade** 
- Código organizado em camadas bem definidas
- Mudanças em uma camada não afetam outras

### **Flexibilidade**
- Fácil troca de implementações (SQLite → PostgreSQL)
- Novos recursos podem ser adicionados sem modificar código existente

### **Escalabilidade**
- Arquitetura preparada para crescimento
- Separação clara de responsabilidades

##  Exemplos de Extensibilidade

### **Novo Filtro**
```python
class TodayTasksFilterStrategy(ITaskFilterStrategy):
    def filter(self, tasks: List[Task]) -> List[Task]:
        today = date.today()
        return [task for task in tasks if task.due_date == today]
```

### **Nova Ordenação**
```python
class UrgencyLevelSortStrategy(ITaskSortStrategy):
    def sort(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t.calculate_urgency_level())
```

### **Novo Comando**
```python
class ArchiveTaskCommand(ICommand):
    def execute(self) -> Task:
        task = self._task_repository.find_by_id(self._task_id)
        task.archive()
        return self._task_repository.update(task)
```

##  Métricas de Qualidade

- **Cobertura de Testes**: Preparado para testes unitários
- **Complexidade Ciclomática**: Baixa devido a funções pequenas
- **Acoplamento**: Baixo devido à inversão de dependência
- **Coesão**: Alta - cada classe tem responsabilidade única

##  Conclusão

Este projeto demonstra a aplicação prática e efetiva de:

-  **Clean Architecture** com separação clara de camadas
-  **Padrões GoF** resolvendo problemas reais de design
-  **Princípios SOLID** garantindo código maintível e extensível  
-  **Clean Code** com código legível e bem estruturado
-  **Interface moderna** com excelente UX/UI

O TaskFlow serve como exemplo de como conceitos teóricos de engenharia de software podem ser aplicados para criar sistemas robustos, escaláveis e de alta qualidade. 
    
