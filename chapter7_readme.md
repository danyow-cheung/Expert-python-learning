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
最後，我們談到了 Python 中內存管理的重要話題。 Python 有自己的垃圾收集器，但它只是為了解決引用計數算法中的循環引用問題而設計的。 
引用計數是管理不再需要的對象的釋放的主要方法。


Python/C API 文檔引入了引用的所有權來解釋它如何處理對象的釋放。 Python 中的對象永遠不會被擁有，它們總是被共享。 
對象的實際創建是由 Python 的內存管理器管理的。 它是 CPython 解釋器的組件，負責為存儲在私有堆中的對象分配和釋放內存。 可以擁有的是對該對象的引用。


Python 中由引用（PyObject* 指針）表示的每個對像都有一個關聯的引用計數。 
當它變為零時，意味著沒有人持有對該對象的任何有效引用，並且可以調用與其類型關聯的釋放器。
Python/C API 提供了兩個用於增加和減少引用計數的宏：Py_INCREF() 和 Py_DECREF()。 
但在我們討論它們的細節之前，我們需要了解更多與引用所有權相關的術語：
- Passing of ownership: 
  每當我們說函數通過引用傳遞所有權時，就意味著它已經增加了引用計數，調用者有責任在不再需要對對象的引用時減少計數。 大多數返回新創建對象的函數，例如 Py_BuildValue，都是這樣做的。
- Borrowed references:
  當函數接收到對某個 Python 對象的引用作為參數時，就會發生引用借用。
- Stolen references:
  當作為調用參數提供時，Python/C API 函數也可以竊取引用而不是藉用它。

## Cpython 
Cython 既是一個優化的靜態編譯器，也是一種編程語言的名稱，它是 Python 的超集。

### Cpython as a source to source compiler 
對於使用 Cython 創建的擴展，您將獲得的主要優勢是使用它提供的超集語言。 
無論如何，可以使用源代碼到源代碼編譯從純 Python 代碼創建擴展。 
這是 Cython 最簡單的方法，因為它幾乎不需要更改代碼，並且可以以非常低的開發成本提供一些顯著的性能改進。


Cython 提供了一個簡單的 cythonize 實用程序功能，使您可以輕鬆地將編譯過程與 distutils 或 setuptools 集成。 假設我們想將 fibonacci() 函數的純 Python 實現編譯為 C 擴展。 如果它位於 fibonacci 模塊中，則最小的 setup.py 腳本可能如下所示：
> chapter7/finbonacci_cpython.py

Cython 用作 Python 語言的源代碼編譯工具還有另一個好處。 
源到源編譯到擴展可以是源分發安裝過程中完全可選的部分。 
如果需要安裝包的環境沒有Cython或任何其他構建先決條件，則可以將其作為普通的純Python包安裝。 
用戶不應注意到以這種方式分發的代碼的行為有任何功能差異。


請注意，Cython 文檔說包括生成的 C 文件以及 Cython 源代碼是分發 Cython 擴展的推薦方式。 同一文檔說，默認情況下應禁用 Cython 編譯，因為用戶在其環境中可能沒有所需的 Cython 版本，這可能會導致意外的編譯問題。 無論如何，隨著環境隔離的到來，這在今天似乎是一個不那麼令人擔憂的問題。 此外，Cython 是 PyPI 上可用的有效 Python 包，因此可以輕鬆將其定義為特定版本的項目需求。 當然，包括這樣一個先決條件是一個具有嚴重影響的決定，應該非常仔細地考慮。 更安全的解決方案是利用 setuptools 包中 extras_require 功能的強大功能，並允許用戶決定是否要將 Cython 與特定環境變量一起使用：
> chapter7/cpython.py
### Cpython as a language 
Cython 不僅是一個編譯器，還是 Python 語言的超集。 
超集意味著允許任何有效的 Python 代碼，並且可以使用其他功能進一步更新它，例如支持調用 C 函數或在變量和類屬性上聲明 C 類型。

我們已經知道 Cython 僅編譯源代碼，生成的代碼使用與我們在手動編寫擴展 C 代碼時使用的相同的 Python/C API。 
注意 fibonacci() 是一個遞歸函數，所以它經常調用自己。 
這意味著雖然我們為輸入參數聲明了靜態類型，但在遞歸調用期間它將像對待任何其他 Python 函數一樣對待自己。 
因此 n-1 和 n-2 將被打包回 Python 對象，然後傳遞給內部 fibonacci() 實現的隱藏包裝層，這將再次將其帶回無符號整數類型。
這將一次又一次地發生，直到我們達到遞歸的最終深度。 這不一定是個問題，但涉及比實際需要更多的參數處理。

## Challenges 
它並不像許多人想像的那麼慢，但永遠不會像 C 語言那麼快。
它具有高度可移植性，但它的解釋器並不像其他語言的編譯器那樣在許多體系結構上可用。 我們可以永遠使用該列表。

### Additional complexity
眾所周知，使用多種不同語言開發應用程序並非易事。 
Python 和 C 是完全不同的技術，很難找到它們的共同點。 
確實沒有沒有錯誤的應用程序。 如果擴展在您的代碼庫中變得普遍，調試就會變得很痛苦。 
不僅因為 C 代碼的調試需要完全不同的工作流程和工具，還因為您需要經常在兩種不同的語言之間切換上下文。

### Debugging 
當涉及到失敗時，擴展可能會非常糟糕地中斷。 與 Python 相比，靜態類型具有很多優勢，並且允許您在編譯步驟中發現很多問題，如果沒有嚴格的測試例程和完整的測試覆蓋率，這些問題在 Python 中很難被發現。 另一方面，所有內存管理都必須手動執行。 而錯誤的內存管理是 C 中大多數編程錯誤的主要原因。在最好的情況下，此類錯誤只會導致一些內存洩漏，逐漸吃掉您所有的環境資源。 最好的情況並不意味著好辦。 如果不使用適當的外部工具（如 Valgrind），內存洩漏真的很難找到。 

無論如何，在大多數情況下，擴展代碼中的內存管理問題將導致在 Python 中無法恢復的分段錯誤，並導致解釋器崩潰而不會引發任何異常。 這意味著您最終將需要配備大多數 Python 程序員不需要使用的其他工具。 這會增加您的開發環境和工作流程的複雜性。

## Interfacing with dynamic libraries without extensions 
多虧了 ctypes（標準庫中的一個模塊）或 cffi（一個外部包），您可以在 Python 中集成幾乎所有已編譯的動態/共享庫，無論它是用什麼語言編寫的。 您可以在純 Python 中完成此操作而無需任何編譯步驟，因此這是用 C 語言編寫擴展的一個有趣的替代方法。

這並不意味著您不需要了解有關 C 的任何知識。這兩種解決方案都需要您對 C 以及動態庫的一般工作方式有合理的了解。 另一方面，它們消除了處理 Python 引用計數的負擔，並大大降低了犯痛苦錯誤的風險。 此外，通過 ctypes 或 cffi 與 C 代碼交互比編寫和編譯 C 擴展模塊更可移植。

### ctypes
ctypes 是最流行的模塊，無需編寫自定義 C 擴展即可從動態庫或共享庫調用函數。 
原因很明顯。 它是標準庫的一部分，因此它始終可用並且不需要任何外部依賴項。 它是一個外部函數接口 (FFI) 庫，並提供用於創建 C 兼容數據類型的 API。

### Loading libraries 
ctypes 中有四種類型的動態庫加載器和兩種使用它們的約定。
 表示動態庫和共享庫的類是 ctypes.CDLL、ctypes.PyDLL、ctypes.OleDLL 和 ctypes.WinDLL。 
 最後兩個只能在 Windows 上使用，所以我們不會在這裡討論它們。 CDLL與PyDLL的區別如下：
- ctypes.CDLL:此類表示加載的共享庫。 這些庫中的函數使用標準調用約定，並假定返回 int。 GIL 在調用過程中被釋放。
- ctypes.PyDLL:該類的工作方式類似於CDLL，但調用過程中不釋放GIL。 執行後，將檢查 Python 錯誤標誌，如果設置了則引發異常。 它僅在直接從 Python/C API 調用函數時有用。
要加載庫，您可以使用適當的參數實例化上述類之一，或者從與特定類關聯的子模塊調用 LoadLibrary() 函數：
- ctypes.cdll.LoadLibrary() for ctypes.CDLL 
- ctypes.pydll.LoadLibrary() for ctypes.PyDLL
- ctypes.windll.LoadLibrary() for ctypes.WinDLL
- ctypes.oledll.LoadLibrary() for ctypes.OleDLL 
  
加載共享庫時的主要挑戰是如何以可移植的方式找到它們。 不同的系統對共享庫使用不同的後綴（Windows 為.dll，OS X 為.dylib，Linux 為.so），
在不同的地方搜索。 這方面的主要罪魁禍首是 Windows，它沒有預定義的庫命名方案。
因此，我們不會討論在此系統上使用 ctypes 加載庫的細節，而是主要關注以一致且相似的方式處理此問題的 Linux 和 Mac OS X。

兩種庫加載約定（LoadLibrary() 函數和特定的庫類型類）都要求您使用完整的庫名稱。 這意味著需要包含所有預定義的庫前綴和後綴。 比如在Linux上加載C標準庫，需要這樣寫：
```
import ctypes 
ctypes.cdll.LoadLibrary('libc.so.6')

```
幸運的是，ctypes.util 子模塊提供了一個 find_library() 函數，它允許使用沒有任何前綴或後綴的名稱加載庫，並且可以在任何具有預定義共享庫命名方案的系統上運行：
```
>>> import ctypes
>>> from ctypes.util import find_library
>>> ctypes.cdll.LoadLibrary(find_library('c'))
<CDLL 'usrlib/libc.dylib', handle 7fff69b97c98 at 0x101b73ac8> >>> ctypes.cdll.LoadLibrary(find_library('bz2'))
<CDLL 'usrlib/libbz2.dylib', handle 10042d170 at 0x101b6ee80> >>> ctypes.cdll.LoadLibrary(find_library('AGL'))
<CDLL 'SystemLibrary/Frameworks/AGL.framework/AGL', handle 101811610 at 0x101b73a58>
```
### Calling C function using ctypes 
當庫成功加載後，常見的模式是將其存儲為與庫同名的模塊級變量。 這些函數可以作為對象屬性訪問，因此調用它們就像從任何其他導入模塊調用 Python 函數一樣：
```python
import ctypes
from ctypes.util import find_library
libc = ctypes.cdll.LoadLibrary(find_library('c'))
libc.printf(b'hello world\n')
```

### Passing Python functions as C callbacks 
將函數實現的部分工作委託給用戶提供的自定義回調是一種非常流行的設計模式。 
C 標準庫中接受此類回調的最著名函數是 qsort() 函數，它提供了快速排序算法的通用實現。 
您不太可能希望使用此算法而不是更適合對 Python 集合進行排序的默認 Python Timsort。 
無論如何，qsort() 似乎是高效排序算法和使用回調機制的 C API 的典型示例，可在許多編程書籍中找到。 這
就是為什麼我們將嘗試使用它作為將 Python 函數作為 C 回調傳遞的示例。


我們已經從使用 ctypes 調用 C 函數部分了解到如何使用乘法運算符從其他 ctypes 類型構造 C 數組。 nel 應該是 size_t，並且它映射到 Python int，因此它不需要任何額外的包裝並且可以作為 len(iterable) 傳遞。 一旦我們知道基本數組的類型，就可以使用 ctypes.sizeof() 函數獲得寬度值。 我們需要知道的最後一件事是如何創建指向與 compar 參數兼容的 Python 函數的指針。
ctypes 模塊包含一個 CFUNTYPE() 工廠函數，它允許我們包裝 Python 函數並將它們表示為 C 可調用函數指針。 第一個參數是包裝函數應該返回的 C 返回類型。 它後面是函數接受的 C 類型的變量列表

### CFEI 
CFFI 是 Python 的外部函數接口，是 ctypes 的有趣替代品。 
它不是標準庫的一部分，但可以作為 PyPI 上的 cffi 包輕鬆獲得。 
它與 ctypes 不同，因為它更強調重用純 C 聲明，而不是在單個模塊中提供廣泛的 Python API。 
它要復雜得多，並且還有一個功能，允許您使用 C 編譯器自動將集成層的某些部分編譯為擴展。 
因此它可以用作填補 C 擴展和 ctypes 之間空白的混合解決方案。


因為是一個很大的工程，不可能簡單的幾段介紹。 另一方面，如果不多說一些，那就太可惜了。 我們已經討論了一個使用 ctypes 集成標準庫中的 qsort() 函數的示例。 因此，顯示這兩個解決方案之間主要區別的最佳方法是使用 cffi 重新實現相同的示例。 我希望一段代碼比幾段文字更有價值：
> chapter7/cffi.py