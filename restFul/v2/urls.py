from restFul.v2.gmarket.gmarket_goods import GmarketGoods
from restFul.v2.gmarket.gmarket_goods_excel import GmarketGoodsExcel

def init_api_v2(api):
    def add_resource(res, path):
        api_v2_url = "/smartconb2c/v2/b2c"
        api.add_resource(res, api_v2_url + path)

    # 지마켓 상품 정보/등록/수정
    add_resource(GmarketGoods, '/gmarket/goods')
    add_resource(GmarketGoodsExcel, '/gmarket/goods/excel')