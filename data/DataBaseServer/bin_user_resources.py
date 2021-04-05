from flask_restful import Resource, abort
from flask import jsonify, request, make_response

from data import ConverterObj
from data.__all_models import User
from data.DataBaseServer import DataBase


class BinUserResource(Resource):

    def get(self):
        db_session = DataBase.create_session()
        if request.json and 'email' in request.json:
            email = request.json['email']
            abort_if_user_not_found(email)
            user = db_session.query(User).filter(User.email == email).first()
            return jsonify(ConverterObj.encode(user))
            # return make_response(jsonify({'error': "No user in the system"}))
        else:
            return make_response(jsonify({'error': "No email in the request"}), 400)


def abort_if_user_not_found(email):
    session = DataBase.create_session()
    user = session.query(User.email == email).first()
    if not user[0]:
        abort(404, message=f"User {email} not found")