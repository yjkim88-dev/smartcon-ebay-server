#_*_ coding: utf-8 _*_

from flask import request
from flask_restful import Resource
from restFul.repository import StrRepository
from restFul.utils import Utils
from B2C.coupon_state import CouponState
from Logger import Logger

import requests

class AddDate(Resource):
    def __init__(self):
        self.add_date_url = 'http://b2b.giftsmartcon.com/coupon/couponPeriod.sc'

    def AddDate(self, tr_id, event_id, member_id, incre_exchange_day):
        params = {
            'TR_ID': tr_id,
            'EVENT_ID': event_id,
            'MEMBER_ID': member_id,
            'INCRE_EXCHANGE_DAY': incre_exchange_day
        }

        response = requests.get(self.add_date_url, params=params)
        soup = Utils().getSoup(response.content)

        couponperiod = soup.find('couponperiod')

        if (couponperiod.resultcode.string == '00'):
            result = soup.find('org_id')

            return couponperiod.resultcode.string, result.exchange_possible_enddate.string
        else:
            return couponperiod.resultcode.string


    # 유효기간 연장
    def post(self):
        Logger.logger.info('post--')
        try:
            args = request.json

            tr_id = args.get('tr_id')
            event_id = args.get('event_id')
            member_id = args.get('member_id')
            incre_exchange_day = args.get('incre_exchange_day')

            Logger.logger.info (tr_id)
            Logger.logger.info (event_id)
            Logger.logger.info (member_id)
            Logger.logger.info (incre_exchange_day)

            result = self.AddDate(tr_id, event_id, member_id, incre_exchange_day)

            ret_list = []

            Logger.logger.info (result[0])

            if (result[0] == '00'):
                obj = {
                    'exchange_possible_enddate': result[1]
                }
                ret_list.append(obj)

                CouponState().updateEndDate(result[1], tr_id)

                return Utils().makeResponse(StrRepository().error_none, ret_list)

            else:
                return Utils().makeResponse(StrRepository().error_not_add_date)


        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
