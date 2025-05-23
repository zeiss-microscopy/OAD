import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zenapi_tools import initialize_zenapi, set_logging
from zenapi_workflow_tools import get_all_job_templates, get_zen_api_job_templates
from public.zen_api.workflows.v3beta import WorkflowServiceStub


async def main():

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi("config.ini")
    workflow_service = WorkflowServiceStub(channel=channel, metadata=metadata)

    await get_all_job_templates(workflow_service)
    await get_zen_api_job_templates(workflow_service)

    channel.close()


if __name__ == "__main__":
    logger = set_logging()
    asyncio.run(main())
