from flask import Flask, Blueprint
from dotenv import load_dotenv
import os

# Importações das camadas
from infrastructure.database import db_connection
from infrastructure.repositories import TaskRepositoryImpl, UserRepositoryImpl
from infrastructure.password_service import BcryptPasswordHasher
from application.commands import CommandInvoker
from application.use_cases import (
    CreateTaskUseCase, UpdateTaskUseCase, CompleteTaskUseCase,
    DeleteTaskUseCase, ListTasksUseCase, GetTaskStatsUseCase,
    RegisterUserUseCase, AuthenticateUserUseCase, UndoActionUseCase, RedoActionUseCase
)
from presentation.controllers import AuthController, TaskController


class DependencyContainer:
    """Container de injeção de dependência - Dependency Injection Pattern"""
    
    def __init__(self):
        # Infraestrutura
        self.task_repository = TaskRepositoryImpl()
        self.user_repository = UserRepositoryImpl()
        self.password_hasher = BcryptPasswordHasher()
        self.command_invoker = CommandInvoker()
        
        # Casos de uso
        self.create_task_use_case = CreateTaskUseCase(self.task_repository, self.command_invoker)
        self.update_task_use_case = UpdateTaskUseCase(self.task_repository, self.command_invoker)
        self.complete_task_use_case = CompleteTaskUseCase(self.task_repository, self.command_invoker)
        self.delete_task_use_case = DeleteTaskUseCase(self.task_repository, self.command_invoker)
        self.list_tasks_use_case = ListTasksUseCase(self.task_repository)
        self.get_stats_use_case = GetTaskStatsUseCase(self.task_repository)
        self.register_user_use_case = RegisterUserUseCase(self.user_repository, self.password_hasher)
        self.authenticate_user_use_case = AuthenticateUserUseCase(self.user_repository, self.password_hasher)
        self.undo_action_use_case = UndoActionUseCase(self.command_invoker)
        self.redo_action_use_case = RedoActionUseCase(self.command_invoker)
        
        # Controladores
        self.auth_controller = AuthController(self.register_user_use_case, self.authenticate_user_use_case)
        self.task_controller = TaskController(
            self.create_task_use_case,
            self.update_task_use_case,
            self.complete_task_use_case,
            self.delete_task_use_case,
            self.list_tasks_use_case,
            self.get_stats_use_case,
            self.undo_action_use_case,
            self.redo_action_use_case
        )


def create_app() -> Flask:
    """Factory para criar a aplicação Flask"""
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    app = Flask(__name__)
    
    # Configurações da aplicação
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-taskflow-2024-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///tasks.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True
    }
    
    # Inicializar banco de dados
    db_connection.init_app(app)
    
    # Criar container de dependências
    container = DependencyContainer()
    
    # Registrar blueprints
    register_blueprints(app, container)
    
    # Criar tabelas do banco
    with app.app_context():
        db_connection.db.create_all()
        print("\n=== SISTEMA DE TAREFAS INICIALIZADO ===")
        print("Banco de dados: tasks.db")
        print("Tabelas: users, tasks")
        print("Clean Architecture ✓")
        print("Padrões GoF implementados: Command, Strategy, Singleton")
        print("Princípios SOLID ✓")
        print("=======================================\n")
    
    return app


def register_blueprints(app: Flask, container: DependencyContainer):
    """Registra os blueprints com as rotas"""
    
    # Blueprint de autenticação
    auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
    
    @auth_bp.route('/login', methods=['GET'])
    def login_form():
        return container.auth_controller.show_login_form()
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        return container.auth_controller.login()
    
    @auth_bp.route('/register', methods=['GET'])
    def register_form():
        return container.auth_controller.show_register_form()
    
    @auth_bp.route('/register', methods=['POST'])
    def register():
        return container.auth_controller.register()
    
    @auth_bp.route('/logout')
    def logout():
        return container.auth_controller.logout()
    
    # Blueprint de tarefas
    tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')
    
    @tasks_bp.route('/')
    @tasks_bp.route('/dashboard')
    def dashboard():
        return container.task_controller.dashboard()
    
    @tasks_bp.route('/new', methods=['GET'])
    def new_task_form():
        return container.task_controller.show_create_form()
    
    @tasks_bp.route('/new', methods=['POST'])
    def create_task():
        return container.task_controller.create_task()
    
    @tasks_bp.route('/<int:task_id>/edit', methods=['GET'])
    def edit_task_form(task_id):
        return container.task_controller.show_edit_form(task_id)
    
    @tasks_bp.route('/<int:task_id>/edit', methods=['POST'])
    def update_task(task_id):
        return container.task_controller.update_task(task_id)
    
    @tasks_bp.route('/<int:task_id>/complete', methods=['POST'])
    def complete_task(task_id):
        return container.task_controller.complete_task(task_id)
    
    @tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
    def delete_task(task_id):
        return container.task_controller.delete_task(task_id)
    
    @tasks_bp.route('/undo', methods=['POST'])
    def undo_action():
        return container.task_controller.undo_action()
    
    @tasks_bp.route('/redo', methods=['POST'])
    def redo_action():
        return container.task_controller.redo_action()
    
    @tasks_bp.route('/api/stats')
    def get_stats():
        return container.task_controller.get_task_stats_api()
    
    # Rota raiz redireciona para dashboard
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('tasks.dashboard'))
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)


if __name__ == '__main__':
    app = create_app()
    print("\n=== INICIANDO APLICAÇÃO ===")
    print("Acesse: http://localhost:5000")
    print("===============================\n")
    # Desabilitar auto-reload para evitar loops
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000) 