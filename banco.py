from database import db
from models import *
def create(app):
 with app.app_context():
    db.create_all()