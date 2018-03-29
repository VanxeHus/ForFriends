from Crypto.Cipher import AES
from Crypto import Random


def Encrypto(self, key, mode, randStr, msg):
    eryObj = AES.new(key, mode, randStr)
    return eryObj.encrypt(msg)


def Decrypto(self, key, mode, randStr, msg):
    eryObj = AES.new(key, mode, randStr)
    return eryObj.decrypt(msg)
