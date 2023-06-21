from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(30))
    expenses = db.relationship('Expense', backref='user')
    permissions = db.relationship('Permission', backref='user')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    expenses = db.relationship('Expense', backref='category')


class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.String(10))
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    value = db.Column(db.Float)
    is_installment = db.Column(db.Boolean)
    installment_count = db.Column(db.Integer)
    name = db.Column(db.String(100))
    comment = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    installments = db.relationship('Installment', backref='expense')


class Installment(db.Model):
    __tablename__ = 'installments'
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'))
    installment_number = db.Column(db.Integer)
    value = db.Column(db.Float)
    due_date = db.Column(db.String(10))


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    permission = db.Column(db.Integer)
