import logging
import os

import click as click

from deepeasy_video_utils import config
from deepeasy_video_utils.cli.commands.generator_command import generator
from deepeasy_video_utils.cli.commands.info_command import info


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
