# AGENTS.md

Async API wrapper for the AniLibria Swagger. The upstream repo is **archived** (last release v0.2.4). PRs target `main` and `dev`; the auto-style workflow opens PRs against `dev`.

## Environment

- **Python 3.13 only** (`requires-python = ">=3.13"`). Code targets py313.
- Managed with **Poetry** (`poetry.lock`), even though the build backend is setuptools and `pyproject.toml` mixes PEP 621 `[project]` with legacy `[tool.poetry]`. Use `poetry install --with dev`, and run all tooling via `poetry run ...`.
- A local `.venv/` already exists.

## Commands

```bash
poetry install --with dev          # deps + dev group (pytest, pytest-asyncio, dotenv, ruff)
poetry run pytest -q tests/ -s     # run all tests
poetry run pytest -q tests/methods/test_account.py -s   # single file (note -s)
poetry run pytest -q tests/methods/test_account.py::test_name -s  # single test
poetry run ruff check .            # lint    (auto-fix: ruff check --fix .)
poetry run ruff format .           # format
```

## Tests hit the live API (not mocked)

`tests/fixtures.py` loads `.env` and reads `ANILIBRIA_API_TOKEN`, `LOGIN`, `PASSWORD`. Without them the integration fixtures (`tests/methods/`) raise `ValueError`; the offline `tests/unit/` suite does not need `.env`. Copy `.env.example`, then get a token via `/accounts/users/auth/login`. CI (`pre-pr.yml`) recreates `.env` from GitHub secrets `ANILIBRIA_API_TOKEN`, `LOGIN`, `PASSWORD`. Integration tests require the `-s` flag because some use stdout/side effects.

## Base URL

- Client default in `api_client.py` is `https://aniliberty.top/api/v1/` (patched, with a comment that the previous URL stopped working).
- Test fixtures use the same host (`https://aniliberty.top/api/v1/`). Keep them in sync when adding endpoints.

## Lint conventions (ruff)

Ruff config lives in `pyproject.toml`: `select = ["ALL"]` (with a long, deliberate ignore list — refer to the file rather than fighting it), `line-length = 79`, double quotes, Google docstrings, `max-complexity = 10`, isort with 2 blank lines after imports. Prefer full parameter/return annotations on all functions. Docstrings are Google-style; `D` (docstring) checks are ignored, so missing docstrings don't fail lint.

## Layout & entrypoints

- `anilibria_api_client/api_client.py` — `AsyncAnilibriaAPI`, the main client. The underlying session is closed automatically after each request; for a pooled session use `async with client.api`. Generic `execute()` calls raw endpoints.
- `anilibria_api_client/base_api/api_class.py` — `API`, the raw aiohttp layer. Returns `dict | str | bytes`, turns HTTP 422 into `AnilibriaValidationException`. Manages the `ClientSession`: it is closed automatically after each request unless `API` is used as a context manager (`async with`), in which case it is pooled and closed on exit.
- `anilibria_api_client/exceptions.py` — `AnilibriaException`, `AnilibriaValidationException`.
- `anilibria_api_client/helper.py` — `auth`, torrent/video downloads (uses `aiofiles`, `m3u8_To_MP4`), `auto_paginate`.
- `anilibria_api_types` (external package) — generated endpoint methods (`anilibria_api_types.methods`), models/responses (`anilibria_api_types.responses`), enums (`anilibria_api_types.enums`), and `errors.ValidationError`.
- `anilibria_api_client/__init__.py` is intentionally empty (`__all__ = []`); import from submodules, e.g. `from anilibria_api_client.api_client import AsyncAnilibriaAPI`.

## Docs

Sphinx docs in `docs/` (furo theme), configured in `.readthedocs.yaml` + `docs/conf.py`. Install with `pip install -e .[docs]` and build with `make html` inside `docs/`.

## Tests

- `tests/unit/` — deterministic offline unit tests (no network, no `.env` needed). These back the package's 100% coverage target.
- `tests/methods/` — live integration tests against the real API; they need `.env` (`ANILIBRIA_API_TOKEN`, `LOGIN`, `PASSWORD`) and may be affected by upstream API/model drift.
