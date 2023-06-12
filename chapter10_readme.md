# Test-Driven Development
測試驅動開發 (TDD) 是一種生產高質量軟件的簡單技術。 它在 Python 社區中被廣泛使用，但在其他社區中也很受歡迎。

由於 Python 的動態特性，測試在 Python 中尤為重要。 它缺少靜態類型，因此在運行代碼並執行其每一行之前，許多甚至是微小的錯誤都不會被注意到。 但問題不僅在於 Python 中的類型如何工作。 請記住，大多數錯誤與錯誤的語法使用無關，而是與可能導致重大失敗的邏輯錯誤和微妙的誤解有關。

### Test-driven development principles 
以最簡單的形式，測試驅動開發過程包括三個步驟：
1. 為尚未實現的新功能或改進編寫自動化測試。
2. 提供剛好通過所有定義測試的最少代碼。 
3. 重構代碼以滿足所需的質量標準。
關於這個開發週期要記住的最重要的事實是測試應該在實現之前編寫。 對於沒有經驗的開發人員來說，這不是一件容易的事，但這是保證您將要編寫的代碼可測試的唯一方法。

測試驅動開發提供了很多好處：
- 它有助於防止軟件回歸
- 它提高了軟件質量
- 它提供了一種代碼行為的低級文檔
- 它允許您在較短的開發週期內更快地生成健壯的代碼
處理測試的最佳約定是將它們全部收集在一個模塊或包中（通常命名為測試），並有一種使用單個 shell 命令運行整個套件的簡單方法。 幸運的是，沒有必要自己構建整個測試工具鏈。 Python 標準庫和 Python Package Index 都帶有大量測試框架和實用程序，可讓您以方便的方式構建、發現和運行測試。 我們將在本章後面討論此類包和模塊的最著名示例。

#### Preventing software regression
在我們的開發人員生活中，我們都面臨著軟件回歸問題。 軟件回歸是由變更引入的新錯誤。 當已知在以前版本的軟件中工作的特性或功能在項目開發過程中的某個時刻被破壞並停止工作時，它就會出現。

回歸的主要原因是軟件的高度複雜性。 在某些時候，不可能猜測代碼庫中的單個更改可能導致什麼。 更改某些代碼可能會破壞其他一些功能，有時會導致惡性副作用，例如無聲地破壞數據。 而高複雜性不僅僅是龐大代碼庫的問題。 當然，代碼量與其複雜性之間存在明顯的相關性，但即使是小項目（幾百分之幾/幾千行代碼）也可能具有如此復雜的架構，以至於很難預測相對較小的變化的所有後果。

向多個開發人員開放代碼庫會放大問題，因為每個人都不會完全了解所有開發活動。 雖然擁有版本控制系統可以防止衝突，但它並不能防止所有不需要的交互。

TDD 有助於減少軟件回歸。 整個軟件可以在每次更改後自動測試。 只要每個功能都有適當的測試集，這就會起作用。 正確完成 TDD 後，測試庫會與代碼庫一起增長。

由於完整的測試活動可能會持續很長時間，因此最好將其委託給一些可以在後台完成工作的持續集成系統。 
#### Improving code quality

#### Providing the best developer documentation

#### Producing robust code faster 

### What kind of tests?

#### Accepetance tests 

#### Unit tests

#### Functional tests

#### Integration tests

#### Load and performance testing 

#### Code quality testing 

### Python standard test tools
#### unittest
#### doctest

## I do test
### unittest pitfalls
### unittest alternatives
#### nose 
##### Test runner 
##### Writing tests 
##### Writing test fixtures 
##### Intergration with setuptools and a plug-in system 
##### Wrap-up
#### py.test
##### Writing test fixtures
##### Disabling test functions and classess
##### Automated distributed tests
##### Wrap-up

### Testing coverage
### Fakes and mocks 
#### Building a fake 
#### Using mocks 
### Testing environment and dependency compatibility
#### Dependency matrix testing 
### Document-driven development
#### Writiing a story

