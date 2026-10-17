from dataclasses import dataclass


@dataclass(frozen=True)
class Options:
    count: int
    width: int
    height: int
    columns: int = 3
    spacing_px: int = 8

    def __post_init__(self):
        for name in ('count', 'width', 'height', 'columns', 'spacing_px'):
            if type(getattr(self, name)) is not int:
                raise ValueError(f'{name} must be an integer')
        if self.count < 0 or self.spacing_px < 0:
            raise ValueError('count and spacing must be nonnegative')
        if self.width <= 0 or self.height <= 0 or self.columns <= 0:
            raise ValueError('width, height, and columns must be positive')
