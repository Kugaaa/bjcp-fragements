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
    split_content = split_text(content)
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
    HighLightWordConfig('malt', highlight_color),
    HighLightWordConfig('hops', highlight_color),
    HighLightWordConfig('hop', highlight_color),
    HighLightWordConfig('yeasts', highlight_color),
    HighLightWordConfig('yeast', highlight_color),

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


def split_text(text):
    result = []
    current_block = ""

    i = 0
    while i < len(text):
        found_match = False
        for highlight_word in highlight_word_list:
            word = highlight_word.word
            ansi = highlight_word.ansi
            if text.startswith(word, i):
                if current_block:
                    result.append(HighlightWord(False, current_block, None))
                result.append(HighlightWord(True, word, ansi))
                current_block = ""
                i += len(word)
                found_match = True
                break

        if not found_match:
            current_block += text[i]
            i += 1

    if current_block:
        result.append(HighlightWord(False, current_block, None))

    return result


def show_abstract(categories: list[CategoryAbstract]):
    for category in categories:
        click.echo(f"[{category.id}] ", nl=False)
        click.secho("** " + category.name + " **", bg=base_bg_color, fg=base_bg_fg_color, bold=True)
        for sub_category in category.sub_categories:
            click.echo(f"- [{sub_category.id}] ", nl=False)
            click.secho(sub_category.name, fg=base_fg_color)
        click.echo("------------------------------")
