import os
from typing import Tuple, AsyncGenerator
from fastapi import Request

def get_range_header(range_header: str, file_size: int) -> Tuple[int, int]:
    """Parse HTTP range header and return start and end positions"""
    if range_header.startswith("bytes="):
        ranges = range_header.replace("bytes=", "").split(",")
        for range_str in ranges:
            start_str, end_str = range_str.split("-")
            start = int(start_str) if start_str else 0
            end = int(end_str) if end_str else file_size - 1
            return start, min(end, file_size - 1)
    return 0, file_size - 1

async def ranged_file_sender(file_path: str, start: int, end: int) -> AsyncGenerator[bytes, None]:
    """Send a file in chunks with support for range requests"""
    with open(file_path, "rb") as video_file:
        video_file.seek(start)
        chunk_size = 1024 * 1024  # 1MB chunks
        remaining = end - start + 1
        while remaining > 0:
            chunk = video_file.read(min(chunk_size, remaining))
            if not chunk:
                break
            remaining -= len(chunk)
            yield chunk

async def file_sender(file_path: str) -> AsyncGenerator[bytes, None]:
    """Send a complete file in one chunk"""
    with open(file_path, "rb") as video_file:
        data = video_file.read()
        yield data
