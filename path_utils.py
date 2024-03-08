import os
from pathlib import Path

base_path = Path(__file__).parent


def get_asset_path(relative_path: str):
	asset_path = base_path.joinpath('assets', relative_path)
	if asset_path.is_file():
		if asset_path.exists():
			return asset_path
		else:
			raise FileNotFoundError(f'No such asset {relative_path}.')
	else:
		raise IsADirectoryError('Provided path is a directory.')
