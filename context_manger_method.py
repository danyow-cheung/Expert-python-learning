from contextlib import contextmanager
@contextmanager
def context_illustration():
    print('entering context')
    try:
        yield 
    except Exception as e:
        print("Leaving context")
        print("With an error (%s)"%e)
        raise 
    else:
        print('leaving context')
        print('with no error')
        