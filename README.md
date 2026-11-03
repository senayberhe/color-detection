# Color Detection

An interactive desktop tool that identifies colors in an image. Click anywhere on a picture and the app shows the closest named color, its hex code, and its RGB values.

## Features

- **Click to identify** – a single click shows the color name, hex code, and RGB values in a banner across the top of the image.
- **Accurate matching** – colors are compared in the CIE Lab color space, which follows human color perception more closely than raw RGB.
- **Noise-resistant sampling** – each click averages a 5×5 pixel area, so speckles in photos don't throw off the result.
- **Fast lookup** – all 865 reference colors are compared at once with NumPy, taking under a millisecond per click.
- **Handles large photos** – images bigger than 1200×800 are scaled down to fit on screen.
- **Readable output** – the banner text switches between black and white to contrast with the detected color, and each result is also printed to the terminal.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/) for dependency management

Dependencies (installed automatically by uv): `opencv-python`, `numpy`, `pandas`.

## Installation

```bash
git clone https://github.com/senayberhe/color-detection.git
cd color-detection
uv sync
```

## Usage

```bash
uv run main.py -i images/colorpic.jpg
```

You can also run the script directly:

```bash
uv run python color_detection.py -i images/colorpic.jpg
```

### Controls

| Action | Result |
| --- | --- |
| Left click | Identify the color at the cursor |
| `Esc` | Quit |
| Close window | Quit |

### Example output

```
Snow #FFFAFA R=250 G=250 B=250
```

## How It Works

1. The reference colors are loaded from `images/colors.csv`, and each one is converted to the Lab color space once at startup.
2. When you click, the app averages the surrounding 5×5 pixels to get a single RGB value.
3. That value is converted to Lab, and the reference color with the smallest Euclidean distance is chosen as the match.
4. The result is drawn on a copy of the image, so the original pixels are never altered and later clicks stay accurate.

## Project Structure

```
color-detection/
├── color_detection.py   # Color matching and interactive viewer
├── main.py              # Entry point
├── images/
│   ├── colors.csv       # Reference color names, hex codes, and RGB values
│   └── *.jpg            # Sample images
├── pyproject.toml       # Project metadata and dependencies
└── uv.lock              # Locked dependency versions
```

### `colors.csv` format

Each row has six columns, with no header:

```
id,name,hex,R,G,B
air_force_blue_raf,"Air Force Blue (Raf)",#5d8aa8,93,138,168
```

To customize the palette, add or edit rows in this format.

## Troubleshooting

- **`Could not read image`** – check the file path. Images are stored in the `images/` folder, e.g. `images/leaves.jpg`.
- **The window doesn't appear** – make sure `opencv-python` is installed (not `opencv-python-headless`) by running `uv sync`.
- **The color name is cut off** – on very narrow images the banner has limited space; the full result is always printed in the terminal.
