import json
import os


def load_config() -> dict:
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    with open(os.path.join(current_dir, 'config.json'), 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config
