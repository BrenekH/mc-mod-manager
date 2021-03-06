"""curse_forge is a Mod Provider for Curse Forge(curseforge.com).
"""

import os, platform, requests
from pathlib import Path
from requests.models import HTTPError
from typing import Dict, Tuple

from ..plugin import DownloadHandler, GenerationHandler, MCMMPlugin, PluginBase

if platform.system() == "Windows":
	cache_dir = Path(f"{os.getenv('LOCALAPPDATA')}/mcmm/cache/curse_forge")
else:
	cache_dir = Path(f"{os.getenv('HOME')}/.cache/mcmm/curse_forge")
cache_dir.mkdir(exist_ok=True, parents=True)

@MCMMPlugin
class CurseForgeModProvider(PluginBase):
	id = "curse_forge"
	help_string = "Curse Forge Mod Provider"

	@DownloadHandler
	def download_mod(self, mc_version, info) -> Tuple[Path, str]:
		id = info["id"]
		name = info["name"]

		r = requests.get(f"https://addons-ecs.forgesvc.net/api/v2/addon/{id}", headers={"User-Agent": "Mozilla/5.0"})
		try:
			r.raise_for_status()
		except HTTPError as e:
			return (Path.cwd(), str(e))

		json_obj = r.json()

		if info["check_file_name"] == None:
			file_id, filename, err_str = self._extract_file(mc_version, json_obj["gameVersionLatestFiles"])
			if err_str != "":
				return (Path.cwd(), err_str)
		else:
			file_id, filename, err_str = self._extract_file_with_file_name_check(mc_version, json_obj["gameVersionLatestFiles"], info["check_file_name"])
			if err_str != "":
				return (Path.cwd(), err_str)

		file_download_url = self._gen_download_url(file_id, filename)

		r = requests.get(file_download_url)
		try:
			r.raise_for_status()
		except HTTPError as e:
			return (Path.cwd(), str(e))

		out_file = cache_dir / f"{name}.jar"

		out_file.parent.mkdir(parents=True, exist_ok=True)

		with out_file.open("wb") as f:
			f.write(r.content)

		return (out_file, "")

	def _extract_file(self, mc_version: str, json_obj) -> Tuple[int, str, str]:
		file_id = 0
		filename = ""
		for obj in json_obj:
			if obj["gameVersion"] == mc_version:
				file_id = obj["projectFileId"]
				filename = obj["projectFileName"]
				break
		else:
			return (0, "", f"No files for Minecraft {mc_version} found!")

		return (file_id, filename, "")

	def _extract_file_with_file_name_check(self, mc_version: str, json_obj, search_file_name: str) -> Tuple[int, str, str]:
		file_id = 0
		filename = ""
		for obj in json_obj:
			if obj["gameVersion"] == mc_version and search_file_name.lower() in obj["projectFileName"].lower():
				file_id = obj["projectFileId"]
				filename = obj["projectFileName"]
				break
		else:
			return (0, "", f"No files for Minecraft {mc_version} found!")

		return (file_id, filename, "")

	def _gen_download_url(self, id: int, filename: str) -> str:
		str_id = str(id)
		return f"https://edge.forgecdn.net/files/{str_id[:4]}/{str_id[4:]}/{filename}"

	@GenerationHandler
	def generate(self) -> Tuple[Dict, str]:
		name = input("Name: ")
		ID = input("ID: ")
		check_file_name = input("Check file name (string that must be in the file name) leave blank for None: ")
		if check_file_name == "":
			check_file_name = None
		return ({"name": name, "id": ID, "check_file_name": check_file_name}, "")
