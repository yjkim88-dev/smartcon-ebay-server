#_*_ coding: utf-8 _*_

import datetime
import requests
from flask import request
from flask_restful import Resource
from restFul.repository import StrRepository

from B2C.order_list_dao import OrderListDao
from B2C.resend_dao import ResendDao
from B2C.sendlog_dao import SendLogDao
from restFul.utils import Utils
from Logger import Logger

class Resend(Resource):
    def __init__(self):
        self.mms_url = "http://b2b.giftsmartcon.com/coupon/couponCreateLotte.sc"

    # MMS 발송
    def sendMMS(self, comp_code, cpn_no, phone, callback, title, add_msg, count, tr_id):
        Logger.logger.info("-------- MMS 재 발송 ----------")

        # if (count < 3):
        params = {
            "COMP_CODE": comp_code,
            "CPN_NO": cpn_no,
            "PHONE": phone.replace("-", ""),
            "CALLBACK": callback.replace("-", ""),
            "TITLE": title,
            "ADD_MSG": add_msg
        }

        Logger.logger.info(params)

        response = requests.get(self.mms_url, params=params)
        soup = Utils().getSoup(response.content)

        body = soup.find("lotte")
        Logger.logger.info(body)

        if body.res_code.string == '00':
            Logger.logger.info('--재전송 횟수 증가--')
            # OrderListDao().setReSendCount(cpn_no, count + 1)
            SendLogDao().setResendCount(cpn_no, count + 1)

            # 수신자 번호 업데이트
            SendLogDao().updateReceiverMobile(phone, tr_id)

            ResendDao().insertResnedLog(comp_code, cpn_no, callback, phone, title, add_msg, count + 1,
                                        datetime.datetime.now(), tr_id)

            results = []
            results.append({'cpn_no': body.cpn_no.string})

            return Utils().makeResponse(StrRepository().error_none, results)

            # GmarketApiService().sendGmarketResult(send_no, auth_num, barcode_num)
        else:
            Logger.logger.info('[[fail]] error code = ' + body.res_code.string)
            Logger.logger.info('[[fail]] error msg = ' + body.res_msg.string)

            return body.res_code.string, body.res_msg.string

    # else:
    #     return Utils().makeResponse(StrRepository().error_resend_count)
    def get(self):
        Logger.logger.info ('get resend')

        tr_id = request.args.get('tr_id')
        Logger.logger.info (tr_id)

        resend_list = ResendDao().selectResendLog(tr_id)

        Logger.logger.info (resend_list)
        result = []
        for resend in resend_list:
            obj = {
                'barcode_num': resend['BARCODE_NUM'],
                'buyer_mobile': resend['BUYER_MOBILE'],
                'receiver_mobile': resend['RECEIVER_MOBILE'],
                'resend_date': str(resend['RESEND_DATE']),
                'tr_id': resend['TR_ID']
            }

            result.append(obj)

        return Utils().makeResponse(StrRepository().error_none, result)


    def post(self):
        Logger.logger.info ('resend')
        try:
            args = request.json

            Logger.logger.info (args)

            if (args is not None):
                tr_id = args.get('tr_id')
                receiver_phone = args.get('phone')
            else:
                tr_id = request.form['tr_id']
                receiver_phone = request.form['phone']

            sends = SendLogDao().selectSendLog(tr_id)
            if (len(sends) > 0):
                result = self.sendMMS(sends[0]['EVENT_ID'], sends[0]['SVC_BARCODE_NUM'], receiver_phone, sends[0]['BUYER_PHONE'],
                                  '', '', sends[0]['RESEND_COUNT'], tr_id)
            else:
                return Utils().makeResponse(StrRepository().error_not_found_send)

            return result

        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
