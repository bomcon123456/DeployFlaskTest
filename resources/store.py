from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store is not found.'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'Store has already existed.'}, 400
        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {'message': 'Failed to create store.'}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store has been deleted.'}
        else:
            return {'message': 'Store is not found.'}, 404


class StoreList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('page', type=int, location='args', default=1)
    parser.add_argument('size', type=int, location='args', default=5)

    def get(self):
        data = StoreList.parser.parse_args()

        # paginate(page,size,flag), flag == False return [] if empty
        res = [store.json() for store in StoreModel.query.paginate(
            data['page'], data['size'], False).items]
        return {'stores': res}
