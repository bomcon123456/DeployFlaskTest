from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float, required=True, help='This field is required.'
    )
    parser.add_argument(
        'store_id', type=float, required=True, help='This field is required.'
    )

    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message': 'Item is not found.'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'Item has already existed.'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        item.save_to_db()

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'message': 'This item is not existed.'}, 404
        item.delete_from_db()
        return {'message': 'Item has been deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
