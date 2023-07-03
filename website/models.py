from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    permission = db.Column(db.Integer)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(30))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    expenses = db.relationship('Expense', backref='user')
    permissions = db.relationship('Permission', foreign_keys=[Permission.owner_id], backref='owner')
    guest_permissions = db.relationship('Permission', foreign_keys=[Permission.guest_id], backref='guest')
    categories = db.relationship('Category', backref='user', lazy='dynamic')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    expenses = db.relationship('Expense', backref='category')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.String(10))
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    value = db.Column(db.Float)
    is_installment = db.Column(db.Boolean)
    installment_count = db.Column(db.Integer)
    installment_value = db.Column(db.Float)
    due_date = db.Column(db.String(10), default=None)
    name = db.Column(db.String(100))
    comment = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

