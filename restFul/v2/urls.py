from restFul.v2.gmarket.gmarket_goods import GmarketGoods

def init_api_v2(api):
    api_v2_url = "/smartconb2c/v2/b2c/{}"
    api.add_resource(GmarketGoods, api_v2_url.format('gmarket/goods'))