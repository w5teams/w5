#!/usr/bin/env python
# encoding:utf-8
import os
import zipfile


class Zip(object):
    @staticmethod
    def save(zip_path, save_path):
        is_zipfile = zipfile.is_zipfile(zip_path)

        if is_zipfile:
            zip_file = zipfile.ZipFile(zip_path)
            zip_list = zip_file.namelist()

            if "app.json" not in zip_list:
                return False, "找不到 app.json 文件"

            if "icon.png" not in zip_list:
                return False, "找不到 icon.png 文件"

            if "readme.md" not in zip_list:
                return False, "找不到 readme.md(小写) 文件"

            for f in zip_list:
                if "__pycache__" not in f and "MACOSX" not in f and "DS_Store" not in f:
                    zip_file.extract(f, save_path)

            zip_file.close()

            return True, ""
        else:
            return False, "zip 文件不存在"

    @staticmethod
    def compress(src_dir, save_name):
        z = zipfile.ZipFile(save_name, 'w', zipfile.ZIP_DEFLATED)

        for dir_path, dir_names, file_names in os.walk(src_dir):
            fpath = dir_path.replace(src_dir, '')
            fpath = fpath and fpath + os.sep or ''

            if "__pycache__" in fpath:
                pass
            else:
                for file_name in file_names:
                    if file_name in [".DS_Store", "__init__.py"]:
                        pass
                    else:
                        z.write(os.path.join(dir_path, file_name), fpath + file_name)

        z.close()
        return True
