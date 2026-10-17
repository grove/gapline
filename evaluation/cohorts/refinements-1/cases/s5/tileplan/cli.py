import argparse
from dataclasses import asdict
import json
from .layout import arrange
from .options import Options


def parser():
    result = argparse.ArgumentParser(description='Calculate raster thumbnail coordinates')
    for name in ('count', 'width', 'height'):
        result.add_argument('--' + name, type=int, required=True)
    result.add_argument('--columns', type=int, default=3)
    result.add_argument('--spacing', type=int, default=8, help='gap in pixels')
    return result


def main(argv=None):
    command = parser()
    args = command.parse_args(argv)
    try:
        options = Options(args.count, args.width, args.height, args.columns, args.spacing)
    except ValueError as error:
        command.error(str(error))
    print(json.dumps(asdict(arrange(options))))


if __name__ == '__main__':
    main()
