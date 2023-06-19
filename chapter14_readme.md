# Useful Design Patterns
設計模式是針對軟件設計中常見問題的可重用的、某種程度上特定於語言的解決方案。 關於此主題的最受歡迎的書籍是設計模式：可重用面向對象軟件的元素，Addison-Wesley Professional，由 Gamma、Helm、Johnson 和 Vlissides 編寫，也稱為四人幫或 GoF。 它被認為是該領域的主要著作，提供了 23 種設計模式的目錄以及 SmallTalk 和 C++ 中的示例。

在設計應用程序代碼時，這些模式有助於解決常見問題。 他們向所有開發人員敲響了警鐘，因為他們描述了經過驗證的開發範例。 但是應該考慮使用的語言來研究它們，因為其中一些在某些語言中沒有意義或者已經內置。
本章描述了 Python 中最有用的模式或討論起來很有趣的模式，並附有實現示例。 以下是與 GoF 定義的設計模式類別對應的三個部分：
- 創建模式：這些模式用於生成具有特定行為的對象
- 結構模式：這些模式有助於為特定用例構建代碼
- 行為模式：這些模式有助於分配責任和封裝行為

## Creational patterns
創建模式處理對象實例化機制。 這樣的模式可能定義了一種關於如何創建對象實例甚至如何構造類的方法。
這些是 C 或 C++ 等編譯語言中非常重要的模式，因為在運行時按需生成類型比較困難。
但是在運行時創建新類型在 Python 中非常簡單。 內置類型函數允許您通過代碼定義一個新的類型對象：

類和類型是內置工廠。 我們已經處理了新類對象的創建，您可以使用元類與類和對像生成進行交互。 這些特性是實現工廠設計模式的基礎，但我們不會在本節中進一步描述它，因為我們在第 3 章“語法最佳實踐——類級以上”中廣泛討論了類和對象創建的主題。

除了工廠之外，GoF 中唯一有趣的用 Python 描述的其他創造性設計模式是單例。

### Singleton
單例將類的實例化限制為僅單個對象實例。
單例模式確保給定的類在應用程序中始終只有一個活動實例。 例如，當您希望將資源訪問限制為進程中的一個且僅一個內存上下文時，可以使用它。 例如，數據庫連接器類可以是處理同步並在內存中管理其數據的單例。 它假設在此期間沒有其他實例與數據庫交互。
```python
class Singleton:
    instance = None 
    def __new__(cls,args,*kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls,args,*kwargs)
        return cls._instance
```
儘管如此，單例不應該有多個繼承級別。 標記為單例的類已經是特定的。

也就是說，許多開發人員認為這種模式是處理應用程序中唯一性的一種繁重方式。 如果需要單例，為什麼不使用帶有函數的模塊來代替，因為 Python 模塊已經是單例了？ 最常見的模式是將模塊級變量定義為需要單例的類的實例。 這樣，您也不會將開發人員限制在您的初始設計中。

## Structural patterns
結構模式在大型應用程序中非常重要。 他們決定代碼的組織方式，並為開發人員提供有關如何與應用程序的每個部分進行交互的方法。
長期以來，Python 世界中最著名的許多結構模式的實現為 Zope 項目提供了 Zope 組件架構 (ZCA)。 它實現了本節中描述的大部分模式，並提供了一組豐富的工具來處理它們。 ZCA 旨在不僅在 Zope 框架中運行，而且還可以在其他框架（如 Twisted）中運行。 它提供了接口和適配器等的實現。

Python 已經通過其語法提供了一些流行的結構模式。 例如，類和函數裝飾器可以被認為是裝飾器模式的一種風格。 此外，對創建和導入模塊的支持是模塊模式的一種體現。
常見結構模式的列表實際上很長。 最初的《設計模式》一書中有多達七種，後來其他文獻擴展了這個列表。 我們不會討論所有這些，而只會關註三個最受歡迎和公認的，它們是：
- Adapter
- Proxy
- Facade 

### Adapter
適配器模式允許從另一個接口使用現有類的接口。 換句話說，適配器包裝類或對象 A，以便它在用於類或對象 B 的上下文中工作。
由於這種語言的輸入方式，在 Python 中創建適配器實際上非常簡單。 Python 中的類型哲學通常被稱為 duck-typing：

根據這條規則，如果一個函數或方法的值被接受，決定不應該基於它的類型，而是基於它的接口。 因此，只要對象的行為符合預期，即具有正確的方法簽名和屬性，它的類型就被認為是兼容的。 這與許多靜態類型語言完全不同，在這些語言中這種東西很少可用。
實際上，當一些代碼打算與給定的類一起工作時，只要它們提供代碼使用的方法和屬性，就可以用另一個類的對象來提供給它。 當然，這假設代碼沒有調用實例來驗證實例是否屬於特定類。
適配器模式基於此理念並定義了一種包裝機制，其中包裝類或對像以使其在並非主要用於它的上下文中工作。 StringIO 是一個典型的例子，因為它適配了 str 類型，所以它可以用作文件類型：
> chapter14/DublinCoreAdapter.py

除了允許替換這一事實之外，適配器模式還可以改變開發人員的工作方式。 使一個對像在特定的上下文中工作是假設對象的類根本不重要。 重要的是此類實現 DublinCoreInfo 正在等待的內容，並且此行為由適配器修復或完成。 因此，代碼可以以某種方式簡單地判斷它是否與實現特定行為的對象兼容。 這可以通過接口來表達。

#### Interfacs
接口是 API 的定義。 它描述了一個類必須以所需行為實現的方法和屬性列表。 這個描述沒有實現任何代碼，只是為任何希望實現接口的類定義了一個明確的契約。 然後任何類都可以以任何它想要的方式實現一個或多個接口。

雖然 Python 更喜歡 duck-typing 而不是顯式接口定義，但有時使用它們可能會更好。 例如，顯式接口定義使框架更容易通過接口定義功能。
好處是類是鬆散耦合的，這被認為是一種很好的做法。 例如，要執行給定的過程，A 類不依賴於 B 類，而是依賴於接口 I。B 類實現 I，但它可以是任何其他類。
許多靜態類型語言（例如 Java 或 Go）都內置了對這種技術的支持。 接口允許函數或方法限制實現給定接口的可接受參數對象的範圍，無論它來自哪種類。 這比將參數限制為給定類型或其子類具有更大的靈活性。 它就像鴨子類型行為的顯式版本：Java 在編譯時使用接口來驗證類型安全，而不是在運行時使用鴨子類型將事物聯繫在一起。

##### Using zope.interface
有一些框架允許您在 Python 中構建顯式接口。 最著名的是 Zope 項目的一部分。 它是 zope.interface 包。 儘管現在 Zope 不像以前那樣流行，但 zope.interface 包仍然是 Twisted 框架的主要組件之一。
zope.interface 包的核心類是 Interface 類。 它允許您通過子類化顯式定義新接口。 假設我們要為矩形的每個實現定義強制接口：
```python
from zope.interface import Interface,Attrbute
class IRectangle(Interface):
    width = Attribute("The width of rectangle")
    height = Attribute("The height of rectangle")
    def area():
        pass 
        # return area of rectangle 
    def perimeter():
        pass 
        # return perimeter of rectangle

```
當您定義了這樣的契約後，您就可以定義新的具體類，為我們的 IRectangle 接口提供實現。 為此，您需要使用 implementer() 類裝飾器並實現所有已定義的方法和屬性：
```python
@implementer(IRectangle)
class Square:
    """ Concrete implementation of square with rectangle interface
    """
    def __init__(self, size):
        self.size = size
    @property
    def width(self):
        return self.size
    @property
    def height(self):
        return self.size
    def area(self):
        return self.size ** 2
def perimeter(self): return 4 self.size
@implementer(IRectangle)
class Rectangle:
    """ Concrete implementation of rectangle
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def area(self):
        return self.width self.height
    def perimeter(self):
        return self.width 2 + self.height 2
```
通常說接口定義了具體實現需要履行的契約。 這種設計模式的主要好處是能夠在使用對象之前驗證契約和實現之間的一致性。 使用普通的鴨子類型方法，您只會在運行時缺少屬性或方法時發現不一致。 使用 zope.interface，您可以使用 zope.interface.verify 模塊中的兩種方法來反省實際實現，以儘早發現不一致之處：

如果您需要驗證來自內置庫的外部類的實例，這尤其麻煩。 zope.interface 為該問題提供了一些解決方案，您當然可以通過使用適配器模式甚至猴子修補自行處理此類問題。 無論如何，此類解決方案的簡單性至少值得商榷。

##### Using function annotations and abstract base classes 
設計模式旨在使問題解決更容易，而不是為您提供更多層次的複雜性。 zope.interface 是一個很棒的概念，可能非常適合某些項目，但它不是靈丹妙藥。 通過使用它，您可能很快就會發現自己花更多的時間來解決第三方類不兼容接口的問題，並提供永無止境的適配器層，而不是編寫實際的實現。 如果您有這種感覺，那麼這表明出現了問題。 幸運的是，Python 支持構建接口的輕量級替代方案。 它不像 zope.interface 或其替代方案那樣是成熟的解決方案，但它通常提供更靈活的應用程序。 您可能需要編寫更多的代碼，但最終您將擁有更可擴展、更好地處理外部類型並且可能更適合未來的東西。


請注意，Python 在其核心中沒有明確的接口概念，而且可能永遠不會有，但具有一些允許您構建類似於接口功能的東西的特性。 特點是：
- 抽象基類 (ABC) 
- 函數註解
- 類型註解
我們解決方案的核心是抽象基類，因此我們將首先介紹它們。
正如您可能知道的那樣，直接類型比較被認為是有害的而不是
蟒蛇。 您應該始終避免如下比較：assert type(instance) == list
以這種方式比較函數或方法中的類型完全破壞了將類子類型作為參數傳遞給函數的能力。 稍微好一點的方法是使用將繼承考慮在內的 isinstance() 函數：
`assert isinstance (instance,list)`
isinstance() 的另一個優點是您可以使用更大範圍的類型來檢查類型兼容性。 例如，如果您的函數希望接收某種序列作為參數，您可以與基本類型列表進行比較：
`assert isinstance (instance,(list,tuple,range))`

我們的 ensure_interface() 示例實現基於 typeannotations 項目中的 typechecked() 裝飾器，該項目試圖提供運行時檢查功能（請參閱 https://github.com/ceronman/typeannotations）。 它的源代碼可能會給您一些關於如何處理類型註釋以確保運行時接口檢查的有趣想法。

##### Using collections.abc 
抽象基類就像用於創建更高抽象級別的小構建塊。 它們允許您實現真正可用的接口，但非常通用，旨在處理比這種單一設計模式更多的東西。 您可以釋放您的創造力並做出神奇的事情，但構建通用且真正可用的東西可能需要大量工作。 可能永遠不會有回報的工作。

這就是為什麼不經常使用自定義抽象基類的原因。 儘管如此，collections.abc 模塊提供了許多預定義的 ABC，允許驗證許多基本 Python 類型的接口兼容性。 使用此模塊中提供的基類，您可以檢查給定對像是否可調用、映射或是否支持迭代等。 將它們與 isinstance() 函數一起使用比將它們與基本 python 類型進行比較要好得多。 即使您不想使用 ABCMeta 定義自己的自定義接口，您也絕對應該知道如何使用這些基類。
您將不時使用的 collections.abc 中最常見的抽象基類是：
- Container
- Iterable 
- Callable 
- Hashable 
- Sized 

### Proxy
代理提供對昂貴或遠程資源的間接訪問。 代理是一個Client和一個Subject之間

它旨在優化 Subject 訪問（如果它們很昂貴）。 例如，第 12 章“優化——一些強大的技術”中描述的 memoize() 和 lru_cache() 裝飾器可以被視為代理。
代理也可用於提供對主題的智能訪問。 例如，可以將大視頻文件打包到代理中，以避免在用戶僅詢問其標題時將它們加載到內存中。
urllib.request 模塊給出了一個例子。 urlopen 是位於遠程 URL 的內容的代理。 創建時，可以獨立於內容本身檢索標頭，而無需閱讀響應的其餘部分：
```python
class Url(object):
    def __init__(self,location):
        self._url = urlopen(location)
    def headers(self):
        return dict(self._url.headers.items())
    def get(self):
        return self._url.read()

```
通過查看 last-modified 標頭，這可用於在獲取其主體以更新本地副本之前確定頁面是否已更改。 讓我們來一個大文件的例子：
```
ubuntu_iso =Url('http://ubuntu.mirrors.proxad.net/hardy/ubuntu-8.04-desktop-
i386.iso')
ubuntu_iso.headers()['Last-Modified']
```
代理的另一個用例是**數據唯一性。**
例如，讓我們考慮一個在多個位置呈現相同文檔的網站。 特定於每個位置的額外字段將附加到文檔中，例如點擊計數器和一些權限設置。 在這種情況下，可以使用代理來處理特定於位置的事務，還可以指向原始文檔而不是複制它。 因此，一個給定的文檔可以有多個代理，如果它的內容髮生變化，所有位置都將從中受益，而無需處理版本同步。

一般來說，代理模式對於實現可能存在於其他地方的東西的本地句柄很有用：
- 使過程更快
- 避免外部資源訪問
- 減少內存負載
- 確保數據唯一性

### Facade
Facade 提供對子系統的高級、更簡單的訪問。
Facade 只不過是使用應用程序功能的快捷方式，無需處理子系統的底層複雜性。 例如，這可以通過在包級別提供高級功能來完成。

Facade 通常在現有系統上完成，其中包的頻繁使用在高級功能中綜合。 通常，不需要類來提供這樣的模式，`__init__`.py 模塊中的簡單函數就足夠了。
requests 包（請參閱 http://docs.python-requests.org/）是一個很好的項目示例，它在復雜的界面上提供了一個大的外觀。 通過提供開發人員易於閱讀的干淨 API，它真正簡化了在 Python 中處理 HTTP 請求和響應的瘋狂操作。 它實際上什至被宣傳為人類的 HTTP。 這種易用性總是要付出一定的代價，但最終的權衡和額外的開銷並不會嚇到大多數人使用 Requests 項目作為他們選擇的 HTTP 工具。 最後，它使我們能夠更快地完成項目，而開發人員的時間通常比硬件更昂貴。

## Bahavioral patterns
行為模式旨在通過構建類之間的交互過程來簡化類之間的交互。
本節提供了您在編寫 Python 代碼時可能需要考慮的流行行為模式的三個示例：
- 觀察員
- 訪客
- 模板

### Observer
觀察者模式用於通知對象列表有關狀態更改的信息觀察到的成分。
Observer 允許通過將新功能與現有代碼庫解耦，以可插入的方式在應用程序中添加功能。 事件框架是觀察者模式的典型實現，如下圖所示。 每次事件發生時，該事件的所有觀察者都會收到觸發該事件的主題的通知。

在 GUI 應用程序的情況下，將代碼與窗口管理內部結構分離可以大大簡化工作。 函數單獨編寫，然後註冊為事件觀察者。 這種方法存在於 Microsoft 的 MFC 框架的最早版本中（參見 http://en.wikipedia.org/wiki/Microsoft_Foundation_Class_Library）和所有 GUI 開發工具，例如 Qt 或 GTK。 許多框架使用信號的概念，但它們只是觀察者模式的另一種表現形式。

該代碼還可以生成事件。 例如，在將文檔存儲在數據庫中的應用程序中，DocumentCreated、DocumentModified 和 DocumentDeleted 可以是代碼提供的三個事件。 適用於文檔的新功能可以將自己註冊為觀察者，以便在每次創建、修改或刪除文檔時得到通知並執行適當的工作。 可以在應用程序中以這種方式添加文檔索引器。 當然，這需要所有負責創建、修改或刪除文檔的代碼都在觸發事件。 但這比在整個應用程序代碼庫中添加索引掛鉤要容易得多！ 遵循這種模式的流行 Web 框架是 Django 及其信號機制。

可以通過在類級別工作來實現 Event 類以在 Python 中註冊觀察者：
> chapter14/observer.py

這個想法是，觀察者使用 Event 類方法註冊自己，並通過帶有觸發它們的主題的 Event 實例獲得通知。 下面是一個具體的 Event 子類的例子，一些觀察者訂閱了它的通知：

### Visitor
和觀察者模式有相同的地方，它允許在不更改其代碼的情況下擴展給定類的功能。 但是訪問者通過定義一個類來更進一步，該類負責保存數據並將算法推送到其他名為 Visitors 的類。 每個訪問者都專門研究一種算法，並且可以將其應用於數據。
此行為非常類似於 MVC 範例（請參閱 http://en.wikipedia.org/wiki/Model-view-controller），其中文檔是通過控制器推送到視圖的被動容器，或者模型包含已更改的數據 由控制器。
訪問者模式是通過在數據類中提供一個入口點來實現的，所有類型的訪問者都可以訪問該入口點。

如果您的應用程序具有被不止一種算法訪問的數據結構，訪問者模式將有助於分離關注點。 數據容器最好只專注於提供對數據的訪問和保存數據，而不是其他任何事情。

### Template
模板通過定義在子類中實現的抽象步驟來幫助設計通用算法。 該模式使用 Liskov 替換原則，維基百科將其定義為：

換句話說，抽像類可以通過在具體類中實現的步驟來定義算法如何工作。 抽像類還可以提供算法的基本或部分實現，並讓開發人員覆蓋其部分。 例如，隊列模塊中 Queue 類的一些方法可以被覆蓋以使其行為不同。
我們來實現一個例子，如下圖所示。
Indexer 是一個索引器類，它分五個步驟處理文本，無論使用何種索引技術，這些都是常見的步驟：
- Text normalization
- Text split 
- Stop words removal 
- Stem words
- Frequency

Indexer 為流程算法提供部分實現，但需要在子類中實現 removestop_words 和 stemwords。 BasicIndexer 實現嚴格的最小值，而 LocalIndex 使用停用詞文件和詞幹數據庫。 FastIndexer 實現所有步驟，並且可以基於快速索引器，例如 Xapian 或 Lucene。
> chapter14/template.py

對於可能變化並且可以表達為孤立的子步驟的算法，應該考慮模板。 這可能是 Python 中最常用的模式，並不總是需要通過子類化來實現。 例如，許多處理算法問題的內置 Python 函數接受允許您將部分實現委託給外部實現的參數。 例如， sorted() 函數允許一個可選的 key 關鍵字參數，稍後由排序算法使用。 這對於在給定集合中查找最小值和最大值的 min() 和 max() 函數也是相同的。
