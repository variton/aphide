"""Tests for JWT signing and verification using the container's SJWTK."""

import os

import pytest
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from xphide.jwtcrypt import JwtCrypt


@pytest.fixture(autouse=True)
def require_signing_key():
    """Require the signing key supplied by the container."""
    if not os.environ.get("SJWTK"):
        pytest.fail("Set a nonempty SJWTK in the container before running these tests.")


@pytest.fixture
def payload():
    """Provide claims without time-dependent expiration."""
    return {"sub": "test-user", "role": "reader"}


def test_load_container_key():
    """Load the signing key from SJWTK at module import."""
    assert JwtCrypt.s_cypher == os.environ["SJWTK"]


def test_encode(payload):
    """Sign a token with the container key and the HS256 algorithm."""
    token = JwtCrypt.encode(payload)

    assert isinstance(token, str)
    assert jwt.get_unverified_header(token)["alg"] == "HS256"
    assert jwt.decode(token, os.environ["SJWTK"], algorithms=["HS256"]) == payload


def test_decode(payload):
    """Verify an independently signed token using the container key."""
    token = jwt.encode(payload, os.environ["SJWTK"], algorithm="HS256")

    assert JwtCrypt.decode(token) == payload


def test_round_trip(payload):
    """Recover the original claims after encoding and decoding."""
    assert JwtCrypt.decode(JwtCrypt.encode(payload)) == payload


def test_custom_key(payload):
    """Use an explicit key instead of the container key for both operations."""
    key = os.environ["SJWTK"] + "-test-override"
    token = JwtCrypt.encode(payload, _key=key)

    assert jwt.decode(token, key, algorithms=["HS256"]) == payload
    assert JwtCrypt.decode(token, _key=key) == payload
    with pytest.raises(JWTError):
        JwtCrypt.decode(token)


def test_reject_wrong_key(payload):
    """Reject a token when verification uses a different key."""
    token = JwtCrypt.encode(payload)

    with pytest.raises(JWTError):
        JwtCrypt.decode(token, _key=os.environ["SJWTK"] + "-wrong")


def test_reject_malformed_token():
    """Reject input that is not a JWT."""
    with pytest.raises(JWTError):
        JwtCrypt.decode("not-a-jwt")


def test_reject_expired_token(payload):
    """Reject a correctly signed token with an expired timestamp."""
    token = JwtCrypt.encode({**payload, "exp": 1})

    with pytest.raises(ExpiredSignatureError):
        JwtCrypt.decode(token)


def test_reject_unapproved_algorithm(payload):
    """Reject tokens signed with an algorithm other than HS256."""
    token = jwt.encode(payload, os.environ["SJWTK"], algorithm="HS512")

    with pytest.raises(JWTError):
        JwtCrypt.decode(token)
