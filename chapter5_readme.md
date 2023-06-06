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
distutils 允許您創建新命令。 可以使用入口點註冊新命令，這是由 setuptools 引入的一種將包定義為插件的簡單方法。
入口點是指向類或函數的命名鏈接，可通過 setuptools 中的某些 API 獲得。 任何應用程序都可以掃描所有已註冊的包並將鏈接的代碼用作插件。

#### Working with packages during development 
使用 setuptools 主要是關於構建和分發包。 但是，您仍然需要知道如何使用它們直接從項目源安裝包

此外，在同時處理多個相關包時，使用 setuptools 直接從您自己的源進行安裝可能是必不可少的。

##### setup.py install 
安裝包時，除了裸 setup.py 腳本之外，另一種方法是使用 pip。
由於它是 PyPA 推薦的工具，因此即使出於開發目的在本地環境中安裝包時也應該使用它。 
要從本地源安裝包，請運行以下命令：
`pip install <project-patch>`



##### setup.py develop or pip-e 
使用 setup.py install 安裝的包將復製到當前環境的站點包目錄中。 這意味著每當您更改該軟件包的源代碼時，您都需要重新安裝它

這就是為什麼 setuptools 提供了一個額外的開發命令，允許我們在開發模式下安裝包。 
此命令在部署目錄（站點包）中創建一個指向項目源的特殊鏈接，而不是將整個包複製到那裡。 
無需重新安裝即可編輯包源，並且它在 sys.path 中可用，因為它是正常安裝的。


pip 還允許以這種模式安裝包。 此安裝選項稱為可編輯模式，可以在安裝命令中使用 -e 參數啟用：
`pip install -e <project-path>`

### Namespace packages 
這至少可以從兩個方面來理解。 第一個是語言上下文中的名稱空間。 我們都在不知道的情況下使用命名空間：
- 模塊的全局命名空間
- 函數或方法調用的本地命名空間
- 內置名稱的命名空間
另一種名稱空間可以在打包級別提供。 
這些是命名空間包。 這通常是一個被忽視的特性，它對於在您的組織或一個非常大的項目中構建包生態系統非常有用。

#### Why is it useful 
With namespace packages, you can store the source tree for each of these subpackages independently:
使用命名空間包，您可以獨立存儲每個子包的源代碼樹：

#### PEP 420 - implict namespace packages 
PEP 420 (Implicit Namespace Packages)

### Uploading a package 
Python Packaging Index 是 Python 社區開源包的主要來源。 任何人都可以自由上傳新包，唯一的要求是在 PyPI 網站上註冊

#### PyPI -Python Package Index 
the official source of open source package distributions. 

##### Uploading to PyPI - or other package index 
任何人都可以註冊並將包上傳到 PyPI，前提是他或她已經註冊了一個帳戶。 包綁定到用戶，
上傳命令 
`python setup.py <dist-command> upload`
此處，<dist-commands> 是創建要上傳的分發的命令列表。 
只有在同一 setup.py 執行期間創建的分發才會上傳到存儲庫。
因此，如果您要一次上傳源代碼分發、構建分發和 wheel 包，則需要發出以下命令：
`python setup.py sdist bdist bdist_wheel upload`

##### .pypirc 
.pypirc 是一個配置文件，用於存儲有關 Python 包存儲庫的信息。 它應該位於您的主目錄中。 該文件的格式如下：
```
[distutils]
index-servers =
pypi other
[pypi]
repository: <repository-url>
username: <username>
password: <password>
[other]
repository: https://example.com/pypi
username: <username>
password: <password>
```
#### Source packages versus built packages 
源代碼分發是最簡單且最獨立於平台的。 對於純 Python 包，這是一個明智的選擇。 這樣的發行版僅包含 Python 源代碼，並且這些源代碼應該已經具有高度可移植性。
更複雜的情況是當你的包引入了一些擴展，例如，用 C 編寫的。源代碼分發仍然可以工作，前提是包用戶在他/她的環境中有一個合適的開發工具鏈。 這主要由編譯器和適當的 C 頭文件組成。 對於這種情況，構建的分發格式可能更適合，因為它可以為特定平台提供已經構建的擴展。

##### sdist 
sdist 命令是最簡單的可用命令。 它創建了一個發布樹，其中復制了運行包所需的一切。 然後將這棵樹歸檔在一個或多個歸檔文件中（通常，它只創建一個 tarball）。 存檔基本上是源代碼樹的副本。

##### bdist and wheels 

當必須創建一些 C 擴展時，構建過程使用系統
編譯器和 Python 頭文件 (Python.h)。 從源代碼構建 Python 時就可以使用此包含文件。 
對於打包發行版，您的系統發行版可能需要一個額外的包。
至少在流行的 Linux 發行版中，它通常被命名為 python-dev。 它包含構建 Python 擴展所需的所有頭文件。


使用的C編譯器是系統編譯器。 對於基於 Linux 的系統或 Mac OS X，這將分別是 gcc 或 clang。 對於 Windows，可以使用 Microsoft Visual C++（有一個免費的命令行版本可用），也可以使用開源項目 MinGW。 這可以在 distutils 中配置。

bdist 命令使用 build 命令來構建二進制分發版。 它調用構建和所有相關命令，然後以與 sdist 相同的方式創建一個存檔。

### Standalone executables 
在涵蓋 Python 代碼打包的材料中，創建獨立的可執行文件是一個經常被忽視的主題。 這主要是因為 Python 在其標準庫中缺少適當的工具，這些工具可以讓程序員創建簡單的可執行文件，用戶無需安裝 Python 解釋器即可運行。

Python 代碼作為一個包分發時，需要 Python 解釋器才能運行。 這給技術水平不夠的用戶帶來了很大的不便。

#### When are standalone executables useful 
在用戶體驗的簡單性比用戶干擾應用程序代碼的能力更重要的情況下，獨立可執行文件很有用。 請注意，將應用程序分發為可執行文件這一事實只會增加代碼閱讀或修改的難度——並非不可能。 它不是一種保護應用程序代碼的方法，只能用作簡化與應用程序交互的一種方法。

獨立可執行文件通常是以下情況的不錯選擇：
- 依賴特定 Python 版本的應用程序可能不容易在目標操作系統上使用
- 依賴於經過修改的預編譯 CPython 源代碼的應用程序 
- 具有圖形界面的應用程序
- 具有許多用不同語言編寫的二進制擴展的項目 
- 遊戲

#### Popular tools 
- PyInstaller 
- cx Freeze
- py2exe and py2app 

#### Security of Python code in executable packages 
重要的是要知道獨立的可執行文件不會以任何方式使應用程序代碼安全。 從這樣的可執行文件中反編譯出嵌入的代碼不是一件容易的事，但肯定是可以做到的。 更重要的是，這種反編譯的結果（如果使用適當的工具完成）可能看起來與原始來源驚人地相似。

這一事實使得獨立的 Python 可執行文件不是封閉源項目的可行解決方案，因為應用程序代碼的洩漏可能會損害組織。 因此，如果僅通過複製應用程序的源代碼就可以復制整個業務，那麼您應該考慮其他方式來分發應用程序。 也許提供軟件即服務對您來說是更好的選擇。

##### Making decompilation harder 
如前所述，目前還沒有可靠的方法來保護應用程序不被反編譯。 儘管如此，還是有一些方法可以讓這個過程變得更難。 但更難並不意味著可能性更小。 對於我們中的一些人來說，最誘人的挑戰是最艱難的挑戰。 我們都知道，這項挑戰的最終獎品非常高：您試圖保護的代碼。
通常反編譯的過程包括幾個步驟：
1. 從獨立的可執行文件中提取項目的字節碼二進製表示。
2. 將二進製表示映射到特定 Python 版本的字節碼。
3. 將字節碼翻譯成 AST。
4. 直接從 AST 重新創建資源。
5. 
