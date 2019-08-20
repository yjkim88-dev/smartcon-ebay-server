from restFul.v2.gmarket.gmarket_goods import GmarketGoods

def init_api_v2(api):
    def add_resource(res, path):
        api_v2_url = "/smartconb2c/v2/b2c"
        api.add_resource(res, api_v2_url + path)

    add_resource(GmarketGoods, '/gmarket/goods')