#_*_ coding: utf-8 _*_

from flask import request
from flask_restful import Resource
from restFul.repository import StrRepository

from B2C.gmarket.goods_regist_api import GoodsRegistApis
from B2C.goods_regist_dao import GoodsRegistDao
from B2C.images_dao import ImagesDao
from restFul.utils import Utils
from Logger import Logger

class GoodsRegist(Resource):
    def get(self):
        Logger.logger.info('get goods')
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            item_no = request.args.get('item_no')

            goods = GoodsRegistDao().selectGoods(start_date, end_date, item_no)
            Logger.logger.info (goods)

            if (len(goods) <= 0):
                return Utils().makeResponse(StrRepository().error_nothing_goods)
            else:
                ret_list = []
                for item in goods:
                    ret_obj = {
                        'price': item['PRICE'],
                        'create_date': str(item['CREATE_DATE']),
                        'modify_date': str(item['MODIFY_DATE']),
                        'use_information': item['USE_INFORMATION'],
                        'auto_term_duration': item['AUTO_TERM_DURATION'],
                        'help_desk_telno': item['HELP_DESK_TELNO'],
                        'large_image': item['LARGE_IMAGE'],
                        'small_image': item['SMALL_IMAGE'],
                        'default_image': item['DEFAULT_IMAGE'],
                        'shipping_group_code': item['SHIPPING_GROUP_CODE'],
                        'expiration_date': str(item['EXPIRATION_DATE']),
                        'apply_place': item['APPLY_PLACE'],
                        'item_no': item['ITEM_NO'],
                        'stock_qty': item['STOCK_QTY'],
                        'item_name': item['ITEM_NAME'],
                        'apply_place_telephone': item['APPLY_PLACE_TELEPHONE'],
                        'gd_html': item['GD_HTML'],
                        'out_item_no': item['OUT_ITEM_NO'],
                        'maker_no': item['MAKER_NO'],
                        'display_date': str(item['DISPLAY_DATE']),
                        'apply_place_url': item['APPLY_PLACE_URL'],
                        'auto_use_term_duration': item['AUTO_USE_TERM_DURATION'],
                        'category_code': item['CATEGORY_CODE']
                    }
                    ret_list.append(ret_obj)

                return Utils().makeResponse(StrRepository().error_none, ret_list)

        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)

    # 상품등록
    def post(self):
        Logger.logger.info ('regist goods')
        try:
            args = request.json
            # image = ImagesDao().selectImage(args.get('item_no'))

            # if (len(image) > 0):
            #     default_image_path = image[0]['default_img_path']
            #     large_image_path = image[0]['large_img_path']
            #     small_image_path = image[0]['small_img_path']

            Logger.logger.info(args)

            default_image_path = args.get('default_image')
            large_image_path = ''
            small_image_path = ''

            expiration_date = args.get('expiration_date')[:4] + '-' + args.get('expiration_date')[4:6] + '-' + \
                              args.get('expiration_date')[6:]


            ############ 1 step 상품 등록 ############
            item_no = ''
            brand_no = 0
            if ('item_no'in args):
                item_no = args.get('item_no')

            soap = GoodsRegistApis().addItem(args.get('out_item_no'), args.get('category_code'), item_no, args.get('item_name'),
                                                args.get('gd_html'), args.get('maker_no'), expiration_date, args.get('price'),
                                                default_image_path, large_image_path, small_image_path, brand_no)

            Logger.logger.info(soap)
            Logger.logger.info(soap.find('faultcode'))
            Logger.logger.info(soap.find('gmktitemno'))

            if soap.find('faultcode') != None:
                return Utils().makeResponse((soap.find('faultcode').string, soap.find('faultstring').string))
            else:
                response = soap.find('additemresponse')
                item_results = response.findChildren('additemresult')
                Logger.logger.info(item_results)

                for result in item_results:
                    if (result['result'] == 'Fail'):
                        return Utils().makeResponse(('-100', result['comment']))
                    else:
                        try:
                            item_no = result['gmktitemno']
                            GoodsRegistDao().insertGoods(args.get('out_item_no'), args.get('category_code'),
                                                         item_no, args.get('item_name'),
                                                         args.get('gd_html'), args.get('maker_no'), expiration_date,
                                                         args.get('price'),
                                                         default_image_path, large_image_path, small_image_path,
                                                         args.get('auto_term_duration'), args.get('auto_use_term_duration'),
                                                         args.get('use_information'), args.get('help_desk_telno'),
                                                         args.get('apply_place'),
                                                         args.get('apply_place_url'), args.get('apply_place_telephone'),
                                                         args.get('expiration_date'),
                                                         args.get('stock_qty'), args.get('user_id'), result['shippinggroupcode'])
                        except KeyError as key:
                            Logger.logger.info (key)
                            pass

            ############ 2 step 상품 고시정보 등록 ############
            soap = GoodsRegistApis().addOfficialInfo(item_no)
            official_response = soap.find('addofficialinforesponse')
            official_results =  official_response.findChildren('addofficialinforesult')
            Logger.logger.info (official_results)

            for result in official_results:
                if (result['result'] == 'Fail'):
                    return Utils().makeResponse(('-100', result['comment']))
                else:
                    pass

            ############ 3 step 쿠폰 정보 등록 ############
            soap = GoodsRegistApis().addCouponInfo(item_no, args.get('price'), args.get('item_name'),
                                                   args.get('auto_term_duration'), args.get('auto_use_term_duration'),
                                                   args.get('use_information'), args.get('help_desk_telno'),
                                                   args.get('apply_place'), args.get('apply_place_url'),
                                                   args.get('apply_place_telephone'), default_image_path,
                                                   args.get('find_guide'), args.get('publication_corp'))

            coupon_response = soap.find('additemcouponresponse')
            coupon_results = coupon_response.findChildren('additemcouponresult')
            Logger.logger.info (coupon_results)

            for result in coupon_results:
                if (result['result'] == 'Fail'):
                    return Utils().makeResponse(('-100', result['comment']))
                else:
                    pass

            ############ 4 step 가격 정보 등록 ############
            soap = GoodsRegistApis().addPriceInfo(item_no, expiration_date, args.get('price'),
                                                  args.get('stock_qty'))
            price_response = soap.find('addpriceresponse')
            price_results = price_response.findChildren('addpriceresult')
            Logger.logger.info (price_results)

            for result in price_results:
                if (result['result'] == 'Fail'):
                    return Utils().makeResponse(('-100', result['comment']))
                else:
                    pass

            ############ 5 step 기타 혜택 등록 ############
            soap = GoodsRegistApis().addPremium(item_no)
            premium_response = soap.find('addpremiumitemresponse')
            premium_results = premium_response.findChildren('addpremiumitemresult')
            Logger.logger.info (premium_results)

            for result in premium_results:
                if (result['result'] == 'Fail'):
                    return Utils().makeResponse(('-100', result['comment']))
                else:
                    pass

            return Utils().makeResponse(StrRepository().error_none)


        except Exception as e:
            Logger.logger.info (e)
            return Utils().makeResponse(StrRepository().error_system)

