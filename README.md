WKSKEY-2.0
============

WKSKEY-2.0 is a tool designed to obtain Widevine keys from Media Presentation Description (MPD) URLs. It uses a modular approach to handle various streaming services, allowing users to easily customize and expand its functionality according to their needs.

Main Features
-------------

- **Modular Service Handling:** WKSKEY-2.0 has a modular structure that separates logic for each streaming service into individual modules. Currently, it supports two services: prime and astro. Each module can handle service-specific DRM requests, including how they handle parameters, cookies, and data sent in requests.
- **Automatic Key Retrieval:** Using PSSH data provided or extracted from the URL MPD, WKSKEY-2.0 can automatically request and process Widevine keys, simplifying the process of obtaining keys for decryption purposes.
- **High Flexibility:** Users can easily add support for new services by creating new service modules and integrating them into the main script.

Usage
-----

To use WKSKEY-2.0, users need to specify the Widevine license URL and other options through command-line arguments. Here's a basic usage example:

```bash
python main.py --license-url [URL_LICENSE] --mpd-url [URL_MPD] --service prime
```

## Adding New Services

To add a new service, create a module in the `services` folder with an implementation that handles specific DRM requests from that service. The module should provide methods such as `get_headers()`, `get_params()`, `get_cookies()`, and `get_data()`. After that, the new module can be integrated into `license_retrieval.py` by adding a special condition for the service in the function `get_license_keys`.

## Directory Structure

- **modules/**: Contains modules used for device configuration and DRM processing.
- **services/**: A per-service module that provides service-specific logic for handling DRM requests and processing.
- **main.py**: The main script that coordinates the key retrieval and processing process.

## Adding Features

- Parses arguments for URLs, PSSH, and proxy settings.
- Extracts PSSH from MPD URLs.
- Retrieves license keys using provided URLs and services.
- Supports user input for PSSH and other required parameters.
- Downloads content using the extracted license keys.

## Contribution

Contributions to WKSKEY-2.0 are greatly appreciated. If you have bug fixes, enhancements, or want to add support for new services, please make a pull request.