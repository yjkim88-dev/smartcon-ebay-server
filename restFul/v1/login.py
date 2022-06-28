#_*_ coding: utf-8 _*_

from flask import request, session, escape
from flask_restful import Resource
from restFul.utils import Utils
from restFul.repository import StrRepository
from B2C.DataBase import MysqlDatabase
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from restFul.aes import AESCipher
from B2C.user_dao import UserDao
from Logger import Logger
import base64, os



class Login(Resource):
    def post(self):
        Logger.logger.info('login')
        print('로그인 시도!!!!')
        try:
            args = request.json
            id = args.get('id')
            password = args.get('password')

            user = UserDao().selectUser(id)
            print('user ========== ', user)
            Logger.logger.info (user)

            if (len(user) <= 0):
                return Utils().makeResponse(StrRepository().error_check_user_password)
            else:
                user_password = AESCipher(user[0]['ENC_KEY'], 16).decrypt(user[0]['PASSWORD'])

                if (user_password == password):
                    auth_token = os.urandom(24)
                    UserDao().updateToken(base64.b64encode(auth_token).decode('utf-8'), user[0]['USERID'])

                    ret = []
                    ret.append({'auth_token': base64.b64encode(auth_token).decode('utf-8')})

                    return Utils().makeResponse(StrRepository().error_none, ret)
                else:
                    return Utils().makeResponse(StrRepository().error_check_user_password)

        except Exception as e:
            print('로그인 실패22222 ======== ', e)
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)






