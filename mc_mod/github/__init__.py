"""github is a Mod Provider for GitHub(github.com).
"""

import os
import requests
from dateutil.parser import isoparse
from github_release import get_releases
from pathlib import Path
from typing import Dict

latest_mc_version = "1.16.5"

save_dir = Path(f"{os.getenv('LOCALAPPDATA')}/mc_mod/cache/github")

save_dir.mkdir(parents=True, exist_ok=True)

def download_mod(info: Dict) -> Path:
	repo = info["repo"]

	if info["releases"] != None:
		return _releases(repo, info["releases"])
	elif info["compile"] != None:
		return _compile(repo, info["compile"])
	else:
		raise RuntimeError("'releases' or 'compile' must be defined")

def _releases(repo: str, info: Dict) -> Path:
	if info["latest"]:
		r = requests.get(f"https://api.github.com/repos/{repo}/releases/latest")
		r.raise_for_status()

		latest_release = r.json()

		for asset in latest_release["assets"]:
			invalid = False
			for s in info["must_contain"]:
				if s not in asset["name"]:
					invalid = True
					break
			if invalid:
				continue

			for s in info["must_not_contain"]:
				if s in asset["name"]:
					invalid = True
					break
			if invalid:
				continue

			r = requests.get(asset["browser_download_url"])
			r.raise_for_status()

			out_file: Path = save_dir / asset["name"]

			with out_file.open("wb") as f:
				f.write(r.content)

			return out_file

		raise RuntimeError(f"Could not locate a valid binary for {info}")

	else: # We have to evaluate all tags against info["tag"]
		matching_releases = [release for release in get_releases(repo) if info["tag"] in release["tag_name"]]

		times = [isoparse(r["published_at"]) for r in matching_releases]

		most_recent_release_time = max(times)

		most_recent_release = [r for r in matching_releases if isoparse(r["published_at"]) == most_recent_release_time][0]

		for asset in most_recent_release["assets"]:
			invalid = False
			for s in info["must_contain"]:
				if s not in asset["name"]:
					invalid = True
					break
			if invalid:
				continue

			for s in info["must_not_contain"]:
				if s in asset["name"]:
					invalid = True
					break
			if invalid:
				continue

			r = requests.get(asset["browser_download_url"])
			r.raise_for_status()

			out_file: Path = save_dir / asset["name"]

			with out_file.open("wb") as f:
				f.write(r.content)

			return out_file

		raise RuntimeError(f"Could not locate a valid binary for {info}")

def _compile(repo: str, info: Dict) -> Path:
	return Path.cwd() / "test.jar"

def _sanitize_url(url: str) -> str:
	if url.startswith("https://") or url.startswith("http://"):
		return url
	return "https://" + url
