import click
from askoclics.cli import pass_context, json_loads
from askoclics.decorators import custom_exception, list_output


@click.command('list')
@pass_context
@custom_exception
@list_output
def cli(ctx):
    """List datasets added in Askomics

Output:

    List of datasets
    """
    return ctx.gi.dataset.list()
