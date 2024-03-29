import os
from main import config
from typing import BinaryIO
from fastapi.responses import StreamingResponse
from fastapi import HTTPException, Request, status


def send_bytes_range_requests(
    file_obj: BinaryIO, start: int, end: int, chunk_size: int = 10_000
):
    """Send a file in chunks using Range Requests specification RFC7233

    `start` and `end` parameters are inclusive due to specification
    """
    with file_obj as f:
        f.seek(start)
        while (pos := f.tell()) <= end:
            read_size = min(chunk_size, end + 1 - pos)
            yield f.read(read_size)


def _get_range_header(range_header: str, file_size: int) -> tuple[int, int]:
    def _invalid_range():
        return HTTPException(
            status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail=f"Не корректны \"range\" запрос (Range:{range_header!r})",
        )

    try:
        h = range_header.replace("bytes=", "").split("-")
        start = int(h[0]) if h[0] != "" else 0
        end = int(h[1]) if h[1] != "" else file_size - 1
    except ValueError:
        raise _invalid_range()

    if start > end or start < 0 or end > file_size - 1:
        raise _invalid_range()
    return start, end


def range_requests_response(
    request: Request, file_name: str, content_type: str
):
    file_path = os.path.join(config.MUSICS_FOLDER, file_name)

    file_size = os.stat(file_path).st_size
    range_header = request.headers.get("range")

    headers = {
        "Content-type": content_type,
        "Connection": "keep-alive",
        "Keep-Alive": "timeout=60",
        "Accept-ranges": "bytes",
        "Content-encoding": "identity",
        "Content-length": str(file_size),
        "Access-control-expose-headers": (
            "Content-type, Accept-ranges, Content-length, "
            "Content-range, Content-encoding"
        ),
    }
    start = 0
    end = file_size - 1
    status_code = status.HTTP_200_OK

    if range_header is not None:
        start, end = _get_range_header(range_header, file_size)
        size = end - start + 1
        headers["Content-length"] = str(size)
        headers["Content-range"] = f"bytes {start}-{end}/{file_size}"
        status_code = status.HTTP_206_PARTIAL_CONTENT

    return StreamingResponse(
        send_bytes_range_requests(open(file_path, mode="rb"), start, end),
        headers=headers,
        status_code=status_code,
    )
