import asyncio
import aiofiles
import os

# Asynchronously list files in a directory
async def list_files_async(directory: str):
    try:
        # Run blocking os.listdir in a thread to avoid blocking the event loop
        return await asyncio.to_thread(os.listdir, directory)
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return []
    except PermissionError:
        print(f"Permission denied: {directory}")
        return []

# Asynchronously read a file's content
async def read_file_async(filepath: str):
    try:
        async with aiofiles.open(filepath, mode='r', encoding='utf-8') as f:
            return await f.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except PermissionError:
        print(f"Permission denied: {filepath}")
    except UnicodeDecodeError:
        print(f"Could not decode file: {filepath}")
    return None

# Main async function
async def main():
    directory = "./test_dir"  # Change to your directory path
    files = await list_files_async(directory)

    # Filter only regular files
    file_paths = [
        os.path.join(directory, f)
        for f in files
        if os.path.isfile(os.path.join(directory, f))
    ]

    # Read all files concurrently
    tasks = [read_file_async(fp) for fp in file_paths]
    contents = await asyncio.gather(*tasks)

    # Print results
    for path, content in zip(file_paths, contents):
        if content is not None:
            print(f"--- {path} ---")
            print(content)

if __name__ == "__main__":
    asyncio.run(main())
