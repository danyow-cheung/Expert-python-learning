# Expert Python Programming,Second Edition

> ref:https://github.com/PacktPublishing/Expert-Python-Programming_Second-Edition

## Current Status of Python
### Getting up to date with change 
PEP document -- Python Enhancement Proposal 

### Stackless Python 
Stackless Python 將自己宣傳為 Python 的增強版本。 Stackless 之所以這樣命名，是因為它避免了依賴於 C 調用堆棧來獲取自己的堆棧。
它實際上是修改後的 CPython 代碼，還添加了一些在創建 Stackless 時核心 Python 實現中缺少的新功能。 
其中最重要的是由解釋器管理的微線程，作為必須依賴於系統內核上下文切換和任務調度的普通線程的廉價和輕量級替代方案。


### IronPython 
IronPython 將 Python 引入 .NET 框架。 該項目得到了 Microsoft 的支持，IronPython 的主要開發人員在那里工作。 對於語言的推廣來說是一個相當重要的實現


### Virtual development environments using Vagrant使用 Vagrant 的虛擬開發環境
Vagrant 提供了一種簡單方便的方式來創建和管理開發環境。它沒有任何額外的依賴關係。 Vagrant 以虛擬機或容器的形式創建新的開發環境。

最重要的配置在一個名為 Vagrantfile 的文件中提供給 Vagrant。 它應該獨立於每個項目。 以下是它提供的最重要的東西：
- 虛擬化提供商的選擇
- Box用作虛擬機鏡像
- 配置方法的選擇
- 虛擬機和虛擬機主機之間的共享存儲
- 需要在 VM 和它的主機之間轉發的端口
- 
Vagrantfile 的語法語言是 Ruby。 示例配置文件提供了一個很好的啟動項目的模板，並且有很好的文檔，所以不需要這種語言的知識。 可以使用單個命令創建模板配置：
`vagrant init`
這將在當前工作目錄中創建一個名為 Vagrantfile 的新文件。 存放此文件的最佳位置通常是相關項目源碼的根目錄。 該文件已經是一個有效的配置，它將使用默認提供程序和基本盒映像創建一個新的 VM。 默認情況下不啟用配置。 添加 Vagrantfile 後，新虛擬機開始使用：
`vagrant up`
Once the new Vagrant environment is up and running, developers can connect to SSH using this shorthand:
`vagrant ssh`

### Interactive debuggers
代碼調試是軟件開發過程中不可或缺的一部分。 許多程序員一生的大部分時間都只使用大量的日誌記錄和打印語句作為他們的主要調試工具，但大多數專業開發人員更喜歡依賴某種調試器。

Python 已經附帶了一個名為 pdb 的內置交互式調試器（請參閱 https://docs.python.org/3/library/pdb.html）。 可以在已有的腳本上通過命令行調用，所以如果程序異常退出，Python會進入事後調試：
```
python -m pdb script.py
```
事後調試雖然有用，但並不涵蓋所有場景。 它只有在應用程序存在但出現錯誤時才有用。 在許多情況下，有問題的代碼只是表現異常，而不會意外退出。 在這種情況下，可以使用此單行習慣用法在特定代碼行上設置自定義斷點：
```
import pdb 
pdf.set_trace()
```

## Syntax Best Practices -- below the Class Level
除了為您的程序實現的算法和架構設計之外，非常注意它的編寫方式對它的發展方式也有很大的影響。 許多程序由於語法晦澀、API 不清晰或標準不合常規而被淘汰並從頭開始重寫。

### Implementation details 

##### List comprehensions 

不要再写这种

```python
evens = []
for i in range(10):
  if i%2==0:
    evens.append(i)
```

改写成

```
[i for i in rage(10) if i%2==0]
```

除了這種寫作更有效率之外，它更短並且涉及的元素更少。 在更大的程序中，這意味著更少的錯誤和更易於閱讀和理解的代碼。



### Adavanced syntax

- Iterators 
- Generators
- Decorators 
- Context managers 



#### Iterators

迭代器可以由内置函数构成

```python
i = iter('abc')
print(next(i)) # a
print(next(i)) # b
print(next(i)) # c
```

再跑一次的話就會報錯，但是可以自己寫一個custom 迭代器

```python
class CountDown:
  def __init__(self,step):
    self.step = step
  def __next__(self):
    if self.step <=0:
      raise StopIteration
    self.step -=1 
    return self.step 
  def __iter__(self):
    return self 
  
# 示範例子
for element in CountDown(4):
  print(element)

```

#### The yield statement 
生成器提供了一種優雅的方式來為返回元素序列的函數編寫簡單而高效的代碼。 
基於 yield 語句，它們允許您暫停函數並返回中間結果。 
該函數保存其執行上下文，如有必要，可以稍後恢復。
```python
def fibonacci():
  a,b = 0,1 
  while True:
    yield b 
    a,b = b,a+b
fib = fibonacci()
next(fib)
next(fib)
[next(fb) for i in range(10)]
```
在那種情況下，用於計算一個元素的資源在大多數情況下不如用於整個過程的資源重要。
因此，它們可以保持較低，使程序更高效。 
例如，斐波那契數列是無限的，但生成它的生成器不需要無限量的內存來一次提供一個值。
一個常見的用例是使用生成器流式傳輸數據緩衝區。 它們可以由播放數據的第三方代碼暫停、
恢復和停止，並且在開始該過程之前不需要加載所有數據。

例如，標準庫中的 tokenize 模塊從文本流中生成標記，並為每個經過處理的行返回一個迭代器，該迭代器可以傳遞給某些處
理：

#### Decorators 
在 Python 中添加了裝飾器，以使函數和方法包裝（接收函數並返回增強函數的函數）更易於閱讀和理解。 最初的用例是能夠將方法定義為類方法或定義頭部的靜態方法。 如果沒有裝飾器語法，它將需要一個相當稀疏和重複的定義：
```python
class WithoutDecorators:
  def some_static_method():
    print('This is static method')
  some_static_method = staticmethod(some_static_method)
  def some_class_method(cls):
    print('this is class method')
  some_class_method = classmethod(some_class_method)

```
如果為了同樣的目的使用裝飾器語法，代碼會更短更容易理解：
```python
class WithDecorators:
  @staticmethod
  def some_static_method():
    print('this is static method')
  
  @staticmethod
  def some_class_method(cls):
    print('this is class method') 
```
#####  一般語法和可能的實現
裝飾器通常是一個命名對象（不允許使用 lambda 表達式），它在調用時接受單個參數（它將是裝飾函數）並返回另一個可調用對象。 這裡用“Callable”代替“function”是有預謀的。 雖然裝飾器通常在方法和函數的範圍內進行討論，但並不限於它們。 事實上，任何可調用的東西（任何實現 __call__ 方法的對像都被認為是可調用的）都可以用作裝飾器，並且它們返回的對象通常不是簡單的函數，而是實現自己的 __call__ 方法的更複雜類的更多實例。

事實上，任何函數都可以用作裝飾器，因為 Python 不強制裝飾器的返回類型。 因此，使用某個函數作為接受單個參數但不返回可調用函數的裝飾器，比方說 str，在語法方面是完全有效的。 如果用戶試圖調用以這種方式裝飾的對象，這最終會失敗。 無論如何，這部分裝飾器語法為一些有趣的實驗創造了一個領域。
###### Decorator does not even need to return a callable!
裝飾器甚至不需要返回可調用對象！

###### As a function
編寫自定義裝飾器的方法有很多種，但最簡單的方法是編寫一個返回包裝原始函數調用的子函數的函數。
通用模式如下：
```python
def mydecorator(function):
  # do something
  result = func(args,**kwargs)
  return result 
return wrapped
```
###### As a class 
```python
class DecoratorAsClass:
  def __init__(self,func):
    self.func = func 
  def __call__(self,args,*kwargs):
    result = self.func(args,*kwargs)
    return result 
```
###### Parametrizing decorators
參數化裝飾器
在實際代碼中，經常需要使用可以參數化的裝飾器。 當函數用作裝飾器時，
解決方案很簡單——必須使用第二層包裝。 下面是裝飾器的一個簡單示例，它在每次調用時重複執行裝飾函數指定的次數：
```python
def repeat(number=3):
  def actual_decorator(func):
    def wrapper(args,*kwargs):
      result = None 
      for _ in range(number):
        result = func(args,*kwargs)
      return result 
    return wrapper 
  return actual_decorator

@repeat(2)
def foo():
  print(1)
foo()
>>> foo
>>> foo
```
###### Introspection preserving decorators
自省保護裝飾器

使用裝飾器的常見缺陷是在使用裝飾器時不保留函數元數據（主要是文檔字符串和原始名稱）。 前面的例子都有這個問題。 他們通過組合創建了一個新函數並返回了一個新對象，而不考慮原始對象的身份。 這使得以這種方式裝飾的函數的調試更加困難，並且還會破壞大多數可能使用的自動文檔工具，因為原始文檔字符串和函數簽名不再可訪問。
但是讓我們詳細看看這個。 假設我們有一些虛擬裝飾器，它只做裝飾和用它裝飾的其他一些功能：

簡單來說就是，寫成這樣，就可以不丟掉元數據
```python
from functools import wraps 
def preserving_decorator(func):
  @wraps(function)
  def wrapped(args,*kwargs):
    '''Internal wrapped function documentation'''
    return function(args,*kwargs)
  return wrapped 
@preserving_decorator()
def function_with_important_docstring():
  '''This is import docstring we do not want to loss '''
print(function_with_important_docstring.__name__)
print(function_with_important_docstring.__doc__)

```


#####  Usage and useful examples用法和有用的例子
由於裝飾器是在首次讀取模塊時由解釋器加載的，因此它們的使用應僅限於可以普遍應用的包裝器。 如果裝飾器綁定到方法的類或它增強的函數的簽名，則應將其重構為常規可調用對像以避免複雜性。 無論如何，當裝飾器處理 API 時，一個好的做法是將它們分組到一個易於維護的模塊中。
裝飾器的常見模式是：
- 參數檢查
- 緩存
- 代理人
- 上下文提供
  
###### Caching 緩存
緩存裝飾器與參數檢查非常相似，但側重於那些內部狀態不影響輸出的函數。 每組參數都可以鏈接到一個唯一的結果。 這種編程風格是函數式編程的特點（參考http://en.wikipedia.org/wiki/Functional_programming），可以在輸入值集合有限的情況下使用。
因此，緩存裝飾器可以將輸出與計算它所需的參數保存在一起，並在後續調用中直接返回。 這種行為稱為記憶化（請參閱 http://en.wikipedia.org/wiki/Memoizing）並且作為裝飾器實現起來非常簡單：
> caching_decorator.py

緩存昂貴的函數可以顯著提高程序的整體性能，但必須謹慎使用。 
緩存值也可以綁定到函數本身以管理其範圍和生命週期，而不是集中式字典。 
但無論如何，更高效的裝飾器將使用基於高級緩存算法的專用緩存庫。

###### Proxy 代理 
代理裝飾器用於使用全局機制標記和註冊函數。
例如，根據當前用戶保護代碼訪問的安全層可以使用具有可調用對象所需的關聯權限的集中式檢查器來實現：
> proxy_decorator.py

###### Context provider 上下文裝飾
上下文裝飾器確保函數可以在正確的上下文中運行，或者在函數前後運行一些代碼。 換句話說，它設置和取消設置特定的執行環境。 例如，當一個數據項必須在多個線程之間共享時，必須使用鎖來確保它免受多次訪問。 這個鎖可以在裝飾器中編碼如下：
> context_provider_decorator.py 


#### Context managers -- the with statement 上下文管理器——with 語句

try...finally 語句可用於確保即使出現錯誤也能運行一些清理代碼。 這有很多用例，例如：
- Closing a file 關閉文件
- Releasing a lock 釋放鎖
- Making a temporary code patch 製作臨時代碼補丁
- Running protected code in a special environment 在特殊環境中運行受保護的代碼

with 語句通過提供一種包裝代碼塊的簡單方法來排除這些用例。 這允許您在塊執行之前和之後調用一些代碼，即使此塊引發異常也是如此。 例如，使用文件通常是這樣完成的：
```python 
hosts = open('demo.txt')
'''Method 1'''
try:
  for line in hosts:
    if line.startswith('#'):
      continue 
    print(line.strip())
  finally:
    hosts.close()
'''Method 2'''
with open('demo.txt') as hosts:
  for line in hosts:
    if line.startswith('#'):
      continue 
    print(line.strip)
```

##### General syntax and possible implementation 一般語法和可能的實施
`with`語句的用法有
1. 
```python
with context_manager:
  #block of code 
```
2. 
```python
with context_manager as context:
  # block of code
```
3. 
```python
with A() as a ,B() as b:
  ...
```
4. 
```python
with A() as a:
  with B() as b:
    ...
```
###### As a class 
任何實現上下文管理器協議的對像都可以用作上下文管理器。 該協議由兩個特殊方法組成：
- __enter__(self)
- __exit__(self,exc_type,exc_value,trackback)

簡而言之，with 語句的執行過程如下：
1. __enter__ 方法被調用。 任何返回值都綁定到指定的 as 子句。
2. 執行內部代碼塊。
3.調用 __exit__ 方法。

__exit__ 接收三個參數，當代碼塊內發生錯誤時將填充這些參數。 如果沒有錯誤發生，所有三個參數都設置為 None。 發生錯誤時， __exit__ 不應重新引發它，因為這是調用者的責任。 但是，它可以通過返回 True 來防止引發異常。 提供它是為了實現一些特定的用例，例如我們將在下一節中看到的 contextmanager 裝飾器。 但是對於大多數用例，此方法的正確行為是進行一些清理，就像 finally 子句所做的一樣； 無論塊中發生什麼，它都不會返回任何內容。
以下是一些實現此協議的上下文管理器的示例，以更好地說明其工作原理：
> context_manger_class.py
###### As a method --the contextlib module 
使用類似乎是實現 Python 語言中提供的任何協議的最靈活方式，但對於許多用例來說，樣板文件可能太多了。 contextlib 模塊已添加到標準庫中，以提供幫助器以與上下文管理器一起使用。 其中最有用的部分是 contextmanager 裝飾器。 它允許您在單個函數中提供 __enter__ 和 __exit__ 部分，由 yield 語句分隔（請注意，這使該函數成為生成器）。 前面用這個裝飾器編寫的例子看起來像下面的代碼：
> context_manger_method.py


### Other syntax elements you may not know yet 您可能還不知道的其他語法元素
#### Function annotations 
函數註解是Python 3最獨特的特性之一，官方文檔說註解是完全可選的關於用戶自定義函數使用的類型的元數據信息，
但實際上並不局限於類型提示，
還有 Python 及其標準庫中沒有任何一項功能利用了此類註釋。 這就是為什麼這個特性是獨一無二的——它沒有任何句法意義。 註釋可以簡單地為函數定義，並且可以在運行時檢索，但僅此而已。 如何處理它們留給開發人員。
##### The general syntax 
Python 文檔中的一個稍微修改過的示例最好地展示瞭如何定義和檢索函數註釋：
```python
def fun(ham:str,eggs:str='eggs')->str:
  pass 
print(fun.__annotations__)

```
如前所述，參數註釋由評估註釋值的表達式定義，表達式前面有一個冒號。 
返回註釋由表示 def 語句結尾的冒號和參數列表後面的文字 -> 之間的表達式定義。
定義後，註釋在函數對象的 __annotations__ 屬性中作為字典可用，並且可以在應用程序運行時檢索。
任何表達式都可以用作註釋並且它位於默認參數附近的事實允許創建一些令人困惑的函數定義，如下所示：
```python
def square(number : 0<=3 and 1=0) -> (+9000):
  return number **2 

square(10)
```
##### The possible uses 
表示此功能的目的是“鼓勵通過元類、裝飾器或框架進行實驗”。 另一方面，正式提出函數註釋的 PEP 3107 列出了以下一組可能的用例：
- 提供類型信息
  - 類型檢查
  - 讓 IDE 顯示函數期望和返回的類型 
  - 函數重載/通用函數 
  - 外語橋
  - 適應
  - 謂詞邏輯函數 
  - 數據庫查詢映射 
  - RPC 參數編組
- 其他信息
  - 參數和返回值的文檔

