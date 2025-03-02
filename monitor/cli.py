import click
import os
from os.path import expanduser

from utils.package import get_package_version
from tracking.anonymous_tracking import AnonymousTracking, track_cli_start, track_cli_exception, track_cli_end
from utils.cli_utils import RequiredIf
from utils.ordered_yaml import OrderedYaml
from config.config import Config
from monitor.data_monitoring import DataMonitoring

yaml = OrderedYaml()


def get_cli_properties() -> dict:

    click_context = click.get_current_context()
    if click_context is None:
        return dict()

    params = click_context.params
    if params is None:
        return dict()

    reload_monitoring_configuration = params.get('reload_monitoring_configuration')
    update_dbt_package = params.get('update_dbt_package')
    full_refresh_dbt_package = params.get('full_refresh_dbt_package')

    return {'reload_monitoring_configuration': reload_monitoring_configuration,
            'update_dbt_package': update_dbt_package,
            'full_refresh_dbt_package': full_refresh_dbt_package,
            'version': get_package_version()}


@click.group(invoke_without_command=True)
@click.option(
    '--days-back', '-d',
    type=int,
    default=7,
    help="Set a limit to how far back edr should look for new alerts"
)
@click.option(
    '--slack-webhook', '-s',
    type=str,
    default=None,
    help="A slack webhook URL for sending alerts to a specific channel (also could be configured once in config.yml)"
)
@click.option(
    '--slack-token', '-st',
    type=str,
    default=None,
    help="A slack token for sending alerts over slack (also could be configured once in config.yml)",
    cls=RequiredIf,
    required_if="slack_channel_name"
)
@click.option(
    '--slack-channel-name', '-ch',
    type=str,
    default=None,
    help="The slack channel which all alerts will be sent to (also could be configured once in config.yml)",
    cls=RequiredIf,
    required_if="slack_token"
)
@click.option(
    '--config-dir', '-c',
    type=str,
    default=os.path.join(expanduser('~'), '.edr'),
    help="Global settings for edr are configured in a config.yml file in this directory "
         "(if your config dir is HOME_DIR/.edr, no need to provide this parameter as we use it as default)."
)
@click.option(
    '--profiles-dir', '-p',
    type=str,
    default=os.path.join(expanduser('~'), '.dbt'),
    help="Specify your profiles dir where a profiles.yml is located, this could be a dbt profiles dir "
         "(if your profiles dir is HOME_DIR/.dbt, no need to provide this parameter as we use it as default).",
)
@click.option(
    '--update-dbt-package', '-u',
    type=bool,
    default=False,
    help="Force downloading the latest version of the edr internal dbt package (usually this is not needed, "
         "see documentation to learn more)."
)
@click.option(
    '--full-refresh-dbt-package', '-f',
    type=bool,
    default=False,
    help="Force running a full refresh of all incremental models in the edr dbt package (usually this is not needed, "
         "see documentation to learn more)."
)
@click.option(
    '--profile-target', '-t',
    type=str,
    default=None,
    help="if you have multiple targets for Elementary, optionally use this flag to choose a specific target"
)
@click.pass_context
def monitor(
    ctx,
    days_back,
    slack_webhook,
    slack_token,
    slack_channel_name,
    config_dir,
    profiles_dir,
    update_dbt_package,
    full_refresh_dbt_package,
    profile_target
):
    click.echo(f"Any feedback and suggestions are welcomed! join our community here - "
               f"https://bit.ly/slack-elementary\n")
    if ctx.invoked_subcommand is not None:
        return
    config = Config(config_dir, profiles_dir, profile_target)
    anonymous_tracking = AnonymousTracking(config)
    track_cli_start(anonymous_tracking, 'monitor', get_cli_properties(), ctx.command.name)
    try:
        data_monitoring = DataMonitoring(
            config=config,
            force_update_dbt_package=update_dbt_package,
            slack_webhook=slack_webhook,
            slack_token=slack_token,
            slack_channel_name=slack_channel_name
        )
        data_monitoring.run(days_back, full_refresh_dbt_package)
        success = data_monitoring.run(days_back, full_refresh_dbt_package)
        track_cli_end(anonymous_tracking, 'monitor', data_monitoring.properties(), ctx.command.name)
        if not success:
            return 1
        return 0
    except Exception as exc:
        track_cli_exception(anonymous_tracking, 'monitor', exc, ctx.command.name)
        raise


@monitor.command()
@click.option(
    '--config-dir', '-c',
    type=str,
    default=os.path.join(expanduser('~'), '.edr'),
    help="Global settings for edr are configured in a config.yml file in this directory "
         "(if your config dir is HOME_DIR/.edr, no need to provide this parameter as we use it as default)."
)
@click.option(
    '--profiles-dir', '-p',
    type=str,
    default=os.path.join(expanduser('~'), '.dbt'),
    help="Specify your profiles dir where a profiles.yml is located, this could be a dbt profiles dir "
         "(if your profiles dir is HOME_DIR/.dbt, no need to provide this parameter as we use it as default).",
)
@click.option(
    '--update-dbt-package', '-u',
    type=bool,
    default=False,
    help="Force downloading the latest version of the edr internal dbt package (usually this is not needed, "
         "see documentation to learn more)."
)
@click.option(
    '--profile-target', '-t',
    type=str,
    default=None,
    help="if you have multiple targets for Elementary, optionally use this flag to choose a specific target"
)
@click.pass_context
def report(ctx, config_dir, profiles_dir, update_dbt_package, profile_target):
    config = Config(config_dir, profiles_dir, profile_target)
    anonymous_tracking = AnonymousTracking(config)
    track_cli_start(anonymous_tracking, 'monitor-report', get_cli_properties(), ctx.command.name)
    try:
        data_monitoring = DataMonitoring(config, update_dbt_package)
        success = data_monitoring.generate_report()
        track_cli_end(anonymous_tracking, 'monitor-report', data_monitoring.properties(), ctx.command.name)
        if not success:
            return 1
        return 0
    except Exception as exc:
        track_cli_exception(anonymous_tracking, 'monitor-report', exc, ctx.command.name)
        raise


@monitor.command()
@click.option(
    '--config-dir', '-c',
    type=str,
    default=os.path.join(expanduser('~'), '.edr'),
    help="Global settings for edr are configured in a config.yml file in this directory "
         "(if your config dir is HOME_DIR/.edr, no need to provide this parameter as we use it as default)."
)
@click.option(
    '--profiles-dir', '-p',
    type=str,
    default=os.path.join(expanduser('~'), '.dbt'),
    help="Specify your profiles dir where a profiles.yml is located, this could be a dbt profiles dir "
         "(if your profiles dir is HOME_DIR/.dbt, no need to provide this parameter as we use it as default).",
)
@click.option(
    '--update-dbt-package', '-u',
    type=bool,
    default=False,
    help="Force downloading the latest version of the edr internal dbt package (usually this is not needed, "
         "see documentation to learn more)."
)
@click.option(
    '--slack-webhook', '-s',
    type=str,
    default=None,
    help="A slack webhook URL for sending alerts to a specific channel (also could be configured once in config.yml)"
)
@click.option(
    '--slack-token', '-st',
    type=str,
    default=None,
    help="A slack token for sending alerts over slack (also could be configured once in config.yml)",
    cls=RequiredIf,
    required_if="slack_channel_name"
)
@click.option(
    '--slack-channel-name', '-ch',
    type=str,
    default=None,
    help="The slack channel which all alerts will be sent to (also could be configured once in config.yml)",
    cls=RequiredIf,
    required_if="slack_token"
)
@click.option(
    '--profile-target', '-t',
    type=str,
    default=None,
    help="if you have multiple targets for Elementary, optionally use this flag to choose a specific target"
)
@click.pass_context
def send_report(
    ctx,
    config_dir,
    profiles_dir,
    update_dbt_package,
    slack_webhook,
    slack_token,
    slack_channel_name,
    profile_target
):
    config = Config(config_dir, profiles_dir, profile_target)
    anonymous_tracking = AnonymousTracking(config)
    track_cli_start(anonymous_tracking, 'monitor-send-report', get_cli_properties(), ctx.command.name)
    try:
        data_monitoring = DataMonitoring(
            config=config,
            force_update_dbt_package=update_dbt_package,
            slack_webhook=slack_webhook,
            slack_token=slack_token,
            slack_channel_name=slack_channel_name
        )
        generated_report_successfully, elementary_html_path = data_monitoring.generate_report()
        sent_report_successfully = data_monitoring.send_report(elementary_html_path)
        if not (generated_report_successfully and sent_report_successfully):
            return 1
        return 0
    except Exception as exc:
        track_cli_exception(anonymous_tracking, 'monitor-send-report', exc, ctx.command.name)
        raise


if __name__ == "__main__":
    monitor()
