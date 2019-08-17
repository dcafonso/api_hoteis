from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required


class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.toJson() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('nome', type=str, required=True,
                           help="The field 'Nome' cannot be left blank!")
    arguments.add_argument('estrelas')
    arguments.add_argument('diaria')
    arguments.add_argument('cidade')

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
