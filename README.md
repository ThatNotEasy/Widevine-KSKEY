# WKSKEY-2.0

WKSKEY-2.0 is a tool designed to obtain Widevine keys from Media Presentation Description (MPD) URLs. It uses a modular approach to handle various streaming services, allowing users to easily customize and expand its functionality according to their needs.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Directory Structure](#directory-structure)
6. [Adding New Services](#adding-new-services)
7. [Contribution](#contribution)
8. [License](#license)

## Introduction

WKSKEY-2.0 is designed to streamline the process of obtaining Widevine keys required for decrypting DRM-protected content from streaming services. It supports a modular architecture, making it easy to extend functionality to new services.

## Features

- **Modular Service Handling**: Separate logic for each streaming service into individual modules.
- **Automatic Key Retrieval**: Automatically requests and processes Widevine keys using PSSH data from MPD URLs.
- **High Flexibility**: Easily add support for new services by creating and integrating new service modules.

## Installation

To install WKSKEY-2.0, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/WKSKEY-2.0.git
cd WKSKEY-2.0
pip install -r requirements.txt
```

## Usage

To use WKSKEY-2.0, specify the Widevine license URL and other options through command-line arguments. Create a new directory named `device` and place the `.wvd` CDM file in that directory. Refer to [KeyDive](https://github.com/hyugogirubato/KeyDive) for more information.

## Basic:
```bash
python main.py --license-url [URL_LICENSE] --mpd-url [URL_MPD] --service bitmovin
```
## With Proxy (COUNTRY CODE):
```bash
python main.py --license-url [URL_LICENSE] --mpd-url [URL_MPD] --service bitmovin -pp US
```
## With Proxy (ROTAETE PROXY):
```bash
python main.py --license-url [URL_LICENSE] --mpd-url [URL_MPD] --service bitmovin -pp rotate
```
## With Proxy (SCRAPE PROXY):
```bash
python main.py --license-url [URL_LICENSE] --mpd-url [URL_MPD] --service bitmovin -pp scrape
```

## Netflix, Skyshowtime & HBOGO
```bash
python main.py -m "<WATCH_URL>" -s "skyshowtime"
python main.py -c "<CONTENT_ID>" -s "netflix"
python main.py -c "<CONTENT_ID>" -s "hbogo"
```

## Directory Structure

- `modules`: Contains modules used for device configuration and DRM processing.
- `services`: Per-service modules that provide service-specific logic for handling DRM requests and processing.
- `main.py`: The main script that coordinates the key retrieval and processing process.

## Adding New Services

To add a new service, create a module in the `services` folder with an implementation that handles specific DRM requests from that service. The module should provide methods such as `get_headers()`, `get_params()`, `get_cookies()`, and `get_data()`. After that, integrate the new module into `license_retrieval.py` by adding a condition for the service in the function `get_license_keys`.

## Contribution

Contributions to WKSKEY-2.0 are greatly appreciated. If you have bug fixes, enhancements, or want to add support for new services, please make a pull request.

## License

WKSKEY-2.0 is released under the [MIT License](LICENSE).

---

Feel free to reach out if you have any questions or need further assistance!
