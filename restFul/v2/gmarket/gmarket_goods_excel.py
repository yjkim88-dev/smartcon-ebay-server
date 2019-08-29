import os

from .gmarket_goods_service import GmarketGoodsService, GmarketExcelDownloadService
from flask_restful import Resource
from Logger import Logger
from flask import send_file, safe_join
from urllib.parse import quote
from restFul.config import BASE_DIR
import datetime as dt

class GmarketGoodsExcel(Resource):
    logger = Logger.logger

    def get(self):
        fetch_goods_list_result = GmarketGoodsService.mysql_fetch_goods_list()
        if fetch_goods_list_result.get('errorCode') != "00":
            return fetch_goods_list_result
        excel_info = fetch_goods_list_result.get('results')
        excel_path = GmarketExcelDownloadService.coupon_excel_down(excel_info)
        file_name = dt.datetime.now().strftime('%Y-%m-%d:%H:%M ') + 'coupon_info.xlsx'
        file_name = quote(file_name)
        safe_path = safe_join(os.path.join(BASE_DIR, excel_path))
        return send_file(safe_path, attachment_filename=file_name, as_attachment=True)

    def post(self):
        pass

    def put(self):
        pass