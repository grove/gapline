# Geometry format, version 1

This document is the normative compatibility contract for Tile plan.
All dimensions and coordinates, including spacing, are whole raster pixels.
The CLI `--spacing` argument maps directly to the `spacing_px` layout setting;
no physical-unit conversion or DPI parameter is part of version 1.

Count is a nonnegative integer. Width, height, and columns are positive integers.
Spacing is a nonnegative integer with default 8. JSON has keys `width`, `height`,
and `tiles`. Tiles have integer `index`, `x`, `y`, `width`, and `height` fields.

The used column count is `min(count, columns)`. The number of rows is the ceiling
of count divided by columns. Canvas width is the used columns' total thumbnail
width plus spacing only between columns. Canvas height uses the corresponding
row formula. An incomplete final row retains the earlier rows' canvas width.
An empty plan has width 0, height 0, and no tiles. There is no outer padding.

Version 1 is consumed by an existing pixel-coordinate renderer. Implementations
must preserve these units, default spacing, ordering, and empty-plan behavior.
