#_*_ coding: utf-8 _*_

from flask import request
from flask_restful import Resource
from restFul.repository import StrRepository
from restFul.utils import Utils
from B2C.coupon_state import CouponState
from Logger import Logger
import requests

class Cpcancel(Resource):
    def __init__(self):
        self.cp_cancel_url = 'http://b2b.giftsmartcon.com/coupon/couponCancel.sc'

    def CpCancel(self, tr_id, member_id):
        params = {
            'TR_ID': tr_id,
            'MEMBER_ID': member_id
        }

        response = requests.get(self.cp_cancel_url, params=params)
        soup = Utils().getSoup(response.content)

        couponcancel = soup.find('couponcancel')

        return couponcancel

    # 주문취소
    def post(self):
        Logger.logger.info('post--')
        try:
            args = request.json

            tr_id = args.get('tr_id')
            member_id = args.get('member_id')
            cancel_user = args.get('cancel_user')

            Logger.logger.info (tr_id)
            Logger.logger.info (member_id)

            result = self.CpCancel(tr_id, member_id)

            print (result)

            if (result.resultcode.string == '00'):
                CouponState().updateCancelUser(cancel_user, tr_id)

                return Utils().makeResponse(StrRepository().error_none)
            else:
                ret = result.resultcode.string, result.resultmsg.string
                return Utils().makeResponse(ret)

        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
