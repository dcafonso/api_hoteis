from flask_restful import Resource, reqparse
from models.site import SiteModel


class Sites(Resource):
    def get(self):
        return {"sites": [site.toJson() for site in SiteModel.query.all()]}


class Site(Resource):
    def get(self, url):
        if SiteModel.find_site(url):
            return SiteModel.find_site(url).toJson()
        return {"message": "Site not found!"}, 404

    def post(self, url):
        if SiteModel.find_site(url):
            return {"message": f"The Site ({url}) already exists!"}, 400
        obj_site = SiteModel(url)
        try:
            obj_site.save_site()
        except:
            return {"message": "An internal error ocurred trying to save site."}, 500
        return obj_site.toJson()

    def delete(self, url):
        obj_site = SiteModel.find_site(url)
        if obj_site:
            try:
                obj_site.delete_site()
            except:
                return {"message": "An internal error ocurred trying to delete site."}, 500
            return {"message": "Site deleted!"}
        return {"message": "Site not found!"}, 404
