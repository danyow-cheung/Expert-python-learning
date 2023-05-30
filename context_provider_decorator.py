from threading import RLock

lock = RLock()
def synchronized(function):
    def _synchronized(args,*kw):
        lock.acquire()
        try:
            return function(args,*kw)
        finally:
            lock.release()
    return _synchronized

@synchronized 
def thread_safe():
    pass 
