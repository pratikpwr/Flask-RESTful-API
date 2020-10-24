from flask_restful import Resource
from models.store_model import StoreModel


class Store(Resource):

    @staticmethod
    def get(name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Store not Found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'Store with name {} already exists'.format(name)}, 404
        new_store = StoreModel(name)
        new_store.save_to_db()
        return new_store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {'message': 'Store {} does not exists.'.format(name)}, 400

        store.delete_from_db()
        return {'message': 'Store {} removed'.format(name)}, 200


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
