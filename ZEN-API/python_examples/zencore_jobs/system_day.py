import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zen_api.workflows.v3beta import (
    WorkflowServiceStub,
    WorkflowServiceGetAvailableJobTemplatesRequest,
)

from zenapi_tools import initialize_zenapi


async def main():

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi("config.ini")
    workflow_service = WorkflowServiceStub(channel=channel, metadata=metadata)

    response = await workflow_service.get_available_job_templates(
        WorkflowServiceGetAvailableJobTemplatesRequest(category="", subcategory="")
    )

    for job_template in response.job_templates:
        print(f"- {job_template.name}:")
        print(f"    - Description: {job_template.description}")
        print(f"    - Category: {job_template.category}")
        print(f"    - Subcategory: {job_template.subcategory}")


if __name__ == "__main__":
    asyncio.run(main())
