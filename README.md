Projeto de Software — Arquitetura, SOLID, Clean Code e Padrões de Projeto
📋 Descrição

Este projeto foi desenvolvido como parte de um trabalho acadêmico com o objetivo de aplicar, de forma prática, os conceitos de Arquitetura de Software, Princípios SOLID, Clean Code e Padrões de Projeto (GoF).

🎯 Objetivos

    Desenvolver um software completo com arquitetura bem definida.

    Aplicar explicitamente os princípios SOLID.

    Garantir boas práticas de Clean Code.

    Implementar e justificar a utilização de ao menos 3 Padrões de Projeto GoF.

    Produzir documentação completa, diagramas UML e disponibilizar o código-fonte de forma organizada.


✅ Tema: Gerenciador de Tarefas CLI (ToDo App)

Descrição:
Um programa de linha de comando onde o usuário pode:

    Criar tarefas com título, descrição, prioridade e prazo.

    Listar tarefas (todas, pendentes, concluídas).

    Marcar como concluída.

    Remover tarefas.

    Filtrar por prioridade ou data.

📐 Arquitetura: Clean Architecture (ou MVC para simplificação)

    Domain Layer: entidades como Tarefa, interfaces dos repositórios.

    Application Layer: casos de uso (AdicionarTarefa, ListarTarefas, etc).

    Infrastructure Layer: persistência simples em JSON ou SQLite.

    Presentation Layer: CLI, interage com o usuário.

🔧 Padrões de Projeto GoF Aplicáveis:

    Command Pattern

        Para encapsular comandos como "criar tarefa", "listar tarefas", etc.

        Facilita a extensão e manutenção (Open/Closed Principle).

    Strategy Pattern

        Para estratégias de ordenação ou filtragem (por data, prioridade).

    Singleton Pattern

        Para o repositório de tarefas (uma única instância gerenciando os dados).

🧱 Princípios SOLID na prática:

    S (Single Responsibility): cada classe com uma única função: entidade, repositório, UI, etc.

    O (Open/Closed): comandos e filtros podem ser estendidos sem mudar código existente.

    L (Liskov): substituição de implementações de persistência ou filtragem sem quebrar o programa.

    I (Interface Segregation): separar contratos como ITarefaRepository, ICommand.

    D (Dependency Inversion): CLI depende de abstrações (ICommand, IRepository), não de implementações diretas.


# Cadastro de Pessoas

Uma aplicação web simples para cadastro e gerenciamento de pessoas, desenvolvida com Flask e PostgreSQL.

## Funcionalidades

- Cadastro de novos usuários
- Validação de e-mail único
- Listagem de todos os usuários cadastrados
- Armazenamento persistente em banco de dados PostgreSQL

## Tecnologias Utilizadas

- Python 3
- Flask
- SQLAlchemy
- PostgreSQL
- HTML/CSS

## Configuração do Ambiente

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```
3. Ative o ambiente virtual:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Executando a Aplicação

1. Certifique-se de que o ambiente virtual está ativado
2. Execute o comando:
   ```bash
   python app.py
   ```
3. Acesse a aplicação em `http://localhost:5000`

## Estrutura do Projeto

```
.
├── app.py              # Arquivo principal da aplicação
├── models/            # Modelos do banco de dados
├── templates/         # Templates HTML
├── static/           # Arquivos estáticos (CSS, JS)
├── .env              # Variáveis de ambiente
├── requirements.txt  # Dependências do projeto
└── README.md         # Este arquivo
``` 
    
