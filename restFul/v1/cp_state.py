#_*_ coding: utf-8 _*_

from flask import request
from flask_restful import Resource
from restFul.repository import StrRepository
from restFul.utils import Utils
from B2C.coupon_state import CouponState
from Logger import Logger

import requests, datetime

class CpState(Resource):
    def __init__(self):
        self.send_state_url = 'http://b2b.giftsmartcon.com/coupon/couponInfo.sc'
        self.coupon_state_url = 'http://b2b.giftsmartcon.com/coupon/couponState.sc'

    # 발송 상태 업데이트
    def updateSendState(self, send_no, order_id, tr_id, event_id, member_id):
        params = {
            'TR_ID': tr_id,
            'EVENT_ID': event_id,
            'MEMBER_ID': member_id
        }

        response = requests.get(self.send_state_url, params=params)
        soup = Utils().getSoup(response.content)

        Logger.logger.info(soup)
        result = soup.find('org_id')

        Logger.logger.info(result)

        if (result != None):
            CouponState().updateSendState(send_no, order_id, result.sms_status.string, result.sms_type.string, result.sms_date.string, tr_id)
            return 0
        else:
            return -1


    # 교환 상태 업데이트
    def updateExchangeState(self, send_no, order_id, tr_id, event_id, member_id):
        params = {
            'TR_ID': tr_id,
            'EVENT_ID': event_id,
            'MEMBER_ID': member_id
        }

        response = requests.get(self.coupon_state_url, params=params)
        soup = Utils().getSoup(response.content)
        result = soup.find('org_id')

        Logger.logger.info (soup)
        if (result != None):
            end_date = datetime.datetime.now()
            claim_date = result.claim_date.string
            exchange_date = result.exchange_date.string

            if (result.valid_end.string != 'null'):
                end_date = result.valid_end.string

            if (claim_date == 'null'):
                claim_date = None

            if (exchange_date == 'null'):
                exchange_date = None

            CouponState().updateCouponState(send_no, order_id, result.claim_type.string, result.rcompany_name.string,
                                result.branch_name.string, result.exchange_status.string, result.valid_start.string, end_date,
                                            claim_date, exchange_date, tr_id)
            return 0
        else:
            return -1

    # 쿠폰 상태 업데이트
    def post(self):
        Logger.logger.info('post--')
        try:
            args = request.json

            tr_id = args.get('tr_id')
            event_id = args.get('event_id')
            member_id = args.get('member_id')
            send_no = args.get('send_no')
            order_id = args.get('order_id')

            Logger.logger.info(tr_id)
            Logger.logger.info(event_id)
            Logger.logger.info(member_id)
            Logger.logger.info(send_no)
            Logger.logger.info(order_id)

            # 발송 상태 업데이트
            retcode = self.updateSendState(send_no, order_id, tr_id, event_id, member_id)
            if (retcode != 0):
                return Utils().makeResponse(StrRepository().error_send_state_update)

            # 교환 상태 업데이트
            retcode = self.updateExchangeState(send_no, order_id, tr_id, event_id, member_id)
            if (retcode != 0):
                return Utils().makeResponse(StrRepository().error_exchange_state_update)

            states = CouponState().selectCouponState(tr_id)
            claim_date = None
            exchange_date = None
            valid_end = None

            if (states[0]['CLAIM_DATE'] != None):
                claim_date = str(states[0]['CLAIM_DATE'])

            if (states[0]['EXCHANGE_DATE'] != None):
                exchange_date = str(states[0]['EXCHANGE_DATE'])

            if (states[0]['VALID_END'] != None):
                valid_end = str(states[0]['VALID_END'])

            result_list = []

            obj = {
                'claim_date': claim_date,
                'exchange_date': exchange_date,
                'valid_end': valid_end,
                'claim_type': states[0]['CLAIM_TYPE'],
                'send_status': states[0]['SEND_STATUS'],
                'exchange_status': states[0]['EXCHANGE_STATUS']
            }

            Logger.logger.info (obj)

            result_list.append(obj)

            return Utils().makeResponse(StrRepository().error_none, result_list)

        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
