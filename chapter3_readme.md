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
#### Mixing super and explict class calls 
#### Heterogeneous arguments 

### Best practices 

## Adavanced attribute access python
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
