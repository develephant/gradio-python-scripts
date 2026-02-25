# AnyIO itself is not a file I/O library — it focuses on async concurrency, networking, and synchronization.
# However, you can still use it to run file operations asynchronously by offloading blocking file reads/writes to a thread pool.
# This is because normal file I/O in Python is blocking, and AnyIO provides to_thread.run_sync() to run such blocking code without freezing the async event loop. -->

# Example: Loading a File with AnyIO
# Python

import anyio

# Blocking function to read a file
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

async def main():
    file_path = "example.txt"

    try:
        # Run the blocking file read in a worker thread
        content = await anyio.to_thread.run_sync(read_file, file_path)
        print("File contents:")
        print(content)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the async main function
anyio.run(main)


# How It Works

# read_file() is a normal blocking function.
# anyio.to_thread.run_sync() runs it in a background thread so it doesn’t block the async loop.
# You can still use AnyIO’s structured concurrency, cancellation, and error handling.


# If You Need Async File I/O
# If you want true non-blocking file I/O, you’d need a library like:

# aiofiles (works with asyncio backend)
# Combine it with AnyIO by selecting the asyncio backend.

# Example with aiofiles under AnyIO:
# Python

# import anyio
# import aiofiles

# async def main():
#     async with aiofiles.open("example.txt", "r") as f:
#         content = await f.read()
#         print(content)

# anyio.run(main, backend="asyncio")

