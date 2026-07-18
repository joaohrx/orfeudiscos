from database import db

class Disco(db.Model):
    __tablename__ = "discos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Numeric(10,2), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    imagem = db.Column(db.String(100), nullable=False)