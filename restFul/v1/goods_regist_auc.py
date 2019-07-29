#_*_ coding: utf-8 _*_

from flask import request
from flask_restful import Resource
from restFul.repository import StrRepository

from B2C.goods_regist_auc_dao import GoodsRegistAucDao
from restFul.utils import Utils
from Logger import Logger

class GoodsRegistAuc(Resource):
    # 상품등록
    def post(self):
        Logger.logger.info ('regist goods auc')

        try:
            args = request.json
            GoodsRegistAucDao().insertEventGoods(args.get('event_id'), args.get('goods_id'), args.get('auc_item_no'))

            return Utils().makeResponse(StrRepository().error_none)

        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)

