#_*_ coding: utf-8 _*_
import requests

from restFul.utils import Utils


class EsmBrandsApis:
    def __init__(self):
        self.api_url_add_item = 'http://tpl.gmarket.co.kr/v1/ItemService.asmx'
        self.headers = {'Content-Type': 'text/xml; charset=utf-8'}

        self.soap_header = """<?xml version="1.0"?>
                                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                                <soap:Header>
                                    <EncTicket xmlns="http://tpl.gmarket.co.kr/">
                                        <encTicket>460D4458B6A91623AF5DF21F3B927745537A1D1D99F552C852025F9C0E0D493929B4132A3C7952031C76CCA91E2663282C0E8411F72BD035727EAFC4F1407951311224EB8CA02825A7A626E200205768DCBF5278561BEDA36A5A733B2E2A1FC0CF1BB798A7C47169CA397B2C2E7DD48F</encTicket>
                                    </EncTicket>
                                </soap:Header>"""

        # Esm 브랜드 검색
        # -	제조사 브랜드의 경우 ESM 노출 정보만 Code조회가 가능
        # -	ESM 미 등록 브랜드는 체번 불가 하며, ESM 미등록 제조사의 경우 기타로 처리 됨
        # MakerName - 제조사명
        # BrandName - 브랜드명
        self.soap_body_search_brand = """<soap:Body>
                                        <AddMakerBrand xmlns="http://tpl.gmarket.co.kr/">
                                          <AddMakerBrand BrandName="%s" />
                                        </AddMakerBrand>
                                    </soap:Body>
                                    </soap:Envelope>"""

    def searchEsmBrand(self, brand_name):
        print ('브랜드 검색')
        self.soap_body_search_brand = self.soap_body_search_brand % (brand_name)

        print (self.soap_body_search_brand)

        response = requests.post(self.api_url_add_item.encode('ascii', 'xmlcharrefreplace'), data=self.soap_header.encode('ascii', 'xmlcharrefreplace') +
                                                                        self.soap_body_search_brand.encode('ascii', 'xmlcharrefreplace'), headers=self.headers)

        return Utils().getSoup(response.content)

