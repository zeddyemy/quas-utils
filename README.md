# quas-utils

Flask-oriented utilities (date/time helpers + decorators).

## Install

```
python -m pip install quas-utils
```

## Usage

Date/time helpers:
```python
from quas_utils.date_time import QuasDateTime, to_gmt1_or_none

now_utc = QuasDateTime.aware_utcnow()
readable = QuasDateTime.format_date_readable(now_utc)
gmt1 = to_gmt1_or_none(now_utc)
```

Decorators:
```python
from quas_utils.decorators import retry, get_time


@retry(retries=3, delay=1.5)
def fetch_from_db():
    ...


@get_time
def heavy_work():
    ...
```
