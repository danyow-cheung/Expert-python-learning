import time
from queue import Queue, Empty
from threading import Thread
from gmaps import Geocoding
api = Geocoding()
PLACES = (
    'Reykjavik', 'Vien', 'Zadar', 'Venice',
    'Wrocław', 'Bolognia', 'Berlin', 'Słubice',
    'New York', 'Dehli',
)
THREAD_POOL_SIZE = 4
def fetch_place(place):
    return api.geocode(place)[0]

def present_result(geocoded):
    print("{:>25s}, {:6.2f}, {:6.2f}".format(
        geocoded['formatted_address'],
        geocoded['geometry']['location']['lat'],
        geocoded['geometry']['location']['lng'],
))

def worker(work_queue,results_queue):
    while not work_queue.empty():
        try:
            item = work_queue.get(block=False)
        except Empty:
            break
        else:
            results_queue.put(
                fetch_place(item)
            )
            work_queue.task_done()

def main():
    work_queue = Queue()
    results_queue = Queue()
    for place in PLACES:
        work_queue.put(place)
    threads = [
        Thread(target=worker,args=(work_queue,results_queue))
        for worker in range(THREAD_POOL_SIZE)
    ]

    for thread in threads:
        thread.start()
    work_queue.join()
    while threads:
        threads.pop().join()
    while not results_queue.empty():
        present_result(results_queue.get())

if __name__ =='__main__':
    started = time.time()
    main()
    elapsed = time.time() - started 
    print()
    print("time elapsed: {:.2f}s".format(elapsed))