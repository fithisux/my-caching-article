from functools import wraps
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, Future
from expiringdict import ExpiringDict
import jsons

lock = Lock()
cache = ExpiringDict(max_len=100, max_age_seconds=10)


def textbook_caching_decorator(f):
    @wraps(f)
    def wrapper_accepting_arguments(*args):
        xxx = jsons.dumps(args)
        with lock:
            result = cache.get(xxx)
            if result is None:
                result = f(*args)
                cache[xxx] = result
        return result

    return wrapper_accepting_arguments


if __name__ == "__main__":

    @textbook_caching_decorator
    def do_something(some_arg1: str, some_arg2: str):
        my_output = some_arg1 + "  " + some_arg2
        print(my_output + ">>>")
        return my_output

    with ThreadPoolExecutor() as executor:
        first_future: Future = executor.submit(do_something, "AAA", "BBB")
        last_future: Future = executor.submit(do_something, "AAA", "BBB")

    print(first_future.result())
    print(last_future.result())
