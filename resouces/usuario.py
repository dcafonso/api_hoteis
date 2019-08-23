from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
import traceback
from flask import make_response, render_template


arguments = reqparse.RequestParser()
arguments.add_argument('login', type=str, required=True,
                       help="The field 'Login' cannot be left blank!")
arguments.add_argument('senha', type=str, required=True,
                       help="The field 'Senha' cannot be left blank")
arguments.add_argument('email', type=str)
arguments.add_argument('ativado', type=bool)


class User(Resource):
    def get(self, user_id):
        obj_user = UserModel.find_user(user_id)
        if obj_user:
            return obj_user.toJson()
        return {"message": "User not found!"}, 404

    @jwt_required
    def delete(self, user_id):
        obj_user = UserModel.find_user(user_id)
        if obj_user:
            try:
                obj_user.delete_user()
            except:
                return {"message": "An internal error ocurred trying to delete user."}, 500
            return {"message": "User deleted!"}
        return {"message": "User not found!"}, 404


class UserRegister(Resource):
    def post(self):
        dados = arguments.parse_args()

        if not dados.get('email') or dados.get('email') is None:
            return {"message": "The field 'E-mail' cannot be left blank!"}, 400

        if UserModel.find_by_email(dados['email']):
            return {"message": f"E-mail ({dados['email']}) already exists!"}, 400

        if UserModel.find_by_login(dados['login']):
            return {"message": f"User ({dados['login']}) already exists!"}, 400

        obj_user = UserModel(**dados)
        obj_user.ativado = False
        try:
            obj_user.save_user()
            obj_user.send_confirmation_email()
        except:
            obj_user.delete_user()
            traceback.print_exc()
            return {"message": "An internal error ocurred trying to save user."}, 500
        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = arguments.parse_args()

        obj_user = UserModel.find_by_login(dados['login'])
        if obj_user and safe_str_cmp(obj_user.senha, dados['senha']):
            if obj_user.ativado:
                access_token = create_access_token(identity=obj_user.user_id)
                return {"access_token": access_token}, 200
            return {"message": "The User is not activated!"}, 400
        return {"message": "The User or Password is incorrect!"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {"message": "Logged out successfully!"}, 200


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {"message": "User not found!"}, 404

        user.ativado = True
        user.save_user()

        header = {"Content-Type": "text/html"}
        return make_response(render_template('user_confirm.html', email=user.email, usuario=user.login), 200, header)
