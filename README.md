# quas-utils

Date/time helpers for the QUAS ecosystem. Install from TestPyPI or PyPI and use:

```
python -m pip install quas-utils
```

```python
from quas_utils.date_time import QuasDateTime, to_gmt1_or_none

now_utc = QuasDateTime.aware_utcnow()
readable = QuasDateTime.format_date_readable(now_utc)
gmt1 = to_gmt1_or_none(now_utc)
```
