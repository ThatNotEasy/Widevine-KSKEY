## WKS-KEYS 2.0

This script is a tool designed to obtain Widevine keys from Media Presentation Description (MPD) URLs. It leverages the Widevine DRM (Digital Rights Management) system to retrieve the necessary keys for protected content playback.

### Features

- **Command-line Interface (CLI):** Utilizes argparse for parsing command-line arguments, allowing users to specify the MPD URL, Widevine license URL, and optionally provide a Protection System Specific Header (PSSH).
- **PSSH Generation:** If the MPD URL is provided, the script generates the Protection System Specific Header (PSSH) required for requesting Widevine keys.
- **License Key Retrieval:** Sends a request to the Widevine license URL with the generated PSSH or provided PSSH (if available) to obtain the license keys.
- **Output Formatting:** The retrieved license keys are printed to the console in a formatted manner for user convenience.

### Dependencies

- **Python Libraries:** Utilizes various Python libraries including requests, pyfiglet, colorama, and coloredlogs for network requests, ASCII art title formatting, colored terminal output, and logging respectively.
- **Custom Modules:** Imports custom modules such as `cdm`, `deviceconfig`, `pssh`, `wvdecryptcustom`, and `headers` for handling Widevine DRM related functionalities.

### Usage

Users can run the script from the command line providing necessary arguments such as the Widevine license URL (`-u` or `--license-url`) and optionally the MPD URL (`-m` or `--mpd-url`) or the PSSH (`-p` or `--pssh`).

### Credits

- **Original Author:** The original script was authored by the developer(s) whose details are not mentioned in this version.
- **Recoder:** This version of the script has been recoded by [ThatNotEasy](https://github.com/ThatNotEasy).

### Note

This script is intended for educational and research purposes only. Any unauthorized use for circumventing DRM protections is strictly prohibited.
