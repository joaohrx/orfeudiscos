from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from banco import create
from models.user import Usuario
from models.disk import Disco
from models.pedido import Pedido

app = Flask(__name__)

app.config["SECRET_KEY"] = "surpresa"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orfeudiscos_database.db"

db.init_app(app)
create(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        if Usuario.query.filter_by(email=email).first():
            flash("E-mail já cadastrado")
            return redirect(url_for("cadastro"))

        usuario = Usuario(
            nome=nome,
            email=email,
            senha=generate_password_hash(senha),
        )

        db.session.add(usuario)
        db.session.commit()

        flash("Cadastro realizado com sucesso")
        return redirect(url_for("login"))

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for("discos"))

        flash("E-mail ou senha inválidos")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/discos")
@login_required
def discos():
    discos = Disco.query.all()
    return render_template(
        "discos.html",
        discos=discos
    )


@app.route("/disco/<int:id>")
@login_required
def disco(id):
    disco = Disco.query.get_or_404(id)
    return render_template(
        "disco.html",
        disco=disco
    )

@app.route("/comprar/<int:id>")
@login_required
def comprar(id):

    disco = Disco.query.get_or_404(id)

    pedido = Pedido(
        usuario_id=current_user.id,
        disco_id=disco.id,
        quantidade=1
    )

    db.session.add(pedido)
    db.session.commit()

    flash("Compra realizada com sucesso!")

    return redirect(url_for("perfil"))

@app.route("/perfil")
@login_required
def perfil():

    pedidos = Pedido.query.filter_by(
        usuario_id=current_user.id
    ).all()

    return render_template(
        "perfil.html",
        usuario=current_user,
        pedidos=pedidos
    )


if __name__ == "__main__":
    app.run(debug=True)