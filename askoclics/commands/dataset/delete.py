import click
from askoclics.cli import pass_context, json_loads
from askoclics.decorators import custom_exception, list_output


@click.command('delete')
@click.argument("datasets", type=str)
@pass_context
@custom_exception
@list_output
def cli(ctx, datasets):
    """Delete a list of files

Output:

    List of the remaining files
    """
    return ctx.gi.dataset.delete(datasets)
