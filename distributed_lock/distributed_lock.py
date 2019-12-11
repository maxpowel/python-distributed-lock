from redis import Redis, exceptions
import time
from uuid import uuid4


class DistributedLock(object):
    def __init__(self, redis_client, lock_name, owner_id=None, lock_ttl=10, poll_time=1):
        """

        :param redis_client: The redis client, can be strict or normal
        :param lock_name: the key to share between all clients. Every key is a different lock
        :param owner_id: just a value to identify who acquired the lock (to debug)
        :param lock_ttl: en expire time. The locks should be fast and an application can die with the lock acquired.
                         Using a lock ttl we are sure the the system will not stuck forever.
        :param poll_time: Time in seconds between every acquire attempt
        """
        self.redis = redis_client
        self.lock_name = lock_name
        self.lock_ttl = lock_ttl
        self.poll_time = poll_time
        if owner_id is None:
            self.owner_id = uuid4().hex
        else:
            self.owner_id = owner_id

    def _acquire(self):
        try:
            # Acquire if we put the value and did not exist before
            pipe = self.redis.pipeline()
            pipe.watch(self.lock_name)
            pipe.multi()
            pipe.set(self.lock_name, self.owner_id, nx=True, ex=self.lock_ttl)
            r = pipe.execute()
            return r[0] is True
        except exceptions.WatchError:
            # There was a conflict when writing the value and redis discarded us, so we didnt acquire the lock
            return False

    def __enter__(self):
        while not self._acquire():
            time.sleep(self.poll_time)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redis.delete(self.lock_name)
