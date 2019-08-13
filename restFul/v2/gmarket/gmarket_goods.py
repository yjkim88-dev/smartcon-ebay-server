from flask_restful import Resource
from flask import request
from restFul.utils import Utils
from restFul.repository import StrRepository
from .gmarket_goods_service import GmarketGoodsService

class GmarketGoods(Resource):
    def get(self):
        print('hi')
        pass

    def post(self):
        post_type = request.values.get('type')
        params = request.json

        if post_type == "excel":
            response = GmarketGoodsService.postExcelGoods(params)

        if post_type == "goods":
            pass

        return response


        pass

    def put(self):
        pass

    def delete(self):
        pass