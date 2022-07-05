"""
Definition: f(n) = f(n-1) + f(n-2)
Method: Recursion
"""

import sys

def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)


if __name__=="__main__":
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
    else:
        print(f"Usage: {sys.argv[0]} <n>. Exiting.")
        sys.exit(1)
    
    result = None
    result = fib(n)

    print(result)
