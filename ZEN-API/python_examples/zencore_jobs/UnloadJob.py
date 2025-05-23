import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zen_api.workflows.v3beta import (
    WorkflowServiceStub,
    WorkflowServiceLoadJobTemplateRequest,
    WorkflowServiceUnloadJobTemplateRequest,
)
from zenapi_tools import initialize_zenapi, set_logging
from zenapi_workflow_tools import is_job_template_loaded


async def main():
    job_template_name = "ZEN-API Job"
    result_path = r"C:\Temp\job_result"

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi("config.ini")

    workflow_service = WorkflowServiceStub(channel=channel, metadata=metadata)

    # Load template to sandbox
    loaded = await is_job_template_loaded(workflow_service)
    logger.info(f"Is job template loaded: {loaded}")

    logger.info(f"Loading job template: {job_template_name}")
    request = WorkflowServiceLoadJobTemplateRequest(job_template_name)
    await workflow_service.load_job_template(request)

    loaded = await is_job_template_loaded(workflow_service)
    logger.info(f"Is job template loaded: {loaded}")

    # Unload job template
    logger.info("Unloading job template...")
    request = WorkflowServiceUnloadJobTemplateRequest()
    await workflow_service.unload_job_template(request)

    loaded = await is_job_template_loaded(workflow_service)
    logger.info(f"Is job template loaded: {loaded}")

    # Load template to custom folder
    logger.info(
        f'Loading job template "{job_template_name}" with result path "{result_path}"'
    )
    request = WorkflowServiceLoadJobTemplateRequest(job_template_name, result_path)
    await workflow_service.load_job_template(request)

    loaded = await is_job_template_loaded(workflow_service)
    logger.info(f"Is job template loaded: {loaded}")

    # Unload job template
    logger.info("Unloading job template...")
    request = WorkflowServiceUnloadJobTemplateRequest()
    await workflow_service.unload_job_template(request)

    loaded = await is_job_template_loaded(workflow_service)
    logger.info(f"Is job template loaded: {loaded}")

    channel.close()


if __name__ == "__main__":
    logger = set_logging()
    asyncio.run(main())
