#!/usr/bin/env python3
"""
Build a single-file version of the game with the music baked in.

index.html normally loads music/*.mp3 from alongside itself. That works when
the game is served from a web address (Vercel) or opened from this computer,
but the claude.ai artifact is one standalone HTML file with no music folder
and no permission to fetch audio from anywhere else — so it would always fall
back to the generated score.

This script compresses the four tracks and inlines them as data: URIs, so the
artifact plays the real music too. index.html itself is left untouched and
keeps using the full-quality files.

Usage:  python build-artifact.py
Output: .build/artifact.html
"""

import base64
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).parent
BUILD = ROOT / ".build"
TRACKS = ["explore", "battle", "story", "victory"]
BITRATE = "64k"          # mono; keeps all four comfortably inside the 16 MB cap
ARTIFACT_LIMIT = 16 * 1024 * 1024


def main() -> int:
    if shutil.which("ffmpeg") is None:
        print("ffmpeg not found - install it or lower the bitrate by hand.")
        return 1

    BUILD.mkdir(exist_ok=True)
    encoded = {}

    for name in TRACKS:
        src = ROOT / "music" / f"{name}.mp3"
        if not src.exists():
            print(f"missing {src}")
            return 1
        small = BUILD / f"{name}.mp3"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
             "-ac", "1", "-b:a", BITRATE, "-ar", "44100", str(small)],
            check=True,
        )
        raw = small.read_bytes()
        encoded[name] = "data:audio/mpeg;base64," + base64.b64encode(raw).decode("ascii")
        print(f"  {name:8} {len(raw) / 1048576:5.2f} MB")

    html = (ROOT / "index.html").read_text(encoding="utf-8")

    # The game reads window.TITAN_MUSIC if it is present, so this prelude has
    # to run before the main script.
    prelude = "<script>window.TITAN_MUSIC={" + ",".join(
        f'{name}:"{data}"' for name, data in encoded.items()
    ) + "};</script>\n"

    marker = "<title>"
    if marker not in html:
        print("could not find <title> to inject before")
        return 1
    out = html.replace(marker, prelude + marker, 1)

    dest = BUILD / "artifact.html"
    dest.write_text(out, encoding="utf-8")

    size = dest.stat().st_size
    print(f"\n{dest}  {size / 1048576:.2f} MB of {ARTIFACT_LIMIT / 1048576:.0f} MB")
    if size > ARTIFACT_LIMIT:
        print("TOO BIG - lower BITRATE and run again.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
