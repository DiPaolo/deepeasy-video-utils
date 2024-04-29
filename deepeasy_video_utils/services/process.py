import subprocess
from typing import List


def run_command(params: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(params, capture_output=True)
