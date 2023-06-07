# Python Extensions in Other Languages
在編寫基於 Python 的應用程序時，您不僅僅局限於 Python 語言。 有諸如 Hy 之類的工具，在第 3 章“語法最佳實踐——類級別之上”中簡要提到過。 它允許您使用將在 Python 虛擬機中運行的其他語言（Lisp 方言）編寫模塊、包甚至整個應用程序。 儘管它使您能夠使用完全不同的語法來表達程序邏輯，但它仍然是完全相同的語言，因為它編譯為相同的字節碼。 這意味著它具有與普通 Python 代碼相同的限制：
- 由於GIL(全局解釋鎖)的存在，線程可用性大大降低
- 它沒有編譯
- 它不提供靜態類型和可能的優化
有助於克服此類核心限制的解決方案是完全用不同語言編寫的擴展，並通過 Python 擴展 API 公開其接口。

## Different language means - C or C++ 
當我們談論不同語言的擴展時，我們幾乎只會想到 C 和 C++。 
即使是像 Cython 或 Pyrex 這樣僅出於擴展目的而提供 Python 語言超集的工具，
實際上也是源到源編譯器，它們從擴展的類 Python 語法生成 C 代碼。

不幸的是，使用裸 Python/C API 僅使用 C 或 C++ 編寫您自己的擴展是非常苛刻的。 不僅因為它需要很好地理解相對難以掌握的兩種語言中的一種，還因為它需要大量的樣板文件。 有很多重複的代碼必須編寫，只是為了提供一個接口，將您實現的邏輯與 Python 及其數據類型粘合在一起。 無論如何，了解如何構建純 C 擴展是件好事，因為：
- 您將更好地理解 Python 的一般工作原理
- 有一天你可能需要調試或維護一個原生的 C/C++ 擴展
- 它有助於理解用於構建擴展的高級工具是如何工作的

### How do extensions in C or C++ work 
如果 Python 解釋器使用 Python/C API 提供適用的接口，則它們能夠從動態/共享庫加載擴展。 
此 API 必須使用隨 Python 源代碼分發的 Python.h C 頭文件併入擴展的源代碼中。 


您需要知道的一件事是，Python/C API 是一項僅限於 CPython 實現的功能。 
已經做出一些努力來為 PyPI、Jython 或 IronPython 等替代實現提供擴展支持，
但目前似乎沒有適合它們的可行解決方案。 
唯一可以輕鬆處理擴展的替代 Python 實現是 Stackless Python，因為它實際上只是 CPython 的修改版本。


Python 的 C 擴展需要編譯成共享/動態庫才能使用，因為顯然沒有直接從源代碼將 C/C++ 代碼導入 Python 的本地方法。
幸運的是，distutils 和 setuptools 提供了幫助程序來將已編譯的擴展定義為模塊，因此
編譯和分發可以使用 setup.py 腳本來處理，就好像它們是普通的 Python 包一樣。 這是來自官方文檔的 setup.py 腳本示例，它處理帶有內置擴展的簡單包的打包：
> chapter7/c_extension.py

## Why you might want to use extensions 

很難說什麼時候用 C/C++ 編寫擴展是一個合理的決定。 一般的經驗法則可能是永遠不會，除非您別無選擇。 但這是一個非常主觀的陳述，為解釋 Python 中無法做到的事情留下了很大的空間。 事實上，很難找到不能使用純 Python 代碼完成的事情，但有些問題擴展可能特別有用：
- 繞過 Python 線程模型中的 GIL（全局解釋器鎖） 提高關鍵代碼段的性能
- 集成第三方動態庫
- 集成用不同語言編寫的源代碼
- 創建自定義數據類型
例如，可以使用不同的並發方法輕鬆克服 GIL 等核心語言約束，例如綠色線程或多處理而不是線程模型。

### Improving performance in critical code sections 
在大多數情況下，解決性能問題實際上只是選擇合適的算法和數據結構，而不是限制語言開銷的常數因子。 
如果代碼已經寫得不好或沒有使用正確的算法，那麼依靠擴展來削減一些 CPU 週期實際上並不是一個好的解決方案。 
通常可以將性能提高到可接受的水平，而無需通過將另一種語言循環到堆棧來增加項目的複雜性。 
如果可能的話，首先應該這樣做。 
無論如何，即使使用最先進的算法方法和最適合我們處理的數據結構，我們也很可能無法單獨使用 Python 來滿足一些任意的技術限制。

### Integrating existing code written in different languages
在計算機科學的短暫歷史中，已經編寫了許多有用的庫。 每次出現一種新的編程語言時都忘記所有這些遺產將是一個巨大的損失，但也不可能可靠地移植任何曾經用任何可用語言編寫的軟件。
C 和 C++ 語言似乎是最重要的語言，它們提供了很多庫和實現，您希望將它們集成到您的應用程序代碼中，而無需將它們完全移植到 Python。 幸運的是，CPython 已經是用 C 編寫的，因此集成此類代碼的最自然方式恰恰是通過自定義擴展。
**CPython yyds**

### Intergrating third-party dynamic libraries 
使用不同技術編寫的代碼的集成不會以 C/C++ 結束。 許多庫，尤其是具有封閉源代碼的第三方軟件，都是作為編譯後的二進製文件分發的。 
在 C 中，加載此類共享/動態庫並調用它們的函數真的很容易。 這意味著您可以使用任何 C 庫，只要您使用 Python/C API 將其包裝成擴展即可。

當然，這不是唯一的解決方案，還有一些工具（例如 ctypes 或 CFFI）允許您使用純 Python 與動態庫交互，而無需在 C 中編寫擴展。
通常，Python/C API 可能仍然是 更好的選擇，因為它在集成層（用 C 語言編寫）和應用程序的其餘部分之間提供了更好的分離。

### Creating custom datatypes 
Python 提供了非常通用的內置數據類型選擇。 其中一些確實使用了最先進的內部實現（至少在 CPython 中），這些實現是專門為 Python 語言量身定制的。 
開箱即用的基本類型和集合的數量對於新手來說可能看起來令人印象深刻，但很明顯它並不能涵蓋我們所有可能的需求。

當然，您可以在 Python 中創建許多自定義數據結構，方法是完全基於某些內置類型或從頭開始將它們構建為全新的類。 
不幸的是，對於某些可能嚴重依賴此類自定義數據結構的應用程序，性能可能還不夠。 複雜集合（如 dict 或 set）的全部功能來自於它們的底層 C 實現。 
為什麼不這樣做並在 C 中實現一些自定義數據結構呢？

## Writing extensions 
正如已經說過的，編寫擴展不是一項簡單的任務，但作為您辛勤工作的回報，它可以給您帶來很多好處。 對於您自己的擴展，最簡單和推薦的方法是使用 Cython 或 Pyrex 等工具，或者簡單地將現有動態庫與 ctypes 或 cffi 集成。 這些項目將提高您的工作效率，並使代碼更易於開發、閱讀和維護。


無論如何，如果您是這個主題的新手，很高興知道您可以通過僅使用裸 C 代碼和 Python/C API 編寫一個擴展來開始您的擴展冒險。
這將提高您對擴展如何工作的理解，也將幫助您了解替代解決方案的優勢。 
為了簡單起見，我們將以一個簡單的算法問題為例，並嘗試使用三種不同的方法來實現它：
- 使用 Cython
- 編寫純 C 擴展
- 使用pyrex 

我們的問題是找到斐波那契數列的第 n 個數。 您不太可能只想為這個問題創建編譯擴展，但它非常簡單，
因此它將作為將任何 C 函數連接到 Python/C API 的一個很好的例子。 
我們唯一的目標是清晰和簡單，因此我們不會嘗試提供最有效的解決方案。 
一旦我們知道了這一點，我們在 Python 中實現的斐波那契函數的參考實現如下所示：
```python
def fibona(n):
    if n<2:
        return 1 
    else:
        return fibona(n-1)+fibona(n-2)
```
請注意，這是 fibonnaci() 函數最簡單的實現之一，可以對其進行大量改進。 我們拒絕改進我們的實現（例如，使用記憶模式），因為這不是我們示例的目的。 以同樣的方式，我們不會在稍後討論 C 或 Cython 中的實現時優化我們的代碼，即使編譯後的代碼提供了更多的可能性來這樣做。

### Pure C extensions 
如前所述，我們將嘗試將 fibonacci() 函數移植到 C 並將其作為擴展公開給 Python 代碼。 與前面的 Python 示例類似的沒有連接到 Python/C API 的裸實現大致如下：s
```C 
long long fibonacci(unsigned int n){
    if (n<2){
        return 1;
    }else{
        return fibonacci(n-1)+fibonacci(n-2);
    }
}
```
下面是一個完整的、功能齊全的擴展示例，它在已編譯的模塊中公開了這個單一功能：
> chapter7/fibonacci.c,chapter7/fibonacci.py
擴展的構建過程可以使用 Python 的 setup.py build 命令初始化，但也會在包安裝時自動執行。 以下記錄顯示了開發模式下的安裝結果和一個簡單的交互式會話，其中檢查並執行了我們編譯的 fibonacci() 函數：
```

$ ls -1a
fibonacci.c
setup.py

$ pip install -e .
Obtaining file:///Users/swistakm/dev/book/chapter7
Installing collected packages: fibonacci
  Running setup.py develop for fibonacci
Successfully installed Fibonacci

$ ls -1ap
build/
fibonacci.c
fibonacci.cpython-35m-darwin.so
fibonacci.egg-info/
setup.py

$ python
Python 3.5.1 (v3.5.1:37a07cee5969, Dec  5 2015, 21:12:44)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more
information.
>>> import fibonacci
>>> help(fibonacci.fibonacci)
Help on built-in function fibonacci in fibonacci:
fibonacci.fibonacci = fibonacci(...)
    fibonacci(n): Return nth Fibonacci sequence number computed
recursively
>>> [fibonacci.fibonacci(n) for n in range(10)]
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
>>>

```
### A closer look at Python/C API 
由於我們知道如何正確打包、編譯和安裝自定義 C 擴展，並且我們確信它會按預期工作，現在是時候詳細討論我們的代碼了。
擴展模塊以包含 Python.h 頭文件的單個 C 預處理器指令開始：
`#include <Python.h>`


### Calling and binding conventions 
如仔細查看 Python/C API 部分中所述，PyMethodDef 結構的 ml_flags 位域包含用於調用和綁定約定的標誌。
**調用約定標誌是：**
- METH_VARARGS
這是 Python 函數或方法的典型約定，它只接受參數作為其參數。 作為此類函數的 ml_meth 字段提供的類型應該是 PyCFunction。 
該函數將提供兩個 PyObject* 類型的參數。 第一個是自身對象（用於方法）或模塊對象（用於模塊函數）。 
具有該調用約定的 C 函數的典型簽名是 PyObject* function(PyObject* self, PyObject* args)。

- METH_KEYWORDS
這是在調用時接受關鍵字參數的 Python 函數的約定。 
其關聯的 C 類型是 PyCFunctionWithKeywords。
C 函數必須接受 PyObject* 類型的三個參數：self、args 和關鍵字參數字典。 
如果與 METH_VARARGS 組合，前兩個參數與前面的調用約定具有相同的含義，
否則 args 將為 NULL。ThetypicalCfunctionsignature 是：PyObject* function(PyObject* self, PyObject* args, PyObject* keywds)。

- METH_NOARGS
這是不接受任何其他參數的 Python 函數的約定。 C 函數應該是 PyCFunction 類型，因此簽名與 METH_VARARGS 約定的簽名相同（兩個 self 和 args 參數）。 唯一的區別是 args 將始終為 NULL，因此無需調用 PyArg_ParseTuple()。 這不能與任何其他調用約定標誌結合使用。

- METH_O
這是接受單個對象參數的函數和方法的簡寫。 C 函數的類型也是 PyCFunction，因此它接受兩個 PyObject* 參數：self 和 args。 它與 METH_VARARGS 的不同之處在於不需要調用 PyArg_ParseTuple()，因為作為 args 提供的 PyObject* 已經表示在對該函數的 Python 調用中提供的單個參數。 這也不能與任何其他調用約定標誌結合使用。

### Exception handling 
C，不像 Python，甚至 C++ 都沒有引發和捕獲異常的語法。 所有錯誤處理通常使用函數返回值和可選的全局狀態來處理，用於存儲可以解釋上次失敗原因的詳細信息。

Python/C API 中的異常處理就是圍繞這個簡單的原則構建的。 每個線程都有一個全局指示器，指示 C API 中發生和運行的最後一個錯誤。 
它被設置為描述問題的原因。 如果此狀態已更改，還有一種標準化的方式來通知函數的調用者,如果在通話期間更改了此狀態：
 
- 如果函數應該返回一個指針，它返回 NULL
- 如果函數應該返回一個 int 類型，它返回 -1
  
以某種方式參與我們的錯誤處理的行被突出顯示。 它從最開始的結果變量的初始化開始，該變量應該存儲我們函數的返回值。 它用 NULL 初始化，正如我們已經知道的那樣，它是錯誤的指示器。 這就是您通常編寫擴展代碼的方式，假設錯誤是代碼的默認狀態。

### Release GIL 
因為擴展主要用於大部分工作在純 C 中執行而無需調用 Python/C API 的情況，所以在某些應用程序部分中釋放 GIL 是可能的（甚至是可取的）。 
多虧了這一點，您仍然可以從擁有多個 CPU 內核和多線程應用程序設計中獲益。 
您唯一需要做的就是用 Python/C API 提供的特定宏包裝已知不使用任何 Python/C API 調用或 Python 結構的代碼塊。 
提供這兩個預處理器宏是為了簡化釋放和重新獲取全局解釋器鎖的整個過程：
- Py_BEGIN_ALLOW_THREADS
  這聲明了保存當前線程狀態的隱藏局部變量，並釋放了 GIL
- Py_END_ALLOW_THREADS 
  這將重新獲取 GIL 並從使用前一個宏聲明的局部變量恢復線程狀態
  

### Reference counting 

## Cpython 

### Cpython as a source to source compiler 

### Cpython as a language 

## Challenges 

### Additional complexity

### Debugging 

## Interfacing with dynamic libraries without extensions 

### ctypes

### Loading libraries 

### Calling C function using ctypes 

### Passing Python functions as C callbacks 

### CFEI 
