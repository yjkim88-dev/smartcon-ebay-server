#_*_ coding: utf-8 _*_
import requests
import html

from restFul.utils import Utils
from Logger import Logger


class GoodsRegistApis:
    def __init__(self):
        self.api_url_add_item = 'http://tpl.gmarket.co.kr/v1/ItemService.asmx'
        self.headers = {'Content-Type': 'text/xml; charset=utf-8'}

        self.soap_header = """<?xml version="1.0" encoding="utf-8"?>
                                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                                <soap:Header>
                                    <EncTicket xmlns="http://tpl.gmarket.co.kr/">
                                        <encTicket>460D4458B6A91623AF5DF21F3B927745537A1D1D99F552C852025F9C0E0D493929B4132A3C7952031C76CCA91E2663282C0E8411F72BD035727EAFC4F1407951311224EB8CA02825A7A626E200205768DCBF5278561BEDA36A5A733B2E2A1FC0CF1BB798A7C47169CA397B2C2E7DD48F</encTicket>
                                    </EncTicket>
                                </soap:Header>"""

        # 상품 등록
        self.soap_body_add_item = """
                                    <soap:Body>
                                        <AddItem xmlns="http://tpl.gmarket.co.kr/">
                                            <AddItem OutItemNo="%s" CategoryCode="%s" GmktItemNo="%s" ItemName="%s" ItemEngName="" ItemDescription="" GdHtml="%s" GdAddHtml="" GdPrmtHtml="" 
                                                MakerNo="%s" BrandNo="%s" ModelName="" IsAdult="false" Tax="Free" FreeGift="" ItemKind="Ecoupon">
                                                <ReferencePrice Kind="Quotation" Price="%s" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <Refusal IsPriceCompare="false" IsNego="false" IsJaehuDiscount="false" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <ItemImage DefaultImage="%s" LargeImage="%s" SmallImage="%s" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <As Telephone="02-561-0671" Address="Seller" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <Shipping SetType="Use" GroupCode="136" RefundAddrNum="0" TransPolicyNo="38174" xmlns="http://tpl.gmarket.co.kr/tpl.xsd">
                                                  <NewItemShipping FeeCondition="Free" FeeBasePrice="0" Fee="0" />
                                                </Shipping>
                                                <BundleOrder BuyUnitCount="1" MinBuyCount="1" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <OrderLimit OrderLimitCount="0" OrderLimitPeriod="0" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <Origin Code="Domestic" Place="서울시 역삼동" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <GoodsKind GoodsKind="New" GoodsStatus="Fine" GoodsTag="New" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                            </AddItem>
                                        </AddItem>
                                    </soap:Body>
                                    </soap:Envelope>"""

        # 고시정보 등록
        self.soap_body_officialinfo = """<soap:Body>
                                            <AddOfficialInfo xmlns="http://tpl.gmarket.co.kr/">
                                              <AddOfficialInfo GmktItemNo="%s" GroupCode="34">
                                                <SubInfoList Code="34-1" AddYn="Y" AddValue="(주)스마트콘" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <SubInfoList Code="34-2" AddYn="N" AddValue="상품 상세 페이지에 제공" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <SubInfoList Code="34-3" AddYn="N" AddValue="상품 상세 페이지에 제공" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <SubInfoList Code="34-4" AddYn="N" AddValue="상품 상세 페이지에 제공" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <SubInfoList Code="34-5" AddYn="Y" AddValue="잔액환불 불가" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <SubInfoList Code="34-6" AddYn="Y" AddValue="02-561-0671" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <SubInfoList Code="34-7" AddYn="Y" AddValue="구매후 10분이내" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <TradeInfoList Code="999-1" AddYn="N" AddValue="상품 상세 페이지에 제공" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <TradeInfoList Code="999-2" AddYn="N" AddValue="상품 상세 페이지에 제공" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <TradeInfoList Code="999-3" AddYn="N" AddValue="상품 상세 페이지에 제공" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <TradeInfoList Code="999-4" AddYn="N" AddValue="상품 상세 페이지에 제공" xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                              </AddOfficialInfo>
                                            </AddOfficialInfo>
                                          </soap:Body>
                                        </soap:Envelope>"""

        # 쿠폰 정보 등록
        self.soap_body_coupon_info = """<soap:Body>
                                             <AddItemCoupon xmlns="http://tpl.gmarket.co.kr/">
                                               <AddItemCoupon GmktItemNo="%s" CouponType="Mobile" CouponMoneyType="FixedAmount"
                                                    CouponMoney="%s" ServiceName="%s" CouponImageUrl="%s" ValidTermType="AutoTerm"
                                                    AutoTermStartDay="0" AutoTermDuration="%s" UseTermType="AutoTerm" AutoUseTermStartDay="0"
                                                    AutoUseTermDuration="%s" UseInformation="%s" HelpDeskTelNo="%s" ApplyPlace="%s"
                                                    ApplyPlaceUrl="%s" ApplyPlaceTelephone="%s" AddBenefit="" RestrictCondition=""
                                                    FindGuide="%s" PublicationCorp="%s" PublicationCorpWebUrl="" IsCustomerNameView="false"
                                                    IsCancel="true"/>
                                             </AddItemCoupon>
                                         </soap:Body>
                                         </soap:Envelope>"""

        # 가격정보 등록
        self.soap_body_price_info = """<soap:Body>
                                         <AddPrice xmlns="http://tpl.gmarket.co.kr/">
                                           <AddPrice GmktItemNo="%s" DisplayDate="%s" SellPrice="%s" StockQty="%s" />
                                         </AddPrice>
                                       </soap:Body>
                                       </soap:Envelope>"""

        # 기타 혜택 등록
        self.soap_body_premium = """<soap:Body>
                                          <AddPremiumItem xmlns="http://tpl.gmarket.co.kr/">
                                             <AddPremiumItem GmktItemNo="%s">
                                                <Discount xmlns="http://tpl.gmarket.co.kr/tpl.xsd">
                                                   <DiscountDate />
                                                </Discount>
                                                <Mileage xmlns="http://tpl.gmarket.co.kr/tpl.xsd" />
                                                <BundleDiscount xmlns="http://tpl.gmarket.co.kr/tpl.xsd">
                                                   <BundleDiscountDate />
                                                   <MultiplePurchaseDiscount />
                                                   <NPlusOneBonusDiscount />
                                                </BundleDiscount>
                                             </AddPremiumItem>
                                          </AddPremiumItem>
                                       </soap:Body>
                                       </soap:Envelope>"""


    def addItem(self, out_item_no, category_code, gmarket_item_no, item_name, gd_html, maker_no, expiration_date,
                    price, default_image, large_image, small_image, brand_no):
        Logger.logger.info ('step 1 상품정보 등록')

        gd_html = html.escape(gd_html)
        Logger.logger.info(gd_html)

        self.soap_body_add_item = self.soap_body_add_item % (out_item_no, category_code, gmarket_item_no, item_name,
                                                             gd_html.replace('"', '&quot;'), maker_no, brand_no,
                                                             price, default_image, large_image,
                                                             small_image)

		
        Logger.logger.info(self.soap_body_add_item)
        response = requests.post(self.api_url_add_item.encode('utf-8', 'xmlcharrefreplace'),
                                 data=self.soap_header.encode('utf-8', 'xmlcharrefreplace') +
                                      self.soap_body_add_item.encode('utf-8', 'xmlcharrefreplace'),
                                 headers=self.headers)

        return Utils().getSoup(response.content)


    def addOfficialInfo(self, gmarket_item_no):
        Logger.logger.info('step 2 고시정보 등록')
        self.soap_body_officialinfo = self.soap_body_officialinfo % (gmarket_item_no)

        Logger.logger.info(self.soap_body_officialinfo)
        response = requests.post(self.api_url_add_item.encode('utf-8', 'xmlcharrefreplace'),
                                 data=self.soap_header.encode('utf-8', 'xmlcharrefreplace') +
                                      self.soap_body_officialinfo.encode('utf-8', 'xmlcharrefreplace'),
                                 headers=self.headers)
        return Utils().getSoup(response.content)


    def addCouponInfo(self, gmarket_item_no, price, goods_name, auto_term_duration, auto_use_term_duration,
                      use_information, help_desk_telno, apply_place, apply_place_url, apply_place_telephone,
                      coupon_img_url, find_guide, publication_corp):
        Logger.logger.info ('step 3 쿠폰 정보 등록')

        self.soap_body_coupon_info = self.soap_body_coupon_info % (gmarket_item_no, price, goods_name, coupon_img_url,
                                                                   auto_term_duration, auto_use_term_duration,
                                                                   use_information, help_desk_telno, apply_place,
                                                                   apply_place_url, apply_place_telephone,
                                                                   find_guide, publication_corp)
        Logger.logger.info(self.soap_body_coupon_info)
        response = requests.post(self.api_url_add_item.encode('utf-8', 'xmlcharrefreplace'),
                                 data=self.soap_header.encode('utf-8', 'xmlcharrefreplace') +
                                      self.soap_body_coupon_info.encode('utf-8', 'xmlcharrefreplace'),
                                 headers=self.headers)

        return Utils().getSoup(response.content)


    def addPriceInfo(self, gmarket_item_no, display_date, price, stock_qty):
        Logger.logger.info ('step 4 가격 정보 등록')
        self.soap_body_price_info = self.soap_body_price_info % (gmarket_item_no, display_date, price, stock_qty)

        Logger.logger.info(self.soap_body_price_info)

        response = requests.post(self.api_url_add_item.encode('utf-8', 'xmlcharrefreplace'),
                                 data=self.soap_header.encode('utf-8', 'xmlcharrefreplace') +
                                      self.soap_body_price_info.encode('utf-8', 'xmlcharrefreplace'),
                                 headers=self.headers)

        return Utils().getSoup(response.content)


    def addPremium(self, gmarket_item_no):
        Logger.logger.info ('step 5 기타혜택 등록')
        self.soap_body_premium = self.soap_body_premium % (gmarket_item_no)

        Logger.logger.info(self.soap_body_premium)

        response = requests.post(self.api_url_add_item.encode('utf-8', 'xmlcharrefreplace'),
                                 data=self.soap_header.encode('utf-8', 'xmlcharrefreplace') +
                                      self.soap_body_premium.encode('utf-8', 'xmlcharrefreplace'),
                                 headers=self.headers)

        return Utils().getSoup(response.content)

