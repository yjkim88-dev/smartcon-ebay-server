#_*_ coding: utf-8 _*_

from flask import request
from flask_restful import Resource
from restFul.repository import StrRepository

from B2C.black_list_dao import BlackListDao
from restFul.utils import Utils
from Logger import Logger

class BlackList(Resource):
    # 조회
    def get(self):
        Logger.logger.info ('get--')
        try:
            phone_num = request.args.get('phone_num')

            if (phone_num == ''):
                phone_num = None

            black_list = BlackListDao().getBlackList(phone_num)

            Logger.logger.info (len(black_list))
            if (len(black_list) <= 0):
                return Utils().makeResponse(StrRepository().error_nothing_blacklist)
            else:
                ret_list = []
                for info in black_list:
                    ret_obj = {
                        'phone_num': info['PHONE_NUM'],
                        'reason': info['REASON'],
                        'modify_date': str(info['MODIFY_DATE']),
                        'regist_date': str(info['REGIST_DATE'])
                    }
                    ret_list.append(ret_obj)

                return Utils().makeResponse(StrRepository().error_none, ret_list)
        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)


    # 등록
    def post(self):
        Logger.logger.info('post--')
        try:
            args = request.json

            phone_num = args.get('phone_num')
            reason = args.get('reason')
            user_id = args.get('user_id')

            Logger.logger.info (user_id)

            black_list = BlackListDao().getBlackList(phone_num)

            for info in black_list:
                Logger.logger.info('search phone num : ' + info['PHONE_NUM'])
                if info['PHONE_NUM'] != None:
                    return Utils().makeResponse(StrRepository().error_already_regist)


            BlackListDao().registBlackList(phone_num, reason, user_id)

            return Utils().makeResponse(StrRepository().error_none)

        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)

    # 수정
    def put(self):
        Logger.logger.info('put--')
        try:
            args = request.json

            phone_num = args.get('phone_num')
            reason = args.get('reason')

            BlackListDao().updateBlackList(phone_num, reason)

            return Utils().makeResponse(StrRepository().error_none)

        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)

    # 삭제
    def delete(self):
        Logger.logger.info ('delete---')
        try:
            # args = request.json
            #
            # phone_num = args.get('phone_num')
            phone_num = request.args.get('phone_num')

            Logger.logger.info (phone_num)
            BlackListDao().deleteBlackList(phone_num)

            return Utils().makeResponse(StrRepository().error_none)

        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)

