from flask_restful import Resource
from flask import request
from restFul.utils import Utils
from .gmarket_goods_service import GmarketGoodsService

class GmarketGoods(Resource):
    def get(self):
        print('hi')
        pass

    def post(self):
        post_type = request.values.get('type')
        params = request.json

        if post_type == "excel":
            code, result = GmarketGoodsService.postExcelGoods(params)

        if post_type == "goods":
            pass
        return Utils().makeResponse(code, result)


        pass

    def put(self):
        pass

    def delete(self):
        pass