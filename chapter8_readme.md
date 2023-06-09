# Managing Code 

This chapter is divided into two parts, which explain:
- How to work with a version control system
- How to set up continuous development processes

首先，代码库的发展如此之快，因此跟踪所做的所有更改非常重要，当许多开发人员都在处理它时更是如此。 这就是版本控制系统的作用。

这是通过为持续集成或持续交付等持续开发过程设置一系列工具来完成的。

## Version control systems 
版本控制系统 (VCS) 提供了一种共享、同步和返回的方式任何类型的文件。 它们分为两个家族：
- 集中式系统 
- 分布式系统

### Centralized systems 集中式系統
原理非常简单——每个人都可以在他/她的系统上获得一份文件副本并对其进行处理。 
从那里，每个用户都可以将他/她的更改提交到服务器。 它们将被应用并提高修订号。 
然后其他用户将能够通过更新同步他们的存储库副本来获得这些更改。

此集中配置中的每个用户都负责将他/她的本地存储库与主存储库同步，以便获得其他用户的更改。 
这意味着当本地修改的文件已被其他人更改和签入时，可能会发生一些冲突。 
执行冲突解决机制，在本例中是在用户系统上，如下图所示：

但尽管有这些优势，集中式 VCS 也有几个缺陷：
- 分支和合并很难处理。 它可能成为一场噩梦。
- 由于系统是中心化的，所以不可能离线提交更改。 当用户重新联机时，这可能会导致对服务器进行巨大的单一提交。最后，它对 Linux 等项目不太适用，许多公司永久维护自己的软件分支，并且没有每个人都有帐户的中央存储库。


尽管存在这些缺陷，主要由于企业环境的惯性，集中式 VCS 仍然在许多公司中很受欢迎。 
许多组织使用的集中式 VCS 的主要示例是 Subversion (SVN) 和并发版本系统 (CVS)。 
版本控制系统集中式架构的明显问题是大多数开源社区已经切换到更可靠的分布式 VCS (DVCS) 架构的原因。


### Distributed systems 分布式系統
分布式 VCS 是对集中式 VCS 缺陷的解决方案。 它不依赖于人们使用的主服务器，而是基于对等原则。 每个人都可以持有和管理自己的项目独立仓库，并与其他仓库同步：

#### Distributed strategies
如果您在公司环境中工作并且每个人都朝着同一个目标努力，那么中央服务器当然仍然需要 DVCS。 
但该服务器的用途与集中式 VCS 完全不同。 它只是一个枢纽，允许所有开发人员在一个地方共享他们的更改，
而不是在彼此的存储库之间拉取和推送。 
这样一个单一的中央存储库（通常称为上游）也可以作为所有团队成员的个人存储库中跟踪的所有更改的备份。

另一种方法包括在服务器上提供多个具有不同访问级别的存储库：
- 不稳定的存储库是每个人都可以推送更改的地方。
- 稳定存储库对除发布管理员以外的所有成员都是只读的。 他们被允许从不稳定的存储库中拉取更改并决定应该合并什么。
- 各种发布存储库对应于发布并且是只读的，我们将在本章后面看到。

### Centralized or distributed 
說實話。 集中式版本控制系統已成為過去。 在我們大多數人都有機會全職遠程工作的時代，受制於集中式 VCS 的所有缺陷是不合理的。 
例如，使用 CVS 或 SVN，您無法在離線時跟踪更改。 這很愚蠢。 當您工作場所的 Internet 連接暫時中斷或中央存儲庫出現故障時，
您應該怎麼辦？ 您是否應該忘記所有的工作流程，只是讓更改堆積起來直到情況發生變化，然後將其作為一大塊非結構化更新提交？ 不！

### Use Git if you can 
github - 分布式版本控制

### Git flow and Github flow 
使用 Git 的非常流行和標準化的方法簡稱為 Git 流。
- 有個主要的工作流，通常被稱為`develop`,最新版本應用程序的所有開發都發生在這裡。
- 新項目功能在稱為功能分支的單獨分支中實現，這些分支始終從開發分支開始。 當一個特性的工作完成並且代碼被正確測試時，這個分支被合併回開發。
- 當 develop 中的代碼穩定（沒有已知錯誤）並且需要新的應用程序發佈時，將創建一個新的發布分支。 此發布分支通常需要額外的測試（廣泛的 QA 測試、集成測試等），因此肯定會發現新的錯誤。 如果發布分支中包含其他更改（例如錯誤修復），則最終需要將它們合併回開發分支。
- 當發布分支上的代碼準備好部署/發佈時，它會被合併到 master 分支，並且 master 上的最新提交被標記為適當的版本標籤。 除了發布分支之外，其他分支都不能合併到主分支。 唯一的例外是需要立即部署或發布的修補程序。
- 需要緊急發布的修補程序總是在從 master 開始的單獨分支上實現。 修復完成後，它會合併到 develop 和 master 分支。 熱修復分支的合併就像一個普通的發布分支一樣完成，因此必須對其進行適當標記，並相應地修改應用程序版本標識符。


圖 5 中展示了 Git 流程的可視化示例。對於那些從未以這種方式工作，也從未使用過分佈式版本控制系統的人來說，這可能有點讓人不知所措。 
無論如何，如果您沒有任何正式的工作流程，那麼在您的組織中確實值得嘗試。 
它有多種好處，還可以解決實際問題。 它對於由多個程序員組成的團隊處理許多不同的功能以及需要提供對多個版本的持續支持時特別有用。

## Continuous development process 持續開發
有一些流程可以極大地簡化您的開發並減少準備好應用程序發布或部署到生產環境的時間。 
他們的名字中經常有連續的，我們將在本節中討論最重要和最受歡迎的。 
重要的是要強調它們是嚴格的技術過程，因此它們幾乎與項目管理技術無關，儘管它們可以與後者高度吻合。

我們將提到的最重要的過程是：
- 持續集成 
- 持續交付 
- 持續部署
這些是技術過程的事實意味著它們的實施嚴格取決於適當工具的使用。
它們每個背後的總體思想都相當簡單，因此您可以構建自己的持續集成/交付/部署工具，但最好的方法是選擇已經構建的東西。
這樣，您可以將更多精力放在構建產品而不是用於持續開發的工具鏈上。

### Continous integration
持續集成，通常縮寫為 CI，是一個利用自動化測試和版本控制系統提供全自動集成環境的過程。 
它可以與集中式版本控制系統一起使用，但實際上只有在使用良好的 DVCS 工具管理代碼時，它才會展翅高飛。
設置存儲庫是邁向持續集成的第一步，持續集成是從極限編程 (XP) 中出現的一組軟件實踐。

實施持續集成的第一個也是最重要的要求是擁有一個完全自動化的工作流程，可以在給定的修訂版中測試整個應用程序，以確定它在技術上是否正確。 技術上正確意味著它沒有已知錯誤，並且所有功能都按預期工作。

CI 背後的總體思想是，測試應該始終在合併到主流開發分支之前運行。 
這只能通過開發團隊的正式安排來解決，但實踐證明這不是一個可靠的方法。 
問題在於，作為程序員，我們往往過於自信，無法批判性地看待我們的代碼。
如果持續集成只建立在團隊安排上，它不可避免地會失敗，因為一些開發人員最終會跳過他們的測試階段，將可能有錯誤的代碼提交到應該始終保持穩定的主流開發分支。 
而且，在現實中，即使是簡單的更改也會引入關鍵問題。


顯而易見的解決方案是利用專用的構建服務器，只要代碼庫發生變化，它就會自動運行所有必需的應用程序測試。 
有許多工具可以簡化這個過程，它們可以很容易地與 GitHub 或 Bitbucket 等版本控制託管服務以及 GitLab 等自託管服務集成。 
使用此類工具的好處是，開發人員可以在本地僅運行選定的測試子集（根據他的說法，這與他當前的工作相關），並為構建服務器留下可能耗時的整套集成測試。 
這確實加快了開發速度，但仍然降低了新功能破壞主流代碼分支中現有穩定代碼的風險。

#### Testing every commit 
持續集成的最佳方法是對推送到中央存儲庫的每個更改執行整個測試套件。 
即使一個程序員在單個分支中推送了一系列多次提交，單獨測試每個更改通常也是有意義的。 
如果您決定在單個存儲庫推送中僅測試最新的變更集，那麼將很難找到中間某處引入的可能回歸問題的來源。

當然，許多 DVCS（例如 Git 或 Mercurial）允許您通過提供將更改歷史一分為二的命令來限制搜索回歸源所花費的時間，但實際上，作為持續集成過程的一部分自動執行此操作要方便得多。這可能需要數十分鐘甚至數小時才能完成。 一台服務器可能不足以在給定時間範圍內對每次提交執行所有構建。


#### Merge testing through CI 
現實是複雜的。 如果一個特性分支上的代碼通過了所有的測試，並不意味著在合併到一個穩定的主流分支時構建不會失敗。 
Git 流程和 GitHub 流程部分中提到的兩種流行的分支策略都假定合併到主分支的代碼始終經過測試和部署。 但是如果您還沒有執行合併，您怎麼能確定滿足這個假設呢？ 由於 Git 流程強調發布分支，因此這是一個較小的問題（如果實施得當並使用得當）。 但對於簡單的 GitHub 流程來說，這是一個真正的問題，合併到 master 往往與衝突有關，並且很可能在測試中引入回歸。 即使對於 Git Flow，這也是一個嚴重的問題。 這是一個複雜的分支模型，所以人們在使用它時肯定會出錯。 因此，如果您不採取特殊的預防措施，您永遠無法確定合併後 master 上的代碼是否會通過測試。

#### Matrix testing 
如果您的代碼需要在不同的環境中進行測試，則矩陣測試是一個非常有用的工具。 根據您的項目需求，您的 CI 解決方案中對此類功能的直接支持可能需要更少或更多


但這只是最簡單的例子。 應用程序必須在必須測試完全不同的參數的多個環境中進行測試的情況並不少見。 舉幾個例子：
- 不同的操作系統
- 不同的數據庫
- 不同版本的支持服務 
- 不同類型的文件系統
全套組合形成一個多維環境參數矩陣，這就是為什麼這樣的設置被稱為矩陣測試。 當您需要如此深入的測試工作流程時，您很可能需要在 CI 解決方案中對矩陣測試提供一些集成支持。

### Continuous delivery 
持續交付是持續集成思想的簡單延伸。 這種軟件工程方法旨在確保應用程序可以隨時可靠地發布。 持續交付的目標是在短時間內發佈軟件。 它通常通過允許對生產中的應用程序進行增量交付來降低成本和發佈軟件的風險。


在許多項目中，自動化測試不足以可靠地判斷給定版本的軟件是否真的準備好發布。 
在這種情況下，額外的手動用戶驗收測試通常由熟練的 QA 人員執行。 
根據您的項目管理方法，這可能還需要客戶的一些批准。 
這並不意味著您不能使用 Git 流程、GitHub 流程或類似的分支策略，如果您的某些驗收測試必須由人工手動執行的話。 
這只會將穩定和發布分支的語義從準備部署更改為準備好進行用戶驗收測試和批准。

### Continuous deployment 
持續部署是將持續交付提升到一個新水平的過程。 對於所有驗收測試都是自動進行且無需客戶手動批准的項目來說，
這是一種完美的方法。 簡而言之，一旦代碼合併到穩定分支（通常是 master），它就會自動部署到生產環境。


這種方法看起來非常好而且健壯，但並不經常使用，因為很難找到不需要手動 QA 測試和新版本發布前某人批准的項目。 無論如何，這絕對是可行的，一些公司聲稱正在以這種方式工作。

為了實施持續部署，您需要與持續交付過程相同的基本先決條件。 此外，通常需要一種更謹慎的方法來合併到一個穩定的分支中。 
在持續集成中合併到 master 中的內容通常會立即進入生產。 
因此，將合併任務移交給 CI 系統是合理的，如通過 CI 進行合併測試部分所述。

### Popular tools for continuous intergration
現在的 CI 工具有各種各樣的選擇。 它們在易用性和可用功能方面差異很大，幾乎每一個都具有一些其他人所沒有的獨特功能。

在這裡，我們將回顧一些流行的免費開源工具，以及付費託管服務。 我真的不想為任何供應商做廣告，所以我們將只討論那些免費提供的開源項目，以證明這種相當主觀的選擇是合理的。 不會給出最佳建議，但我們會指出任何解決方案的優缺點。 如果您仍然有疑問，下一節描述常見的持續集成陷阱應該可以幫助您做出正確的決定。


### Choosing the right tool and common pitfalls 
> 選擇正確的工具和常見的陷阱
如前所述，沒有完美的 CI 工具可以適用於每個項目，
最重要的是，適用於它使用的每個組織和工作流程。 
對於託管在 GitHub 上的開源項目，我只能給出一個建議。 對於具有平台獨立代碼的小型代碼庫，
Travis CI 似乎是最佳選擇。 它很容易上手，只需最少的工作量，您就會立即得到滿足。

#### Problem 1: too complex build strategies
一些組織喜歡將超出合理水平的事物形式化和結構化。 在創建計算機軟件的公司中，這在兩個領域尤其如此：項目管理工具和在 CI 服務器上構建策略。

項目管理工具的過度配置通常會導致 JIRA（或任何其他管理軟件）上的問題處理工作流程變得如此復雜，以至於當用圖表表示時，它們永遠無法容納一堵牆。 如果您的經理有這種配置/控制狂，您可以與他交談或將他換成另一位經理（讀作：辭掉您目前的工作）。 不幸的是，這並不能可靠地確保在這方面有任何改進。

確實不需要製定複雜的策略來決定應該測試哪個提交或分支。 無需將測試限制在特定標籤上。 無需排隊提交即可執行更大的構建。 無需通過自定義提交消息禁用構建。 您的持續集成過程應該易於推理。 測試一切！ 總是測試！ 就這樣！ 如果沒有足夠的硬件資源來測試每次提交，則添加更多硬件。 請記住，程序員的時間比矽芯片更昂貴。

#### Problem 2: too long building time 
較長的構建時間會扼殺任何開發人員的性能。 如果您需要等待數小時才能知道您的工作是否正確完成，那麼您就無法提高工作效率。 
當然，在測試您的功能時有其他事情可做會有很大幫助。 不管怎樣，作為人類，
我們在同時處理多項任務方面真的很糟糕。 在不同的問題之間切換需要時間，最終會使我們的編程性能降為零。 一次處理多個問題時很難保持專注。


解決方案非常簡單：不惜任何代價保持快速構建。 首先，嘗試找到瓶頸並對其進行優化。 如果構建服務器的性能是問題所在，則嘗試橫向擴展。 如果這沒有幫助，則將每個構建分成更小的部分並並行化。


有很多解決方案可以加快緩慢的構建測試，但有時對這個問題無能為力。 例如，如果您有自動瀏覽器測試或需要對外部服務執行長時間運行的調用，則很難將性能提高到超出某些硬性限制。 例如，當你的 CI 中自動驗收測試的速度成為問題時，那麼你可以放鬆測試一切，測試總是規則一點。 對程序員來說最重要的通常是單元測試和靜態分析。 因此，根據您的工作流程，緩慢的瀏覽器測試有時可能會及時推遲到準備發布的那一刻。


降低構建運行速度的另一個解決方案是重新考慮應用程序的整體架構設計。 
如果測試應用程序需要花費大量時間，這通常表明應該將其拆分為幾個可以單獨開發和測試的獨立組件。 
將軟件編寫成巨大的整體是通向失敗的最短路徑之一。 通常，任何軟件工程過程都會因未正確模塊化的軟件而中斷。

#### Problem 3: external job definitions
一些持續集成系統，尤其是 Jenkins，允許您完全通過 Web UI 設置大部分構建配置和測試過程，而無需接觸代碼存儲庫。 但是你真的應該避免將構建步驟/命令的簡單入口點以外的任何東西放入外部系統。 這是一種只會帶來麻煩的 CI 反模式。

作為全局外部構建定義引入的問題的示例，我們假設我們有一些開源項目。 
最初的開發很忙，我們不關心任何風格指南。 我們的項目很成功，因此開發需要另一個主要版本。 
一段時間後，我們從 0.x 版本轉移到 1.0，並決定重新格式化您的所有代碼以符合 PEP 8 指南。 
將靜態分析檢查作為 CI 構建的一部分是一種很好的方法，因此我們決定將 pep8 工具的執行添加到我們的構建定義中。 
如果我們只有一個全局的外部構建配置，那麼如果需要對舊版本的代碼進行一些改進，就會出現問題。 
假設有一個關鍵的安全問題需要在應用程序的兩個分支中修復：0.x 和 1.y。 
我們知道 1.0 版以下的任何內容都不符合樣式指南，新引入的針對 PEP 8 的檢查會將構建標記為失敗。


該問題的解決方案是使構建過程的定義盡可能接近源代碼。 對於某些 CI 系統（Travis CI 和 GitLab CI），您默認獲得該工作流。 對於其他解決方案（Jenkins 和 Buildbot），
您需要格外小心，以確保大部分構建過程都包含在您的代碼中，而不是某些外部工具配置中。 幸運的是，您有很多選擇可以實現這種自動化：
- Bash 腳本 
- Makefiles 
- Python 代碼

#### Problem 4: lack of isolation

不幸的是，在以持續集成過程為目的測試代碼時，這通常是不夠的。 測試環境應該盡可能接近生產環境，如果沒有額外的系統級虛擬化，很難做到這一點。
如果在構建應用程序時未確保適當的系統級隔離，您可能會遇到的主要問題是：
- 在文件系統或支持服務（緩存、數據庫等）中的構建之間存在一些狀態
- 多個構建或測試通過環境、文件系統或支持服務相互連接
- 由於未在構建服務器上捕獲的生產操作系統的特定特徵而發生的問題

