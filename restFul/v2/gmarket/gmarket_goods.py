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

        response = Utils().makeResponse(StrRepository().error_system)

        if post_type == "excel":
            response = GmarketGoodsService.goods_api(params)

        if post_type == "market":
            response = GmarketGoodsService.market_api(params)

        return response

    def put(self):
        post_type = request.values.get('type')
        params = request.json

        response = Utils().makeResponse(StrRepository().error_system)

        if post_type == "market":
            response = GmarketGoodsService.market_api(params)

        elif post_type == "official":
            response = GmarketGoodsService.official_api(params)

        elif post_type == "coupon":
            response = GmarketGoodsService.coupon_market_api(params)

        elif post_type == "price":
            response = GmarketGoodsService.price_api(params)

        elif post_type == "premium":
            response = GmarketGoodsService.premium_api(params)
        return response
