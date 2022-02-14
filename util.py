from pathlib import Path

root = Path(__file__).parent


def get_real_path(abs_path):
    return root / abs_path
