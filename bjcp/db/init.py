import json

import storage


def init_bjcp_datas(data):
    categories = data['styleguide']['category']
    list_categories = []
    list_sub_categories = []

    # 获取所有的分类和子分类
    for category in categories:
        for sub_category in category['subcategory']:
            sub_category['category_id'] = category['id']
            list_sub_categories.append(sub_category)
        category.pop('subcategory')
        list_categories.append(category)

    storage.init_categories(list_categories)
    print("insert categories success")
    storage.init_sub_categories(list_sub_categories)
    print("insert sub categories success")
    storage.init_sub_categories_count(len(list_sub_categories))
    print("insert sub categories count success")


if __name__ == '__main__':
    with open('../resource/bjcp2021.json') as f:
        data = json.load(f)
        init_bjcp_datas(data)
