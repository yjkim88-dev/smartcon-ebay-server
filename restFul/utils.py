#_*_ coding: utf-8 _*_

import os, bs4, datetime

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class Utils:
    def makeResponse(self, error, data=[]):
        return {'errorCode': error[0], 'errorMsg': error[1], 'results': data}

    def getSoup(self, contents):
        if os.name == 'posix':
            return bs4.BeautifulSoup(contents, "html.parser")
        else:
            return bs4.BeautifulSoup(contents, "lxml")

    def getTrId(self):
        now = datetime.datetime.now()
        return now.strftime("%Y%m%d%H%M%S%f")[:50]

    def allowedFile(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def noneToSpace(self, str):
        result = ''
        if (str is None):
            return result
        else:
            return str

    @staticmethod
    def set_xml_element_attrib(element, attr_name, value):
        if value is not None:
            element.attrib[attr_name] = str(value)