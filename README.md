# tenor-dl

Simple CLI script to download gifs from tenor.com.

## Installation

```bash
pip3 install tenor-dl
```

## Usage

```bash
usage: tenor-dl [-h] [-o OUTPUT] [-u] URL

simple script to download gifs from tenor.com

positional arguments:
  URL                   tenor.com URL to download the gif from

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output path or use "-" for STDOUT
  -u, --urlonly         only print direct link to gif and exit
```

## Example Usage

```bash
tenor-dl https://tenor.com/view/rage-work-pc-stressed-pissed-gif-15071896
```
