#_*_ coding: utf-8 _*_

import os
from flask import request, redirect
from flask_restful import Resource
from restFul.utils import Utils
from restFul.repository import StrRepository
from B2C.images_dao import ImagesDao
from Logger import Logger

class Images(Resource):
    def post(self):
        try:
            Logger.logger.info ('upload image')

            if ('file' not in request.files):
                Logger.logger.info ('No file part')
                return redirect(request.url)

            file = request.files['file']
            Logger.logger.info (request.form['username'])
            Logger.logger.info (request.form['item_no'])
            Logger.logger.info (request.form['out_item_no'])

            temp_str = os.path.splitext(file.filename)

            Logger.logger.info (temp_str[1])

            if file.filename == '':
                Logger.logger.info ('No selected file')
                return redirect (request.url)

            if file and Utils().allowedFile(file.filename):
                #filename = secure_filename(file.filename)
                filename = request.form['item_no'] + '_' + request.form['out_item_no'] + temp_str[1]
                Logger.logger.info (filename)

                file.save(os.path.dirname(os.path.abspath(__file__)) + "/../../static/images/" + filename)
                ImagesDao().insertImages(request.form['item_no'], request.form['out_item_no'], request.url_root + 'static/images/' + filename,
                                         request.url_root + 'static/images/' + filename, request.url_root + 'static/images/' + filename)

                return Utils().makeResponse(StrRepository().error_none)


        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)


