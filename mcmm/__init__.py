from sys import argv

from .commands import _activate_dispatcher
from .commands import _download_dispatcher
from .plugin_internal import load_providers

__version__ = "0.0.1-alpha.1"

def cli():
	"""cli parses out sys.argv and dispatches the appropriate commands.
	"""
	command = argv[1] # mcmm [command]

	if command == "activate":
		_activate_dispatcher(argv[2:])

	elif command == "download":
		mod_providers = load_providers(["mcmm.curse_forge", "mcmm.optifine", "mcmm.github"])
		_download_dispatcher(argv[2:], mod_providers)
