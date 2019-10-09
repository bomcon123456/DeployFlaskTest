from db import db
from app import app

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()  # create the data.db unless it's already existed
