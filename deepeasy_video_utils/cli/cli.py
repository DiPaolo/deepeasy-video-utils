import logging
import os
import sys

import click as click

import deepeasy_video_utils.cli.utils as cli_utils
from deepeasy_video_utils import config
from deepeasy_video_utils.cli.commands.generator_command import generator
from deepeasy_video_utils.cli.commands.info_command import info
from deepeasy_video_utils.cli.common import logger
from deepeasy_video_utils.cli.ret_codes import LOOP_CMD_START_RET_CODE
from deepeasy_video_utils.services.video_generator import loop_video


@click.group()
@click.option('--debug/--no-debug', default=None)
@click.option('--perf/--no-perf', default=None, help='Calculate performance')
def cli(debug: bool, perf: bool):
    # apply env variables first;
    # commands line parameters have higher priority, so it goes after
    _apply_env_variables_to_config()
    # ... and cached variables next
    _apply_cached_variables_to_config()

    if debug is not None:
        config.DEBUG = debug
        config.DEBUG_PRINT = debug

    if perf is not None:
        config.CALC_PERFORMANCE = perf

    if config.DEBUG:
        logging.getLogger().setLevel(logging.DEBUG)


cli.add_command(generator)
cli.add_command(info)


@cli.command(help='Loop source video')
@click.option('-f', '--file', type=str, metavar='filename', help='Source video file')
@click.option('-d', '--duration', type=int, metavar='duration', help='Target duration in seconds')
def loop(file: str, duration: int):
    if file is None:
        logger.error('failed to loop video: file is not specified')
        click.echo("filename is not specified. Please specify it using '-f' or '--file'", err=True)
        sys.exit(LOOP_CMD_START_RET_CODE + 0)

    if config.CALC_PERFORMANCE:
        perf_counter = cli_utils.start_perf_counter(f"loop video")

    filename = loop_video(file, duration)

    if config.CALC_PERFORMANCE:
        cli_utils.print_perf_counter_report(perf_counter)

    if filename is None:
        err_msg = 'failed to loop video: unknown error'
        logger.error(err_msg)
        click.echo(err_msg, err=True)
        sys.exit(LOOP_CMD_START_RET_CODE + 1)

    click.echo(filename)

    sys.exit(0)


def init_app():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # database and other initializations


def deinit_app():
    _store_cached_variables()


def _get_env_val_as_bool(val) -> bool:
    return val if type(val) == bool else val.lower() in ['true', 'yes', '1']


def _apply_env_variables_to_config():
    env_debug_val = os.environ.get('DPZ_VIDEO_UTILS_DEBUG')
    if env_debug_val:
        config.DEBUG = _get_env_val_as_bool(env_debug_val)


def _apply_cached_variables_to_config():
    # user_name = cache.get_cached_value('USER_NAME')
    # if user_name:
    #     config.USER_NAME = user_name
    #
    # user_password = cache.get_cached_value('USER_PASSWORD')
    # if user_password:
    #     config.USER_PASSWORD = user_password
    pass


def _store_cached_variables():
    # if config.USER_NAME:
    #     cache.save_cached_value('USER_NAME', config.USER_NAME)
    #
    # if config.USER_PASSWORD:
    #     cache.save_cached_value('USER_PASSWORD', config.USER_PASSWORD)

    pass
