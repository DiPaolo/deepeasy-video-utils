import sys

import click

import deepeasy_video_utils.cli.utils as cli_utils
from deepeasy_video_utils.services.utils import sec_to_human_readable
from deepeasy_video_utils.services.video_generator import generate_test_video


@click.group()
def generator():
    pass


@generator.command()
# @click.option('--name', type=str, default=None, help='Name of logs to list')
def test_signal():
    # if name is None:
    #     logger.error('failed to list logs: logs name is not specified')
    #     click.echo("ERROR: Logs name is not specified. Please specify it using '--name'")
    #     sys.exit(LOGS_CMD_START_RET_CODE + 0)
    #
    # utils.use_credentials()

    perf_counter = cli_utils.start_perf_counter(f"list {name} logs")

    # total_count, logins_logs = logs_service.get_login_logs()

    # limited_logs = len(logins_logs)

    # logger.info(f'getting login logs done (total_count={total_count}, limited_logs={limited_logs})')

    framerates = [
        # 15, 20, 21, 24,
        25,
        # 29, 30, 50, 60
    ]
    durations = [
        # 1,
        # 4, 5, 6,
        # 9, 10, 11,
        15,
        # 29, 30, 31,
        # 44, 45, 46,
        # 59, 60, 61,
        # # 99, 100, 101,
        # 119, 120, 121,
        # 599, 600, 601,
        # 60 * 60 - 1, 60 * 60, 60 * 60 + 1,
        # 2 * 60 * 60 - 1, 2 * 60 * 60, 2 * 60 * 60 + 1,
        # 6 * 60 * 60 - 1, 6 * 60 * 60, 6 * 60 * 60 + 1,
        # 6 * 60 * 60 + 60 + 10,
        # 6 * 60 * 60 + 12 * 60 + 33,
        # 6 * 60 * 60 + 47 * 60 + 52
    ]
    resolutions = [(640, 480)]

    for resolution in resolutions:
        width = resolution[0]
        height = resolution[1]

        for framerate in framerates:
            for duration in durations:
                print(f'generating {width}x{height}@{framerate} of {sec_to_human_readable(duration)}...', end=' ')
                filename = generate_test_video(width, height, duration, framerate)
                print(f'OK: {filename}' if filename else 'failed')

    # if total_count == 0:
    #     click.echo(f"No login logs found")
    #     sys.exit(0)
    #
    # click.echo(f"Found {total_count} login logs. {limited_logs} will be shown:")
    # for l in logins_logs:
    #     click.echo(f'  {l.created_date} {l.user_id}')

    cli_utils.print_perf_counter_report(perf_counter)

    sys.exit(0)
