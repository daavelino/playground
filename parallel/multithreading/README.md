


Advantages:
- It does not block the user. This is because threads are independent of each other.
- Better use of system resources is possible since threads execute tasks parallely.
- Enhanced performance on multi-processor machinces.
- Multi-threaded servers and interactive GUIs use multithreading exclusively.

Disadvantages:
- As number of threads increase, complexity increases.
- Synchronization of shared resources (objects, data) is necessary.
- It is difficult to debug, result sometimes is unpredictable.
- Potential dealocks with leads to starvation, i.e. some threads may not be served with a bad design.
- Constructing and synchronizing threads is CPU/memory intensive.
