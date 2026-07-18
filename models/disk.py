from database import db
from flask_login import UserMixin

class Disco(UserMixin,db.Model):
    __tablename__ = "discos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Numeric, nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    