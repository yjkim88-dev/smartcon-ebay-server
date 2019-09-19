import xlrd
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from restFul.v2.gmarket.goods_regist_dao import GoodsRegistDao

workbook = xlrd.open_workbook('./b2c_scms_import.xlsx')

ws = workbook.sheet_by_index(0)

ncol = ws.ncols
nrow = ws.nrows

scms_gmkt_goods_infos = []

for row in range(nrow):
    goods = ws.row_values(row)
    obj = {
        'CREATE_DATE': goods[0],
        'MODIFY_DATE': goods[1],
        'OUT_ITEM_NO': goods[2],
        'CAEGORY_CODE': goods[3],
        'ITEM_NO': int(goods[4]),
        'ITEM_NAME': goods[5],
        'GD_HTML': goods[6],
        'MAKER_NO': goods[7],
        'EXPIRATION_DATE': goods[8] if goods[8] != '' else None,
        'PRICE': goods[9],
        'DEFAULT_IMAGE': goods[10],
        'AUTO_TERM_DURATION': goods[11],
        'AUTO_USE_TERM_DURATION': goods[12],
        'USE_INFORMATION': goods[13],
        'HELP_DESK_TELNO': goods[14],
        'APPLY_PLACE': goods[15],
        'APPLY_PLACE_URL': goods[16],
        'APPLY_PLACE_TELEPHONE': goods[17],
        'DISPLAY_DATE': goods[18],
        'STOCK_QTY': goods[19],
        'REGIST_USER': goods[20],
        'SHIPPING_GROUP_CODE': int(goods[21]),
    }

    scms_gmkt_goods_infos.append(obj)

result = 0
## auto_use_term 버그잡기
for goods in scms_gmkt_goods_infos:
    result += GoodsRegistDao().upload_scms_data(goods)

print("{}개중 {}개 작업 완료".format(len(scms_gmkt_goods_infos),result))