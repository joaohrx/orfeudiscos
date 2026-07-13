from database import db
def create(app):
 with app.app_context():
    db.create_all()