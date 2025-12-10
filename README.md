# quas-utils

Flask-oriented utilities: date/time helpers, decorators, and misc helpers for Flask + SQLAlchemy stacks.

## Install

```bash
python -m pip install quas-utils
```

## Contents
- `quas_utils.date_time`: UTC helpers, formatting/parsing, fixed GMT+1 conversion.
- `quas_utils.decorators`: `retry` for DB-backed retries, `get_time` for simple timing logs.
- `quas_utils.misc`: Flask/SQLAlchemy helpers (pagination, slugs, key normalization, etc.).
- `quas_utils.helpers.loggers`: Thin logging helpers that use Flask app logger when available.

## Usage

### Date/time
```python
from quas_utils.date_time import QuasDateTime, to_gmt1_or_none

now_utc = QuasDateTime.aware_utcnow()
readable = QuasDateTime.format_date_readable(now_utc)  # e.g., "10th December"
gmt1 = to_gmt1_or_none(now_utc)  # fixed +1h offset
```

### Decorators
```python
from quas_utils.decorators import retry, get_time

@retry(retries=3, delay=1.5)
def fetch_from_db():
    ...

@get_time
def heavy_work():
    ...
```

### Misc Flask helpers
```python
from quas_utils.misc import (
    paginate_results,
    normalize_keys,
    generate_slug,
    int_or_none,
    get_or_404,
    redirect_url,
    parse_bool,
)

# Pagination (expects objects with .to_dict())
page_items = paginate_results(request, results, result_per_page=20)

# Key normalization (handles acronyms)
payload = {"userID": 1, "HTTPCode": 200}
normalized = normalize_keys(payload)  # {"user_id": 1, "http_code": 200}

# Slug generation (Flask-SQLAlchemy models)
slug = generate_slug("My Name", model=MyModel, max_attempts=5, add_timestamp=True)

# Safe int parsing
value = int_or_none(request.args.get("count"))

# Fetch or abort
item = get_or_404(MyModel.query.filter_by(id=123))

# Redirect helper
next_url = redirect_url(default="admin.index")

# Boolean parsing
flag = parse_bool(request.args.get("active"))
```

## Notes
- Targets Flask + SQLAlchemy; dependencies are declared in `pyproject.toml`.
- GMT+1 conversion is a fixed offset (no DST). Use `zoneinfo` if you need real timezone handling.
