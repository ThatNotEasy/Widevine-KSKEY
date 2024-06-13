import os
import subprocess
import json
import requests
import xml.etree.ElementTree as ET
from pymediainfo import MediaInfo
from colorama import init, Fore
from modules.logging import setup_logging

init(autoreset=True)

logging = setup_logging()

def fetch_mpd(mpd_url, proxy=None):
    response = requests.get(mpd_url, proxies=proxy)
    response.raise_for_status()
    return response.text

def parse_mpd(mpd_content, proxy=None):
    root = ET.fromstring(mpd_content)
    namespaces = {'mpd': 'urn:mpeg:dash:schema:mpd:2011'}

    video_tracks = []
    audio_tracks = []
    subtitle_tracks = []

    video_id = 1
    audio_id = 1
    subtitle_id = 1

    for adaptation_set in root.findall('.//mpd:AdaptationSet', namespaces):
        mimeType = adaptation_set.get('mimeType', '')

        if 'video' in mimeType:
            for representation in adaptation_set.findall('mpd:Representation', namespaces):
                bandwidth = representation.get('bandwidth')
                width = representation.get('width')
                height = representation.get('height')
                codecs = representation.get('codecs')
                if width is not None and height is not None:
                    resolution = f"{width}x{height}"
                    quality_label = get_quality_label(int(width), int(height))
                    video_tracks.append({
                        'id': video_id,
                        'bandwidth': int(bandwidth),
                        'resolution': resolution,
                        'codecs': codecs,
                        'quality_label': quality_label
                    })
                    video_id += 1
                else:
                    print(Fore.YELLOW + f"Skipped a video representation with missing width or height attributes.")

        elif 'audio' in mimeType:
            lang = adaptation_set.get('lang', 'und')
            for representation in adaptation_set.findall('mpd:Representation', namespaces):
                bandwidth = representation.get('bandwidth')
                codecs = representation.get('codecs', 'unknown')
                if bandwidth is not None:
                    audio_tracks.append({
                        'id': audio_id,
                        'language': lang,
                        'bandwidth': int(bandwidth),
                        'codecs': codecs
                    })
                    audio_id += 1
                else:
                    print(Fore.YELLOW + f"Skipped an audio representation with missing bandwidth attribute.")

        elif 'text' in mimeType or 'subtitles' in mimeType:
            lang = adaptation_set.get('lang', 'und')
            for representation in adaptation_set.findall('mpd:Representation', namespaces):
                subtitle_tracks.append({
                    'id': subtitle_id,
                    'language': lang,
                })
                subtitle_id += 1

    return video_tracks, audio_tracks, subtitle_tracks

def get_quality_label(width, height):
    if width >= 3840 or height >= 2160:
        return "UHD"
    elif width >= 1920 or height >= 1080:
        return "HD"
    elif width >= 1280 or height >= 720:
        return "HD"
    else:
        return "SD"

def display_tracks(tracks, track_type):
    if not tracks:
        print(Fore.RED + f"{track_type} Tracks Not Found!")
        return

    print(Fore.BLUE + f"\n{track_type} Tracks:")
    print(Fore.MAGENTA + "=" * 110)
    for track in tracks:
        if track_type == "Video":
            print(f"{Fore.GREEN}{track['id']}: {Fore.YELLOW}Resolution: {track['resolution']} "
                  f"{Fore.MAGENTA}({track['quality_label']}) {Fore.RED}- {Fore.YELLOW}Bandwidth: {track['bandwidth']}bps "
                  f"{Fore.RED}- {Fore.GREEN}Codecs: {track['codecs']}")
        elif track_type == "Audio":
            print(f"{Fore.GREEN}{track['id']}: {Fore.YELLOW}Language: {track['language']} "
                  f"{Fore.RED}- {Fore.YELLOW}Bandwidth: {track['bandwidth']}bps {Fore.RED}- {Fore.GREEN}Codecs: {track['codecs']}")
        elif track_type == "Subtitle":
            print(Fore.CYAN + f"ID: {track['id']} - Language: {track['language']}")

def validate_keys(keys):
    valid_keys = []
    for key in keys:
        try:
            key = key.replace("--key ", "")
            key_id, key_value = key.split(':')
            valid_keys.append(f"{key_id.strip()}:{key_value.strip()}")
        except ValueError:
            logging.error("Key format error with key: %s", key)
            continue
    return valid_keys

def get_mp4_info(file_path):
    try:
        media_info = MediaInfo.parse(file_path)
        info = media_info.to_data()
        return info
    except Exception as e:
        logging.error(f"An error occurred while retrieving MP4 info: {e}")
        return None

def save_mp4_info(info, save_name):
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    log_file_path = os.path.join(logs_dir, f"{save_name}_info.json")
    try:
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            json.dump(info, log_file, indent=4)
        logging.info(f"MP4 info saved to {log_file_path}")
    except Exception as e:
        logging.error(f"An error occurred while saving MP4 info: {e}")

def reencode_video_to_hd(input_file, output_file):
    try:
        command = [
            'ffmpeg', '-i', input_file, '-vf', 'scale=1920:1080', '-c:v', 'libx264', 
            '-preset', 'slow', '-crf', '18', '-c:a', 'copy', output_file
        ]
        logging.info(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True)
        logging.info(f"Video re-encoded to HD successfully: {output_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to re-encode video to HD: {e}")

def segment_video_for_dash(input_file, output_mpd):
    try:
        command = [
            'mp4box', '-dash', '4000', '-rap', '-frag-rap', '-profile', 'onDemand', 
            '-out', output_mpd, input_file
        ]
        logging.info(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True)
        logging.info(f"Video segmented for DASH successfully: {output_mpd}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to segment video for DASH: {e}")

def download_video(url, save_name, keys, output_format, save_video_quality, save_audio_quality):
    temp_dir = "content"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    lang = input(f"{Fore.GREEN}Subtitle Language {Fore.RED}(eg: EN): {Fore.WHITE}")
    command = f'N_m3u8DL-RE "{url}" --save-dir {temp_dir} --save-name {save_name}'
    for key in keys:
        command += f' --key {key}'
    command += f' -mt -M format={output_format}:muxer=ffmpeg -sv {save_video_quality} -sa {save_audio_quality} -ss {lang}'
    
    logging.info(f"{Fore.GREEN}Running command: {Fore.RED}{command}{Fore.RESET}")
    logging.info(f"{Fore.MAGENTA}Please be patient ..{Fore.RESET}")

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True, encoding='utf-8', errors='replace')
        stdout, stderr = process.communicate()

        if stdout:
            print(stdout)
        if stderr:
            print(stderr)

        if process.returncode != 0:
            logging.error(f"Command failed with exit code {process.returncode}")
            raise subprocess.CalledProcessError(process.returncode, command)

        logging.info(f"{Fore.GREEN}Download completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"{Fore.RED}Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
        return False
    except FileNotFoundError:
        logging.error(f"{Fore.RED}m3u8dl.exe not found. Make sure it is installed and in the system PATH.")
        return False
    except Exception as e:
        logging.error(f"{Fore.RED}An error occurred: {e}")
        return False

def post_process_video(save_name, temp_dir):
    mp4_file_path = os.path.join(temp_dir, f"{save_name}.mp4")
    if os.path.exists(mp4_file_path):
        mp4_info = get_mp4_info(mp4_file_path)
        if mp4_info:
            save_mp4_info(mp4_info, save_name)

        hd_video_path = os.path.join(temp_dir, f"{save_name}_hd.mp4")
        reencode_video_to_hd(mp4_file_path, hd_video_path)

    encrypted_file_path = os.path.join(temp_dir, f"{save_name}.encrypted")
    if os.path.exists(encrypted_file_path):
        os.remove(encrypted_file_path)

def drm_downloader(url, save_name, keys, output_format='mkv', save_video_quality='best', save_audio_quality='best'):
    valid_formats = ['mp4', 'ts', 'flv', 'mkv']
    if output_format not in valid_formats:
        raise ValueError(f"Invalid output_format '{output_format}'. Valid formats are: {', '.join(valid_formats)}")
    
    if not all(isinstance(param, str) and param for param in [url, save_name, output_format, save_video_quality, save_audio_quality]):
        raise ValueError("URL, save_name, output_format, save_video_quality, and save_audio_quality must all be non-empty strings")
    if not keys or not all(isinstance(key, str) and ':' in key for key in keys):
        raise ValueError("Keys must be a non-empty list of strings in the format 'key_id:key_value'")

    init(autoreset=True)
    mpd_content = fetch_mpd(url)
    video_tracks, audio_tracks, subtitle_tracks = parse_mpd(mpd_content)

    display_tracks(video_tracks, "Video")
    display_tracks(audio_tracks, "Audio")
    display_tracks(subtitle_tracks, "Subtitle")

    temp_dir = "content"
    if download_video(url, save_name, keys, output_format, save_video_quality, save_audio_quality):
        # post_process_video(save_name, temp_dir)
        return True
    return False
