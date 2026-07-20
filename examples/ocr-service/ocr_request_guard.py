"""Input and concurrency guard for a synthetic OCR endpoint."""

import asyncio
from dataclasses import dataclass


ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}


@dataclass(frozen=True)
class Upload:
    filename: str
    content: bytes


class OcrGuard:
    def __init__(self, max_bytes: int = 10 * 1024 * 1024) -> None:
        self.max_bytes = max_bytes
        self._semaphore = asyncio.Semaphore(1)

    def validate(self, upload: Upload) -> None:
        suffix = "." + upload.filename.rsplit(".", 1)[-1].lower()
        if suffix not in ALLOWED_EXTENSIONS:
            raise ValueError("unsupported file extension")
        if not upload.content:
            raise ValueError("empty file")
        if len(upload.content) > self.max_bytes:
            raise ValueError("file too large")

    async def infer(self, upload: Upload, engine) -> str:
        self.validate(upload)
        async with self._semaphore:
            return await engine(upload.content)
