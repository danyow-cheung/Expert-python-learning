class ContextIllustration:
    def __enter__(self):
        print('entering context')
    def __exit__(self, exc_type, exc_value, traceback):
        print('leaving context')
    
        if exc_type is None:
            print("with no errors")
        else:
            print("with an error(%s) "%exc_value)
    