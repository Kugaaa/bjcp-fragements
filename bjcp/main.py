import click
import bjcp.viewer as viewer
import bjcp.service.service as service


@click.group()
def cli():
    pass


@cli.command(name='c', help="BJCP style catalogue")
def dictionary():
    all_abstract = service.get_all_abstract()
    viewer.show_abstract(all_abstract)
    click.echo()


@cli.command(name='r', help="random BJCP style")
def random():
    random_info = service.random_sub_category()
    viewer.show_sub_category_all(random_info)
    click.echo()


@cli.command(name='q', help="query BJCP style by id")
@click.option('-id', type=str, required=True, help="category or sub category id")
def query(id: str):
    info = service.get_sub_category_by_id(id)
    viewer.show_sub_category_all(info)
    click.echo()


if __name__ == '__main__':
    random()
