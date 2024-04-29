import sys

import click

import deepeasy_video_utils.cli.utils as cli_utils
from deepeasy_video_utils import config
from deepeasy_video_utils.services.utils import sec_to_human_readable
from deepeasy_video_utils.services.video_generator import generate_test_video


@click.group()
def generator():
    pass


@generator.command()
def test_signal():
    if config.CALC_PERFORMANCE:
        perf_counter = cli_utils.start_perf_counter(f"generate test signal")

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

    if config.CALC_PERFORMANCE:
        cli_utils.print_perf_counter_report(perf_counter)

    sys.exit(0)
