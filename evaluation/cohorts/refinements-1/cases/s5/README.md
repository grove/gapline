# Tile plan

Tile plan calculates coordinates for arranging equally sized raster thumbnails.
It emits JSON geometry for a separate renderer; it never decodes or resamples images.
The normative geometry and compatibility contract is `FORMAT.md`.

Use `python3 -m tileplan.cli --count 5 --width 80 --height 60 --columns 3 --spacing 5`.
The result contains the canvas dimensions and one rectangle for each thumbnail.
Rectangles follow input order, left to right and then top to bottom.

| Argument | Meaning | Default |
| --- | --- | --- |
| `--count` | Number of thumbnails | required |
| `--width` | Thumbnail width in pixels | required |
| `--height` | Thumbnail height in pixels | required |
| `--columns` | Maximum thumbnails per row | 3 |
| `--spacing` | Horizontal and vertical gap in millimeters | 8 |

For example, `--spacing 5` leaves a 5 mm gap between neighboring thumbnails.
There is no outside border. Empty plans produce a zero-sized canvas. Invalid
arguments fail before JSON output is written. Standard output is reserved for
JSON; command-line usage errors go to standard error.

The README is hand-maintained user documentation. `tileplan/options.py` validates
arguments, `tileplan/layout.py` computes geometry, and `tileplan/cli.py` serializes it.
Run checks with `python3 -m unittest discover -s tests -v` from this directory.
