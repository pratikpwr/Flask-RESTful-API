import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel


# noinspection PyBroadException
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field can not be blank")
    parser.add_argument('password', type=str, required=True, help="This field can not be blank")

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User already exists, Use different username.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": 'User Created Successfully'}, 201
        # try:
        #     connection = sqlite3.connect('data.db')
        #     cursor = connection.cursor()
        #
        #     query = "INSERT INTO users VALUES (NULL, ?, ?)"
        #     cursor.execute(query, (data['username'], data['password']))
        #
        #     connection.commit()
        #     connection.close()
        # except:
        #     return {'message': 'An error occurred.'}, 500
