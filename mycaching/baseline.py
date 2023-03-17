from threading import Lock
from concurrent.futures import ThreadPoolExecutor, Future
from cachetools import cached, TTLCache

lock = Lock()

if __name__ == "__main__":

    @cached(cache=TTLCache(maxsize=10, ttl=60), lock=lock)
    def do_something(some_arg: str):
        print(some_arg)

    with ThreadPoolExecutor() as executor:
        first_future: Future = executor.submit(do_something, "AAA")
        last_future: Future = executor.submit(do_something, "AAA")

    first_future.result()
    last_future.result()
