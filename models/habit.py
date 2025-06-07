from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models.person import db

class Habit(db.Model):
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ideal_time = db.Column(db.Time)  # Horário ideal para realizar o hábito
    frequency = db.Column(db.String(20), nullable=False)  # 'daily', 'weekly', 'weekdays', 'weekends'
    category = db.Column(db.String(50))  # 'physical', 'mental', 'social', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relacionamento com o usuário
    user = db.relationship('User', backref=db.backref('habits', lazy=True))
    
    # Relacionamento com os check-ins
    check_ins = db.relationship('HabitCheckIn', backref='habit', lazy=True, cascade='all, delete-orphan')

    def __init__(self, name, description, ideal_time, frequency, category, user_id):
        self.name = name
        self.description = description
        self.ideal_time = ideal_time
        self.frequency = frequency
        self.category = category
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'ideal_time': self.ideal_time.strftime('%H:%M') if self.ideal_time else None,
            'frequency': self.frequency,
            'category': self.category,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id
        }

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_by_category(cls, category):
        return cls.query.filter_by(category=category).all()

class HabitCheckIn(db.Model):
    __tablename__ = 'habit_check_ins'

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    check_in_time = db.Column(db.Time, nullable=False, default=datetime.utcnow().time)
    notes = db.Column(db.Text)

    def __init__(self, habit_id, notes=None):
        self.habit_id = habit_id
        self.notes = notes

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'habit_id': self.habit_id,
            'check_in_date': self.check_in_date.strftime('%Y-%m-%d'),
            'check_in_time': self.check_in_time.strftime('%H:%M:%S'),
            'notes': self.notes
        }

    @classmethod
    def get_by_habit_and_date(cls, habit_id, date):
        return cls.query.filter_by(habit_id=habit_id, check_in_date=date).first()

    @classmethod
    def get_by_habit(cls, habit_id):
        return cls.query.filter_by(habit_id=habit_id).order_by(cls.check_in_date.desc()).all()

    @classmethod
    def get_by_user_and_date(cls, user_id, date):
        return cls.query.join(Habit).filter(
            Habit.user_id == user_id,
            HabitCheckIn.check_in_date == date
        ).all() 