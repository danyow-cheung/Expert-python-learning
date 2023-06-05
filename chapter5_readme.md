## Writing a Package 
專注於編寫和發布 Python 包的可重複過程。 其意圖是：
- 縮短開始實際工作之前設置所有內容所需的時間
- 提供一種標準化的方式來編寫包
- 簡化測試驅動開發方法的使用
- 為了促進發布過程

### Creating a package 
Python 打包一開始可能有點讓人不知所措。 主要原因是對創建 Python 包的正確工具感到困惑。 
不管怎樣，一旦你創建了你的第一個包，你就會發現這並不像看起來那麼難。 此外，了解適當的、最先進的打包工具也有很大幫助。
#### The confusing state of Python packaging tools
很長一段時間以來，Python 打包的狀態非常混亂，花了很多年才組織起來討論這個話題。 一切都始於 1998 年推出的 distutils 包，後來在 2003 年被 setuptools 增強。這兩個項目開始了一個漫長而復雜的故事，包括分支、替代項目和完全重寫，試圖一勞永逸地修復 Python 的打包生態系統。 
不幸的是，這些嘗試中的大多數都沒有成功。 結果恰恰相反。 每個旨在取代 setuptools 或 distutils 的新項目只會加劇圍繞打包工具的巨大混亂。 一些這樣的分支被合併回它們的祖先（比如 distribute 是 setuptools 的一個分支）但有些被遺棄了（比如 distutils2）。


幸運的是，這種狀態正在逐漸改變。 成立了一個名為 Python Packaging Authority (PyPA) 的組織，以恢復打包生態系統的秩序和組織。 Python 打包用戶指南 (https://packaging.python.org) 由 PyPA 維護，是有關最新打包工具和最佳實踐的權威信息來源。 將其視為有關包裝的最佳信息來源和本章的補充閱讀材料。 該指南還包含與打包相關的更改和新項目的詳細歷史記錄，因此如果您已經了解一些但想確保您仍然使用正確的工具，它將很有用。

##### The current landscape of Python packaging thanks to PyPA 
PyPA 除了提供打包的權威指南外，還維護打包項目和打包新官方方面的標準化流程。 
PyPA 的所有項目都可以在 GitHub 上的一個組織下找到：https://github.com/pypa。
其中一些已經在書中提到了。 最值得注意的是：
- pip
- virtualenv
- twine
- warehouse
由於 PyPA 的參與，逐步放棄 egg 格式以支持構建發行版的 wheels 已經在發生。 未來或許會給我們帶來更多清新的氣息。 
PyPA 正在積極致力於倉庫，旨在完全取代當前的 PyPI 實現。 這將是打包歷史上的一大步，
因為 pypi 太老了，而且被忽視了一個項目，只有我們中的少數人可以想像在不完全重寫的情況下逐步改進它。

##### Tool recommendations
Python Packaging User Guide 就使用包的推薦工具提供了一些建議。 它們通常可以分為兩組：用於安裝包的工具和用於包創建和分發的工具。

PyPA 推薦的第一組實用程序已在第 1 章“Python 的現狀”中提到，但為了保持一致性，讓我們在這裡重複它們：
- 使用 pip 從 PyPI 安裝包
- 使用 virtualenv 或 venv 對 Python 環境進行應用級隔離

Python Packaging User Guide 對包創建和分發工具的推薦如下：
- 使用 setuptools 來定義項目和創建源代碼分佈
- 使用 twine 將包分發上傳到 PyPI

#### Project configuration 
很明顯，組織大型應用程序代碼的最簡單方法是將其拆分為多個包。 這使代碼更簡單，更易於理解、維護和更改。 它還最大限度地提高了每個包的可重用性。 它們就像組件一樣。
##### setup.py
必須分發的包的根目錄包含一個 setup.py 腳本。 它定義了 distutils 模塊中描述的所有元數據，並作為參數組合在對標準 setup() 函數的調用中。 儘管 distutils 是一個標準庫模塊，但建議您改用 setuptools 包，它提供了對標準 distutils 的多項增強功能。
因此，該文件的最少內容是：
```python
from setuptools import setup 
setup(
    name = 'mypackage'
)
```
實際的命令列表更長，並且可能因可用的設置工具擴展而異。 它被截斷以僅顯示與本章最重要和最相關的內容。 
標準命令是 distutils 提供的內置命令，而額外命令是由第三方包創建的，例如 setuptools 或任何其他定義和註冊新命令的包。 
另一個包註冊的一個這樣的額外命令是 wheel 包提供的 bdist_wheel。

##### setup.cfg
setup.cfg 文件包含 setup.py 腳本命令的默認選項。 如果構建和分發包的過程更複雜並且需要將許多可選參數傳遞給 setup.py 命令，
這將非常有用。 這允許您在每個項目的基礎上將此類默認參數存儲在代碼中。 這將使您的分發流程獨立於項目，並提供關於您的包是如何構建和分發給用戶和其他團隊成員的透明度。

##### MANIFEST.in
當使用 sdist 命令構建發行版時，distutils 會瀏覽包目錄以查找要包含在存檔中的文件。 distutils 將包括：
- py_modules、packages 和 scripts 選項隱含的所有 Python 源文件
- ext_modules 選項中列出的所有 C 源文件
與 glob 模式 test/test*.py 匹配的文件是：README、README.txt、setup.py 和 setup.cfg。

##### Most important metadata
除了正在分發的包的名稱和版本之外，安裝程序可以接收的最重要的參數是：
- 描述：這包括一些描述包的句子 long_description：這包括可以在 reStructuredText 中的完整描述
- 關鍵字：這是定義包的關鍵字列表作者：這是作者的姓名或組織
- author_email：這是聯繫電子郵件地址
- url：這是項目的URL
- license：這是許可證（GPL、LGPL 等）
- packages：這是包中所有名稱的列表； setuptools 提供了一個叫做 find_packages 的小函數來計算這個 namespace_packages: This is a list of - - - namespaced packages

##### Trove classifiers 
PyPI 和 distutils 提供了一個解決方案，用於使用一組稱為 trove 分類器的分類器對應用程序進行分類。 所有的分類器形成一個樹狀結構。 
每個分類器都是一種字符串形式，其中每個名稱空間都由 :子字符串分隔。 它們的列表作為 setup() 函數的分類器參數提供給包定義。 
以下是 PyPI 上可用的某些項目的分類器示例列表（此處為 solrq）：

在撰寫本書時，PyPI 上有 608 個可用的分類器，分為九大類：
- 開發狀態 
- 環境
- 框架 
- 目標受眾 
- 許可證
- 自然語言
- 操作系統
- 編程語言
- 主題

##### Common patterns
對於沒有經驗的開發人員來說，創建用於分發的包可能是一項乏味的任務。 setuptools 或 distuitls 在其 setup() 函數調用中接受的大部分元數據都可以手動提供，忽略了這可能在項目的其他部分可用的事實：
```python
from setuptools import setup
setup(
    name="myproject",
    version="0.0.1",
    description="mypackage project short description",
    long_description="""
        Longer description of mypackage project
        possibly with some documentation and/or
        usage examples
    """,
    install_requires=[
        'dependency1',
        'dependency2',
        'etc',
] )
```
######  Automated inclusion of version string from package 
PEP 440（版本標識和依賴規範）文檔指定了版本和依賴規範的標準。 這是一份很長的文檔，涵蓋了公認的版本規範方案以及 Python 打包工具中的版本匹配和比較應該如何工作。 
如果您正在使用或計劃使用複雜的項目版本編號方案，則必須閱讀本文檔。 如果你使用的是一個簡單的方案，由一個、兩個、三個或更多數字組成，用點分隔，那麼你可以放棄閱讀 PEP 440。如果你不知道如何選擇合適的版本控制方案，我非常 建議遵循第 1 章“Python 的現狀”中已經提到的語義版本控制。


另一個問題是在何處包含包或模塊的版本說明符。 PEP 396（模塊版本號）正好解決了這個問題。 請注意，它只是信息性的並且具有延遲狀態，因此它是
 
不是標準軌道的一部分。 不管怎樣，它描述的是現在看來是事實上的標準。 根據 PEP 396，如果包或模塊指定了版本，則應將其作為包根 (`__init__.py`) 或模塊文件的 `__version__ `屬性包含在內。 另一個事實上的標準是還包括包含版本部分元組的 VERSION 屬性。 這有助於用戶編寫兼容性代碼，因為如果版本控制方案足夠簡單，則可以輕鬆比較此類版本元組。


######  README file
儘管如此，出於各種原因，許多開發人員仍希望使用不同的標記語言。 最受歡迎的選擇是 Markdown，它是 GitHub 上的默認標記語言——目前大多數開源 Python 開發都在這裡進行。 所以，通常，GitHub 和 Markdown 愛好者要么忽略這個問題，要么提供兩個獨立的文檔文本。 提供給 PyPI 的描述要么是項目 GitHub 頁面上可用內容的簡短版本，要么是在 PyPI 上表現不佳的普通未格式化 Markdown。

######  Managing dependencies
許多項目需要安裝和/或使用一些外部包。 當依賴項列表很長時，就會出現如何管理它的問題。 在大多數情況下，答案非常簡單。 不要過度設計問題。 保持簡單並在 setup.py 腳本中明確提供依賴項列表：
```python
from setuptools import setup 
setup(
    name='some-package',
    install_requires=['falcon', 'requests', 'delorean']
    # ...
)
```
一些 Python 開發人員喜歡使用 requirements.txt 文件來跟踪其包的依賴項列表。 在某些情況下，您可能會找到這樣做的原因，但在大多數情況下，這是該項目的代碼未正確打包的時代遺留問題。 不管怎樣，即使像 Celery 這樣著名的項目仍然堅持這個約定。 所以如果你不願意改變你的習慣，或者你以某種方式被迫使用需求文件，那麼至少要正確地使用它。 這是從 requirements.txt 文件中讀取依賴項列表的一種流行習慣用法：


#### The custom setup command 
#### Working with packages during development 
##### setup.py install 
##### Uninstalling packages 
##### setup.py develop or pip-e 


### Namespace packages 
#### Why is it useful 
#### PEP 420 - implict namespace packages 
#### Namespace packages in previous python versions 

### Uploading a package 
#### PyPI -Python Package Index 
##### Uploading to PyPI - or other package index 
##### .pypirc 
#### Source packages versus built packages 
##### sdist 
##### bdist and wheels 

