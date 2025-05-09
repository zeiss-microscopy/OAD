import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from Connection import Connection
from zenapi_tools import initialize_zenapi, set_logging
from zen_api.workflows.v3beta import WorkflowServiceStub
from zen_api.workflows.v1beta import (
    JobResourcesServiceStub,
)

from zenapi_workflow_tools import monitor_status, run_job

#########################
#
# ZEN core job are typically stored here: C:\ProgramData\Carl Zeiss\ZENCore\UserArchive\Templates
#
# ZEN core must run in ZEN API mode !!!
#
#########################


async def main():
    job_template_name = "ZEN-API Job"
    result_path = r"C:\Temp\job_result"

    # job parameters to be modified. Set to None or leave out to run job w/o modification
    params = {"res_image_processing_sigma_x": 50, "res_image_processing_sigma_y": 1}

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi("config.ini")

    workflow_service = WorkflowServiceStub(channel=channel, metadata=metadata)
    job_resources_service = JobResourcesServiceStub(channel=channel, metadata=metadata)

    run_job_task = run_job(
        workflow_service,
        job_template_name,
        job_resources_service,  # optional parameter
        parameters=params,  # optional parameter
        result_path=result_path,  # optional parameter
        verbose=True,  # optional parameter
    )

    # monitor_status_task = monitor_status(workflow_service)
    # await asyncio.gather(monitor_status_task, run_job_task)

    # short version without monitoring
    await asyncio.gather(run_job_task)

    channel.close()


if __name__ == "__main__":
    logger = set_logging()
    asyncio.run(main())
