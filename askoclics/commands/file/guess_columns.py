import click
from askoclics.cli import pass_context, json_loads
from askoclics.decorators import custom_exception, list_output


@click.command('guess_columns')
@click.argument("files", type=str)
@pass_context
@custom_exception
@list_output
def cli(ctx, files):
    """Get the guessed columns for a file

Output:

    List of files containing info
    """
    return ctx.gi.file.guess_columns(files)
