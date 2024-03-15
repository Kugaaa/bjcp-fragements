import random
from typing import Union

import bjcp.db.storage as storage


class Category:
    id: str
    name: str
    notes: str


class SubCategory:
    id: str
    name: str
    impression: str
    aroma: str
    appearance: str
    flavor: str
    mouthfeel: str
    comments: str
    history: str
    ingredients: str
    comparison: str
    statistics: Union[str, dict]
    examples: list
    tags: list
    category: Category


class CategoryAbstract:
    doc_id: str
    id: str
    name: str
    sub_categories: list


class SubCategoryAbstract:
    doc_id: str
    id: str
    name: str


def random_sub_category() -> SubCategory:
    count = storage.select_sub_categories_count()
    # 随机数 [1,count]
    random_id = random.randint(1, count)

    # 查询子分类
    sub_category_result = storage.select_sub_category_by_doc_id(random_id)
    return query_and_build_category(sub_category_result)


def query_and_build_category(sub_category_result):
    category_id = sub_category_result['category_id']
    category_result = storage.select_categories_by_id(category_id)
    try:
        sub_category = wrap(category_result, sub_category_result)
    except Exception as e:
        print("wrap error sub category id: ", sub_category_result['id'])
        raise e
    return sub_category


def get_all_abstract() -> list[CategoryAbstract]:
    categories = storage.select_all_category()
    sub_categories = storage.select_all_sub_category()
    category_abstract_list = []
    for category in categories:
        category_abstract = CategoryAbstract()
        category_abstract.doc_id = category.doc_id
        category_abstract.id = category['id']
        category_abstract.name = category['name']
        if not category_abstract.name:
            category_abstract.name = category_abstract.id
        sub_abstract_list = []
        for sub_category in sub_categories:
            if sub_category['category_id'] == category_abstract.id:
                sub_category_abstract = SubCategoryAbstract()
                sub_category_abstract.doc_id = sub_category.doc_id
                sub_category_abstract.id = sub_category['id']
                sub_category_abstract.name = sub_category['name']
                sub_abstract_list.append(sub_category_abstract)
        category_abstract.sub_categories = sub_abstract_list
        category_abstract_list.append(category_abstract)
    return category_abstract_list


def wrap(category_result, sub_category_result):
    # SubCategory
    sub_category = SubCategory()
    sub_category.id = sub_category_result['id']
    sub_category.name = sub_category_result['name']
    sub_category.impression = sub_category_result.get('impression', None)
    sub_category.aroma = sub_category_result.get('aroma', None)
    sub_category.appearance = sub_category_result.get('appearance', None)
    sub_category.flavor = sub_category_result.get('flavor', None)
    sub_category.mouthfeel = sub_category_result.get('mouthfeel', None)
    sub_category.comments = sub_category_result.get('comments', None)
    sub_category.history = sub_category_result.get('history', None)
    sub_category.ingredients = sub_category_result.get('ingredients', None)
    sub_category.comparison = sub_category_result.get('comparison', None)

    """
    对于 statistics 字段做一个特殊逻辑
    如果一个风格没有 statistics 字段，那么它的结构为
    "statistics" : {
        "notes" : ""
    }
    这时将 notes 取出放在 statistics 属性上
    """
    statistics = sub_category_result.get('statistics', None)
    if 'notes' in statistics:
        sub_category.statistics = statistics.get('notes', None)
    else:
        sub_category.statistics = statistics

    sub_category.examples = sub_category_result.get('examples', None)
    sub_category.tags = sub_category_result.get('tags', None)

    # Category
    sub_category.category = Category()
    sub_category.category.id = category_result['id']
    sub_category.category.name = category_result['name']
    if not sub_category.category.name:
        sub_category.category.name = sub_category.category.id
    sub_category.category.notes = category_result.get('notes', None)
    return sub_category


def get_sub_category_by_id(sub_category_id: str):
    sub_category_result = storage.select_sub_category_by_id(sub_category_id)
    return query_and_build_category(sub_category_result)
