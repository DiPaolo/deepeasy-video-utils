import pickle
from typing import Dict, Optional

_CACHE_FILENAME = '.deepeasy_video_utils.dat'


def _load_cache() -> Optional[Dict[str, str | int]]:
    try:
        with open(_CACHE_FILENAME, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


def get_cached_value(value_name: str, default: Optional[str | int] = None) -> str | int:
    data = _load_cache()

    value_name = value_name.lower()
    if data is None or value_name not in data:
        return default

    return data[value_name]


def save_cached_value(value_name: str, value: str | int):
    data = _load_cache()
    if data is None:
        data = dict()

    data[value_name.lower()] = value

    with open(_CACHE_FILENAME, 'wb') as f:
        pickle.dump(data, f)
