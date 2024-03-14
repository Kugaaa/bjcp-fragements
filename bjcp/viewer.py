from bjcp.service.service import SubCategory
from bjcp.service.service import CategoryAbstract
import click
import re

__sub_category_basic_params = {"id", "name", "category"}

# 背景色
base_bg_color = 220

# 背景色的前景色
base_bg_fg_color = 16

# 前景色
base_fg_color = 226

# 高亮颜色
highlight_color = 228


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
        return '\n'.join('- ' + key + ': ' + (
            f"[{value['min']}, {value['max']}]" if isinstance(value, dict) else str(value)) for key, value
                         in content.items())
    return content


def show_content(content: str):
    split_content = split_text(content)
    for highlight_word in split_content:
        if highlight_word.is_in_array:
            click.secho(highlight_word.content, fg=highlight_color, bold=True, nl=False)
        else:
            click.echo(highlight_word.content, nl=False)
    click.echo()


highlight_word_list = ['beer']


class HighlightWord:
    def __init__(self, is_in_array, content):
        self.is_in_array = is_in_array
        self.content = content


def split_text(text):
    result = []
    current_block = ""

    i = 0
    while i < len(text):
        found_match = False
        for word in highlight_word_list:
            if text.startswith(word, i):
                if current_block:
                    result.append(HighlightWord(False, current_block))
                result.append(HighlightWord(True, word))
                current_block = ""
                i += len(word)
                found_match = True
                break

        if not found_match:
            current_block += text[i]
            i += 1

    if current_block:
        result.append(HighlightWord(False, current_block))

    return result


def show_abstract(categories: list[CategoryAbstract]):
    for category in categories:
        click.echo(f"[{category.id}] ", nl=False)
        click.secho("** " + category.name + " **", bg=base_bg_color, fg=base_bg_fg_color, bold=True)
        for sub_category in category.sub_categories:
            click.echo(f"- [{sub_category.id}] ", nl=False)
            click.secho(sub_category.name, fg=base_fg_color)
        click.echo("------------------------------")
