import os
import threading

def hello_from_thread():
    print(f'Hello flow {threading.current_thread()}!')

hello_thread = threading.Thread(target=hello_from_thread)
hello_thread.start()

total_threads = threading.active_count()
thread_name = threading.current_thread().name

print(f'Current moment Python complete {total_threads} flows')
print(f'name current flow {thread_name}')
hello_thread.join()