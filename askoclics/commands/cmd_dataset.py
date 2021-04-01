import click
from askoclics.commands.dataset.delete import cli as delete
from askoclics.commands.dataset.list import cli as list
from askoclics.commands.dataset.publicize import cli as publicize


@click.group()
def cli():
    """
    Manipulate datasets managed by Askomics
    """
    pass


cli.add_command(delete)
cli.add_command(list)
cli.add_command(publicize)
