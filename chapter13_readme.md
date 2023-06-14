# Concurrency
並發性及其表現形式之一——並行處理——是軟件工程領域最廣泛的主題之一。 本書的大部分章節也涵蓋了廣闊的領域，幾乎所有章節都可以作為單獨一本書的大主題。 但是並發這個話題本身就非常龐大，它可以佔據幾十個位置，我們仍然無法討論它的所有重要方面和模型。

這就是為什麼我不會試圖愚弄你，並且從一開始就聲明我們幾乎不會觸及這個話題的表面。 本章的目的是展示為什麼你的應用程序可能需要並發，何時使用它，以及你可能在 Python 中使用的最重要的並發模型是什麼：
- 多線程threading
- 多processing
- 異步編程asynchronous programming

我們還將討論允許您在代碼中實現這些模型的一些語言特性、內置模塊和第三方包。 但我們不會詳細介紹它們。 將本章的內容作為您進一步研究和閱讀的切入點。 它在這裡指導您了解基本思想並幫助您決定是否真的需要並發，如果需要，哪種方法最適合您的需要。

## Why concurrency
而第二個問題的答案可能會讓一些曾經認為這是並行處理同義詞的人感到驚訝。 但並發性與並行性不同。 並發不是應用程序實現的問題，而只是程序、算法或問題的屬性。 並行性只是解決並發問題的可能方法之一。
萊斯利·蘭波特 (Leslie Lamport) 在他 1976 年發表的分佈式系統中的時間、時鐘和事件排序論文中說：
“如果兩個事件都不能因果影響另一個，則兩個事件是同時發生的。”


通過將事件外推到程序、算法或問題，如果某事物可以完全或部分分解為與順序無關的組件（單元），我們可以說它是並發的。 這些單元可以相互獨立處理，處理順序不影響最終結果。 這意味著它們也可以同時或併行處理。 如果我們以這種方式處理信息，那麼我們確實是在進行並行處理。 但這仍然不是強制性的。

## Multithreading
### What is multithreading
### How python deals with threads
### When should threading be used 
#### Building responsive interfaces
#### Delegating work
#### Multiuser applications
#### An example of a threaded application
##### Using one thread per item
##### Using a thread pool
##### Using two-way queues
##### Dealing with errors and rate limiting

## Multiprocessing
### The built-in multiprocessing module
#### Using process pools
#### Using multiprocessing dummy as a multithreading interface 

## Asynchoronous programming
### Cooperative multitasking and asynchronous I/O
### Python async and await keywords
### asyncio in older versions of Python
### A practical example of asynchronous programming 
### Integrating nonasynchronous code with async using futures
####  Executors and futures
#### Using executors in an event loop
