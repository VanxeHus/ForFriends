#!usr/bin/python
#coding=utf-8
import hashlib
def MD5Encrypto_withSalt(password,salt):
    md5=hashlib.md5()
    md5.update((password+salt).encode("utf-8"))
    return md5.hexdigest()
def MD5Encrypto_noSalt(password):
    md5=hashlib.md5()
    md5.update((password).encode("utf-8"))
    return md5.hexdigest()