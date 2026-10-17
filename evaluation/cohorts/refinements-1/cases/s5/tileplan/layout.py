from dataclasses import dataclass


@dataclass(frozen=True)
class Tile:
    index: int
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class Plan:
    width: int
    height: int
    tiles: tuple[Tile, ...]


def arrange(options):
    if options.count == 0:
        return Plan(0, 0, ())
    columns = min(options.count, options.columns)
    rows = (options.count + options.columns - 1) // options.columns
    width = columns * options.width + (columns - 1) * options.spacing_px
    height = rows * options.height + (rows - 1) * options.spacing_px
    tiles = []
    for index in range(options.count):
        row, column = divmod(index, options.columns)
        tiles.append(Tile(
            index,
            column * (options.width + options.spacing_px),
            row * (options.height + options.spacing_px),
            options.width,
            options.height,
        ))
    return Plan(width, height, tuple(tiles))
