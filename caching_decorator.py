import time 
import hashlib
import pickle

cache ={}
def is_obsolete(entry,duration):
    return time.time() - entry['time']>duration

def compute_key(function,args,kw):
    key = pickle.dumps((function.__name__,args,kw))
    return hashlib.sha1(key).hexdigest()

'''
SHA 散列密鑰是使用有序參數值構建的，結果存儲在全局字典中。 
哈希是使用 pickle 生成的，它是凍結所有作為參數傳遞的對象的狀態的捷徑，
確保所有參數都是好的候選者。 
持續時間參數用於在自上次函數調用以來經過太多時間時使緩存值無效。
'''
def memorize(duration=10):
    def _momoize(function):
        def __memoize(args,*kw):
            key = compute_key(function,args,kw)
            if (key in cache and not is_obsolete(cache[key],duration)):
                print('we got a winner ')
                return cache[key]['value']
            
            # computing 
            result = function(args,*kw)
            # storing the result 
            cache[key] = {
                "value":result,
                "time":time.time()

            }
            return result 
        return __memoize 
    return _momoize 
'''
Example Usage
'''
@memorize()
def very_very_very_complex_stuff(a,b):
    return a+b 

print(very_very_very_complex_stuff(2,2))
print(very_very_very_complex_stuff(2,2))
print(cache)