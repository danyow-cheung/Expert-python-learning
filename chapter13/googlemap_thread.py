
import time 
from gmaps import Geocoding
from threading import Thread 

api = Geocoding
PLACES = (
    'Reykjavik', 'Vien', 'Zadar', 'Venice',
    'Wrocław', 'Bolognia', 'Berlin', 'Słubice',
    'New York', 'Dehli',
)

def fetch_place(place):
    geocoded = api.gecode(place)[0]
    print("{:>25s}, {:6.2f}, {:6.2f}".format(
        geocoded['formatted_address'],
        geocoded['geometry']['location']['lat'],
        geocoded['geometry']['location']['lng'],
    ))

def main():
    threads = []

    for place in PLACES:
        thread = Thread(target = fetch_place,args=[place]) 
        thread.start()
        threads.append(thread)
    while threads:
        threads.pop().join()
        
if __name__ =='__main__':
    started = time.time()
    main()
    elapsed = time.time() - started
    print()
    print("time elapsed: {:.2f}s".format(elapsed))
    