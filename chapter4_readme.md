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
對於私有方法和函數，通常添加前導下劃線。 由於 Python 中的名稱修改功能，這條規則頗受爭議。 當一個方法有兩個前導下劃線時，它會被解釋器即時重命名，以防止與任何子類的方法發生名稱衝突。
示例
```python
class Base(object):
    def __secret(self):
        print("don't tell")
    def public(self):
        self.__secret()

class Derived(Base):
    def __secret(self):
        print("never never")
```

但最佳實踐，正如 BDFL（Guido，終生仁慈的獨裁者，參見 http://en.wikipedia.org/wiki/BDFL）所說，
是通過查看 __mro__（方法解析順序）來避免使用名稱重整 在子類中編寫方法之前，類的值。 必須謹慎更改基類的私有方法。
有關此主題的更多信息，多年前 Python-Dev 郵件列表中出現了一個有趣的線程，人們在其中爭論名稱重整的實用程序及其在該語言中的命運。

#### Special methods 
特殊方法 (https://docs.python.org/3/reference/datamodel.html#special-method-names) 
以雙下劃線開頭和結尾，正常方法不應使用此約定。 一些開發人員習慣於將它們稱為雙下劃線的合成詞。
 它們用於運算符重載、容器定義等。 為了可讀性，它們應該放在類定義的開頭：
```python
class WeirdInt(int):
    def __add__(self,other):
        return int.__add__(self,other)+1
    
    def __repr__(self):
        return '<weirdo %d>'%self 
    #public api 
    def do_this(self):
        print('This')
    def do_that(self):
        print('that')
class BadHabits:
    def __my_method__(self):
        print("ok") 
```

#### Arguments
參數是小寫的，如果需要的話有下劃線。 它們遵循與變量相同的命名規則。

#### Properties 
屬性的名稱是小寫的，或者是帶下劃線的小寫。 大多數時候，它們代表一個對象的狀態，可以是名詞或形容詞，或者在需要時是一個小短語：
```python
class Connection:
    connected = []
    def connect(self,user):
        self.connected.append(user)
    @property
    def connected_people(self):
        return ",".join(self._connected)

```

#### Classes 
類的名稱總是採用 駝峰命名，並且可能有前導
當它們對模塊私有時加下劃線。
類和實例變量通常是名詞短語，與作為動詞短語的方法名形成使用邏輯：

#### Module and packages 
除了特殊模塊 `__init__` 之外，模塊名稱都是小寫的，沒有下劃線。以下是標準庫中的一些示例：
- os
- sys
- shutil

當模塊對包私有時，會添加前導下劃線。 編譯的 C 或 C++ 模塊通常用下劃線命名，並在純 Python 模塊中導入。
包名稱遵循相同的規則，因為它們的行為更像結構化的模塊。

## The nameing guide 
一組通用的命名規則可以應用於變量、方法、函數和屬性。 類和模塊的名稱在命名空間構造中也起著重要作用，
進而影響代碼的可讀性。 這個迷你指南提供了常見的模式和反模式來選擇它們的名字。

### Using the has or is prefix for Boolean elements 
當一個元素包含一個布爾值時，is 和 has 前綴提供了一種自然的方式來使其在其名稱空間中更具可讀性：
```python
class DB:
    is_connected = False 
    has_cache = False 
```

### Using plurals for variables that are collections 
當一個元素持有一個集合時，使用複數形式是個好主意。 當某些映射像序列一樣公開時，它們也可以從中受益：

```python
class DB:
    connected_users  = ['Tarek'] 
    tables = {
        "Customer":['id','first_name','last_name']
    }
```
### Using explicit names for dictionaries
當變量包含映射時，您應該盡可能使用顯式名稱。 例如，如果一個字典包含一個人的地址，它可以命名為 persons_addresses：
```python
persons_addresses = {'Bill':"6565 Monty Roade",'Pamela':"45 Python street"}
persons_addresses['Pamela']
```
### Avoiding generic names
如果您的代碼沒有構建新的抽像數據類型，那麼使用諸如列表、字典、序列或元素之類的術語，即使是局部變量，也是有害的。 它使代碼難以閱讀、理解和使用。 還必須避免使用內置名稱，以避免在當前命名空間中隱藏它。 也應避免使用通用動詞，除非它們在名稱空間中有意義。
相反，應該使用特定領域的術語：
```python

def compute(data):  # too generic
    for element in data:
        yield element ** 2
def squares(numbers):  # better
    for number in numbers:
        yield number ** 2

```
還有一個應該避免的包名列表。 從長遠來看，任何不提供任何關於其內容線索的內容都會對項目造成很大的傷害。 
諸如 misc、tools、utils、common 或 core 之類的名稱很容易變成無窮無盡的各種不相關的質量很差的代碼片段，
而且這些代碼片段的大小似乎呈指數級增長。 在大多數情況下，這種模塊的存在是懶惰或缺乏足夠設計努力的標誌。
此類模塊名稱的愛好者可以簡單地預防未來並將它們重命名為 trash 或 dumpster，因為這正是他們的隊友最終將如何對待此類模塊。


在大多數情況下，擁有更多小模塊幾乎總是更好，即使內容很少，但名稱能很好地反映內部內容。 
老實說，像 utils 和 common 這樣的名字本身並沒有錯，可以負責任地使用它們。 
但現實表明，在許多情況下，它們反而成為了快速擴散的危險結構反模式的存根。 
如果你行動不夠快，你可能永遠無法擺脫它們。 
因此，最好的方法就是簡單地避免這種有風險的組織模式，並在項目中的其他人引入時將其消滅在萌芽狀態。
### Avoiding existing names
使用上下文中已經存在的名稱是不好的做法，因為它會使閱讀，更具體地說，調試變得非常混亂：

## Best practices for arguments 
函數和方法的簽名是代碼完整性的守護者。 他們推動其使用並構建其 API。 除了我們之前看到的命名規則外，還必須特別注意參數。 
這可以通過三個簡單的規則來完成：
- 通過迭代設計建立論點
- 相信論據和你的測試
- 小心使用 *args 和 **kwargs 魔術參數
- 
### Building arguments by iterative design    
每個函數都有一個固定且定義明確的參數列表，可以使代碼更加健壯。 
但這在第一個版本中無法做到，因此必須通過迭代設計來構建參數。 它們應該反映元素創建的精確用例，並相應地發展。
例如，當附加一些參數時，它們應該盡可能具有默認值，以避免任何回歸：

當必須更改公共元素的參數時，將使用棄用過程，這將在本節後面介紹。

### Trust the arguments and your tests
鑑於 Python 的動態類型特性，一些開發人員在其函數和方法的頂部使用斷言來確保參數具有正確的內容：
```python
def division(dividend, divisor):
    assert isinstance(dividend, (int, float))
    assert isinstance(divisor, (int, float))
    return dividend / divisor
```
當庫中的代碼被外部元素使用時，進行斷言會很有用，因為傳入的數據可能會破壞事物甚至造成損害。 這發生在處理數據庫或文件系統的代碼中。
另一種方法是模糊測試 (http://en.wikipedia.org/wiki/Fuzz_testing)，其中將隨機數據片段發送到程序以檢測其弱點。 當發現新的缺陷時，可以修復代碼以解決這個問題，同時進行新的測試。
讓我們注意確保遵循 TDD 方法的代碼庫朝著正確的方向發展，並且變得越來越健壯，因為每次出現新故障時都會對其進行調整。 當它以正確的方式完成時，測試中的斷言列表在某種程度上變得類似於先決條件列表。

### Using args and *kwargs magic arguments carefully
*args 和 **kwargs 參數可以破壞函數或方法的穩健性。 它們使簽名變得模糊，並且代碼通常會在不應該構建的地方開始構建一個小的參數解析器：

魔術參數有時無法避免，尤其是在元編程中。 例如，它們在創建裝飾器時不可或缺，裝飾器可以處理具有任何類型簽名的函數。 在更全局的範圍內，在處理剛剛遍歷函數的未知數據的任何地方，魔術參數都很棒：
```python
import logging 
def log(**context):
    logging.info('Context is:\n%s\n' % str(context))

```
## Class names 
類的名字要簡潔、準確，從名字就足以明白這個類是乾什麼的。 一種常見的做法是使用後綴來告知其類型或性質，例如：
- SQLEngine 
- MimeTypes 
- StringWidget 
- 測試用例
對於基類或抽像類，可以按如下方式使用 Base 或 Abstract 前綴：
- BaseCookie
- Abstract Formatter 抽象格式化程序
最重要的是要與類屬性保持一致。 例如，盡量避免類及其屬性名稱之間的冗餘：

## Module and package names 
模塊和包名稱告知其內容的用途。 名字很短，小寫，沒有下劃線：
- sqlite
- postgres
- sha1
如果它們正在實現一個協議，它們通常以 lib 為後綴：
```python
import smtplib
import urllib
import telnetlib
```
當一個模塊變得複雜並且包含很多類時，最好創建一個包並將模塊的元素拆分到其他模塊中。

## Useful tools 
可以使用以下工具來控制和製定以前的部分約定和做法：
- Pylint：這是一個非常靈活的源代碼分析器
- pep8 和 flake8：它們是一個小型代碼風格檢查器，以及一個向其添加一些更有用的功能（如靜態分析和復雜性測量）的包裝器

### Pylint 
除了一些質量保證指標外，Pylint 還允許您檢查給定的源代碼是否遵循命名約定。 它的默認設置對應於 PEP 8，並且 Pylint 腳本提供了 shell 報告輸出。


默認啟用的可用檢查列表很長。 重要的是要知道一些規則是任意的，不會輕易適用於每個代碼庫。 
請記住，一致性總是比遵守某些武斷的標準更有價值。 
幸運的是，Pylint 非常可調，因此如果您的團隊使用一些與默認假設不同的命名和編碼約定，您可以輕鬆配置它以檢查與這些約定的一致性。

### pep8 and flake8 
pep8 是一種只有一個目的的工具：它僅提供針對 PEP 8 代碼約定的樣式檢查。這是與 Pylint 的主要區別，Pylint 具有許多附加功能。 
對於只對 PEP 8 標準的自動代碼樣式檢查感興趣的程序員來說，這是最佳選擇，無需任何額外的工具配置，如 Pylint 的情況。

## Summary 

