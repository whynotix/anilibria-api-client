# Anilibria-Api-Client (tests)

The suite has two parts:

- `tests/unit/` — deterministic offline unit tests (no network, no `.env`).
- `tests/methods/` — live integration tests against the real API.

## Setup (integration tests only)

1. Create a `.env` file.
2. Copy the keys from `.env.example`: `ANILIBRIA_API_TOKEN`, `LOGIN`, `PASSWORD`.
3. Get a token via the `/accounts/users/auth/login` method.

The offline unit tests in `tests/unit/` do not need `.env`.

## Run tests

```bash
# offline unit tests (no network, no .env)
poetry run pytest -q tests/unit -s

# a single integration file
poetry run pytest -q tests/methods/test_account.py -s

# everything
poetry run pytest -q tests/ -s
```

Integration tests require the `-s` flag because some use stdout/side effects.

## Coverage

```bash
poetry run pytest -q tests/ -s --cov=anilibria_api_client --cov-report=term-missing
```
