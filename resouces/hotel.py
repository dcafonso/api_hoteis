from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from flask_jwt_extended import jwt_required
import sqlite3
from resouces.filtros import select, normalize_path_params


path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave]
                         for chave in dados if dados[chave] is not None}
        params = normalize_path_params(**dados_validos)

        values = tuple([params[chave] for chave in params])
        consulta = cursor.execute(select(com_cidade=False) if not params.get(
            'cidade') else select(com_cidade=True), values)

        hoteis = []

        for linha in consulta:
            hoteis.append({
                "hotel_id": linha[0],
                "nome": linha[1],
                "estrelas": linha[2],
                "diaria": linha[3],
                "cidade": linha[4],
                "site_id": linha[5],
            })

        return {'hoteis': hoteis}


class Hotel(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('nome', type=str, required=True,
                           help="The field 'Nome' cannot be left blank!")
    arguments.add_argument('estrelas')
    arguments.add_argument('diaria')
    arguments.add_argument('cidade')
    arguments.add_argument('site_id', type=int, required=True,
                           help="The field 'Site ID' cannot be left blank!")

    def get(self, hotel_id):
        obj_hotel = HotelModel.find_hotel(hotel_id)
        if obj_hotel:
            return obj_hotel.toJson()
        return {"message": "Hotel not found!"}, 404

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": f"Hotel ID ({hotel_id}) already exists!"}

        dados = Hotel.arguments.parse_args()

        if not SiteModel.find_by_id(dados.get('site_id')):
            return {"message": "Site ID not found!"}, 404

        obj_hotel = HotelModel(hotel_id, **dados)

        try:
            obj_hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel."}, 500

        return obj_hotel.toJson(), 200

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.arguments.parse_args()

        obj_hotel = HotelModel.find_hotel(hotel_id)
        if obj_hotel:
            obj_hotel.update_hotel(**dados)
            try:
                obj_hotel.save_hotel()
            except:
                return {"message": "An internal error ocurred trying to save hotel."}, 500
            return obj_hotel.toJson(), 200
        obj_hotel = HotelModel(hotel_id, **dados)
        try:
            obj_hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel."}, 500
        return obj_hotel.toJson(), 201

    @jwt_required
    def delete(self, hotel_id):
        obj_hotel = HotelModel.find_hotel(hotel_id)
        if obj_hotel:
            try:
                obj_hotel.delete_hotel()
            except:
                return {"message": "An internal error ocurred trying to delete hotel."}, 500
            return {"message": "Hotel deleted!"}
        return {"message": "Hotel not found!"}, 404
