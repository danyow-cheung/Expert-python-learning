class Metaclass(type):
    '''
    name、bases 和 namespace 參數與前面解釋的 type() 調用具有相同的含義，
    但這四種方法中的每一種都可以有不同的目的：
    '''
    def __new__(mcs,name,bases,namespace):
        # 它负责类对象的实际创建，其方式与创建普通类的方式相同。 
        # 第一个位置参数是元类对象。 在前面的示例中，它只是一个元类。 请注意，mcs 是此参数的流行命名约定。    
        return super().__new__(mcs,name,bases,namespace)
    
    @classmethod
    def __prepare__(mcs, name,bases,**kwargs) :
        # 这将创建一个空的命名空间对象。 默认情况下，它返回一个空字典，但可以重写它以返回任何其他映射类型。 
        # 请注意，它不接受名称空间作为参数，因为在调用它之前名称空间不存在。    
        return super().__prepare__(name, bases, **kwargs)

    def __init__(cls,name,bases,namespace,**kwargs):
        # 这在元类实现中并不常见，但与普通类具有相同的含义。 一旦使用 __new__() 创建，
        # 它就可以执行额外的类对象初始化。 
        # 第一个位置参数现在按照约定命名为 cls 以标记这已经是一个创建的类对象（元类实例）而不是元类对象。 
        # 当 __init__() 被调用时，类已经被构建，所以这个方法可以做的事情比 __new__() 方法少。 
        # 实现这种方法与使用类装饰器非常相似，
        # 但主要区别在于 __init__() 将为每个子类调用，而不会为子类调用类装饰器。
        super().__init__(name,bases,namespace)
    
    def __call__(cls,args,*kwargs):
        # 这在元类的实例被调用时被调用。 
        # 元类的实例是一个类对象（参考图3）；
        #  当您创建类的新实例时会调用它。 这可用于覆盖创建和初始化类实例的默认方式。
        return super().__call__(args,*kwargs)
    
    
    
