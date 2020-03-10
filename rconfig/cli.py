import json
import os
import sys
from pprint import pformat

from rconfig import load_config_from_consul
from rconfig.utils import to_bash


try:
    import click
except ImportError:
    sys.stderr.write('Missing cli packages.\nRun pip install "rconfig[cli]"')


@click.group()
@click.option(
    '-h',
    '--host',
    required=True,
    default=os.environ.get('RCONFIG_CONSUL_HOST'),
    show_default=True,
    help='Host of a consul server',
)
@click.option(
    '-a',
    '--access',
    required=True,
    default=os.environ.get('RCONFIG_CONSUL_ACCESS_KEY'),
    show_default=True,
    help='Access key for a consul server',
)
@click.option(
    '-p',
    '--port',
    type=click.INT,
    default=os.environ.get('RCONFIG_CONSUL_PORT', 8500),
    show_default=True,
    help='Port of consul server',
)
@click.option('-k', '--key', required=True, multiple=True, help='Consul key')
@click.pass_context
def cli(ctx, host, port, access, key):
    config = load_config_from_consul(host, port, access, *key)
    ctx.obj = dict()
    ctx.obj['CONFIG'] = config


@cli.command()
@click.pass_context
def list(ctx):  # pylint: disable=redefined-builtin
    "Show all config for given keys"
    if ctx.obj['CONFIG']:
        click.echo(pformat(ctx.obj['CONFIG']))
    else:
        click.echo('No config for given keys')
        sys.exit(1)


@cli.command()
@click.pass_context
@click.option('--prefix', default='', help='Prefix for environment keys')
@click.option(
    '-f',
    '--format',
    type=click.Choice(['json', 'bash'], case_sensitive=False),
    default='bash',
    show_default=True,
    help='Format of exported data',
)
def export(ctx, prefix, format):  # pylint: disable=R0913,W0622
    "Print out bash command export for all found config"
    if format == 'bash':
        envs = to_bash(ctx.obj['CONFIG'], prefix=prefix)
    else:
        envs = json.dumps(ctx.obj['CONFIG'])
    if not envs:
        sys.exit(1)
    click.echo(envs)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
