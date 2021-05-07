from json import load
from sys import argv

from . import curse_forge, github, optifine
from .commands import _activate_dispatcher
from .commands import _download_dispatcher
from .dirs import gen_config_dir
from .plugin_internal import load_providers

__version__ = "0.0.1-alpha.1"

def cli():
	"""cli parses out sys.argv and dispatches the appropriate commands.
	"""
	command = argv[1] # mcmm [command]

	if command == "activate":
		_activate_dispatcher(argv[2:])

	elif command == "download":
		internal_mps = [curse_forge, optifine, github]
		config_dir = gen_config_dir()
		config_file = config_dir / "config.json"

		if not config_file.exists():
			with config_file.open("w") as f:
				f.write(r'{"mod_providers": []}')

		with config_file.open("r") as f:
			user_conf = load(f)

		mod_providers = load_providers(user_conf["mod_providers"] + internal_mps)
		_download_dispatcher(argv[2:], mod_providers)
