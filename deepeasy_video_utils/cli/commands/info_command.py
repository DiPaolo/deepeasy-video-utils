import sys

import click

import deepeasy_video_utils.cli.utils as cli_utils
from deepeasy_video_utils import config
from deepeasy_video_utils.cli.common import logger
from deepeasy_video_utils.cli.ret_codes import GENERATOR_CMD_START_RET_CODE
from deepeasy_video_utils.services.video_utils import get_video_duration


@click.group()
def info():
    pass


@info.command()
@click.option('-f', '--file', type=str, metavar='filename', help='Get media duration in seconds')
def duration(file: str):
    if file is None:
        logger.error('failed to get duration: file is not specified')
        click.echo("filename is not specified. Please specify it using '-f' or '--file'", err=True)
        sys.exit(GENERATOR_CMD_START_RET_CODE + 0)

    if config.CALC_PERFORMANCE:
        perf_counter = cli_utils.start_perf_counter(f"get media duration")

    duration_sec = get_video_duration(file)
    if duration_sec.is_integer():
        duration_sec = int(duration_sec)

    click.echo(duration_sec)

    if config.CALC_PERFORMANCE:
        cli_utils.print_perf_counter_report(perf_counter)

    sys.exit(0)
