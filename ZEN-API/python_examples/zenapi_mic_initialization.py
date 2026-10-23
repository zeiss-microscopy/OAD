import asyncio
import sys
from pathlib import Path

from grpclib import GRPCError
from grpclib.const import Status

# import the auto-generated python modules
from zen_api.lm.hardware.v1 import (
    MicroscopeServiceGetFocusStateRequest,
    MicroscopeServiceGetFocusStateResponse,
    MicroscopeServiceGetStageStateRequest,
    MicroscopeServiceGetStageStateResponse,
    MicroscopeServiceGetStateRequest,
    MicroscopeServiceGetStateResponse,
    MicroscopeServiceStartInitializationRequest,
    MicroscopeServiceStub,
)
from zen_api_utils.misc import initialize_zenapi, set_logging

# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
# config_path = script_dir / "config.ini"
config_path = script_dir / "my_config.ini"


async def main(args):
    del args

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(config_path)

    # get services
    microscope_service = MicroscopeServiceStub(channel=channel, metadata=metadata)

    try:

        # check if microscope is already initialized
        mic_state_response: MicroscopeServiceGetStateResponse = await microscope_service.get_state(
            MicroscopeServiceGetStateRequest()
        )

        if mic_state_response.is_initialized:
            logger.info("Microscope is already initialized.")

            # check if focus is already calibrated
            try:
                focus_state_response: MicroscopeServiceGetFocusStateResponse = await microscope_service.get_focus_state(
                    MicroscopeServiceGetFocusStateRequest()
                )
            except GRPCError as exc:
                if exc.status != Status.FAILED_PRECONDITION:
                    raise
                logger.warning(f"Focus calibration state is unavailable on this microscope: {exc}")
            else:
                if focus_state_response.is_calibrated:
                    logger.info("Focus is already calibrated.")
                else:
                    logger.warning("Focus is not calibrated.")

            try:
                stage_state_response: MicroscopeServiceGetStageStateResponse = await microscope_service.get_stage_state(
                    MicroscopeServiceGetStageStateRequest()
                )
            except GRPCError as exc:
                if exc.status != Status.FAILED_PRECONDITION:
                    raise
                logger.warning(f"Stage calibration state is unavailable on this microscope: {exc}")
            else:
                if stage_state_response.is_calibrated:
                    logger.info("Stage is already calibrated.")
                else:
                    logger.warning("Stage is not calibrated.")

            return

        logger.info("Microscope is not initialized. Starting initialization...")
        init_response = await microscope_service.start_initialization(MicroscopeServiceStartInitializationRequest())
        logger.info(f"Microscope initialization started: {init_response}")
    finally:
        channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
