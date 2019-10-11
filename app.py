import os

from dotenv import load_dotenv  # Uncomment if deploy to heroku
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from security import identity, authenticate

# Uncomment if deploy to heroku
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db'
)
app.secret_key = os.environ.get('APP_SECRET_KEY')

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

api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(StoreList, '/stores')
