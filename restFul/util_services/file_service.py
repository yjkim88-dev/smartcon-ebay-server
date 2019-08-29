import os


class FileService:

    def __init__(self, folder_path = None):
        self.__folder_path = folder_path

    @staticmethod
    def file_check(file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    def file_save(self, file, filename, brand_id):
        file_path = os.path.join(self.__folder_path, brand_id)

        full_path = os.path.join(file_path, filename)
        self.file_check(file_path)
        try:
            file.save(full_path)
        except Exception as e:
            print(e)

        return full_path