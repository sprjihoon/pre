import os


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()
