from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Enum as SQLEnum
from sqlalchemy.sql import func
import enum

# Singleton para instância do banco de dados
class DatabaseConnection:
    """Singleton para gerenciar a conexão com o banco de dados"""
    _instance = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._db = SQLAlchemy()
        return cls._instance
    
    @property
    def db(self):
        return self._db
    
    def init_app(self, app):
        """Inicializa o banco com a aplicação Flask"""
        self._db.init_app(app)


# Instância singleton do banco
db_connection = DatabaseConnection()
db = db_connection.db


# Enums para o banco de dados
class PriorityEnum(enum.Enum):
    LOW = "baixa"
    MEDIUM = "media"
    HIGH = "alta"
    URGENT = "urgente"


class TaskStatusEnum(enum.Enum):
    PENDING = "pendente"
    IN_PROGRESS = "em_progresso"
    COMPLETED = "concluida"
    CANCELLED = "cancelada"


# Modelos do banco de dados
class UserModel(db.Model):
    """Modelo de banco para usuários"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    # Relacionamento com tarefas
    tasks = db.relationship('TaskModel', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'


class TaskModel(db.Model):
    """Modelo de banco para tarefas"""
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(SQLEnum(PriorityEnum), nullable=False, default=PriorityEnum.MEDIUM)
    due_date = Column(Date)
    status = Column(SQLEnum(TaskStatusEnum), nullable=False, default=TaskStatusEnum.PENDING)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Foreign Key para usuário
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    def __repr__(self):
        return f'<Task {self.title} - {self.status.value}>' 