import sys
from threading import Thread
from subprocess import run, DEVNULL
from time import time 
from datetime import timedelta

def launch(p, n):
    start = time()
    run(["python", p, n], stdout=DEVNULL, stderr=DEVNULL)
    end = time()

    result[p] = str(timedelta(seconds=end - start))



if __name__=="__main__":

    if len(sys.argv) == 4:
        p1 = sys.argv[1]
        p2 = sys.argv[2]
        n = sys.argv[3]
    else:
        print(f"Usage: {sys.argv[0]} <program1> <program2>. Exiting.")
        sys.exit(1)

    result = dict()

    
    t1 = Thread(target=launch, args=(p1, n))
    t2 = Thread(target=launch, args=(p2, n))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print(result)
