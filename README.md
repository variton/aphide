# xphide

Python utilities for bcrypt password hashing, JWT signing and verification, and environment variable loading.

## Requirements and installation

Requires Python 3.14 or newer. From the repository root:

```sh
python -m pip install -e .
```

For development and tests, install the development dependency group with uv:

```sh
uv sync --group dev
```

## Configuration

The client code or calling environment must define a nonempty `SJWTK` environment variable before running the tests. This variable supplies the JWT signing key and must be set before importing `xphide.jwtcrypt`, because the default key is read at import time.

```sh
export SJWTK='local-test-signing-key'
```

Use a private signing key for application deployments and keep it out of version control.

## Usage

### Password hashing

```python
from xphide.crypt import Crypt

password_hash = Crypt.hash("example-password")
assert Crypt.is_equal(password_hash, "example-password")
```

Password strings must be ASCII, matching the encoding used by `Crypt`.

### JWT signing and verification

With `SJWTK` defined before importing the module:

```python
from xphide.jwtcrypt import JwtCrypt

token = JwtCrypt.encode({"sub": "user-123"})
payload = JwtCrypt.decode(token)
assert payload["sub"] == "user-123"
```

JWTs use HS256. Both methods also accept an explicit signing key through the `_key` argument.

### Environment variables

```python
from xphide.envvar_loader import load

signing_key = load()  # Reads SJWTK.
custom_value = load("MY_VARIABLE")
```

`load` returns `None` when the requested variable is missing.

## Tests

After installing the development dependencies, run from the repository root:

```sh
export SJWTK='local-test-signing-key'
uv run pytest
```

The JWT tests require a nonempty `SJWTK` supplied by the client or calling environment; they fail if it is missing or empty.

## License

MIT. See [LICENSE](LICENSE).
