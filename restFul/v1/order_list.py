#_*_ coding: utf-8 _*_

from flask import request
from flask_restful import Resource
from restFul.repository import StrRepository

from B2C.order_list_dao import OrderListDao
from B2C.coupon_state import CouponState
from B2C.sendlog_dao import SendLogDao
from restFul.utils import Utils
from Logger import Logger

import requests, datetime

class OrderList(Resource):
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

        result = soup.find('org_id')

        CouponState().updateSendState(send_no, order_id, result.sms_status.string, result.sms_type.string, result.sms_date.string, tr_id)

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

        end_date = datetime.datetime.now()

        if (result.valid_end.string != 'null'):
            end_date = result.valid_end.string

        CouponState().updateCouponState(send_no, order_id, result.claim_type.string, result.rcompany_name.string,
                            result.branch_name.string, result.exchange_status.string, result.valid_start.string, end_date, tr_id)


    # 입력
    def post(self):
        Logger.logger.info ('--post--')
        try:

            # args = request.json

            order_no = request.form['order_no']
            send_no = request.form['send_no']
            item_count = request.form['item_count']
            item_name = request.form['item_name']
            item_no = request.form['item_no']
            buyer_mobile = request.form['buyer_mobile']
            receiver_mobile = request.form['receiver_mobile']
            payment_date = request.form['payment_date']
            send_request_date = request.form['send_request_date']
            member_id = request.form['member_id']
            out_item_no = request.form['out_item_no']
            barcode_num = request.form['barcode_num']
            send_date = request.form['send_date']
            event_id = request.form['event_id']
            tr_id = request.form['tr_id']
            order_state = 2

            Logger.logger.info(order_no)
            Logger.logger.info(send_no)
            Logger.logger.info(order_state)
            Logger.logger.info(item_count)
            Logger.logger.info(item_name)
            Logger.logger.info(item_no)
            Logger.logger.info(buyer_mobile)
            Logger.logger.info(receiver_mobile)
            Logger.logger.info(payment_date)
            Logger.logger.info(send_request_date)
            Logger.logger.info(member_id)
            Logger.logger.info(out_item_no)
            Logger.logger.info(barcode_num)
            Logger.logger.info(send_date)
            Logger.logger.info(event_id)
            Logger.logger.info(tr_id)


            # 파라메터 체크
            if (order_no is None or send_no is None or item_count is None or item_name is None or
                        item_no is None or buyer_mobile is None or receiver_mobile is None or payment_date is None
                        or send_request_date is None or member_id is None or barcode_num is None or send_date is None
                        or event_id is None or tr_id is None):
                raise Exception

            OrderListDao().insertOrder(order_no, send_no, order_state, item_count, item_name, item_no, "", "",
                                       buyer_mobile, "",
                                       receiver_mobile, payment_date, send_request_date, datetime.datetime.now(),
                                       member_id, out_item_no)

            SendLogDao().insertSendLog(order_no, send_no, '00', "", send_date, barcode_num, receiver_mobile,
                                       buyer_mobile, event_id, tr_id, member_id)

            CouponState().insertCouponState(send_no, order_no, tr_id)

            return Utils().makeResponse(StrRepository().error_none)

        except Exception as e:
            Logger.logger.info ('exception---')
            Logger.logger.info (e)
            return Utils().makeResponse(StrRepository().error_system)

    # option1 : 채널 주문번호
    # option2 : 채널 상품코드
    # option3 : 상품명
    # option4 : 채널
    # option5 : 주문자HP
    # option6 : 수신자HP
    # option7 : 연동코드
    # option8 : 이벤트 ID
    # option9 : 바코드 번호
    # option10 : 발송 상태
    # option11 : 교환 상태
    # option12 : 쿠폰 상태
    # 조회
    def get(self):
        try:
            Logger.logger.info ('get--')

            param_start_date = request.args.get('start_date')
            param_end_date = request.args.get('end_date')
            param_data_select = request.args.get('data_select')
            param_search_text = request.args.get('search_text')

            Logger.logger.info (param_start_date)
            Logger.logger.info (param_end_date)
            Logger.logger.info (param_data_select)
            Logger.logger.info (param_search_text)

            # p = re.compile('[0-9]{8}')
            # startDate = p.match(param_start_date)
            # endDate = p.match(param_end_date)
            #
            # Logger.logger.info (startDate)
            # Logger.logger.info (endDate)

            if (param_start_date != None and param_end_date != None):
                orders = OrderListDao().getOrderList(param_start_date, param_end_date, param_data_select, param_search_text)
                Logger.logger.info (orders)

                ret_list = []

                for order in orders:
                    # 발송로그 조회 및 상태 업데이트
                    sends = SendLogDao().selectSendLogSendNom(order['ORDER_NO'], param_data_select, param_search_text)
                    Logger.logger.info(sends)
                    for send in sends:
                        # 발송 상태 조회
                        # self.updateSendState(send['SEND_NO'], send['ORDER_NO'], send['TR_ID'], send['EVENT_ID'], send['MEMBER_ID'])

                        # 교환 상태 조회
                        # self.updateExchangeState(send['SEND_NO'], send['ORDER_NO'], send['TR_ID'], send['EVENT_ID'], send['MEMBER_ID'])

                        # 쿠폰 상태 가져옴
                        states = CouponState().selectCouponState(send['TR_ID'])
                        claim_date = None
                        exchange_date = None
                        valid_end = None

                        if (states[0]['CLAIM_DATE'] != None):
                            claim_date = str(states[0]['CLAIM_DATE'])

                        if (states[0]['EXCHANGE_DATE'] != None):
                            exchange_date = str(states[0]['EXCHANGE_DATE'])

                        if (states[0]['VALID_END'] != None):
                            valid_end = str(states[0]['VALID_END'])

                        ret_obj = {
                            'resend_count': send['RESEND_COUNT'],
                            'send_request_date': str(order['SEND_REQUEST_DATE']),
                            'item_no': order['ITEM_NO'],
                            'alert_result': send['ALERT_RESULT'],
                            'out_item_no': order['OUT_ITEM_NO'],
                            'item_name': order['ITEM_NAME'],
                            'order_no': order['ORDER_NO'],
                            'payment_date': str(order['PAYMENT_DATE']),
                            'buyer_name': order['BUYER_NAME'],
                            'buyer_mobile': order['BUYER_MOBILE'],
                            'b2c_order_id': order['B2C_ORDER_ID'],
                            'buyer_id': order['BUYER_ID'],
                            'receiver_mobile': send['RECEIVER_PHONE'],
                            'item_count': order['ITEM_COUNT'],
                            'receiver_name': order['RECEIVER_NAME'],
                            'alert_fail_reason': send['ALERT_FAIL_REASON'],
                            'member_id': order['MEMBER_ID'],
                            'ecoupon_auth_num': order['ECOUPON_AUTH_NUM'],
                            'send_no': order['SEND_NO'],
                            'svc_event_id': send['EVENT_ID'],
                            'svc_barcode_num': send['SVC_BARCODE_NUM'],
                            'tr_id': send['TR_ID'],
                            'claim_type': states[0]['CLAIM_TYPE'],
                            'claim_date': claim_date,
                            'send_status': states[0]['SEND_STATUS'],
                            'exchange_date': exchange_date,
                            'exchange_status': states[0]['EXCHANGE_STATUS'],
                            'exception': order['B2C_EXCEPTION'],
                            'valid_end': valid_end,
                            'cancel_user': states[0]['CANCEL_USER']
                        }

                        ret_list.append(ret_obj)

                return Utils().makeResponse(StrRepository().error_none, ret_list)
            else:
                return Utils().makeResponse(StrRepository().error_order_type)

        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
