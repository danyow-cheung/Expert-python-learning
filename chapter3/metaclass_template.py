class Metaclass(type):
    '''
    name、bases 和 namespace 參數與前面解釋的 type() 調用具有相同的含義，
    但這四種方法中的每一種都可以有不同的目的：
    '''
    def __new__(mcs,name,bases,namespace):
        return super().__new__(mcs,name,bases,namespace)
    
    @classmethod
    def __prepare__(mcs, name,bases,**kwargs) :
        return super().__prepare__(name, bases, **kwargs)

    def __init__(cls,name,bases,namespace,**kwargs):
        super().__init__(name,bases,namespace)
    
    def __call__(cls,args,*kwargs):
        return super().__call__(args,*kwargs)
    
