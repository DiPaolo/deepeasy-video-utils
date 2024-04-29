import os
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
@click.option('-f', '--file', type=str, metavar='filename',
              help='Get media duration (in seconds) of specific file')
@click.option('-d', '--dir', type=str, metavar='directory',
              help='Get media duration (in seconds) for every media in folder')
def duration(file: str, dir: str):
    if file is None and dir is None:
        logger.error('failed to get duration: neither filename nor directory is specified')
        click.echo("neither filename nor directory is specified. Please specify one of them using "
                   "'-f'/'--file' or '-d'/'--dir'", err=True)
        sys.exit(GENERATOR_CMD_START_RET_CODE + 0)

    if file and dir:
        logger.error('failed to get duration: the both file and directory are specified')
        click.echo("the both file and directory are specified. Please specify exactly one of them", err=True)
        sys.exit(GENERATOR_CMD_START_RET_CODE + 1)

    if config.CALC_PERFORMANCE:
        perf_counter = cli_utils.start_perf_counter(f"get media duration")

    def process_file(filename, exit_on_error: bool):
        duration_sec = get_video_duration(filename, True if exit_on_error else False)

        if duration_sec is None:
            if exit_on_error:
                err_msg = 'failed to get duration: unknown error'
                logger.error(err_msg)
                click.echo(err_msg, err=True)
                sys.exit(GENERATOR_CMD_START_RET_CODE + 2)
        else:
            if duration_sec.is_integer():
                duration_sec = int(duration_sec)

            if exit_on_error:
                click.echo(duration_sec)
            else:
                click.echo(f'{os.path.basename(filename)}: {duration_sec}')

    if file:
        process_file(file, True)
    elif dir:
        for file in [os.path.join(dir, file) for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]:
            process_file(file, False)
    else:
        pass

    if config.CALC_PERFORMANCE:
        cli_utils.print_perf_counter_report(perf_counter)

    sys.exit(0)
