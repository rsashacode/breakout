"""
Utility functions for handling paths
"""

import os
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent


def get_asset_path(relative_path: str) -> Path:
    """
    Get the absolute path of an asset.

    Note:
        The relative path must be relative to the asset directory. For example: "images/background/background.png"

    Args:
        relative_path (pathlib.Path): Path of an asset in assets folder.

    Returns:
        Path: An absolute path of an asset provided.
    """
    asset_path = base_path.joinpath('assets', relative_path)
    if asset_path.is_file():
        if asset_path.exists():
            return asset_path
        raise FileNotFoundError(f'No such asset {relative_path}.')
    raise IsADirectoryError(f'Provided path {asset_path} is a directory.')
