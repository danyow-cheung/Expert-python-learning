# Choosing Good Names 
## PEP8 and naming best practices 
PEP 8 (http://www.python.org/dev/peps/pep-0008) 提供了编写 Python 代码的风格指南。
除了空格缩进、最大行长度和其他有关代码布局的细节等基本规则外，PEP 8 还提供了大多数代码库遵循的命名约定部分。

### Why and when to follow PEP8 
如果你想接受其他程序员的任何合作，那么你一定要坚持使用 PEP 8，

### Beyond PEP8 - team specific style guidelines 
此外，在某些情况下，在一些没有定义样式指南的旧项目中，严格遵守 PEP 8 可能是不可能的，或者在经济上不可行。 
此类项目仍将受益于实际编码约定的形式化，即使它们不反映官方的 PEP 8 规则集。 
请记住，比与 PEP 8 保持一致更重要的是项目内部的一致性。 
如果规则是正式的并且可以作为每个程序员的参考，那么在项目和组织内保持一致性就容易多了。

## Naming styles 

The different naming styles used in Python are:
- CamelCase骆驼香烟盒
- mixedCase大小写混合
- UPPERCASE, and UPPER_CASE_WITH_UNDERSCORES lowercase and lower_case_with_underscores 
大写和 UPPER_CASE_WITH_UNDERSCORES 小写和 lower_case_with_underscores
- `_leading and trailing_` underscores下划线, and sometimes `__doubled__` underscores下划线

### Variables 
Python 中有两种变量：
- 常量
- 公共变量和私有变量

#### Constants
对于常量全局变量，使用带下划线的大写字母。 它通知开发人员给定的变量代表一个常量值。

#### Naming and usage 
A good practice is to gather all the constants in a single file in the package. That is how Django works, for instance. A module named settings.py provides all the constants:
```python
# config.py 
SQL_USER = 'tarek' 
SQl_PASSWORD = 'secret'
SQL_URI = 'postgres://%s:%s@localhost/db' % (
    SQL_USER, SQL_PASSWORD
)
MAX_THREADS = 4 
```
另一种方法是使用可以使用 ConfigParser 模块解析的配置文件，或者使用诸如 ZConfig 之类的高级工具，
它是 Zope 中用来描述其配置文件的解析器。 但有些人认为，在 Python 等语言中使用另一种文件格式有点矫枉过正，
因为在 Python 中，文件可以像文本文件一样容易编辑和更改。

#### Public and private variables 
对于可变且可通过导入自由使用的全局变量，需要保护时应使用带下划线的小写字母。 但是这些类型的变量并不经常使用，因为模块通常会提供 getter 和 setter 以在需要保护它们时使用它们。 在这种情况下，前导下划线可以将变量标记为包的私有元素：
```python
observers = []
def add_observer(observer):
    observers.append(observer)

def get_observers():
    return tuple(observers)
```

位于函数和方法中的变量遵循相同的规则，并且永远不会标记为私有，因为它们是上下文的本地变量。

对于类或实例变量，只有在使变量成为公共签名的一部分不会带来任何有用信息或者是多余的情况下，才必须使用私有标记（前导下划线）。

换句话说，如果变量在方法内部使用以提供公共特性，并且专用于这个角色，最好将其设为私有。

例如，为财产提供动力的属性是良好的私人公民：
```python
class Citizen(object):
    def __init__(self):
        self._message = 'Rosebud'
    def get_message(self):
        return self._message 
    
    kane = property(getmessage)
```
另一个例子是保持内部状态的变量。 这个值是
对其余代码没有用，但参与类的行为
```python
class UnforgivingElephant(object):
    def __init__(self,name):
        self.name = name 
        self._people_to_stopm_on = []
    def get_slapped_by(self,name):
        self._people_to_stomp_on.append(name)
        print("Ouch")
    def revenge(self):
        print("10 years later")
        for person in self._people_to_stomp_on:
            print('%s stomps on %s' % (self.name, person))
```

#### Functions and methods 
函数和方法应使用小写字母并带有下划线。 在旧的标准库模块中，这条规则并不总是正确的。 Python 3 对标准库做了很多重组，所以它的大部分函数和方法都有一个一致的大小写。 不过，对于某些模块（如线程），您可以访问使用混合大小写的旧函数名称（例如，currentThread）。 这是为了更容易向后兼容，但如果您不需要在旧版本的 Python 中运行您的代码，那么您应该避免使用这些旧名称。

#### The private controversy
#### Special methods 
#### Arguments
#### Properties 
#### Classes 
#### Module and packages 

## The nameing guide 
### Using the has or is prefix for Boolean elements 
### Using plurals for variables that are collections 
### Using explicit names for dictionaries
### Avoiding generic names
### Avoiding existing names

## Best practices for arguments 
### Building arguments by iterative design                                   
### Trust the arguments and your tests
### Using args and *kwargs magic arguments carefully

## Class names 
## Module and package names 
## Useful tools 
### Pylint 
### pep8 and flake8 
## Summary 

