import os

from tinydb import *

# 获取当前模块的路径
current_path = os.path.dirname(__file__)
categories_path = os.path.join(current_path, 'categories.json')
sub_categories_path = os.path.join(current_path, 'sub_categories.json')
config_path = os.path.join(current_path, 'config.json')

# 初始化 TinyDB
__db_categories = TinyDB(categories_path)
__db_sub_categories = TinyDB(sub_categories_path)
__db_config = TinyDB(config_path)

__query = Query()


def init_sub_categories_count(count: int):
    __db_config.insert({'sub_categories_count': count})


def select_sub_categories_count():
    result = __db_config.search(__query.sub_categories_count.exists())
    if not result:
        raise KeyError("sub_categories_count not found.")
    return result[0]['sub_categories_count']


def init_categories(data):
    __db_categories.truncate()
    __db_categories.insert_multiple(data)


def init_sub_categories(data):
    __db_sub_categories.truncate()
    __db_sub_categories.insert_multiple(data)


def select_sub_category_by_doc_id(doc_id: int):
    return __db_sub_categories.get(doc_id=doc_id)


def select_sub_category_by_id(sub_category_id: str):
    return __db_sub_categories.get(__query.id == sub_category_id)


def select_categories_by_id(category_id: str):
    return __db_categories.get(__query.id == category_id)


def select_all_sub_category():
    return __db_sub_categories.all()


def select_all_category():
    return __db_categories.all()
