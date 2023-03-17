from concurrent.futures import ThreadPoolExecutor, Future

if __name__ == "__main__":

    def do_something(some_arg: str):
        print(some_arg)

    with ThreadPoolExecutor() as executor:
        first_future: Future = executor.submit(do_something, "AAA")
        last_future: Future = executor.submit(do_something, "AAA")

    first_future.result()
    last_future.result()
