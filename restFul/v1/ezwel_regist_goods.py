#_*_ coding: utf-8 _*_

import requests, datetime, json
from flask import request
from flask_restful import Resource
from restFul.utils import Utils
from restFul.repository import StrRepository
from Logger import Logger
from py4j.java_gateway import JavaGateway


class EzwelRegistGoods(Resource):
    def __init__(self):
        # test
 #       self.send_goods_url = "http://dev-ecapi.ezwel.com/ecpn/registGoods"
 #       self.send_regist_goods_url = "http://dev-ecapi.ezwel.com/ecpn/registGoodsImg"
 #       self.send_regist_goods_shop_url = "http://dev-ecapi.ezwel.com/ecpn/registGoodsShop"
 #       self.send_regist_goods_rn_url = "http://dev-ecapi.ezwel.com/ecpn/registGoodsRnSet"


        # real
        self.send_goods_url = "http://ecapi.ezwel.com/ecpn/registGoods"
        self.send_regist_goods_url = "http://ecapi.ezwel.com/ecpn/registGoodsImg"
        self.send_regist_goods_shop_url = "http://ecapi.ezwel.com/ecpn/registGoodsShop"
        self.send_regist_goods_rn_url = "http://ecapi.ezwel.com/ecpn/registGoodsRnSet"


        # test
        self.event_id = '11998'

    # 상품등록
    def goodsRegist(self, csp_cd, csp_goods_cd, goods_nm, display_cd, valid_period_ext_yn, exchange_site,
                    concurrent_capa, holiday_cd, contact_no, open_hm, close_hm, shop_disp_yn, addr1, addr2,
                    post, parking_info, resv_yn, resv_cancel_cd, resv_cancel_etc, grp_resv_yn, cancel_yn,
                    normal_price, sale_price, buy_price, buy_qty_for_each, goods_memo, goods_add_info, noti_cd,
                    send_period_ext_yn):

        gateway = JavaGateway()
        java_app = gateway.entry_point

        # step1. 상품 등록
        goods_params = {
            'cspCd': java_app.encode(Utils().noneToSpace(csp_cd)),
            'cspGoodsCd': java_app.encode(Utils().noneToSpace(csp_goods_cd)),
            'goodsNm': java_app.encode(Utils().noneToSpace(goods_nm)),
            'displayCd': java_app.encode(Utils().noneToSpace(display_cd)),
            'validPeriodExtYn': java_app.encode(Utils().noneToSpace(valid_period_ext_yn)),
            'exchangeSite': java_app.encode(Utils().noneToSpace(exchange_site)),
            'concurrentCapa': java_app.encode(Utils().noneToSpace(concurrent_capa)),
            'holidayCd': java_app.encode(Utils().noneToSpace(holiday_cd)),
            'contactNo': java_app.encode(Utils().noneToSpace(contact_no)),
            'openHm': java_app.encode(Utils().noneToSpace(open_hm)),
            'closeHm': java_app.encode(Utils().noneToSpace(close_hm)),
            'shopDispYn': java_app.encode(Utils().noneToSpace(shop_disp_yn)),
            'addr1': java_app.encode(Utils().noneToSpace(addr1)),
            'addr2': java_app.encode(Utils().noneToSpace(addr2)),
            'post': java_app.encode(Utils().noneToSpace(post)),
            'parkingInfo': java_app.encode(Utils().noneToSpace(parking_info)),
            'resvYn': java_app.encode(Utils().noneToSpace(resv_yn)),
            'resvCancelCd': java_app.encode(Utils().noneToSpace(resv_cancel_cd)),
            'resvCancelEtc': java_app.encode(Utils().noneToSpace(resv_cancel_etc)),
            'grpResvYn': java_app.encode(Utils().noneToSpace(grp_resv_yn)),
            'cancelYn': java_app.encode(Utils().noneToSpace(cancel_yn)),
            'normalPrice': java_app.encode(Utils().noneToSpace(normal_price)),
            'salePrice': java_app.encode(Utils().noneToSpace(sale_price)),
            'buyPrice': java_app.encode(Utils().noneToSpace(buy_price)),
            'buyQtyForEach': java_app.encode(Utils().noneToSpace(buy_qty_for_each)),
            'goodsMemo': java_app.encode(Utils().noneToSpace(goods_memo)),
            'goodsAddInfo': java_app.encode(Utils().noneToSpace(goods_add_info)),
            'notiCd': java_app.encode(Utils().noneToSpace(noti_cd)),
            'sendPeriodExtYn': java_app.encode(Utils().noneToSpace(send_period_ext_yn))
        }
        print(goods_params)

        response = requests.post(self.send_goods_url, params=goods_params)
        Logger.logger.info("ezwel goodsregist Response")
        Logger.logger.info(response.status_code)
        Logger.logger.info(response.content)
        soup = Utils().getSoup(response.content)
        print(soup.prettify())

        return soup.find('responseezwel')

    def registImage(self, goodscd, img_url, img_detail_url):
        gateway = JavaGateway()
        java_app = gateway.entry_point

        # step2. 상품 이미지 등록
        # image_params = {
        #     'goodsCd': java_app.encode(Utils().noneToSpace(goodscd)),  # 상품 등록시 리턴되는 상품코드
        #     'imgUrl': java_app.encode(Utils().noneToSpace(img_url)),
        #     'imgDetailUrl': java_app.encode(Utils().noneToSpace(img_detail_url))
        # }
        image_params = {
            'goodsCd': 1,  # 상품 등록시 리턴되는 상품코드
            'imgUrl': 2,
            'imgDetailUrl': 3
        }

        Logger.logger.info(image_params)

        response = requests.post(self.send_regist_goods_url, params=image_params)
        print(response)
        Logger.logger.info("registImage Response")
        Logger.logger.info(response)
        Logger.logger.info(response.content)
        soup = Utils().getSoup(response.content)

        return soup.find('responseezwel')


    def registStore(self, goodscd, addr1, addr2, contact_no, directions, latitude, longitude, post, shop_nm):
        gateway = JavaGateway()
        java_app = gateway.entry_point

        # step3. 상품 매장 정보 등록
        goods_shop_params = {
            'goodsCd': java_app.encode(Utils().noneToSpace(goodscd)),
            'addr1': java_app.encode(Utils().noneToSpace(addr1)),
            'addr2': java_app.encode(Utils().noneToSpace(addr2)),
            'contactNo': java_app.encode(Utils().noneToSpace(contact_no)),
            'directions': java_app.encode(Utils().noneToSpace(directions)),
            'latitude': java_app.encode(Utils().noneToSpace(latitude)),
            'longitude': java_app.encode(Utils().noneToSpace(longitude)),
            'post': java_app.encode(Utils().noneToSpace(post)),
            'shopNm': java_app.encode(Utils().noneToSpace(shop_nm))
        }

        Logger.logger.info(goods_shop_params)
        
        response = requests.post(self.send_regist_goods_shop_url, params=goods_shop_params)
        Logger.logger.info("ezwel registStore Response")
        Logger.logger.info(response.status_code)
        Logger.logger.info(response.content)
        soup = Utils().getSoup(response.content)

        return soup.find('responseezwel')


    def registPin(self, goodscd, expire_start_dd, expire_end_dd, expire_type_cd, afterIss_expire_day, rn_length,
                  send_type_cd):
        gateway = JavaGateway()
        java_app = gateway.entry_point

        # step4. 핀정보 등록
        regist_goods_rn_params = {
            'goodsCd': java_app.encode(Utils().noneToSpace(goodscd)),
            'expireStartDd': java_app.encode(Utils().noneToSpace(expire_start_dd)),
            'expireEndDd': java_app.encode(Utils().noneToSpace(expire_end_dd)),
            'expireTypeCd': java_app.encode(Utils().noneToSpace(expire_type_cd)),
            'afterIssExpireDay': java_app.encode(Utils().noneToSpace(afterIss_expire_day)),
            'rnLength': java_app.encode(Utils().noneToSpace(rn_length)),
            'sendTypeCd': java_app.encode(Utils().noneToSpace(send_type_cd))
        }

        Logger.logger.info(regist_goods_rn_params)

        response = requests.post(self.send_regist_goods_rn_url, params=regist_goods_rn_params)
        Logger.logger.info("ezwel registPin Response")
        Logger.logger.info(response.status_code)
        Logger.logger.info(response.content)
        soup = Utils().getSoup(response.content)

        Logger.logger.info(soup.prettify())

        return soup.find('responseezwel')


    def post(self):
        try:
            json_param = request.json
            Logger.logger.info (json_param)

            # 상품등록 파라메터
            csp_cd = json_param.get('cspCd')
            csp_goods_cd = json_param.get('cspGoodsCd')
            goods_nm = json_param.get('goodsNm')
            display_cd = json_param.get('displayCd')
            valid_period_ext_yn = json_param.get('validPeriodExtYn')
            exchange_site = json_param.get('exchangeSite')
            concurrent_capa = json_param.get('concurrentCapa')
            holiday_cd = json_param.get('holidayCd')
            contact_no = json_param.get('contactNo')
            open_hm = json_param.get('openHm')
            close_hm = json_param.get('closeHm')
            shop_disp_yn = json_param.get('shopDispYn')
            addr1 = json_param.get('addr1')
            addr2 = json_param.get('addr2')
            post = json_param.get('post')
            parking_info = json_param.get('parkingInfo')
            resv_yn = json_param.get('resvYn')
            resv_cancel_cd = json_param.get('resvCancelCd')
            resv_cancel_etc = json_param.get('resvCancelEtc')
            grp_resv_yn = json_param.get('grpResvYn')
            cancel_yn = json_param.get('cancelYn')
            normal_price = json_param.get('normalPrice')
            sale_price = json_param.get('salePrice')
            buy_price = json_param.get('buyPrice')
            buy_qty_for_each = json_param.get('buyQtyForEach')
            goods_memo = json_param.get('goodsMemo')
            goods_add_info = json_param.get('goodsAddInfo')
            noti_cd = json_param.get('notiCd')
            send_period_ext_yn = json_param.get('sendPeriodExtYn')

            # 이미지등록 파라메터
            img_url = json_param.get('imgUrl')
            img_detail_url = json_param.get('imgDetailUrl')

            # 상품 매장정보 파라메터
            directions = json_param.get('directions')
            latitude = json_param.get('latitude')
            longitude = json_param.get('longitude')
            shop_nm = json_param.get('shopNm')

            # 상품 핀정보 파라메터
            expire_start_dd = json_param.get('expireStartDd')
            expire_end_dd = json_param.get('expireEndDd')
            expire_type_cd = json_param.get('expireTypeCd')
            afterIss_expire_day = json_param.get('afterIssExpireDay')
            rn_length = json_param.get('rnLength')
            send_type_cd = json_param.get('sendTypeCd')

            if (csp_goods_cd is None or goods_nm is None or display_cd is None or
                valid_period_ext_yn is None or shop_disp_yn is None or resv_cancel_cd is None or
                normal_price is None or buy_qty_for_each is None or goods_memo is None or noti_cd is None or
                img_url is None or img_detail_url is None or expire_start_dd is None or send_type_cd is None or expire_type_cd is None):
                raise Exception

            if (expire_type_cd == '01' and expire_end_dd is None):
                return Utils().makeResponse(StrRepository().error_ezwel_end_date)

            if (expire_type_cd == '02' and afterIss_expire_day is None):
                return Utils().makeResponse(StrRepository().error_ezwel_end_date_count)

            # 상품등록
            ezwel_result = self.goodsRegist(csp_cd, csp_goods_cd, goods_nm, display_cd, valid_period_ext_yn, exchange_site,
                    concurrent_capa, holiday_cd, contact_no, open_hm, close_hm, shop_disp_yn, addr1, addr2,
                    post, parking_info, resv_yn, resv_cancel_cd, resv_cancel_etc, grp_resv_yn, cancel_yn,
                    normal_price, sale_price, buy_price, buy_qty_for_each, goods_memo, goods_add_info, noti_cd,
                    send_period_ext_yn)

            if (ezwel_result.result.string == '0000'):
                Logger.logger.info ('상품 등록 성공')

                # 이미지 등록
                ezwel_img_regist_goods_result = self.registImage(ezwel_result.goodscd.string, img_url, img_detail_url)
                Logger.logger.info (ezwel_img_regist_goods_result)

                if (ezwel_img_regist_goods_result.result.string == '0000'):
                    Logger.logger.info('상품 이미지 등록 성공')
                    if (shop_disp_yn == 'Y'):
                        ezwel_regist_goods_shop_result = self.registStore(ezwel_img_regist_goods_result.goodscd.string,
                                                                          addr1, addr2, contact_no, directions, latitude,
                                                                          longitude, post, shop_nm)

                        if (ezwel_regist_goods_shop_result.result.string == '0000'):
                            Logger.logger.info('상품 매장 등록 성공')

                            ezwel_goods_regist_rn_result = self.registPin(ezwel_regist_goods_shop_result.goodscd.string,
                                                                          expire_start_dd, expire_end_dd, expire_type_cd,
                                                                          afterIss_expire_day, rn_length, send_type_cd)



                            if (ezwel_goods_regist_rn_result.result.string == '0000'):
                                Logger.logger.info('핀 정보 등록 성공')

                                data = {
                                    'goods_code': ezwel_goods_regist_rn_result.goodscd.string
                                }

                                return Utils().makeResponse(StrRepository().error_none, data)
                            else:
                                Logger.logger.info ('핀 정보 등록 실패')

                                data = {
                                    'goods_code': ezwel_goods_regist_rn_result.goodscd.string
                                }

                                return Utils().makeResponse(StrRepository().error_ezwel_goods_pin, data)
                        else:
                            Logger.logger.info('매장 정보 등록 실패')

                            data = {
                                'goods_code': ezwel_regist_goods_shop_result.goodscd.string
                            }

                            return Utils().makeResponse(StrRepository().error_ezwel_goods_shop, data)
                    else:
                        Logger.logger.info ('매장등록 하지 않음')
                        ezwel_goods_regist_rn_result = self.registPin(ezwel_img_regist_goods_result.goodscd.string,
                                                                      expire_start_dd, expire_end_dd, expire_type_cd,
                                                                      afterIss_expire_day, rn_length, send_type_cd)

                        if (ezwel_goods_regist_rn_result.result.string == '0000'):
                            Logger.logger.info('핀 정보 등록 성공')

                            data = {
                                'goods_code': ezwel_goods_regist_rn_result.goodscd.string
                            }

                            return Utils().makeResponse(StrRepository().error_none, data)
                        else:
                            Logger.logger.info('핀 정보 등록 실패')

                            data = {
                                'goods_code': ezwel_goods_regist_rn_result.goodscd.string
                            }

                            return Utils().makeResponse(StrRepository().error_ezwel_goods_pin, data)

                else:
                    Logger.logger.info ('상품 이미지 등록 실패')
                    data = {
                        'goods_code': ezwel_img_regist_goods_result.goodscd.string
                    }

                    return Utils().makeResponse(StrRepository().error_ezwel_goods_image, data)
            else:
                Logger.logger.info('상품 등록 실패')

                return Utils().makeResponse(StrRepository().error_ezwel_goods)

        except Exception as e:
            Logger.logger.info (e)
            return Utils().makeResponse(StrRepository().error_system)



