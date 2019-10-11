import os

from dotenv import load_dotenv  # Uncomment if deploy to heroku
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import identity, authenticate
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister

# Uncomment if deploy to heroku
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db'
)
app.secret_key = 'TopSecretKey'


@app.before_first_request
def create_tables():
    db.create_all()  # create the data.db unless it's already existed


api = Api(app, errors={
    'JWTError': {
        'status': 401,
        'message': 'Session is over. Please sign in again',
        'err_code': 'token_expired'
    },
    'Exception': {
        'status': 500,
        'message': 'Sorry, something bad has happened.',
        'err_code': 'internal_server_error'
    }
})
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__':
    from db import db

    db.init_app(app)

    app.run(port=5000)
