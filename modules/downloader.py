import os
import subprocess
import json
import requests
import xml.etree.ElementTree as ET
from pymediainfo import MediaInfo
from colorama import init, Fore
import random, tempfile, string
from modules.logging import setup_logging

init(autoreset=True)

logging = setup_logging()

def fetch_mpd(manifest_url, headers=None, proxy=None):
    response = requests.get(manifest_url, headers=headers, proxies=proxy)
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

def validate_keys(key: str):
    try:
        key = key.replace("--key ", "")
        key_id, key_value = key.split(':')
        return f"{key_id.strip()}:{key_value.strip()}"
    except ValueError:
        logging.error("Key format error with key: %s", key)
        return None

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

def direct_downloads(url: str, output_name: str, proxy: str = None):
    """
    Downloads DRM-protected content using N_m3u8DL-RE.

    Parameters:
    url (str): The URL of the MPD file.
    output_name (str): The name of the output file.
    proxy (str): The proxy to be used for the download (optional).
    
    Returns:
    None
    """
    try:
        content_dir = "content"
        os.makedirs(content_dir, exist_ok=True)
        
        # Header and proxy configuration
        headers = 'User-Agent: Dalvik/2.1.0 (Android 13)'
        
        # Prepare the command
        cmd = (
            f'N_m3u8DL-RE "{url}" '
            f'--header "{headers}" '
            f'--save-dir "{content_dir}" --save-name "{output_name}" '
            f'-mt -sv "BEST" -sa "BEST" -M format=mp4 --del-after-done'
        )

        # Adding proxy to the command if specified
        if proxy:
            cmd += f' --custom-proxy "http://{proxy}"'
        
        logging.info(f"Starting download: {url}")
        result = os.system(cmd)
        
        if result == 0:
            logging.info(f"Download completed successfully. Files saved to: {content_dir}")
        else:
            logging.error(f"Download failed with return code {result}")
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    
    
def drm_downloader(url: str, output_name: str, key: str, proxy: str):
    """
    Downloads DRM-protected content using N_m3u8DL-RE.

    Parameters:
    url (str): The URL of the mpd file.
    output_name (str): The name of the output file.
    key (str): The decryption key.
    
    Returns:
    None
    """
    try:
        content_dir = "content"
        os.makedirs(content_dir, exist_ok=True)
        headers = 'User-Agent: Dalvik/2.1.0 (Android 13)'
        # Prepare the command
        cmd = (
            f'N_m3u8DL-RE "{url}" --key "{key}" '
            f'--header "{headers}" '
            f'--save-dir "{content_dir}"  --save-name "{output_name}" '
            f'-mt -sv "BEST" -sa "BEST" -M format=mp4 --del-after-done'
        )
        
        logging.info(f"Starting download: {url}")
        # logging.debug(f"Command: {cmd}")
        
        # Execute the command
        result = os.system(cmd)
        
        if result == 0:
            logging.info(f"Download completed successfully. Files saved to: {content_dir}")
            # input_file = os.path.join(content_dir, output_name + ".mp4")
            # output_file = os.path.join(content_dir, output_name + "_60fps.mp4")
            # change_frame_rate(input_file, output_file, 60)
        else:
            logging.error(f"Download failed with return code {result}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


def change_frame_rate(input_file, output_file, frame_rate=60):
    """
    Changes the frame rate of a video using FFmpeg.

    Parameters:
    input_file (str): The path to the input video file.
    output_file (str): The path to the output video file.
    frame_rate (int): The desired frame rate (default is 60).
    """
    try:
        cmd = f'ffmpeg -i "{input_file}" -r {frame_rate} -fps_mode vfr -vf fps={frame_rate} "{output_file}"'
        logging.info(f"Running command: {cmd}")
        result = os.system(cmd)

        if result == 0:
            logging.info(f"Frame rate changed successfully. Output saved to: {output_file}")
        else:
            logging.error(f"Error: Command failed with exit code {result}")
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

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

def get_random_folder(base_dir='content'):
    """Generate a random folder name inside the base_dir and create it."""
    folder_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    folder_path = os.path.join(base_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def list_available_formats(url):
    """List the available formats for the given URL using yt-dlp."""
    temp_output = tempfile.mktemp(dir='content')
    command = f'yt-dlp -F --allow-u --list-formats "{url}" > "{temp_output}" 2>&1'
    os.system(command)
    
    with open(temp_output, 'r') as file:
        format_output = file.read()
    os.unlink(temp_output)
    
    return format_output

def yt_dlp_downloader(url, download_speed=1, format_option='best'):
    """
    Attempts to download the video from the given URL using yt-dlp with the specified format.
    Captures output to handle specific errors related to format availability.
    Args:
        url (str): The URL of the video to download.
        download_speed (int, optional): Download speed limit in MBps. Default is 1 MBps.
        format_option (str, optional): Format specifier for yt-dlp. Default is 'best'.
    Returns:
        str: Path to the downloaded video or a specific error message.
    """
    try:
        output_template = os.path.join(get_random_folder(), '%(title)s.%(ext)s')
        temp_output = tempfile.mktemp(dir='content')  # Create a temporary file in content directory to capture output

        # Prepare command with output redirection to temp file
        command = (
            f'yt-dlp -f {format_option} "{url}" '
            '--downloader aria2c '
            '--allow-unplayable-formats '
            '--ignore-errors '
            '--no-abort-on-error '
            '--no-warnings '
            '--quiet '
            '--merge-output-format mkv '
            f'--limit-rate {download_speed * 1024 * 1024} '
            f'--output "{output_template}" > "{temp_output}" 2>&1'
        )

        # Execute the command
        result = os.system(command)
        if result != 0:
            # Read the output from the temporary file
            with open(temp_output, 'r') as file:
                output = file.read()
            os.unlink(temp_output)  # Remove the temporary file after reading

            if "Requested format is not available" in output:
                logging.error("yt-dlp reported an error: " + output)
                available_formats = list_available_formats(url)
                return "Error: Requested format is not available. Use '--list-formats' for a list of available formats.\nAvailable formats:\n" + available_formats
            else:
                logging.error("yt-dlp failed with exit code: " + str(result))
                return "Download failed. Check logs for details."

        os.unlink(temp_output)  # Clean up the temporary file
        return f"Downloaded successfully to {output_template}"

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"