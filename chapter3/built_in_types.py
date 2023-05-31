
class DistinctError(ValueError):
    '''
    Raise when duplicate value is added to a distinctdict
    '''

class distinctdict(dict):
    '''Dictionary that does not accept duplicate values '''
    def __setitem__(self,key, value) -> None:
        if value in self.values():
            if ( (key in self and self[key] != value ) or key not in self):
                raise DistinctError('This value already exists for different key')
        
        super().__setitem__(key,value)


'''
如果您查看現有代碼，您可能會發現許多類部分實現了內置類型，
並且作為子類型可能更快更簡潔。 
例如，列表類型管理序列，並且可以在每次類在內部使用序列時使用：
'''

class Folder(list):
    def __init__(self,name):
        self.name = name 
    def dir(self,nesting=0):
        offset = ' '* nesting 
        print('%s%s/' % (offset, self.name))
        for element in self:
            if hasattr(element,'dir'):
                element.dir(nesting+1)
            else:
                print("%s  %s" % (offset, element))

if __name__ =='__main__':
    # my = distinctdict()
    # my['key'] = 'value'
    # my['other_key'] = 'value2'
    # print(my)
    # 示範2 
    tree = Folder('project')
    tree.append('readme.txt')
    tree.dir()
    src = Folder('src')
    src.append('script.py')
    tree.append(src)    
    tree.dir()