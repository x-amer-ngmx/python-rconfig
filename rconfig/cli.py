import sys
from pprint import pformat

from rconfig import (
    _serialize_value, _set_environment_variables, load_config_from_consul,
)


try:
    import click
except ImportError:
    sys.stderr.write('Missing cli packages.\nRun pip install "rconfig[cli]"')


@click.group()
@click.option('-h', '--host', required=True, help='Host of consul server')
@click.option(
    '-p', '--port', default=8500, type=click.INT, help='Port of consul server',
)
@click.option(
    '-a', '--access', required=True, help='Access key to consul server',
)
@click.option('--root', required=True, help='Root key')
@click.option('--app', required=True, help='Application key')
@click.option('--env', required=True, help='Environment key')
@click.option('--common', default='common', help='Common key')
@click.pass_context
def cli(ctx, host, port, access, root, app, env, common):
    ctx.obj = dict()
    ctx.obj['HOST'] = host
    ctx.obj['PORT'] = port
    ctx.obj['ACCESS'] = access
    ctx.obj['ROOT'] = root
    ctx.obj['APP'] = app
    ctx.obj['ENV'] = env
    ctx.obj['COMMON'] = common


@cli.command()
@click.pass_context
def list(ctx):  # pylint: disable=redefined-builtin
    "Show all config for given keys"
    host = ctx.obj['HOST']
    port = ctx.obj['PORT']
    access = ctx.obj['ACCESS']
    root = ctx.obj['ROOT']
    app = ctx.obj['APP']
    env = ctx.obj['ENV']
    common = ctx.obj['COMMON']
    config = load_config_from_consul(
        host, port, access, root, app, env, common,
    )
    if config:
        click.echo(pformat(config))
    else:
        click.echo('No config for given keys')
        sys.exit(1)


@cli.command()
@click.pass_context
@click.option('--prefix', default='', help='Prefix for environment keys')
def set_envs(ctx, prefix):  # pylint: disable=R0913
    "Set envs in current subprocess"
    host = ctx.obj['HOST']
    port = ctx.obj['PORT']
    access = ctx.obj['ACCESS']
    root = ctx.obj['ROOT']
    app = ctx.obj['APP']
    env = ctx.obj['ENV']
    common = ctx.obj['COMMON']
    config = \
        load_config_from_consul(host, port, access, root, app, env, common)
    if config:
        _set_environment_variables(config, prefix)
    else:
        click.echo('No config for given keys')
        sys.exit(1)


@cli.command()
@click.pass_context
@click.option('--prefix', default='', help='Prefix for environment keys')
def export(ctx, prefix):  # pylint: disable=R0913
    "Print out bash command export for all found config"
    host = ctx.obj['HOST']
    port = ctx.obj['PORT']
    access = ctx.obj['ACCESS']
    root = ctx.obj['ROOT']
    app = ctx.obj['APP']
    env = ctx.obj['ENV']
    common = ctx.obj['COMMON']
    config = load_config_from_consul(
        host, port, access, root, app, env, common,
    )
    envs = ' '.join(
        f'{prefix}{key}="{_serialize_value(value)}"'
        for key, value in config.items()
    )
    if not envs:
        sys.exit(1)
    click.echo(f'export {envs}')


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
