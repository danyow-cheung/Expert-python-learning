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
#### Real-life example -lazily evaluated attributes 
### Properties 
### Slots 

## Metaprogramming
### Decorators -- a method of metaprogramming 
### class decorators 
### using the __new__ () method to overide instance creation process 

### Metaclassess 

#### The general syntax 
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
