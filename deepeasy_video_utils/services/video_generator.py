import math
import os
from typing import Optional

from deepeasy_video_utils.services.process import run_command
from deepeasy_video_utils.services.utils import sec_to_human_readable
from deepeasy_video_utils.services.video_utils import get_video_duration


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
