from flask_restful import Resource
from flask import request
from .gmarket_goods_service import GmarketGoodsService

class GmarketGoods(Resource):
    def get(self):
        print('hi')
        pass

    def post(self):
        post_type = request.values.get('type')
        if post_type == "excel":
            params = request.json
            GmarketGoodsService.postGoodsBundle(params)



        pass

    def put(self):
        pass

    def delete(self):
        pass