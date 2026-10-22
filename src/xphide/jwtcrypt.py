"""jwtcrypt module."""

from jose import jwt
from xphide.envvar_loader import load

class JwtCrypt:
    """A class that encodes and decodes an entity.

    Methods
    -------
    encode(_payload)
        returns json token.

    decode(_token)
        returns the decoded payload.
    """

    s_cypher = load()

    @staticmethod
    def encode(_payload: dict, _key: str = None) -> str:
        """Encode a given payload.

        Parameters
        ----------
        _payload: str
            the payload to encode
        """
        return jwt.encode(_payload, key=_key or JwtCrypt.s_cypher)

    @staticmethod
    def decode(_token: str, _key: str = None) -> object:
        """Decode the jw token.

        Parameters
        ----------
        _token: str
            the token (encrypted payload)

        Returns
        -------
        Any
            the decoded payload
        """
        return jwt.decode(
            _token, key=_key or JwtCrypt.s_cypher, algorithms=["HS256"]
        )
