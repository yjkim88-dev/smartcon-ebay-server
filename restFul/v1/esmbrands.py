
#_*_ coding: utf-8 _*_

from flask import request
from flask_restful import Resource
from restFul.repository import StrRepository
from restFul.utils import Utils
from B2C.gmarket.esm_brands_api import EsmBrandsApis
from Logger import Logger

class EsmBrands(Resource):
    # 조회
    def get(self):
        Logger.logger.info ('get--')
        try:
            brand_name = request.args.get('brand_name')

            soap = EsmBrandsApis().searchEsmBrand(brand_name)
            Logger.logger.info(soap)

            response = soap.find('addmakerbrandresponse')
            item_results = response.findChildren('addmakerbrandresult')

            Logger.logger.info (item_results)
            ret_list = []
            for result in item_results:
                ret_obj = {
                    'maker_name': result['makername'],
                    'brand_name': result['brandname'],
                    'maker_no': result['makerno'],
                    'brand_no': result['brandno'],
                    'result': result['result'],
                    'comment': result['comment']
                }
                ret_list.append(ret_obj)

            return Utils().makeResponse(StrRepository().error_none, ret_list)

        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)