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
@click.option(
    "--skip_preview",
    help="Skip the preview step for big files",
    is_flag=True
)
@click.option(
    "--public",
    help="Set the generated dataset as public (admin only)",
    is_flag=True
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, file_id, entity="", custom_uri="", skip_preview=False, public=False):
    """Send an integration task for a specified file_id

Output:

    Dictionary of task information
    """
    return ctx.gi.file.integrate_bed(file_id, entity=entity, custom_uri=custom_uri, skip_preview=skip_preview, public=public)
