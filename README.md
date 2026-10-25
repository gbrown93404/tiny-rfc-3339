# tiny-rfc-3339

A focused validator for the RFC 3339 date-time format. Returns `True` if a string is a valid RFC 3339 timestamp, `False` otherwise.

```python
from tiny_rfc_3339 import is_rfc3339

assert is_rfc3339("2025-01-02T15:04:05Z")
assert not is_rfc3339("2025-01-02")
assert not is_rfc3339("2025-01-02T15:04:05")
```

## Why this exists

If you just need to *reject* invalid timestamps, pulling in a full datetime parser (or worse, a calendar library) is heavy. This library hand-codes the RFC 3339 grammar so there is nothing to install and no dependency tree to audit. The trade-off: it returns a boolean. It does not parse into a `datetime` object, so if you need timezone-aware arithmetic, use `datetime.fromisoformat` after a validity check.

## The awkward edge

RFC 3339 permits a fractional second with any number of digits. It does not require the `T` separator to be uppercase (lowercase `t` is legal). The `Z` designator is likewise case-insensitive. Both uppercase and lowercase forms are accepted here.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

