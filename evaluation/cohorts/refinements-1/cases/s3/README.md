# Field sensor ledger

A local ledger for named sensors with temperature readings. Input readings use
Celsius (`C`) or Fahrenheit (`F`); summaries always use Celsius. This is a data
preparation utility, not an alerting or safety system.

A reading has a nonblank sensor name, an aware timestamp, and a finite numeric
value. Booleans are not numeric values here. The supported sensor range is -273.15 through 1000 C inclusive,
or -459.67 through 1832 F inclusive; units are case-sensitive. Values outside
these ranges, including arbitrarily large integers, are rejected before conversion. Each `(sensor, instant)` identifies one
reading. A later valid submission replaces that reading, including when supplied
in a different timezone. Input batches are atomic: one invalid reading leaves the
entire ledger unchanged. Empty batches are accepted. Input may arrive out of order.

A summary selects `[start, stop)` instants for exactly one sensor. It returns count,
minimum, maximum, and arithmetic mean, or `None` for each statistic when empty.
Bounds must be aware and `start < stop`. Stored rows are returned in timestamp order
as immutable values. Summaries do not round results; display rounding is a caller's
choice. Ordinary floating-point tolerance applies to conversion comparisons.

`fieldlog/reading.py` validates input, `fieldlog/ledger.py` owns storage, and
`fieldlog/summary.py` computes window statistics. This in-memory library is single
threaded. Run `python3 -m unittest discover -s tests -v` in this directory.
