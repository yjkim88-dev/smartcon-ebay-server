
#_*_ coding: utf-8 _*_

import base64
import json
from Crypto.PublicKey import RSA
from flask import jsonify, make_response, session
from flask_restful import Resource
from restFul.utils import Utils
from restFul.repository import StrRepository
from Logger import Logger

class RsaGenerator(Resource):
    def get(self):
        private_key = RSA.generate(1024)
        public_key = private_key.publickey()
        Logger.logger.info(private_key)
        Logger.logger.info(public_key)

        session['private_key'] = base64.b64encode(private_key.exportKey('DER')).decode('utf-8')
        Logger.logger.info ('----- private_key encode ------')
        Logger.logger.info (session['private_key'])

        return {'public_key': base64.b64encode(public_key.exportKey('DER')).decode('utf-8')}

