"""Asynchronous helpers for ZEN pixel-stream consumers."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterable, AsyncIterator
from typing import Any


async def merge_channel_streams(
    streams: list[tuple[int, AsyncIterable[Any]]],
) -> AsyncIterator[tuple[int, Any]]:
    """Merge channel streams while preserving the source channel index."""
    iterators = [(channel, stream.__aiter__()) for channel, stream in streams]
    tasks = {asyncio.create_task(iterator.__anext__()): (channel, iterator) for channel, iterator in iterators}
    try:
        while tasks:
            done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                channel, iterator = tasks.pop(task)
                try:
                    response = task.result()
                except StopAsyncIteration:
                    continue
                tasks[asyncio.create_task(iterator.__anext__())] = (channel, iterator)
                yield channel, response
    finally:
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)


async def close_async_iterator(iterator: AsyncIterator[Any]) -> None:
    """Close an asynchronous iterator when it supports ``aclose``."""
    close = getattr(iterator, "aclose", None)
    if close is not None:
        await close()
