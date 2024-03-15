import re

from bjcp.service.service import SubCategory
from bjcp.service.service import CategoryAbstract
import click
from prettytable import PrettyTable

__sub_category_basic_params = {"id", "name", "category"}

# 背景色
base_bg_color = 220

# 背景色的前景色
base_bg_fg_color = 16

# 前景色
base_fg_color = 226

# 高亮颜色
highlight_color = 228

# 表格高亮颜色
table_highlight_color = 221


def show_sub_category_all(sub_category: SubCategory):
    # basic info
    click.echo("[" + sub_category.category.id, nl=False)
    click.secho("] ", nl=False)
    click.secho(sub_category.category.name + " > ", nl=False)
    click.secho("[" + sub_category.id + "] " + sub_category.name, fg=base_fg_color)

    # category notes
    if sub_category.category.notes:
        click.echo()
        click.secho("** Category Notes **", fg=base_fg_color)
        show_content(sub_category.category.notes)

    # sub category
    attributes = vars(sub_category)
    not_none_attributes = {
        key: value
        for key, value in attributes.items()
        if value is not None and key not in __sub_category_basic_params
    }

    for key, value in not_none_attributes.items():
        click.echo()
        # key capitalize first letter
        key = key.capitalize()
        click.secho("** " + key + " **", bg=base_bg_color, fg=base_bg_fg_color, bold=True)
        click.pause('')
        value = format_handle(value)
        show_content(value)


def format_handle(content):
    if isinstance(content, list):
        return '\n'.join('- ' + str(line) for line in content)
    if isinstance(content, dict):
        statistics_tb = PrettyTable(['dimensions', 'min', 'max'])
        for key, value in content.items():
            statistics_tb.add_row([str(key), value['min'], value['max']])
        return statistics_tb.__str__()
    return content


def show_content(content: str):
    split_content = split_highlight_text(content)
    for highlight_word in split_content:
        if highlight_word.is_in_array:
            click.secho(highlight_word.content, fg=highlight_word.ansi, bold=True, nl=False)
        else:
            click.echo(highlight_word.content, nl=False)
    click.echo()


class HighLightWordConfig:
    def __init__(self, word, ansi):
        self.word = word
        self.ansi = ansi


highlight_word_list = [
    HighLightWordConfig('beers', highlight_color),
    HighLightWordConfig('beer', highlight_color),
    HighLightWordConfig('malts', 220),
    HighLightWordConfig('malt', 220),
    HighLightWordConfig('hops', 119),
    HighLightWordConfig('hop', 119),
    HighLightWordConfig('yeasts', 230),
    HighLightWordConfig('yeast', 230),
    HighLightWordConfig('water', 87),

    HighLightWordConfig('og', table_highlight_color),
    HighLightWordConfig('ibus', table_highlight_color),
    HighLightWordConfig('fg', table_highlight_color),
    HighLightWordConfig('srm', table_highlight_color),
    HighLightWordConfig('abv', table_highlight_color),
]


class HighlightWord:
    def __init__(self, is_in_array, content, ansi):
        self.is_in_array = is_in_array
        self.content = content
        self.ansi = ansi


def remove_symbols(string):
    pattern = r'[^a-zA-Z0-9]'  # 匹配非字母、非数字、非空格的字符
    return re.sub(pattern, '', string)


def split_highlight_text(text: str):
    result = []
    highlight_words_set = {highlight_word.word: highlight_word for highlight_word in highlight_word_list}
    split_space = re.split(r'(\s)', text)
    for split in split_space:
        remove_symbols_spit = remove_symbols(split)
        if remove_symbols_spit in highlight_words_set:
            highlight_word_config = highlight_words_set.get(remove_symbols_spit)
            result.append(HighlightWord(True, highlight_word_config.word, highlight_word_config.ansi))
        else:
            result.append(HighlightWord(False, split, None))
    return result


def show_abstract(categories: list[CategoryAbstract]):
    for category in categories:
        click.echo(f"[{category.id}] ", nl=False)
        click.secho("** " + category.name + " **", bg=base_bg_color, fg=base_bg_fg_color, bold=True)
        for sub_category in category.sub_categories:
            click.echo(f"- [{sub_category.id}] ", nl=False)
            click.secho(sub_category.name, fg=base_fg_color)
        click.echo("------------------------------")
