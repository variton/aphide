# xphide

Python utilities for bcrypt password hashing, Fernet encryption and decryption, JWT signing and verification, and environment variable loading.

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

### Encryption and decryption

```python
from xphide.xcrypt import Encoding, Xcrypt

crypt = Xcrypt(encoding=Encoding.UTF8)
token = crypt.encrypt("Café")  # Returns bytes.
assert crypt.decrypt(token) == "Café"  # Returns str.
```

`Xcrypt` defaults to ASCII; select `Encoding.UTF8` for non-ASCII text. Despite
the current type annotations, `encrypt` returns a bytes token, which can be
passed directly to `decrypt`.

Each default instance generates its own Fernet key. To decrypt data across
instances or application restarts, securely retain a key and supply a Fernet
cipher created from it:

```python
from cryptography.fernet import Fernet
from xphide.xcrypt import Xcrypt

key = Fernet.generate_key()  # Generate once and store securely for reuse.
writer = Xcrypt(cipher=Fernet(key))
reader = Xcrypt(cipher=Fernet(key))

assert reader.decrypt(writer.encrypt("secret")) == "secret"
```

Decryption raises `cryptography.fernet.InvalidToken` for invalid or tampered
tokens, or tokens encrypted with a different key.

### JWT signing and verification

With `SJWTK` defined before importing the module:

```python
from xphide.jwtcrypt import JwtCrypt

token = JwtCrypt.encode({"sub": "user-123"})
payload = JwtCrypt.decode(token)
assert payload["sub"] == "user-123"
```

JWTs use HS256. Both methods also accept an explicit signing key through the `_key` argument.
An explicit nonempty key overrides the value loaded from `SJWTK`:

```python
token = JwtCrypt.encode({"sub": "user-123"}, _key="example-key")
payload = JwtCrypt.decode(token, _key="example-key")
```

JWT payloads are signed, not encrypted. Invalid tokens or signatures raise
`jose.exceptions.JWTError`; expired tokens raise its subclass
`jose.exceptions.ExpiredSignatureError`.

### Environment variables

```python
from xphide.envvar_loader import load

signing_key = load()  # Reads SJWTK.
custom_value = load("MY_VARIABLE")
```

`load` returns `None` when the requested variable is missing and preserves an
empty string when the variable is defined but empty. It reads the process
environment; it does not load `.env` files.

## Tests

After installing the development dependencies, run from the repository root:

```sh
export SJWTK='local-test-signing-key'
uv run pytest
```

The JWT tests require a nonempty `SJWTK` supplied by the client or calling environment; they fail if it is missing or empty.

## License

MIT. See [LICENSE](LICENSE).
