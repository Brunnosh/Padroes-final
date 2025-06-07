from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailNotValidError
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(128))

    def __init__(self, name, email, age, password=None):
        self.name = name
        self.email = email
        self.age = age
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_email(email):
        try:
            # Validate and normalize email
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError as e:
            raise ValueError(str(e))

    def save(self):
        try:
            # Validate email before saving
            self.email = self.validate_email(self.email)
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Este e-mail já está cadastrado.")
        except ValueError as e:
            db.session.rollback()
            raise e

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id) 