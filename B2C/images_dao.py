#_*_ coding: utf-8 _*_

from B2C.DataBase import MysqlDatabase

class ImagesDao:
    def __init__(self):
        # 등록된 이미지 조회
        self.query_select_image = "SELECT * FROM b2c_images WHERE item_no = %s"

        # 이미지 경로 저장
        self.query_insert_images = "INSERT INTO b2c_images (item_no, out_item_no, default_img_path, small_img_path, large_img_path)" \
                                    "VALUES (%s, %s, %s, %s, %s)"
        # 이미지 경로 업데이트
        self.query_update_images = "UPDATE b2c_images SET default_img_path = %s, small_img_path = %s, large_img_path = %s " \
                                    "WHERE item_no = %s"

    def insertImages(self, item_no, out_item_no, default_img_path, small_img_path, large_img_path):
        db = MysqlDatabase()
        images = self.selectImage(item_no)

        if (len(images) <= 0):
            db.executeQuery(self.query_insert_images, item_no, out_item_no, default_img_path, small_img_path,
                            large_img_path)
        else:
            db.executeQuery(self.query_update_images, default_img_path, small_img_path, large_img_path, item_no)

    def selectImage(self, item_no):
        db = MysqlDatabase()
        return db.selectQuery(self.query_select_image, item_no)


