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
5. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione as seguintes variáveis:
     ```
     DATABASE_URL=sua_url_do_postgresql
     SECRET_KEY=sua_chave_secreta
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