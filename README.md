Distributed Lock
================

Sometimes, to avoid race conditions and this kind of things you need a lock.
This is very common for example when you have to insert an element but first
you have to check it is was already inserted. You can check that the element
is not inserted but during the process of insert, other entity (process, thread...)
could insert the same element and then you got a duplicated value.

This non atomic tasks should be done in an atomic way, that is what a lock is for.
All languages have this feature for threading, but what happens when you have
several machines in every part of the world running the same code?

This library is for that.

Installing
==========
```bash
pip install distributed-lock
```

How does it work
================
Using redis. Redis is known to use a single thread to make operations. This ensures
that even if redis receives two requests at the same time, one will be processed first
and the other in second place. That is exactly what we want.

Basically, our application tries to acquire the lock. If you get an error, wait. If you dont,
you acquired the lock and you are safe to run your code. If two applications tries to acquire
the lock at the same time, redis will decide. Only one will acquire and all others will get an
error. That is. 

Why redis?
=========
Redis is fast, lightweight, easy to use and compatible with most of languages. So this
solution is easy to implement and language agnostic (and fast and reliable or course)!

Example
=======

```python
from distributed_lock import DistributedLock
from redis import Redis
import time
redis_client = Redis()

with DistributedLock(redis_client, lock_name="register_user", lock_ttl=30):
    # do here the thing that should not be done in parallel
    for i in ["a", "b", "c", "d"]:
        print(i)
    # If you run this code in several threads, processes at the same time, you will
    # always see "abcd", not mixed words. Of course, when using threads or processes
    # using this library is "totally wrong", the idea is to use it in a task queue or
    # places that where you know nothing about others.

```