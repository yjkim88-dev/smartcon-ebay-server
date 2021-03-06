#_*_ coding: utf-8 _*_

from flask import Flask, make_response, request, render_template
from flask_restful import Api
from restFul.v1.black_list import BlackList
from restFul.v1.order_list import OrderList
from restFul.v1.goods_regist import GoodsRegist
from restFul.v1.goods_regist_auc import GoodsRegistAuc
from restFul.v1.resend import Resend
from restFul.v1.images import Images
from restFul.v1.esmbrands import EsmBrands
from restFul.v1.login import Login
from restFul.v1.rsagenerator import RsaGenerator
from restFul.v1.signup import SignUp
from restFul.v1.ezwel_regist_goods import EzwelRegistGoods
from restFul.utils import Utils
from restFul.v1.add_date import AddDate
from restFul.v1.cp_state import CpState
from restFul.v1.cp_cancel import Cpcancel
from B2C.DataBase import MysqlDatabase
from B2C.user_dao import UserDao
from Logger import Logger
from restFul.v2.urls import init_api_v2

import requests, hashlib

app = Flask(__name__, template_folder="static")
api = Api(app)

init_api_v2(api)

app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

# app.secret_key = os.urandom(24)
# print ('==secret key==')
# print (app.secret_key)
# app.secret_key = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

def unauthorized():
    response = make_response('401 Unauthorized', 401)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    response.headers.add("Access-Control-Allow-Headers",
                         "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With, restKey")
    return response

@app.before_request
def before_request():
    Logger.logger.info("{}".format(request))

@app.after_request
def after_request(response):
    restKey = request.headers.get("restKey")
    # userId = request.headers.get("userId")
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    response.headers.add("Access-Control-Allow-Headers",
                         "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With, restKey")

    if (request.method != 'OPTIONS'):
        if "/smartconb2c/v1/b2c" in request.path or "/smartconb2c/v2/b2c" in request.path:
            if "login" not in request.path and "signup" not in request.path and "resend" not in request.path:
                if restKey == None:
                    return unauthorized()
                else:
                    tmpSplit = restKey.split(',')
                    user = UserDao().selectUser(tmpSplit[0])

                    if user[0]['AUTH_TOKEN'] != tmpSplit[1]:
                        return unauthorized()

    return response

    # response.headers.add("restKey", restKey)
    # return response

@app.teardown_request
def shutdown_session(exception=None):
    #db_session.remove()
    Logger.logger.info("shutdown session")

# @app.route('/smartconb2c/resend', methods=['POST', 'GET'])
# def popup():
#     print (request.form['GmktItemNo'])
#     print (request.form['ContrNo'])
#     print (request.form['TimeStamp'])
#     print (request.form['JaehuCustNo'])
#     print (request.form['CheckSum'])
#
#     hash = hashlib.sha1()
#     hash.update(('gmarket_' + request.form['ContrNo'] + request.form['GmktItemNo'] + request.form['TimeStamp'] + request.form['JaehuCustNo'] + '_gmarket').encode('utf-8'))
#
#     print (hash.hexdigest())
#     print (hash.digest())
#
#     if (hash.hexdigest() != request.form['CheckSum']):
#         return render_template('dist/error.html', error='???????????? ?????? ???????????????. (check_sum)')
#
#     # ????????????
#     select_query_order = "select * from b2c_order where send_no = %s"
#
#     # ????????????
#     select_query_send = "select * from b2c_send_log where send_no = %s"
#
#     # ?????? ??????
#     select_query_goods = "select * from b2c_goods where item_no = %s"
#
#     coupon_state_url = 'http://b2b.giftsmartcon.com/coupon/couponState.sc'
#
#     db = MysqlDatabase()
#     order = db.selectQuery(select_query_order, request.form['ContrNo'])
#     send_logs = db.selectQuery(select_query_send, request.form['ContrNo'])
#     goods = db.selectQuery(select_query_goods, request.form['GmktItemNo'])
#
#     print (order)
#     print (send_logs)
#     print (goods)
#
#     if (len(order) <= 0):
#         return render_template('dist/error.html', error='?????? ????????? ???????????? ????????????.')
#     if (len(send_logs) <= 0):
#         return render_template('dist/error.html', error='?????? ????????? ???????????? ????????????.')
#     if (len(goods) <= 0):
#         return render_template('dist/error.html', error='????????? ???????????? ????????????.')
#
#     item = {
#         'receiver_mobile': order[0]['RECEIVER_MOBILE'],
#         'start_date': '',
#         'end_date': '',
#         'goods_image': goods[0]['DEFAULT_IMAGE'],
#         'goods_name': order[0]['ITEM_NAME'],
#         'use_place': goods[0]['APPLY_PLACE'],
#         'duration': goods[0]['AUTO_USE_TERM_DURATION'],
#         'count': order[0]['ITEM_COUNT'],
#         'hints': goods[0]['USE_INFORMATION']
#     }
#
#     sends_ret = []
#     for send in send_logs:
#         params = {
#             'TR_ID': send['TR_ID'],
#             'EVENT_ID': send['EVENT_ID'],
#             'MEMBER_ID': send['MEMBER_ID']
#         }
#
#         response = requests.get(coupon_state_url, params=params)
#         soup = Utils().getSoup(response.content)
#         result = soup.find('org_id')
#
#         print (result)
#         item['start_date'] = result.valid_start.string[:4] + '.' + result.valid_start.string[4:6] + '.' + result.valid_start.string[6:8]
#         item['end_date'] = result.valid_end.string[:4] + '.' + result.valid_end.string[4:6] + '.' + result.valid_end.string[6:8]
#
#         count = 0
#         if send['RESEND_COUNT'] == 0:
#             count = 2
#         if send['RESEND_COUNT'] == 1:
#             count = 1
#
#         barcode = send['SVC_BARCODE_NUM'][:4] + '-' + 'xxxx' + '-' + 'xxxx'
#
#         tmpObj = {
#             'barcode_num': barcode,
#             'resend_count': count,
#             'tr_id': send['TR_ID'],
#             'receiver_mobile': send['RECEIVER_PHONE']
#         }
#         print (tmpObj)
#         sends_ret.append(tmpObj)
#
#     return render_template('dist/resend_popup.html', obj=item, obj2=sends_ret)

# ????????? ?????? ??????/??????
api.add_resource(EzwelRegistGoods, '/smartconb2c/v1/b2c/ezwelRegistGoods')

# ??????????????? ??????/??????
api.add_resource(BlackList, '/smartconb2c/v1/b2c/blacklist')

# ????????????
api.add_resource(OrderList, '/smartconb2c/v1/b2c/orders')

# ?????? ??????/??????
api.add_resource(GoodsRegist, '/smartconb2c/v1/b2c/goods')

# ?????? ?????? ?????? (???????????? ?????? ?????????)
api.add_resource(GoodsRegistAuc, '/smartconb2c/v1/b2c/goods_regist_auc')

# ?????????
api.add_resource(Resend, '/smartconb2c/v1/b2c/resend')

# ???????????? ??????
api.add_resource(AddDate, '/smartconb2c/v1/b2c/add_date')

# ?????? ????????????
api.add_resource(CpState, '/smartconb2c/v1/b2c/cp_state')

# ??? ??????
api.add_resource(Cpcancel, '/smartconb2c/v1/b2c/cancel')

# ????????? ????????? URL
api.add_resource(Images, '/smartconb2c/v1/b2c/template/upload')

# ESM ????????? ??????
api.add_resource(EsmBrands, '/smartconb2c/v1/b2c/search_brands')

# RSA ????????? ??????
api.add_resource(RsaGenerator, '/smartconb2c/v1/b2c/generatekey')

# ?????????
api.add_resource(Login, '/smartconb2c/v1/b2c/login')

# ????????????
api.add_resource(SignUp, '/smartconb2c/v1/b2c/signup')


# ????????? Push
# api.add_resource(Push, '/smartconb2c/v1/b2c/push')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5556, debug=True)
    # app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)
