from database import db
from models import *
from models.disk import Disco

def create(app):
    with app.app_context():
        db.create_all()

        if Disco.query.count() == 0:
            discos = [
                Disco(
                    nome="Abbey Road",
                    preco=219.90,
                    descricao="Álbum clássico dos Beatles lançado em 1969.",
                    imagem="abbeyroad.jpeg"
                ),
                Disco(
                    nome="Thriller",
                    preco=189.90,
                    descricao="Álbum de Michael Jackson.",
                    imagem="thriller.jpg"
                ),
                Disco(
                    nome="Nevermind",
                    preco=179.90,
                    descricao="Clássico do Nirvana.",
                    imagem="nevermind.jpeg"
                ),
                Disco(
                    nome="OK Computer",
                    preco=199.90,
                    descricao="Segundo melhor álbum dos Radioheads.",
                    imagem="okcomputa.jpg"
                ),
                Disco(
                    nome="The Dark Side of the Moon",
                    preco=249.90,
                    descricao="Obra-prima do Pink Floyd.",
                    imagem="dsotm.jpg"
                ),
            ]

            db.session.add_all(discos)
            db.session.commit()