from typing import Optional


def sec_to_human_readable(sec: int) -> str:
    h = sec // 3600
    sec = sec % 3600

    m = sec // 60
    sec = sec % 60

    left_text = ''
    # if h > 0 or (h == 0 and left.days > 0):
    if h > 0:
        left_text += f'{h}hr'

    if m > 0:
        # if m > 0 or (m == 0 and (h > 0 or left.days > 0)):
        left_text += f'{m}min'

    if sec > 0:
        # if sec > 0 or (sec == 0 and (m > 0 or h > 0 or left.days > 0)):
        left_text += f'{sec}sec'

    return left_text


def sec_to_ffmpeg_duration(sec: float) -> Optional[str]:
    msec = int(sec * 1000)

    h = msec // 3600000
    msec = msec % 3600000

    m = msec // 60000
    msec = msec % 60000

    sec = msec // 1000
    msec = msec % 1000

    return f'{h:02}:{m:02}:{sec:02}'
