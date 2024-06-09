import os
import shutil
import subprocess
import json
from pymediainfo import MediaInfo
from modules.logging import setup_logging
from colorama import init, Fore, Style

init(autoreset=True)

logging = setup_logging()

def validate_keys(keys):
    """
    Validates and formats keys into 'key_id:key_value' strings.

    Parameters:
    keys (list): A list of keys, where each key is a string in the format 'key_id:key_value'.

    Returns:
    list: A list of formatted keys as strings.
    """
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
    """
    Retrieves and returns information about an MP4 file using pymediainfo.

    Parameters:
    file_path (str): The path to the MP4 file.

    Returns:
    dict: A dictionary containing information about the MP4 file.
    """
    try:
        media_info = MediaInfo.parse(file_path)
        info = media_info.to_data()
        return info
    except Exception as e:
        logging.error(f"An error occurred while retrieving MP4 info: {e}")
        return None

def save_mp4_info(info, save_name):
    """
    Saves the MP4 info to a JSON file in the logs directory.

    Parameters:
    info (dict): The information to save.
    save_name (str): The base name for the saved file.
    """
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
    """
    Re-encodes a video to HD resolution.

    Parameters:
    input_file (str): The path to the input video file.
    output_file (str): The path to the output HD video file.
    """
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
    """
    Segments a video for MPEG-DASH.

    Parameters:
    input_file (str): The path to the input video file.
    output_mpd (str): The path to the output MPD file.
    """
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
    """
    Downloads video using m3u8dl.exe with specified parameters.

    Parameters:
    url (str): The URL to download.
    save_name (str): The name to save the file as.
    keys (list): A list of keys in the format "key_id:key_value".
    output_format (str): The output format.
    save_video_quality (str): The video quality.
    save_audio_quality (str): The audio quality.
    """
    temp_dir = "content"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    lang = input(f"{Fore.GREEN}Subtitle Language {Fore.RED}(eg: EN): {Fore.WHITE}")
    command = f'N_m3u8DL-RE.exe "{url}" --save-dir {temp_dir} --save-name {save_name}'
    for key in keys:
        command += f' --key {key}'
    command += f' -mt -M {output_format} -sv {save_video_quality} -sa {save_audio_quality} -ss {lang}'
    
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
    """
    Post-processes the downloaded video: gets info, re-encodes to HD, and segments for DASH.

    Parameters:
    save_name (str): The base name of the saved video file.
    temp_dir (str): The directory where the video file is saved.
    """
    mp4_file_path = os.path.join(temp_dir, f"{save_name}.mkv")
    if os.path.exists(mp4_file_path):
        mp4_info = get_mp4_info(mp4_file_path)
        if mp4_info:
            save_mp4_info(mp4_info, save_name)

        hd_video_path = os.path.join(temp_dir, f"{save_name}_hd.mkv")
        reencode_video_to_hd(mp4_file_path, hd_video_path)

    encrypted_file_path = os.path.join(temp_dir, f"{save_name}.encrypted")
    if os.path.exists(encrypted_file_path):
        os.remove(encrypted_file_path)

def drm_downloader(url, save_name, keys, output_format='mkv', save_video_quality='best', save_audio_quality='best'):
    """
    Main function to download and process DRM-protected video.

    Parameters:
    url (str): The URL to download.
    save_name (str): The name to save the file as.
    keys (list): A list of keys in the format "key_id:key_value".
    output_format (str): The output format, default is 'mp4'.
    save_video_quality (str): The video quality, default is 'best'.
    save_audio_quality (str): The audio quality, default is 'best'.
    """
    valid_formats = ['mp4', 'ts', 'flv', 'mkv']
    if output_format not in valid_formats:
        raise ValueError(f"Invalid output_format '{output_format}'. Valid formats are: {', '.join(valid_formats)}")
    
    if not all(isinstance(param, str) and param for param in [url, save_name, output_format, save_video_quality, save_audio_quality]):
        raise ValueError("URL, save_name, output_format, save_video_quality, and save_audio_quality must all be non-empty strings")
    if not keys or not all(isinstance(key, str) and ':' in key for key in keys):
        raise ValueError("Keys must be a non-empty list of strings in the format 'key_id:key_value'")

    temp_dir = "content"
    if download_video(url, save_name, keys, output_format, save_video_quality, save_audio_quality):
        post_process_video(save_name, temp_dir)
        return True
    return False