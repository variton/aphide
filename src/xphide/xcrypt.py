"""xcrypt module."""

from enum import Enum

from cryptography.fernet import Fernet

class Encoding(Enum):
    ASCII = 1
    UTF8 = 2

ENCODINGMAPPER = { Encoding.ASCII : "ascii", Encoding.UTF8 : "utf-8" }
                
class Xcrypt:
    """xcrypt class."""

    def __init__(self,encoding:Encoding=Encoding.ASCII,
                      mappper:dict=ENCODINGMAPPER,
                      cipher:object=None):
        
        if cipher is None:
            key = Fernet.generate_key()
            cipher = Fernet(key)

        self.cipher_=cipher
        self.encoding_=ENCODINGMAPPER[encoding]

    def encrypt(self,data: str) -> str:
        return self.cipher_.encrypt(data.encode(self.encoding_))

    def decrypt(self,data: str) -> str:
        return self.cipher_.decrypt(data).decode(self.encoding_)
