#!/usr/bin/env python
# encoding:utf-8
import zipfile


class Zip(object):
    @staticmethod
    def save(zip_path, save_path):
        is_zipfile = zipfile.is_zipfile(zip_path)

        if is_zipfile:
            zip_file = zipfile.ZipFile(zip_path)
            zip_list = zip_file.namelist()

            if "app.json" not in zip_list:
                return False

            if "icon.png" not in zip_list:
                return False

            if "readme.md" not in zip_list:
                return False

            for f in zip_list:
                if "__pycache__" not in f and "MACOSX" not in f and "DS_Store" not in f:
                    zip_file.extract(f, save_path)

            zip_file.close()

            return True
        else:
            return False
