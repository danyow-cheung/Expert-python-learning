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

