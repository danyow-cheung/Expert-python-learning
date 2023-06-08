from random import shuffle 
from cffi import FFI 

ffi = FFI()
ffi.cdef("""
    void qsort(void base,size_t nel,size_t width,int(compar) (const void,const void));
    """)
C = ffi.dlopen(None)
@ffi.callback("int(void *,void*)")
def cffi_int_compare(a,b):

    int_a = ffi.cast('int*',a)[0]
    int_b = ffi.cast('int*',b)[0]
    print(" %s cmp %s" % (int_a, int_b))
    return int_a - int_b 

def main():
    numbers = list(range(5))
    shuffle(numbers)
    print("suffled",numbers)
    c_array = ffi.new("int[]",numbers)
    C.qsort(
        c_array,len(c_array),ffi.sizeof('int'),cffi_int_compare,
    )
    print('sorted',list(c_array))
if __name__ =='__main__':
    main()
    