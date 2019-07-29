#_*_ coding: utf-8 _*_

from flask import request
from flask_restful import Resource
from restFul.utils import Utils
from restFul.repository import StrRepository
from restFul.aes import AESCipher
from B2C.user_dao import UserDao
from Logger import Logger

import base64, os

class SignUp(Resource):
    def post(self):
        try:
            args = request.json
            id = args.get('id')
            password = args.get('password')
            
            Logger.logger.info(id)
            Logger.logger.info(password)

            key = base64.b64encode(os.urandom(16)).decode('utf-8')
            enc_password = AESCipher(key[:16], 16).encrypt(password)

            auth_token = os.urandom(24)
            UserDao().insertUser(id, enc_password, base64.b64encode(auth_token).decode('utf-8'), key[:16])

            return Utils().makeResponse(StrRepository().error_none)

        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
