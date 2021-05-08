from pathlib import Path
from typing import Dict, Tuple

from ..plugin import DownloadHandler, GenerationHandler, MCMMPlugin, PluginBase

@MCMMPlugin
class ModrinthModProvider(PluginBase):
	@DownloadHandler
	def download(metadata: Dict) -> Tuple[Path, str]:
		# TODO: Implement
		return (Path.cwd(), "Not implemented")

	@GenerationHandler
	def generate() -> Tuple[Dict, str]:
		# TODO: Implement
		return ({}, "Not implemented")
