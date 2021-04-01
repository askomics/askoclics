import click
from askoclics.cli import pass_context, json_loads
from askoclics.decorators import custom_exception, list_output


@click.command('list')
@pass_context
@custom_exception
@list_output
def cli(ctx):
    """List files added in Askomics

Output:

    List with files
    """
    return ctx.gi.file.list()
