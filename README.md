# MP4/MOV Resolution Patcher

A lightweight, zero-dependency Python command-line tool designed to patch the resolution dimensions embedded within specific MP4/QuickTime video atoms (such as `tkhd` or `mvhd`). 

This script directly manipulates the binary data of the video file, allowing you to scale the internal display resolution without re-encoding the actual video stream.

## Features

- **Zero Dependencies:** Uses only native Python standard libraries (`argparse`, `os`, `sys`).
- **Binary-Level Precision:** Modifies the Big-Endian 32-bit integers inside MP4 boxes directly in memory.
- **Flexible Scaling:** Supports fractional multipliers (e.g., `1.5`, `2.0`, `0.5`).
- **Custom Atom Targeting:** Defaults to the Track Header (`tkhd`) atom but allows targeting any valid 4-character atom.

## Requirements

- Python 3.x or higher.

## Installation

Simply download or copy the `patch_resolution.py` script into your project directory. No additional packages are required.

## Usage

Run the script from your terminal or command prompt by providing the required input, output, and scale parameters.

### Command-Line Arguments

|Argument|Short|Required|Description|
|-------:|----:|-------:|----------:|
|--input|-i|Yes|Path to the source MP4/MOV video file.|
|--output|-o|Yes|Path where the modified video file will be saved.|
|-scale|-s|Yes|Scale factor multiplier (e.g., 1.5, 2.0, 0.5).|
|--atom|-a|No|The 4-character atom name to target. (Default: tkhd)|

### Examples 

1. Double the resolution of a video (2.0x)
    ```bash
    python patch_resolution.py -i input.mp4 -o output_double.mp4 -s 2.0
    ```
2. Scale down a video to 75% of its original size (0.75x)
    ```Bash
    python patch_resolution.py -i holiday.mov -o holiday_scaled.mov -s 0.75
    ```
3. Target a specific atom (e.g., Movie Header mvhd)
    ```Bash
    python patch_resolution.py --input video.mp4 --output video_patched.mp4 --scale 2.0 --atom mvhd
    ```
4. View the built-in help menu
    ```Bash
    python patch_resolution.py --help
    ```
    
## How It Works

- **Safe File Handling:** The script safely reads the source file entirely as a mutable bytearray.
- **Atom Lookup:** It searches for the byte-pattern matching your specified 4-character atom.
- **Validation:** It verifies if the atom box size meets the minimum requirement (>= 84 bytes) to safely contain the width and height offsets.
- **Bitwise Modification:** It extracts the current resolution integers, calculates the new scaled dimensions using flooring logic, and injects the new Big-Endian 32-bit values back into the exact byte offsets.

## License 

This project is open-source and available under the MIT License.
