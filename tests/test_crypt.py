"""Unit tests for the Crypt class."""
import pytest
import bcrypt

from xphide.crypt import Crypt

@pytest.fixture(name="fake_pwd")
def fake_pwd_fixture():
    """Provides a fake pwd."""
    return "#obl1V1on&shah7"

@pytest.fixture(name="hash_obj")
def generate_hash_fixture(fake_pwd):
    """Creates a hash object."""
    xhash=Crypt.hash(fake_pwd)
    return xhash

def test_hash(hash_obj,fake_pwd):
    """Tests the hashing method."""
    assert fake_pwd != hash_obj 

def test_is_equal(fake_pwd,hash_obj):
    """Tests the usage of the hash seed."""
    assert Crypt.is_equal(hash_obj,fake_pwd) == True
