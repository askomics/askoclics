import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, dict_output


@click.command('integrate_bed')
@click.argument("file_id", type=str)
@click.option(
    "--entity",
    help="Name of the entity (default to file name)",
    type=str
)
@click.option(
    "--custom_uri",
    help="Custom uri",
    type=str
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, file_id, entity="", custom_uri=""):
    """Send an integration task for a specified file_id

Output:

    Dictionary of task information
    """
    return ctx.gi.file.integrate_bed(file_id, entity=entity, custom_uri=custom_uri)
