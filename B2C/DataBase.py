#_*_ coding: utf-8 _*_

import pymysql.cursors
from restFul.config import DbCfg
from Logger import Logger

class MysqlDatabase:
    def __init__(self):
        self.conn = None

    def connection(self):
        self.conn = pymysql.connect(host=DbCfg().HOST,
                                    port=int(DbCfg().PORT),
                                    user=DbCfg().ID,
                                    password=DbCfg().PASSWORD,
                                    db=DbCfg().DB,
                                    charset=DbCfg().CHARSET)

    def executeQuery(self, query, *argsa):
        try:
            self.connection()
            with self.conn.cursor() as cursor:
                cursor.execute(query, argsa)

            self.conn.commit()
            print (cursor.lastrowid)
        except BaseException as e:
            Logger.logger.info('==== Error executeQuery ====')
            Logger.logger.info(e)
            self.conn.rollback()
            self.conn.close()

        finally:
            self.conn.close()

    def selectQuery(self, query, *argsa):
        try:
            self.connection()

            # pymysql.cursors.DictCursor 결과값을 튜플이 아닌 Dict형태로 받아옴
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, argsa)

                result = cursor.fetchall()

                return result
        except Exception as e:
            Logger.logger.info(e)
            self.conn.rollback()
            self.conn.close()

        finally:
            self.conn.close()
