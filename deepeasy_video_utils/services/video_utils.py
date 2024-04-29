import json

from deepeasy_video_utils.services.process import run_command


def get_video_duration(filename: str) -> float:
    # ffprobe -v error -show_entries stream=duration -print_format json Best\ Kittycat\ Song\ \[OFFICIAL\]\ feat.\ GRUMPY\ CAT.mp4
    ret = run_command(
        ['ffprobe', '-hide_banner', '-v', 'error', '-show_entries', 'stream=duration', '-print_format', 'json',
         filename])
    json_data = json.loads(ret.stdout)

    max_duration = 0.0
    for stream in json_data['streams']:
        cur_duration = float(stream['duration'])
        if cur_duration > max_duration:
            max_duration = cur_duration

    return max_duration
