import logging, json, datetime, os
import logging.config

def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance()

@singleton
class Logger:
    def __init__(self):
        with open('/home/ebayb2c/SmartconEbayAdmin/src/logging.json', 'r') as f:
            config = json.load(f)

        # 파일명 설정
#        log_filename = config['handlers']['info_time_handler']['filename']
#        base, extension = os.path.splitext(log_filename)
#        today = datetime.datetime.today()
#        log_filename = '{}{}{}'.format(
#            base,
#            today.strftime('%Y%m%d'),
#            extension
#        )

#        config['handlers']['info_time_handler']['filename'] = log_filename
        logging.config.dictConfig(config)
        # file logger 가져옴

        self.logger = logging.getLogger('filelogger')
