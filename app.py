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

app = Flask(__name__)

app.config["SECRET_KEY"] = "sua_chave_secreta"
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
            return redirect(url_for("index"))

        flash("E-mail ou senha inválidos")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/perfil")
@login_required
def perfil():
    return render_template("perfil.html", usuario=current_user)


if __name__ == "__main__":
    app.run(debug=True)