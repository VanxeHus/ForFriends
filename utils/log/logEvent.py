#!usr/bin/python
# coding=utf-8

# log the type of running func
def LogEvent(type):
    def logType(f):
        def innerLog(*args, **kw):
            print ("[%s]%s()" % (type, f.__name__))
            if args:
                for i in range(0,len(args)):
                    print ("--args %s:%s--" %(i,args[i]))
            else:
                print("--args:null--")
            if kw:
                for key in kw:
                    print ("--key:%s value:%s--"%(key,kw[key]))
            else:
                print("--kw:null--")
            f(*args, **kw)
        return innerLog

    return logType