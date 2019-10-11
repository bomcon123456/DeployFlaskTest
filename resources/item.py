from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float, required=True
    )
    parser.add_argument(
        'store_id', type=float, required=True
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

        item = ItemModel(name=name, **data)
        item.save_to_db()

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'message': 'Item is not found.'}, 404
        item.delete_from_db()
        return {'message': 'Item has been deleted.'}

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
    parser = reqparse.RequestParser()
    parser.add_argument('page', type=int, location='args', default=1)
    parser.add_argument('size', type=int, location='args', default=5)

    def get(self):
        data = ItemList.parser.parse_args()
        paginator = ItemModel.query.paginate(
            data['page'], data['size'], False)

        res = [item.json() for item in paginator.items]
        return {
            'items': res,
            'currentPage': paginator.page,
            'perPage': paginator.per_page,
            'total': paginator.total
        }
