"""
Definition: f(n) = f(n-1) + f(n-2)
Method: Dynamic Programming
"""

import sys

def fib(n):
    f = [0, 1]

    for i in range(2, n + 1):
        f.append(f[i-1] + f[i-2])

    return f[n]

if __name__=="__main__":
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
    else:
        print(f"Usage: {sys.argv[0]} <n>. Exiting.")
        sys.exit(1)
    
    result = None
    result = fib(n)

    print(result)
