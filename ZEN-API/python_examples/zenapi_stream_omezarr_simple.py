"""Run experiment-driven OME-Zarr streaming with optional post-processing.

Set ``PYRAMID_LEVELS`` to:
    - 0 to disable post-acquisition pyramid creation.
    - 1 to create a 2x Y/X level.
    - 2 to create 2x and 4x Y/X levels.
    - 3 to create 2x, 4x, and 8x Y/X levels.

Level 0 is written and sharded during acquisition. Pyramid generation runs
after acquisition and writes only levels 1..N. Set
``SPATIAL_SHARD_SIZE_CHUNKS`` to ``None`` to disable sharding for all levels.
"""

import asyncio
from pathlib import Path

from zenapi_stream2omezarr_experiment import stream_experiment

script_dir = Path(__file__).resolve().parent

PYRAMID_LEVELS = 3
SPATIAL_SHARD_SIZE_CHUNKS = 2


def main() -> None:
    """Run the configured example acquisition."""
    output = asyncio.run(
        stream_experiment(
            "ZEN_API_OMEZARR_Stream_Wellplate",
            zenapi_config=script_dir / "my_config.ini",
            output_dir=Path(r"F:\Zen_Output\streaming"),
            start_experiment=False,
            channel_index=None,
            spatial_shard_size_chunks=SPATIAL_SHARD_SIZE_CHUNKS,
            pyramid_levels=PYRAMID_LEVELS,
            validate_ome_zarr=True,
        )
    )
    print(output)


if __name__ == "__main__":
    main()
