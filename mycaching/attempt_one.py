from threading import Lock
from concurrent.futures import ThreadPoolExecutor, Future
from expiringdict import ExpiringDict

lock = Lock()
cache = ExpiringDict(max_len=100, max_age_seconds=10)

if __name__ == "__main__":

    def do_something(some_arg: str):
        with lock:
            result = cache.get(some_arg)
            if result is None:
                print(some_arg)
                cache[some_arg] = True

    with ThreadPoolExecutor() as executor:
        first_future: Future = executor.submit(do_something, "AAA")
        last_future: Future = executor.submit(do_something, "AAA")

    first_future.result()
    last_future.result()
