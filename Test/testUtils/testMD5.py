import utils.encrypt.MD5 as MD5
def testNo_salt():
    p=MD5.MD5Encrypto_noSalt("xsfxsfxsf")
    print p
    print MD5.MD5Encrypto_withSalt(p,"originSalt")
testNo_salt()