from functools import wraps
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, Future
from expiringdict import ExpiringDict
import jsons


def caching_decorator(max_len, max_age_seconds):
    def decorator(f):
        @wraps(f, updated=())
        class OurTTLCache:
            def __init__(self, f):
                self.lock = Lock()
                self.f = f
                self.cache = ExpiringDict(
                    max_len=max_len, max_age_seconds=max_age_seconds
                )

            def __call__(self, *args):
                xxx = jsons.dumps(args)
                with self.lock:
                    result = self.cache.get(xxx)
                    if result is None:
                        result = self.f(*args)
                        self.cache[xxx] = result
                    return result

            def clear(self):
                with self.lock:
                    self.cache = ExpiringDict(
                        max_len=max_len, max_age_seconds=max_age_seconds
                    )

        return OurTTLCache(f)

    return decorator


if __name__ == "__main__":

    @caching_decorator(100, 10)
    def do_something(some_arg1: str, some_arg2: str):
        my_output = some_arg1 + "  " + some_arg2
        print(my_output + ">>>")
        return my_output

    with ThreadPoolExecutor() as executor:
        first_future: Future = executor.submit(do_something, "AAA", "BBB")
        last_future: Future = executor.submit(do_something, "AAA", "BBB")

    print(first_future.result())
    print(last_future.result())

    with ThreadPoolExecutor() as executor:
        first_future = executor.submit(do_something, "AAA", "BBB")
        last_future = executor.submit(do_something, "AAA", "BBB")

    print(first_future.result())
    print(last_future.result())

    do_something.clear()

    with ThreadPoolExecutor() as executor:
        first_future = executor.submit(do_something, "AAA", "BBB")
        last_future = executor.submit(do_something, "AAA", "BBB")

    print(first_future.result())
    print(last_future.result())
