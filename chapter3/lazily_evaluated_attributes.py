class InintOnAccess:
    def __init__(self,klass,args,*kwargs):
        self.klass = klass 
        self.args = args 

        self.kwargs = kwargs 
        self._initialized = None 
    
    def __get__(self,instancem,owner):
        if self._initialized is None:
            print("Initiliazed ")
            # `**語法需要映射`
            # self._initialized = self.klass(*self.args,**self.kwargs) 
            self._initialized = self.klass(self.args,*self.kwargs) 

        else:
            print("Cached")
        return self._initialized

if __name__=='__main__':

    class Myclass:
        lazily_initialized = InintOnAccess(list,'argument')


    m = Myclass()
    m.lazily_initialized
    m.lazily_initialized
