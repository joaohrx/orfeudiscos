from flask import Flask, render_template, request
from database import db
from banco import create
from models.user import Usuario

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orfeudiscos_database.db"
db.init_app(app)
create(app)
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/cadastro', methods = ["GET", "POST"])
def cadastro():

    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        
        user = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(user)
        db.session.commit()
    return render_template("cadastro.html")    
        
        

@app.route('/login')
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)