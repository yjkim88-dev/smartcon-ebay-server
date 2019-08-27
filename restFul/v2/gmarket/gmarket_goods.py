from .gmarket_goods_service import GmarketGoodsService
from restFul.repository import StrRepository
from flask_restful import Resource
from restFul.utils import Utils
from flask import request
from Logger import Logger



class GmarketGoods(Resource):
    def get(self):
        Logger.logger.info("[GET] gmarket goods")
        try:
            params = request.args
            gmkt_goods_result = GmarketGoodsService.mysql_fetch_goods(params)
            if gmkt_goods_result.get('errorCode') != "00":
                return Utils().makeResponse((StrRepository().error_system))
        except BaseException as e:
            Logger.logger.info('[GET] GmarketGoods Faild')
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
        return gmkt_goods_result


    def post(self):
        post_type = request.values.get('type')
        params = request.json

        response = Utils().makeResponse(StrRepository().error_system)

        if post_type == "excel":
            response = GmarketGoodsService.goods_api(params)

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
