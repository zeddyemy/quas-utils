# quas-utils

Flask-focused helpers for quick, practical tasks: HTTP responses, retry/timing decorators, timezone-aware datetime utilities, simple logging, and a handful of misc helpers (slugging, random strings, key normalization).

## Install

```bash
python -m pip install quas-utils
# or for local dev
python -m pip install -e .
```

## What’s inside
- HTTP responses: `success_response`, `error_response` for consistent JSON replies.
- Decorators: `retry` for flaky DB calls; `get_time` to log execution time.
- Date/time: `QuasDateTime` helpers and `to_gmt1_or_none` for fixed GMT+1 conversions.
- Logging: `console_log`, `log_exception` thin wrappers over Flask/logging.
- Misc: slug generation, key normalization to `snake_case`, random strings/numbers, pagination.

## Quickstart (Flask)

```python
from flask import Flask
from quas_utils.api import success_response, error_response
from quas_utils.decorators import retry, get_time
from quas_utils.logging.loggers import console_log

app = Flask(__name__)

@app.route("/health")
def health():
    return success_response("ok", 200, {"service": "quas-utils"})

@app.route("/fragile")
@retry(retries=3, delay=1.5)
@get_time
def fragile_work():
    console_log("INFO", "doing work…")
    # raise on failure; retry will handle
    return success_response("done", 200)

@app.errorhandler(Exception)
def on_error(err):
    return error_response(str(err), 500)
```

## API cheat sheet

### HTTP responses
```python
from quas_utils.api import success_response, error_response
success_response("created", 201, {"id": 1})
error_response("not found", 404)
```

### Decorators
```python
from quas_utils.decorators import retry, get_time

@retry(retries=5, delay=2)
def fetch_from_db():
    ...

@get_time
def heavy_work():
    ...
```

### Date/time
```python
from quas_utils.date_time import QuasDateTime, to_gmt1_or_none

now = QuasDateTime.aware_utcnow()
pretty = QuasDateTime.format_date_readable(now)
gmt1 = to_gmt1_or_none(now)
```

### Logging helpers
```python
from quas_utils.logging.loggers import console_log, log_exception

console_log("INFO", "starting job")
try:
    risky()
except Exception as exc:
    log_exception("risky failed", exc)
```

### Misc helpers
```python
from quas_utils.misc import (
    normalize_keys,
    generate_random_string,
    generate_random_number,
    generate_slug,
    paginate_results,
)

normalize_keys({"firstName": "Ada", "address": {"zipCode": "12345"}})
generate_random_string(length=12, prefix="user")
generate_random_number(length=6)
# generate_slug expects a SQLAlchemy model with `.query`
```

## Notes
- Target Python: 3.12+
- Depends on Flask; `retry` expects SQLAlchemy installed for DB-related exceptions.
- The project uses the `src/` layout; imports are always `quas_utils.*` (no `src` in paths).
