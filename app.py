from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
# from flask_login import LoginManager, current_user, login_user, logout_user
from models.person import db, Person
from models.user import User
from models.habit import Habit, HabitCheckIn
from datetime import datetime, timedelta
from dotenv import load_dotenv
from functools import wraps
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change')
# Configurando SQLite como banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cadastro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()
    print("\n=== BANCO DE DADOS INICIALIZADO ===")
    print("Banco de dados: cadastro.db")
    print("Tabelas: people, users, habits, habit_check_ins")
    print(f"Objeto do banco de dados: {db}")
    print("===============================\n")

# Decorator para proteger rotas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Filter for current_user in templates
@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return dict(current_user=user)

# Filtros personalizados para templates
@app.template_filter('category_color')
def category_color(category):
    colors = {
        'physical': 'success',
        'mental': 'info',
        'social': 'primary',
        'productivity': 'warning'
    }
    return colors.get(category, 'secondary')

@app.template_filter('frequency_label')
def frequency_label(frequency):
    labels = {
        'daily': 'Diário',
        'weekly': 'Semanal',
        'weekdays': 'Dias Úteis',
        'weekends': 'Fins de Semana'
    }
    return labels.get(frequency, frequency)

@app.template_filter('time')
def format_time(time):
    return time.strftime('%H:%M') if time else '-'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print("\n=== TENTATIVA DE LOGIN ===")
        print(f"Email: {email}")
        print("===============================\n")

        user = User.get_by_email(email)
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['email'] = user.email # Keep email in session for display
            # login_user(user)
            print(f"Login bem-sucedido para: {email}")
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        
        print(f"Falha no login para: {email}")
        flash('E-mail ou senha inválidos.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        print("\n=== TENTATIVA DE REGISTRO ===")
        print(f"Email: {email}")
        print("===============================\n")

        if password != confirm_password:
            flash('As senhas não coincidem.', 'error')
            return render_template('register.html')

        if User.get_by_email(email):
            flash('Este e-mail já está em uso.', 'error')
            return render_template('register.html')

        try:
            user = User(email=email, password=password)
            db.session.add(user)
            db.session.commit()
            print(f"Usuário registrado com sucesso: {email}")
            flash('Conta criada com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao registrar usuário: {str(e)}")
            flash('Erro ao criar conta. Tente novamente.', 'error')

    return render_template('register.html')

@app.route('/logout')
def logout():
    # logout_user()
    if 'user_id' in session:
        print(f"\n=== LOGOUT ===")
        print(f"Usuário: {session.get('email')}")
        print("===============================\n")
    session.clear()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        # Should not happen if login_required works correctly, but as a fallback
        flash('Erro ao carregar dados do usuário.', 'error')
        return redirect(url_for('logout'))

    # Obter filtros
    filter_value = request.args.get('filter', 'all')

    # Buscar hábitos do usuário com base no filtro
    habits_query = Habit.query.filter_by(user_id=user_id)

    if filter_value != 'all':
        if filter_value in ['completed', 'pending']:
            # Filtering based on check-ins requires joining or separate queries
            # For simplicity based on current structure, let's assume habits
            # are marked as completed if they have a check-in for today.
            today = datetime.now().date()
            checked_habit_ids = [ci.habit_id for ci in HabitCheckIn.get_by_user_and_date(user_id, today)]
            
            if filter_value == 'completed':
                habits_query = habits_query.filter(Habit.id.in_(checked_habit_ids))
            elif filter_value == 'pending':
                habits_query = habits_query.filter(Habit.id.notin_(checked_habit_ids))
        else:
            # Assume filter_value is a category
            habits_query = habits_query.filter_by(category=filter_value)

    habits = habits_query.all()

    # Adicionar status de checked_today para cada hábito
    today = datetime.now().date()
    today_check_ins = {ci.habit_id for ci in HabitCheckIn.get_by_user_and_date(user_id, today)}
    for habit in habits:
        habit.checked_today = habit.id in today_check_ins

    # Calcular estatísticas
    total_habits = Habit.query.filter_by(user_id=user_id).count()
    today_completed = len([h for h in habits if h.checked_today])
    today_total = len(habits) # Note: This counts habits shown based on filter, might need adjustment depending on desired stat logic
    
    # Calcular taxa de conclusão geral (exemplo simplificado)
    all_check_ins_count = HabitCheckIn.query.join(Habit).filter(Habit.user_id == user_id).count()
    all_possible_check_ins = total_habits # This is too simple, needs logic based on frequency over time
    # A more accurate completion rate would need date range and frequency logic
    completion_rate = (all_check_ins_count / all_possible_check_ins * 100) if all_possible_check_ins > 0 else 0

    stats = {
        'total_habits': total_habits,
        'today_completed': today_completed,
        'today_total': total_habits, # Use total_habits for overall stat
        'completion_rate': completion_rate,
        # TODO: Implement weekly_rate, current_streak, longest_streak more accurately
    }
    
    # Obter categorias únicas para filtros
    # TODO: Fetch actual categories from user's habits or a predefined list
    categories = ['Saúde', 'Estudos', 'Pessoal', 'Trabalho', 'Exercício'] # Example categories

    # Obter a saudação baseada na hora
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = 'Bom dia'
    elif current_hour < 18:
        greeting = 'Boa tarde'
    else:
        greeting = 'Boa noite'

    return render_template('dashboard.html', 
                         user=user, # Pass the user object
                         habits=habits,
                         stats=stats,
                         filter=filter_value,
                         categories=categories,
                         greeting=greeting)

@app.route('/habits/new', methods=['GET', 'POST'])
@login_required
def new_habit():
    categories = ['Saúde', 'Estudos', 'Pessoal', 'Trabalho', 'Exercício'] # Lista de categorias

    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            category = request.form['category']
            frequency = request.form['frequency']
            ideal_time = datetime.strptime(request.form['ideal_time'], '%H:%M').time() if request.form['ideal_time'] else None

            habit = Habit(
                name=name,
                description=description,
                category=category,
                frequency=frequency,
                ideal_time=ideal_time,
                user_id=session['user_id']
            )
            db.session.add(habit)
            db.session.commit()

            flash('Hábito criado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar hábito: {str(e)}', 'error')
             # Render form again with data and messages
            return render_template('habit_form.html', categories=categories,
                                   name=request.form.get('name', ''), description=request.form.get('description', ''),
                                   category=request.form.get('category', ''), frequency=request.form.get('frequency', ''),
                                   idealTime=request.form.get('ideal_time', ''))

    # GET request
    return render_template('habit_form.html', categories=categories)

@app.route('/habits/<int:habit_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_habit(habit_id):
    categories = ['Saúde', 'Estudos', 'Pessoal', 'Trabalho', 'Exercício'] # Lista de categorias

    habit = Habit.query.get(habit_id)

    if not habit or habit.user_id != session['user_id']:
        flash('Hábito não encontrado.', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        try:
            habit.name = request.form['name']
            habit.description = request.form['description']
            habit.category = request.form['category']
            habit.frequency = request.form['frequency']
            habit.ideal_time = datetime.strptime(request.form['ideal_time'], '%H:%M').time() if request.form['ideal_time'] else None

            db.session.commit()

            flash('Hábito atualizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar hábito: {str(e)}', 'error')
             # Render form again with data and messages
            return render_template('habit_form.html', habit=habit, categories=categories)

    # GET request
    return render_template('habit_form.html', habit=habit, categories=categories)

@app.route('/habits/<int:habit_id>/delete', methods=['POST'])
@login_required
def delete_habit(habit_id):
    habit = Habit.get_by_id(habit_id)
    
    if not habit or habit.user_id != session['user_id']:
        flash('Hábito não encontrado.', 'error')
        return redirect(url_for('dashboard'))

    try:
        habit.delete()
        flash('Hábito excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir hábito: {str(e)}', 'error')

    return redirect(url_for('dashboard'))

@app.route('/habits/<int:habit_id>/check-in', methods=['POST'])
@login_required
def check_in_habit(habit_id):
    habit = Habit.get_by_id(habit_id)
    
    if not habit or habit.user_id != session['user_id']:
        return jsonify({'error': 'Hábito não encontrado'}), 404

    try:
        notes = request.form.get('notes')
        check_in = HabitCheckIn(habit_id=habit_id, notes=notes)
        check_in.save()
        
        return jsonify({
            'success': True,
            'message': 'Check-in realizado com sucesso!',
            'check_in': check_in.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n=== INICIANDO APLICAÇÃO ===")
    print("Acesse: http://localhost:5000")
    print("===============================\n")
    app.run(debug=True) 