import time
import uuid

import click

from deepeasy_video_utils.cli.common import logger

_COUNTERS = {}  # key - UUID, value - tuple that contains name + perf counter value


def start_perf_counter(operation_name: str) -> uuid.UUID:
    new_uuid = uuid.uuid4()
    _COUNTERS[new_uuid] = (operation_name, time.perf_counter())
    return new_uuid


def print_perf_counter_report(perf_counter_uuid: uuid.UUID) -> float:
    if perf_counter_uuid not in _COUNTERS:
        logger.error(f'failed to print perf_counter report: unknown uuid (uuid={perf_counter_uuid})')
        return 0.0

    perf_counter_info = _COUNTERS.pop(perf_counter_uuid)

    elapsed_seconds = time.perf_counter() - perf_counter_info[1]

    msg_text = f"operation '{perf_counter_info[0]}' took {elapsed_seconds:0.4f} seconds"
    logger.info(msg_text)

    # first letter must be upper-cased as long as we show it to the user
    click.echo(msg_text[0].upper() + msg_text[1:])

    return elapsed_seconds


def get_first_letter_uppercased(text: str) -> str:
    return text[0].upper() + text[1:]
