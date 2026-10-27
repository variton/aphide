"""Tests for Fernet encryption and decryption through Xcrypt."""

import base64

import pytest
from cryptography.fernet import Fernet, InvalidToken

from xphide.xcrypt import Encoding, Xcrypt


@pytest.fixture
def cipher():
    """Provide an independent Fernet cipher for interoperability checks."""
    return Fernet(Fernet.generate_key())


def test_default_encoding():
    """Default to ASCII and generate a usable Fernet cipher."""
    crypt = Xcrypt()

    assert crypt.encoding_ == "ascii"
    assert isinstance(crypt.cipher_, Fernet)
    assert crypt.decrypt(crypt.encrypt("secret")) == "secret"


def test_encrypt(cipher):
    """Produce a token decryptable by the supplied cipher."""
    crypt = Xcrypt(cipher=cipher)

    token = crypt.encrypt("secret")

    assert isinstance(token, bytes)
    assert cipher.decrypt(token) == b"secret"


def test_decrypt(cipher):
    """Decode a token produced independently by the supplied cipher."""
    crypt = Xcrypt(cipher=cipher)
    token = cipher.encrypt(b"secret")

    assert crypt.decrypt(token) == "secret"


@pytest.mark.parametrize(
    ("encoding", "plaintext"),
    [
        (Encoding.ASCII, ""),
        (Encoding.ASCII, "Hello, world! 123"),
        (Encoding.UTF8, ""),
        (Encoding.UTF8, "Café — こんにちは 🔐"),
    ],
)
def test_round_trip(encoding, plaintext):
    """Preserve empty strings and text supported by each encoding."""
    crypt = Xcrypt(encoding=encoding)

    assert crypt.decrypt(crypt.encrypt(plaintext)) == plaintext


def test_utf8_encrypt(cipher):
    """Encode non-ASCII plaintext as UTF-8 before encrypting."""
    crypt = Xcrypt(encoding=Encoding.UTF8, cipher=cipher)

    assert cipher.decrypt(crypt.encrypt("café")) == "café".encode("utf-8")


def test_ascii_rejects_non_ascii():
    """Propagate encoding errors for text outside ASCII."""
    with pytest.raises(UnicodeEncodeError):
        Xcrypt().encrypt("café")


def test_ascii_decrypt_rejects_non_ascii(cipher):
    """Propagate decoding errors for plaintext outside ASCII."""
    token = cipher.encrypt("café".encode("utf-8"))

    with pytest.raises(UnicodeDecodeError):
        Xcrypt(cipher=cipher).decrypt(token)


def test_instances_generate_independent_keys():
    """Reject a token encrypted by a separate default instance."""
    token = Xcrypt().encrypt("secret")

    with pytest.raises(InvalidToken):
        Xcrypt().decrypt(token)


@pytest.mark.parametrize("token", [b"", b"not-a-fernet-token"])
def test_reject_invalid_token(token):
    """Propagate Fernet validation failures."""
    with pytest.raises(InvalidToken):
        Xcrypt().decrypt(token)


def test_reject_tampered_token(cipher):
    """Reject a valid token whose authenticated ciphertext was modified."""
    token = cipher.encrypt(b"secret")
    raw = bytearray(base64.urlsafe_b64decode(token))
    raw[25] ^= 1

    with pytest.raises(InvalidToken):
        Xcrypt(cipher=cipher).decrypt(base64.urlsafe_b64encode(raw))
