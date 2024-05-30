import asyncio
import shutil
import os
import re
from colorama import Fore
from third_party.utils import lang_codes

video_reg = re.compile(
    r"video\[\d+\]\[(?P<quality>\d+)p\]" + \
    r"\[(?P<profile>[^\]]+)\]"
)
audio_subs_reg = re.compile(
    r"(audio|subtitles)\[\d+\]\[(?P<language>[^\]]+)\]" + \
    r"\[(?P<id>[^\]]+)\](?:\[(?P<codec>[^\]]+))?"
)

codecs = {
    "MAIN": "H.264",
    "HIGH": "H.264",
    "BASELINE": "H.264",
    "HEVC": "H.265",
    "HDR": "HDR.H.265"
}

class Muxer:
    def __init__(self, folder, muxed, verbose, keep):
        self.folder = folder
        self.muxed = muxed
        self.verbose = verbose
        self.keep = keep
        self.command = []

    async def run(self) -> dict:
        files = {
            "video": [],
            "audio": [],
            "subtitles": [],
        }
        data = {}
        for file in os.listdir(self.folder):
            for track in files.keys():
                if track not in file:
                    continue
                files[track].append(f"{self.folder}/{file}")

        for k in files.keys():
            if k == "video":
                for v in files[k]:
                    match = video_reg.search(v)
                    data["quality"] = match.group("quality")
                    data["vcodec"] = codecs.get(match.group("profile"))
                    # Adjust video compression settings for high quality
                    self.command += [
                        "mkvmerge",
                        "--output",
                        self.muxed,
                        "--compression",
                        "0:none",
                        "(", v, ")",
                    ]
            if k == "audio":
                for v in files[k]:
                    match = audio_subs_reg.search(v)
                    audio_language = lang_codes.get(match.group("id"))
                    if "audios" not in data:
                        data["audios"] = []
                    data["audios"].append(audio_language[1].upper())
                    data["acodec"] = match.group("codec")
                    # Adjust audio compression settings for high quality
                    self.command += [
                        "--language",
                        "0:"+audio_language[1],
                        "--track-name",
                        "0:"+match.group("language"),
                        "--compression",
                        "0:none",
                        "(", v, ")",
                    ]
            if k == "subtitles":
                for v in files[k]:
                    match = audio_subs_reg.search(v)
                    subtitle_language = lang_codes.get(match.group("id"))
                    # Ensure subtitles are added without compression
                    self.command += [
                        "--language",
                        "0:"+subtitle_language[1],
                        "--track-name",
                        "0:"+match.group("language"),
                        "--default-track",
                        "0:no",
                        "--forced-track",
                        "0:" + ("yes" if "Forced" in v else "no"),
                        "--compression",
                        "0:none",
                        "(", v, ")",
                    ]

        try:
            proc = await asyncio.create_subprocess_exec(
                *self.command,
                stdout=asyncio.subprocess.PIPE if not self.verbose else None,
                stderr=asyncio.subprocess.PIPE if not self.verbose else None
            )
            await proc.communicate()
        except:
            print(f"{Fore.YELLOW}[Widevine-KSKEY]: {Fore.RED}mkvmerge not found in your PATH or in your working folder.{Fore.RESET}")
            raise FileNotFoundError("mkvmerge not found in your PATH or in your working folder.")
        if not self.keep:
            shutil.rmtree(self.folder)
        return data