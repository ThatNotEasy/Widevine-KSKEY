import re
from third_party.utils import lang_codes

class Parse:
    def __init__(self, playlist, client):

        self.video_streams = sorted([
            dict(
                bitrate=track["bitrate"],
                url=track["urls"][0]["url"],
                size=track["size"],
                w=track["res_w"],
                h=track["res_h"]
            ) for track in playlist["result"]["video_tracks"][0]["streams"]],
            key=lambda x: x["bitrate"], reverse=True
        )
    
        self.audio_streams = dict()
        for track in playlist["result"]["audio_tracks"]:
            track_language = track["language"]
            name = track["languageDescription"]
            if "Audio Description" in name:
                continue
            language = lang_codes.get(track_language, [None])[0]
            if not language:
                print(f"{track_language} skipped. Please report this!")
                continue
            is_original = "Original" in name
            audio_list = list(map(lambda x: x.lower(), client.audio_language))

            if not (is_original and "original" in audio_list) \
            and language not in self.audio_streams:
                if language.lower() not in audio_list and "all" not in audio_list:
                    continue
            
            self.audio_streams[language] = sorted([
                dict(
                    bitrate=stream["bitrate"],
                    url=stream["urls"][0]["url"],
                    size=stream["size"],
                    language=language,
                    language_code=track["language"]
                ) for stream in track["streams"]],
                key=lambda x: x["bitrate"], reverse=True
            )

        self.audio_description_streams = dict()
        for track in playlist["result"]["audio_tracks"]:
            track_language = track["language"]
            name = track["languageDescription"]
            if "Audio Description" not in name:
                continue
            language = lang_codes.get(track_language, [None])[0]
            if not language:
                print(f"{track_language} skipped. Please report this!")
                continue
            audesc_list = list(map(lambda x: x.lower(), client.audio_description_language))
            if language.lower() not in audesc_list and "all" not in audesc_list:
                continue
            self.audio_description_streams[language+"AD"] = sorted([
                dict(
                    bitrate=stream["bitrate"],
                    url=stream["urls"][0]["url"],
                    size=stream["size"],
                    language=f"{language} (Audio Description)",
                    language_code=track["language"]
                ) for stream in track["streams"]],
                key=lambda x: x["bitrate"], reverse=True
            )

        self.subtitle_streams = dict()
        for track in playlist["result"]["timedtexttracks"]:
            if track["languageDescription"] == "Off" or \
            not track["language"] or track["isNoneTrack"] or \
            track["trackType"] == "ASSISTIVE": # I skip ASSISTIVE cuz yes
                continue
            track_language = track["language"]
            language = lang_codes.get(track_language, [None])[0]
            if not language:
                print(f"{track_language} skipped. Please report this!")
                continue
            subtitles_list = list(map(lambda x: x.lower(), client.subtitle_language))
            if language.lower() not in subtitles_list and "all" not in subtitles_list:
                continue
            url = list(track["ttDownloadables"]["webvtt-lssdh-ios8"]["downloadUrls"].values())[0]
            self.subtitle_streams[language] = [
                dict(url=url, language=language,
                    language_code=track["language"])
            ]

        self.forced_streams = dict()
        for track in playlist["result"]["timedtexttracks"]:
            if not track["isForcedNarrative"] or \
            not track["language"] or track["isNoneTrack"] or \
            track["trackType"] == "ASSISTIVE": # I skip ASSISTIVE cuz yes:
                continue
            track_language = track["language"]
            language = lang_codes.get(track_language, [None])[0]
            if not language:
                print(f"{track_language} skipped. Please report this!")
                continue
            forced_list = list(map(lambda x: x.lower(), client.forced_language))
            if language.lower() not in forced_list and "all" not in forced_list:
                continue
            url = list(track["ttDownloadables"]["webvtt-lssdh-ios8"]["downloadUrls"].values())[0]
            self.forced_streams[language+"F"] = [
                dict(url=url, language=f"{language} (Forced)",
                    language_code=track["language"])
            ]
