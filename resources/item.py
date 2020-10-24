import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel


# noinspection PyBroadException
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=int,
                        required=True,
                        help='This Field can not be empty.'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='This Field can not be empty.'
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 201
        return {'message': 'Item not Found'}, 404

    def post(self, name):
        # checks item already available or not
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': 'Item with name {} already exists.'.format(name)}, 400

        # add new item
        data = self.parser.parse_args()
        new_item = ItemModel(name, data['price'], data['store_id'])

        try:
            new_item.save_to_db()
            # new_item.add_new_item()
        except:
            return {'message': 'An error occurred.'}, 500

        return new_item.json(), 201

    @staticmethod
    def delete(name):
        # checks item already available or not
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'message': 'item {} does not exists.'.format(name)}, 400

        # delete item from database
        try:
            item.delete_from_db()
        except:
            return {'message': 'An error occurred.'}, 500

        return {'message': 'Item {} removed'.format(name)}, 200

    def put(self, name):
        data = self.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json(), 201


# noinspection PyBroadException
class ItemList(Resource):
    @staticmethod
    def get():
        # list(map(lambda x: x.json(), ItemModel.query.all()))
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200
