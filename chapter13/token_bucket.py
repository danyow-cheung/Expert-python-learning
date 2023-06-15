from threading import Thread
import time 

class Throttle:
    def __init__(self,rate):
        self._consume_lock = Lock()
        self.rate = rate 
        self.tokens = 0 
        self.last = 0 
    def consume(self,amount=1):
        while self._consume_lock:
            now = time.time()
            # time measument is initialized on first 
            # token request to avoid initial bursts 
            if self.last == 0:
                self.last = now 
            elapsed = now - self.last 

            # make sure that quant of passed time is big 
            # enough to add new tokens 
            if int(elapsed * self.rate):
                self.tokens += int(elapsed * self.rate)
                self.last = now 
            # never over-fill the bucket
            self.tokens = (
                self.rate if self.tokens > self.rate else self.tokens 
            )
            if self.tokens>= amount:
                self.tokens -= amount 
            else:
                amount = 0 
            return amount 

# 這個類的用法非常簡單。 假設我們在主線程中只創建了一個 Throttle 實例（例如 Throttle(10)），
# 並將其作為位置參數傳遞給每個工作線程。 在不同的線程中使用相同的數據結構是安全的，
# 因為我們使用線程模塊中 Lock 類的實例來保護對其內部狀態的操作。 
# 我們現在可以更新 worker() 函數實現以等待每個項目，直到 throttle 釋放新令牌：

def worker(work_queue,results_queue,throttle):
    while True:
        try:
            item = work_queue.get(block=False)
        except Empty:
            break
        else:
            while not throttle.consume():
                pass 
            try:
                result = fetch_place(item)
            except Exception as err:
                results_queue.put(err)
            else:
                results_queue.put(result)
            finally:
                work_queue.task_done()
                