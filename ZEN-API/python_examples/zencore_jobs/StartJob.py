import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zen_api.workflows.v3beta import (
    WorkflowServiceStub,
    WorkflowServiceStartJobRequest,
    WorkflowServiceWaitJobRequest,
    WorkflowServiceLoadJobTemplateRequest,
)
from zenapi_tools import initialize_zenapi, set_logging
from zenapi_workflow_tools import (
    is_job_running,
    is_job_template_loaded,
    get_status,
    monitor_status,
)
from typing import Optional


async def start_job(
    workflow_service: WorkflowServiceStub,
    job_template_name: Optional[str] = None,
    result_path: Optional[str] = None,
) -> None:
    # Initial status
    status = await get_status(workflow_service)
    logger.info(f"Initial status: {status}")

    # Load template to sandbox
    loaded = await is_job_template_loaded(workflow_service)
    logger.info(f"Is job template loaded: {loaded}")

    if result_path is None:
        logger.info(f"Loading job template: {job_template_name}")
    else:
        logger.info(
            f'Loading job template "{job_template_name}" with result path "{result_path}"'
        )
    request = WorkflowServiceLoadJobTemplateRequest(job_template_name, result_path)
    await workflow_service.load_job_template(request)

    loaded = await is_job_template_loaded(workflow_service)
    logger.info(f"Is job template loaded: {loaded}")

    status = await get_status(workflow_service)
    logger.info(f"Status after loading the job template: {status}")

    # Run job
    running = await is_job_running(workflow_service)
    logger.info(f"Is job running: {running}")

    logger.info("Starting loaded job template...")
    request = WorkflowServiceStartJobRequest()
    await workflow_service.start_job(request)
    logger.info("Job started")

    loaded = await is_job_template_loaded(workflow_service)
    logger.info(f"Is job template loaded: {loaded}")

    running = await is_job_running(workflow_service)
    logger.info(f"Is job running: {running}")

    status = await get_status(workflow_service)
    logger.info(f"Status after running the loaded job template: {status}")

    # Wait for the job to finish
    logger.info("Waiting for job to finish...")
    request = WorkflowServiceWaitJobRequest()
    await workflow_service.wait_job(request)

    loaded = await is_job_template_loaded(workflow_service)
    logger.info(f"Is job template loaded: {loaded}")

    running = await is_job_running(workflow_service)
    logger.info(f"Is job running: {running}")

    status = await get_status(workflow_service)
    logger.info(f"Status after waiting for the job to finish: {status}")


async def main():
    job_template_name = "ZEN-API Job"
    result_path = r"C:\Temp\job_result"

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi("config.ini")
    workflow_service = WorkflowServiceStub(channel=channel, metadata=metadata)

    # use the archive
    start_job_task = start_job(workflow_service, job_template_name)
    monitor_status_task = monitor_status(workflow_service)
    await asyncio.gather(monitor_status_task, start_job_task)

    # use a custom folder
    start_job_task = start_job(workflow_service, job_template_name, result_path)
    monitor_status_task = monitor_status(workflow_service)
    await asyncio.gather(monitor_status_task, start_job_task)

    channel.close()


if __name__ == "__main__":
    logger = set_logging()
    asyncio.run(main())
