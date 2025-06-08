from flask import request, session, render_template, redirect, url_for, flash, jsonify
from typing import Optional, Dict, Any
from datetime import datetime, date
from domain.entities import Priority, TaskStatus
from application.use_cases import (
    CreateTaskUseCase, UpdateTaskUseCase, CompleteTaskUseCase,
    DeleteTaskUseCase, ListTasksUseCase, GetTaskStatsUseCase,
    RegisterUserUseCase, AuthenticateUserUseCase, UndoActionUseCase, RedoActionUseCase
)


class BaseController:
    """Controlador base com funcionalidades comuns"""
    
    def get_current_user_id(self) -> Optional[int]:
        """Obtém o ID do usuário atual da sessão"""
        return session.get('user_id')
    
    def require_authentication(self) -> Optional[tuple]:
        """Verifica se o usuário está autenticado, retorna redirecionamento se não estiver"""
        if not self.get_current_user_id():
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return None
    
    def parse_priority(self, priority_str: str) -> Priority:
        """Converte string para enum Priority"""
        priority_map = {
            'baixa': Priority.LOW,
            'media': Priority.MEDIUM,
            'alta': Priority.HIGH,
            'urgente': Priority.URGENT
        }
        return priority_map.get(priority_str, Priority.MEDIUM)
    
    def parse_date(self, date_str: str) -> Optional[date]:
        """Converte string para date, retorna None se inválida"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None


class AuthController(BaseController):
    """Controlador responsável pela autenticação"""
    
    def __init__(self, register_use_case: RegisterUserUseCase, auth_use_case: AuthenticateUserUseCase):
        self._register_use_case = register_use_case
        self._auth_use_case = auth_use_case
    
    def show_login_form(self):
        """Exibe o formulário de login"""
        return render_template('auth/login.html')
    
    def show_register_form(self):
        """Exibe o formulário de registro"""
        return render_template('auth/register.html')
    
    def login(self):
        """Processa o login do usuário"""
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        try:
            user = self._auth_use_case.execute(email, password)
            if user:
                session['user_id'] = user.id
                session['email'] = user.email
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('tasks.dashboard'))
            else:
                flash('Email ou senha inválidos.', 'error')
        except ValueError as e:
            flash(str(e), 'error')
        
        return render_template('auth/login.html')
    
    def register(self):
        """Processa o registro de novo usuário"""
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if password != confirm_password:
            flash('As senhas não coincidem.', 'error')
            return render_template('auth/register.html')
        
        try:
            self._register_use_case.execute(email, password)
            flash('Conta criada com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e), 'error')
        
        return render_template('auth/register.html')
    
    def logout(self):
        """Faz logout do usuário"""
        session.clear()
        flash('Você foi desconectado.', 'info')
        return redirect(url_for('auth.login'))


class TaskController(BaseController):
    """Controlador responsável pelas operações de tarefas"""
    
    def __init__(self, create_task_use_case: CreateTaskUseCase, 
                 update_task_use_case: UpdateTaskUseCase,
                 complete_task_use_case: CompleteTaskUseCase,
                 delete_task_use_case: DeleteTaskUseCase,
                 list_tasks_use_case: ListTasksUseCase,
                 get_stats_use_case: GetTaskStatsUseCase,
                 undo_use_case: UndoActionUseCase,
                 redo_use_case: RedoActionUseCase):
        self._create_task_use_case = create_task_use_case
        self._update_task_use_case = update_task_use_case
        self._complete_task_use_case = complete_task_use_case
        self._delete_task_use_case = delete_task_use_case
        self._list_tasks_use_case = list_tasks_use_case
        self._get_stats_use_case = get_stats_use_case
        self._undo_use_case = undo_use_case
        self._redo_use_case = redo_use_case
    
    def dashboard(self):
        """Exibe o dashboard com lista de tarefas"""
        auth_check = self.require_authentication()
        if auth_check:
            return auth_check
        
        user_id = self.get_current_user_id()
        filter_type = request.args.get('filter', 'all')
        sort_type = request.args.get('sort', 'creation_date')
        
        try:
            tasks = self._list_tasks_use_case.execute(user_id, filter_type, sort_type)
            stats = self._get_stats_use_case.execute(user_id)
            
            # Obter a saudação baseada na hora
            current_hour = datetime.now().hour
            if current_hour < 12:
                greeting = 'Bom dia'
            elif current_hour < 18:
                greeting = 'Boa tarde'
            else:
                greeting = 'Boa noite'
            
            return render_template('tasks/dashboard.html', 
                                 tasks=tasks, 
                                 stats=stats,
                                 filter=filter_type,
                                 sort=sort_type,
                                 greeting=greeting,
                                 current_user_email=session.get('email'))
        except Exception as e:
            flash(f'Erro ao carregar tarefas: {str(e)}', 'error')
            return render_template('tasks/dashboard.html', tasks=[], stats={})
    
    def show_create_form(self):
        """Exibe o formulário de criação de tarefa"""
        auth_check = self.require_authentication()
        if auth_check:
            return auth_check
        
        return render_template('tasks/form.html')
    
    def create_task(self):
        """Cria uma nova tarefa"""
        auth_check = self.require_authentication()
        if auth_check:
            return auth_check
        
        user_id = self.get_current_user_id()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = self.parse_priority(request.form.get('priority', 'media'))
        due_date = self.parse_date(request.form.get('due_date', ''))
        
        try:
            self._create_task_use_case.execute(title, description, priority, due_date, user_id)
            flash('Tarefa criada com sucesso!', 'success')
            return redirect(url_for('tasks.dashboard'))
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('tasks/form.html', 
                                 title=title, 
                                 description=description,
                                 priority=priority.value if priority else None,
                                 due_date=due_date)
    
    def show_edit_form(self, task_id: int):
        """Exibe o formulário de edição de tarefa"""
        auth_check = self.require_authentication()
        if auth_check:
            return auth_check
        
        # Aqui você precisaria buscar a tarefa para preencher o formulário
        # Por simplicidade, vou apenas renderizar o template
        return render_template('tasks/form.html', task_id=task_id, is_edit=True)
    
    def update_task(self, task_id: int):
        """Atualiza uma tarefa existente"""
        auth_check = self.require_authentication()
        if auth_check:
            return auth_check
        
        user_id = self.get_current_user_id()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = self.parse_priority(request.form.get('priority', 'media'))
        due_date = self.parse_date(request.form.get('due_date', ''))
        
        try:
            self._update_task_use_case.execute(task_id, user_id, title, description, priority, due_date)
            flash('Tarefa atualizada com sucesso!', 'success')
            return redirect(url_for('tasks.dashboard'))
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('tasks/form.html', 
                                 task_id=task_id, 
                                 is_edit=True,
                                 title=title, 
                                 description=description,
                                 priority=priority.value if priority else None,
                                 due_date=due_date)
    
    def complete_task(self, task_id: int):
        """Marca uma tarefa como concluída"""
        auth_check = self.require_authentication()
        if auth_check:
            return auth_check
        
        user_id = self.get_current_user_id()
        
        try:
            self._complete_task_use_case.execute(task_id, user_id)
            return jsonify({'success': True, 'message': 'Tarefa marcada como concluída!'})
        except ValueError as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    def delete_task(self, task_id: int):
        """Remove uma tarefa"""
        auth_check = self.require_authentication()
        if auth_check:
            return auth_check
        
        user_id = self.get_current_user_id()
        
        try:
            self._delete_task_use_case.execute(task_id, user_id)
            flash('Tarefa removida com sucesso!', 'success')
        except ValueError as e:
            flash(str(e), 'error')
        
        return redirect(url_for('tasks.dashboard'))
    
    def undo_action(self):
        """Desfaz a última ação"""
        auth_check = self.require_authentication()
        if auth_check:
            return auth_check
        
        try:
            success = self._undo_use_case.execute()
            if success:
                return jsonify({'success': True, 'message': 'Ação desfeita com sucesso!'})
            else:
                return jsonify({'success': False, 'message': 'Nenhuma ação para desfazer'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    def redo_action(self):
        """Refaz uma ação"""
        auth_check = self.require_authentication()
        if auth_check:
            return auth_check
        
        try:
            success = self._redo_use_case.execute()
            if success:
                return jsonify({'success': True, 'message': 'Ação refeita com sucesso!'})
            else:
                return jsonify({'success': False, 'message': 'Nenhuma ação para refazer'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    def get_task_stats_api(self):
        """API para obter estatísticas das tarefas"""
        auth_check = self.require_authentication()
        if auth_check:
            return jsonify({'error': 'Authentication required'}), 401
        
        user_id = self.get_current_user_id()
        
        try:
            stats = self._get_stats_use_case.execute(user_id)
            return jsonify(stats)
        except Exception as e:
            return jsonify({'error': str(e)}), 500 