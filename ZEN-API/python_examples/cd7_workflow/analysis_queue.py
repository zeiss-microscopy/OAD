#################################################################
# File        : analysis_queue.py
# Institution : Carl Zeiss Microscopy GmbH
#
# Decouples image analysis from microscope control via an asyncio.Queue.
#
# Design:
#   Acquisition loop                 Background pipeline
#   ----------------                 -------------------
#   run_acquisition()
#          |
#          +-- create_task() ------> wait_for_file_ready()
#          |                          queue.put(czi_path)
#          |                                  |
#   continue with next well             analysis_worker()
#                                             |
#                                      queue.task_done()
#
# File polling yields through asyncio.sleep(), and run_analysis() dispatches its
# CPU-bound work to a thread. Microscope control therefore remains responsive while
# the previous CZI is analyzed.
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import asyncio
from pathlib import Path
from typing import NoReturn

from image_analysis import run_analysis
from tqdm import tqdm
from zen_api_utils.misc import set_logging

logger = set_logging()


# ---------------------------------------------------------------------------
# File-ready detection
# ---------------------------------------------------------------------------


async def wait_for_file_ready(
    czi_path: Path,
    poll_interval_s: float = 1.0,
    file_settle_s: float = 3.0,
) -> None:
    """
    Wait asynchronously until *czi_path* exists **and** its size has been
    stable for at least *file_settle_s* seconds.

    A stable file size is used as a portable indication that writing has
    finished. This works on local and mapped network drives without an
    OS-specific file watcher.

    Args:
        czi_path: Path to the CZI file that ZEN is writing.
        poll_interval_s: Interval between file-size checks (seconds).
        file_settle_s: Duration for which the file size must remain unchanged
            before the file is considered fully written (seconds).
    """
    logger.info(f"Waiting for file to appear: {czi_path}")

    # Acquisition may return before a network share exposes the new file.
    while not czi_path.exists():
        await asyncio.sleep(poll_interval_s)

    logger.info(f"File detected, waiting for write to complete: {czi_path}")

    # Seeing the file is not enough: ZEN may still be appending image data.
    last_size: int = -1
    stable_since: float | None = None
    loop = asyncio.get_event_loop()

    while True:
        try:
            current_size = czi_path.stat().st_size
        except OSError:
            # File briefly disappeared (e.g. ZEN is replacing it) — retry
            await asyncio.sleep(poll_interval_s)
            continue

        now = loop.time()

        if current_size == last_size:
            if stable_since is None:
                stable_since = now
            elif (now - stable_since) >= file_settle_s:
                break  # Size unchanged for long enough: the file is ready.
        else:
            # File is still growing
            stable_since = None
            last_size = current_size

        await asyncio.sleep(poll_interval_s)

    size_mb = czi_path.stat().st_size / 1_048_576
    logger.info(f"File ready ({size_mb:.1f} MB): {czi_path}")


# ---------------------------------------------------------------------------
# Non-blocking enqueue helper
# ---------------------------------------------------------------------------


async def enqueue_when_ready(
    queue: asyncio.Queue[Path],
    czi_path: Path,
    poll_interval_s: float = 1.0,
    file_settle_s: float = 3.0,
) -> None:
    """
    Wait until *czi_path* is fully written to disk, then put it on *queue*.

    This coroutine is meant to be launched as a :func:`asyncio.create_task`
    so that waiting for the file never blocks the acquisition loop.

    Args:
        queue: The analysis job queue shared with :func:`analysis_worker`.
        czi_path: Path to the CZI file being monitored.
        poll_interval_s: Forwarded to :func:`wait_for_file_ready`.
        file_settle_s: Forwarded to :func:`wait_for_file_ready`.
    """
    await wait_for_file_ready(czi_path, poll_interval_s, file_settle_s)
    await queue.put(czi_path)
    logger.info(f"Enqueued for analysis: {czi_path.name}")


# ---------------------------------------------------------------------------
# Background analysis worker
# ---------------------------------------------------------------------------


async def analysis_worker(
    queue: asyncio.Queue[Path],
    results: list[dict[str, str | int]],
    pbar: "tqdm[NoReturn] | None" = None,
) -> None:
    """
    Continuously consume CZI paths from *queue*,
    runs image analysis for each one, and appends per-plane result rows
    to the shared *results* list.

    Each row contains:
        - ``well_id``      : well label extracted from the CZI filename
          (e.g. ``"A1"`` from ``A1_20260225_143022.czi``)
        - ``czi_file``     : CZI filename (stem only, no extension)
        - ``z_plane``      : 0-based z-plane index
        - ``object_count`` : number of segmented objects on that plane
        - ``status``       : ``"ok"`` or ``"error: <message>"``

    Args:
        queue: Shared :class:`asyncio.Queue` populated by
            :func:`enqueue_when_ready`.
        results: Shared list that receives one ``dict`` per (well, z-plane).
            Because asyncio is single-threaded this list is safe to append
            to without a lock.
        pbar: Optional :class:`tqdm.tqdm` progress bar.  When provided it is
            advanced by 1 after every completed (or failed) job so the caller
            can track analysis progress independently of acquisition.
    """
    logger.info("Analysis worker started — waiting for jobs ...")

    while True:
        czi_path: Path = await queue.get()

        # Remove the final date and time fields:
        # "A1_20260225_143022.czi" -> "A1". Joining the preceding fields also
        # supports well identifiers that contain underscores.
        stem_parts = czi_path.stem.split("_")
        well_id = "_".join(stem_parts[:-2]) if len(stem_parts) > 2 else czi_path.stem

        try:
            # One queue item represents one CZI; run_analysis returns one count
            # for every Z-plane in that file.
            counts: list[int] = await run_analysis(
                czi_path,
                measure_properties=("label", "area", "centroid", "bbox"),
            )
            logger.info(f"Analysis completed for {czi_path.name}: {counts}")

            for z_plane, count in enumerate(counts):
                results.append(
                    {
                        "well_id": well_id,
                        "czi_file": czi_path.stem,
                        "z_plane": z_plane,
                        "object_count": count,
                        "status": "ok",
                    }
                )

        except asyncio.CancelledError:
            # Do not convert shutdown into an analysis-error row. The finally
            # block still balances the queue item before cancellation propagates.
            raise

        except (IndexError, OSError, RuntimeError, TypeError, ValueError) as exc:
            logger.error(f"Analysis worker FAILED for {czi_path.name}: {exc}")
            # Preserve failed wells in the CSV instead of silently dropping them.
            results.append(
                {
                    "well_id": well_id,
                    "czi_file": czi_path.stem,
                    "z_plane": -1,
                    "object_count": -1,
                    "status": f"error: {exc}",
                }
            )

        finally:
            # queue.join() in the orchestrator can return only after every item
            # retrieved with queue.get() has a matching task_done() call.
            queue.task_done()
            if pbar is not None:
                pbar.update(1)
