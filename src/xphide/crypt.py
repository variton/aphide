"""crypt module."""

import bcrypt


class Crypt:
    """A class that generate an encrypted string."""

    s_encoding_ = "ascii"

    @staticmethod
    def hash(entity: str) -> str:
        """Generate hash for a given entity."""

        x_bytes = bytes(entity, Crypt.s_encoding_)
        x_hash = bcrypt.hashpw(x_bytes, bcrypt.gensalt())
        return x_hash.decode(Crypt.s_encoding_)

    @staticmethod
    def is_equal(x_hash: str, entity: str) -> bool:
        """Check if an entity is equal to the encrypted object."""

        x_bytes = bytes(entity, Crypt.s_encoding_)
        ret = bcrypt.checkpw(x_bytes, bytes(x_hash, Crypt.s_encoding_))
        return True if ret else False
