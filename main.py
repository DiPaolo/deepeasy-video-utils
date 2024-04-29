import json
import math
import os
import subprocess
from typing import List, Optional


def run_command(params: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(params, capture_output=True)


def get_video_duration(filename: str) -> float:
    # ffprobe -v error -show_entries stream=duration -print_format json Best\ Kittycat\ Song\ \[OFFICIAL\]\ feat.\ GRUMPY\ CAT.mp4
    ret = run_command(['ffprobe', '-v', 'error', '-show_entries', 'stream=duration', '-print_format', 'json',
                       filename])
    json_data = json.loads(ret.stdout)

    max_duration = 0.0
    for stream in json_data['streams']:
        cur_duration = float(stream['duration'])
        if cur_duration > max_duration:
            max_duration = cur_duration

    return max_duration


def generate_10hrs_video(src_filename: str) -> None:
    target_duration_sec = 41 * 60 * 60
    src_duration = get_video_duration(src_filename)
    loop_count = math.ceil(target_duration_sec / src_duration)

    # ffmpeg -stream_loop 60 -i Best\ Kittycat\ Song\ \[OFFICIAL\]\ feat.\ GRUMPY\ CAT.mp4 -c copy Best\ Kittycat\ Song\ \[OFFICIAL\]\ feat.\ GRUMPY\ CAT\ 1\ hour.mp4
    splitted_filename = os.path.splitext(src_filename)
    src_base_filename = splitted_filename[0]
    src_ext = splitted_filename[1]
    run_command(['ffmpeg', '-stream_loop', str(loop_count), '-i', src_filename, '-c', 'copy', '-y',
                 f'{src_base_filename} 10 hours{src_ext}'])


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


def generate_test_video(width: int, height: int, duration_sec: int, framerate: float) -> Optional[str]:
    filter = f"drawtext=fontfile=tf.ttf: timecode='00\:00\:00\:00': r={framerate}: fontcolor=0xccFFFF@1: fontsize=96: box=1: boxcolor=0x000000@0.2"
    # filter1 = f"drawtext=fontfile=tf.ttf: text=WTF: x=10: y=400: fontcolor=0xccFFFF@1: fontsize=96: box=1: boxcolor=0x000000@0.2"
    filter = f"[in]drawtext=fontfile=tf.ttf: timecode='00\:00\:00\:00': r={framerate}: x=20: y=0: fontcolor=0xccFFFF@1: fontsize=96: box=1: boxcolor=0x000000@0.2, drawtext=fontfile=tf.ttf: text='{width}x{height}@{framerate}, {sec_to_human_readable(duration_sec)}': x=20: y=(w)-200: fontcolor=0xccFFFF@1: fontsize=36: box=1: boxcolor=0x000000@0.2[out]"
    # filter = "[in]drawtext=fontsize=60:timecode='00\:00\:00\:00':r={framerate}:x=20:y=0[out]"
    out_filename = \
        f'test_tv_signal_{width}_{height}_{framerate}fps_{sec_to_human_readable(duration_sec)}.mp4'

    cmdline = ['ffmpeg', '-f', 'lavfi', '-i', f'testsrc=duration={duration_sec}:size={width}x{height}:rate={framerate}',
               '-vf', filter, '-c:v', 'libx264', '-b:v', '500k', '-minrate', '500k', '-maxrate', '500k', '-bufsize',
               '500k', '-pix_fmt', 'yuv420p', out_filename]

    ret = run_command(cmdline)

    if ret.returncode != 0:
        print(ret.stderr)
        return None

    return out_filename


def main() -> None:
    framerates = [
        15, 20, 21, 24,
        25,
        29, 30, 50, 60
    ]
    durations = [
        1,
        # 4, 5, 6,
        9, 10, 11,
        15,
        29, 30, 31,
        # 44, 45, 46,
        59, 60, 61,
        # # 99, 100, 101,
        119, 120, 121,
        599, 600, 601,
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


if __name__ == '__main__':
    main()
