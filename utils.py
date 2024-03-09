from pathlib import Path

base_path = Path(__file__).parent


def get_asset_path(relative_path: str):
	"""
	Get the absolute path of an asset.

	Note:
		The relative path must be relative to the asset directory. For example: "images/background/background.png"

	Args:
		relative_path (pathlib.Path): Path of an asset in assets folder.

	Returns:
		str: An absolute path of an asset provided.
	"""
	asset_path = base_path.joinpath('assets', relative_path)
	if asset_path.is_file():
		if asset_path.exists():
			return asset_path
		else:
			raise FileNotFoundError(f'No such asset {relative_path}.')
	else:
		raise IsADirectoryError('Provided path is a directory.')
