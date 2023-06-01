class RevealAccess(object):
    '''
    A data descriptor that sets and returns values 
    normally and prints a message logging their access
    '''
    def __init__(self,initival=None,name='var') -> None:
        self.val = initival
        self.name = name 
    
    def __get__(self,obj,objtype):
        print('Retrieving ',self.name)
        return self.val 
    
    def __set__(self,obj,val):
        print('Updating ',self.name)
        self.val = val 

class  myClass(object):
    x = RevealAccess(10, 'var "x"')
    y = 5 

if __name__ =="__main__":
    m = myClass()
    print(m.x)
    m.x = 20 
    print(m.x)
    print(m.y)
    