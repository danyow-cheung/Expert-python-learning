
# class CommonBase:
#     def __init__(self) -> None:
#         print('CommonBase')
#         super().__init__()

# class Base1(CommonBase):
#     def __init__(self) -> None:
#         print("Base1")
#         super().__init__()


# class Base2(CommonBase):
#     def __init__(self) -> None:
#         print("Base2")
#         super().__init__()

# class MyClass(Base1,Base2):
#     def __init__(self,arg) -> None:
#         print("my base")
#         super().__init__(arg)

'''
An attempt to create a MyClass instance will raise TypeError 
due to the mismatch of the parent classes' __init__() signatures:
'''
# try:
#     MyClass(10)
# finally:
#     print('error')
'''
一種解決方案是使用包含 *args 和 **kwargs 魔法的參數和關鍵字參數，
以便所有構造函數傳遞所有參數，即使它們不使用它們也是如此：
'''


class CommonBase:
    def __init__(self,args,*kwargs) -> None:
        print('CommonBase')
        super().__init__()

class Base1(CommonBase):
    def __init__(self,args,*kwargs) -> None:
        print("Base1")
        super().__init__(args,*kwargs)


class Base2(CommonBase):
    def __init__(self,args,*kwargs) -> None:
        print("Base2")
        super().__init__(args,*kwargs)

class MyClass(Base1,Base2):
    def __init__(self,arg) -> None:
        print("my base")
        super().__init__(arg)


try:
    MyClass(10)
finally:
    print('error')
'''
不過這是一個糟糕的修復，因為它使所有構造函數都接受任何類型的參數。 
它會導致代碼薄弱，因為任何東西都可以通過。
 另一種解決方案是使用 MyClass 中特定類的顯式 __init__() 調用，但這會導致第一個陷阱。
'''
