from database import db

class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    disco_id = db.Column(
        db.Integer,
        db.ForeignKey("discos.id"),
        nullable=False
    )

    quantidade = db.Column(db.Integer, nullable=False, default=1)

    usuario = db.relationship("Usuario", backref="pedidos")
    disco = db.relationship("Disco")