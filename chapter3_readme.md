# Chapter 3. Syntax Best Practices – above the Class Level
## subclassing built-in types 
在 Python 中子類化內置類型非常簡單。 稱為對象的內置類型是所有內置類型以及所有未指定顯式父類的用戶定義類的共同祖先。 由於這一點，每當需要實現一個行為幾乎類似於其中一種內置類型的類時，最佳實踐就是對其進行子類型化。


現在，我們將向您展示一個名為 distinctdict 的類的代碼，它使用了這種技術。 它是通常的 Python dict 類型的子類。 這個新類的行為在大多數方面都像普通的 Python 字典。 但是當有人試圖添加一個具有相同值的新條目時，它不會允許具有相同值的多個鍵，它會引發一個帶有幫助消息的 ValueError 子類：
> chapter3/built_in_types.py


**tips最常使用的場景**
當您要創建一個類似於序列或映射的新類時，請考慮其功能並查看現有的內置類型。 collections 模塊使用許多有用的容器擴展了基本的內置類型。 大多數時候你最終會使用其中之一。

## Accessing methods from superclasses 
super 是一個內置類，可用於訪問屬於對象超類的屬性。
> chapter3/superclasses.py 

關於 super 應該注意的最後也是最重要的一點是它的第二個參數是可選的。 當只提供第一個參數時，super 返回一個無界類型。 這在使用類方法時特別有用：
> chapter3/superclasses_method.py
> 
### Understanding Python's method Resolution Order 
它描述了 C3 如何構建類的線性化，也稱為優先級，它是祖先的有序列表。 此列表用於查找屬性。 本節稍後將更詳細地描述 C3 算法。


進行 MRO 更改是為了解決創建通用基類型（對象）時引入的問題。 在更改為 C3 線性化方法之前，如果一個類有兩個祖先（請參閱圖 1），對於不使用多重繼承模型的簡單情況，方法解析的順序非常容易計算和跟踪。 以下是在 Python 2 下不會使用 C3 作為方法解析順序的代碼示例：
```python
class Base1:
    pass 
class Base2:
    def method(self):
        print("Base2")

class MyClass(Base1,Base2):
    pass 

```
簡單來說，就是python3改變了繼承的方法，使得上面的代碼可以得到輸出`Base2`

### Super pitfalls 
回到super。 在使用多重繼承層次結構時，它的使用是相當危險的，主要是因為類的初始化。 在 Python 中，基類不會在 __init__() 中隱式調用，因此由開發人員調用它們。 我們將看到幾個例子。

#### Mixing super and explict class calls 混合super和explict類調用
> chapter3/superpitfalls_super_explict.py
如代碼結果，classB會被調用兩次

這是由於 A.__init__(self) 調用而發生的，該調用是使用 C 實例進行的，因此使 super(A, self).__init__() 調用 B.__init__() 方法。
換句話說，應該在整個類層次結構中使用 super。 問題是有時這個層次結構的一部分位於第三方代碼中。 多重繼承引入的層次結構調用的許多相關陷阱

#### Heterogeneous arguments 異類論證
> chapter3/superpitfalls_Heterogeneous_argu.py


### Best practices 
為了避免所有提到的問題，並且在 Python 在該領域發展之前，我們需要考慮以下幾點：
- 應避免多重繼承：它可以用第 14 章“有用的設計模式”中介紹的一些設計模式代替。
- super 用法必須保持一致：在類層次結構中，super 應該無處不在。 混合超級調用和經典調用是一種令人困惑的做法。 人們傾向於避免使用 super，因為他們的代碼更明確。 
- 如果您也以 Python 2 為目標，則顯式繼承 Python 3 中的對象：沒有指定任何祖先的類在 Python 2 中被識別為舊式類。在 Python 2 中應避免將舊式類與新式類混合。
- 調用母類時必須查看類層次結構：為避免出現任何問題，每次調用父類時，都必須快速瀏覽一下涉及的 MRO（使用 __mro__）。

## Adavanced attribute access patterns 
許多C++和Java程序員剛開始學習Python時，都對Python沒有private關鍵字感到驚訝。 最接近的概念是名稱修改。 每次屬性以 __ 為前綴時，它都會被解釋器即時重命名：
```python
class MyClass:
    __secret_value = 1 
instance = Myclass() # error

```
Accessing the __secret_value attribute by its initial name will raise an AttributeError exception:
通過其初始名稱訪問 __secret_value 屬性將引發 AttributeError 異常：

提供此功能是為了避免繼承下的名稱衝突，因為使用類名作為前綴對屬性進行重命名。 它不是真正的鎖，因為可以通過其組合名稱訪問該屬性。 此功能可用於保護某些屬性的訪問，但實際上，永遠不應使用 __。 當屬性不是公共的時，使用的約定是 _ 前綴。 這不會調用任何修改算法，而只是將屬性記錄為類的私有元素，並且是流行的樣式。

Python 中還有其他機制可以將類的公共部分與私有代碼一起構建。 作為 OOP 設計關鍵特性的描述符和屬性應該用於設計乾淨的 API。


### Descriptors 
描述符是 Python 中復雜屬性訪問的基礎。 它們在內部用於實現屬性、方法、類方法、靜態方法和超類型。 它們是定義如何訪問另一個類的屬性的類。 換句話說，一個類可以將一個屬性的管理委託給另一個類。

描述符類基於構成描述符協議的三個特殊方法：
- `__set__(self, obj, type=None):`只要設置了屬性，就會調用此方法。 在以下示例中，我們將其稱為設置器。 
- `__get__(self, obj, value)：`每當讀取屬性時都會調用它（稱為 getter）。
- `__delete__(self, obj)：`這在屬性上調用 delis 時被調用。

實現 __get__() 和 __set__() 的描述符稱為數據描述符。 如果它只是實現了__get__()，那麼它就被稱為非數據描述符。
展示數據描述符是怎麼work的
> chapter3/data_descriptors.py

由於開頭所述的事實，數據和非數據描述符之間的區別很重要。 Python 已經使用描述符協議將類函數作為方法綁定到實例。 它們還為 classmethod 和 staticmethod 裝飾器背後的機制提供支持。 這是因為，實際上，函數對像也是非數據描述符：

因此，如果 __dict__ 優先於非數據描述符，我們將無法在運行時動態覆蓋已構造實例的特定方法。 幸運的是，多虧了描述符在 Python 中的工作方式。 它是可用的，因此開發人員可以使用一種稱為 monkey-patching 的流行技術來更改實例的工作方式，而無需子類化。

#### Real-life example -lazily evaluated attributes
描述符的一個示例用法可能是將類屬性的初始化延遲到從實例訪問它的那一刻。 如果此類屬性的初始化取決於全局應用程序上下文，這可能很有用。 另一種情況是這樣的初始化非常昂貴，但不知道在導入類時是否會使用它。 這樣的描述符可以按如下方式實現：
> chapter3/lazily_evaluated_attributes.py 

對於使用 OpenGL 編寫的應用程序，這通常是正確的。 例如，在 OpenGL 中創建著色器非常昂貴，因為它需要編譯用 GLSL
下面的示例顯示了 PyOpenGL 的 lazy_property 裝飾器（這裡是 lazy_class_attribute）的修改版本在一些虛構的基於 OpenGL 的應用程序中的可能用法。 為了允許在不同類實例之間共享屬性，需要對原始 lazy_property 裝飾器進行突出顯示的更改：
> chapter3/opengl.py 
### Properties 
這些屬性提供了一個內置的描述符類型，它知道如何將一個屬性鏈接到一組方法。 屬性有四個可選參數：fget、fset、fdel 和 doc。 可以提供最後一個來定義鏈接到屬性的文檔字符串，就好像它是一個方法一樣。 下面是一個 Rectangle 類的示例，可以通過直接訪問存儲兩個角點的屬性或使用寬度和高度屬性來控制它：
> chapter3/properties.py

### Slots 
開發人員幾乎從未使用過的一個有趣功能是插槽。 它們允許您使用 `__slots__` 屬性為給定類設置靜態屬性列表，並跳過在該類的每個實例中創建 `__dict__` 字典。 它們旨在為屬性很少的類節省內存空間，因為 `__dict__` 不是在每個實例中都創建的。

除此之外，他們還可以幫助設計需要凍結其簽名的類。 例如，如果您需要在類上限制語言的動態特性，定義插槽可以提供幫助：
```python
class Frozen:
    __slots__ ['ice','cream']
>>> '__dict__' in dir(Frozen)
False
>>> 'ice' in dir(Frozen)
True
>>> frozen = Frozen()
>>> frozen.ice = True
>>> frozen.cream = None
>>> frozen.icy = True
Traceback (most recent call last):
  File "<input>", line 1, in <module>
AttributeError: 'Frozen' object has no attribute 'icy'

```
應謹慎使用此功能。 當使用 __slots__ 限制一組可用屬性時，動態地向對象添加一些東西要困難得多。 一些技術，例如猴子修補，不適用於定義了槽的類的實例。 幸運的是，如果派生類沒有定義自己的槽，則可以將新屬性添加到派生類中：

## Metaprogramming元編程
> "Metaprogramming is a technique of writing computer programs that can treat themselves as data, so you can introspect, generate, and/or modify itself while running."
> “元編程是一種編寫可以將自身視為數據的計算機程序的技術，因此您可以在運行時自省、生成和/或修改自身。”
**通過定義，我們可以區分 Python 中元編程的兩種主要方法。**

- 第一種方法側重於語言自省其基本元素（如函數、類或類型）並即時創建或修改它們的能力。 Python 為這方面的開發人員提供了很多工具。 最簡單的是裝飾器，它允許向現有函數、方法或類添加額外的功能。 
- 接下來是允許您干擾類實例進程創建的類的特殊方法。 最強大的是元類，它允許程序員甚至完全重新設計 Python 的面向對象編程範例的實現。 

在這裡，我們還提供了一系列不同的工具，允許程序員直接使用原始純文本格式或更易於編程訪問的抽象語法樹 (AST) 形式的代碼。 第二種方法當然更複雜，也更難使用，但可以做一些非常特別的事情，例如擴展 Python 的語言語法，甚至創建您自己的領域特定語言 (DSL)。


### Decorators -- a method of metaprogramming 
```python
def decorated_function():
    pass 
decorated_function = some_decorator(decorated_function)
```
這清楚地顯示了裝飾器的作用。 它接受一個函數對象並在運行時修改它。 結果，一個新的函數（或其他任何東西）基於先前同名的函數對像被創建。 這甚至可能是一個複雜的操作，它執行一些內省以根據原始功能的實現方式給出不同的結果。 所有這一切意味著裝飾器可以被視為一種元編程工具。
這是個好消息。 裝飾器相對容易捕捉，並且在大多數情況下可以使代碼更短、更易於閱讀並且維護成本更低。 Python 中可用的其他元編程工具更難掌握和掌握。 此外，它們可能根本不會使代碼簡單。


### class decorators 
Python 的一個鮮為人知的語法特性是類裝飾器。 它們的語法和工作方式與第 2 章語法最佳實踐中提到的函數裝飾器完全相同——在類級別下。 
唯一的區別是它們應該返回一個類而不是函數對象。 這是一個示例類裝飾器，它修改 `__repr__()` 方法以返回縮短為任意數量字符的可打印對象表示：
```python
def short_repr(cls):
    cls.__repr__ = lambda self:super(cls,self).__repr__()[:8]
    return cls 
@short_repr
class ClassWithRelativelyLongName:
    pass 

```

### using the `__new__ ()` method to overide instance creation process 

The special method `__new__()` is a static method responsible for creating class instances. 
特殊方法 `__new__()` 是負責創建類實例的靜態方法。
```python
class InstanceCountingClass:
    instances_created = 0 
    def __new__(cls,args,*kwargs):
        print('__new__() called with',cls,args,kwargs)
        instance = super().__new__(cls)
        instance.number = cls.instances_created 
        cls.instances_created +=1 
    def __init__(self,attribute):
        print('__init__ called with',self,attribute)
        self.attribute = attribute

```
`__new__()` 方法通常應該返回特色類的實例，但它它也有可能返回其他類實例。 如果確實發生了（返回不同的類實例），那麼將跳過對` __init__() `方法的調用。 當需要修改非可變類實例（例如某些 Python 的內置類型）的創建行為時，這一事實很有用：

```python
class NonZero(int):
    def __new__(cls,value):
        return super().__new__(cls,value) if value != 0 else None 
    def __init__(self,skipped_value):
        print('__init__() called')
        super().__init__()
```
那麼，什麼時候使用 `__new__()` 呢？ 答案很簡單：僅當 `__init__()` 不夠用時。 已經提到了一個這樣的案例。 這是不可變的內置 Python 類型的子類，例如 int、str、float、frozenset 等。 這是因為一旦創建，就無法在 `__init__()` 方法中修改此類不可變對象實例。

### Metaclassess 元類
Metaclass is a Python feature that is considered by many as one of the most difficult thing in this language and thus avoided by a great number of developers. 
元類是一個 Python 特性，被許多人認為是該語言中最困難的事情之一，因此被大量開發人員避免。

元類是定義其他類型（類）的類型（類）。 為了理解它們是如何工作的，最重要的是要知道定義對象實例的類也是對象。 所以，如果它們是對象，那麼它們就有一個關聯的類。 每個類定義的基本類型就是內置類型類。

#### The general syntax 
對內置 type() 類的調用可以用作 class 語句的動態等效項。 它根據名稱、基類和包含其屬性的映射創建一個新的類對象：
```python
def method(self):
    return 1 
klass = type('MyClass', (object,), {'method': method})
>>> instance = klass()
>>>  instance.method()
1 

# 這種方法和下面的相同
class MyClass:
    def method(self):
        return 1 

```
使用 class 語句創建的每個類都隱式使用 type 作為其元類。 可以通過向類語句提供元類關鍵字參數來更改此默認行為：
```python
class ClassWithAMetaclass(metaclass=type):
    pass
```
作為元類參數提供的值通常是另一個類對象，但它可以是接受與類型類相同的參數並期望返回另一個類對象的任何其他可調用對象。 調用簽名是type(name, bases, namespace)，解釋如下：
- name：這是將存儲在 `__name__` 屬性中的類的名稱 
- bases：這是將成為 `__bases__` 屬性的父類列表，將用於構造新創建的類命名空間的 
- sMRO：這是一個命名空間 （映射）具有將成為 `__dict__` 屬性的類主體的定義
考慮元類的一種方法是 `__new__()` 方法，但在類定義的更高級別。
儘管可以使用顯式調用 type() 的函數來代替元類，但通常的方法是使用從 type 繼承的不同類來實現此目的。 元類的通用模板如下：
> chapter3/metaclass_template.py

#### New python3 syntax for mataclasses 
#### Metaclass usage 
#### Metaclass pitfalls 

### Some tips on code generation
#### exec,eval and compile 
#### Abstract syntax tree 
##### Import hooks
#### Projects using code generation patterns 
##### Falcon's compiled router 
##### Hy 
