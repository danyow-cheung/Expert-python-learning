from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool

def main(use_threads=True):
    if use_threads:
        pool_cls = ThreadPool
    else:
        pool_cls = ProcessPool
    with pool_cls(POOL_SIZE) as pool:
        results = pool.map(fetch_place,PLACES)
    for result in results:
        print(result)
        