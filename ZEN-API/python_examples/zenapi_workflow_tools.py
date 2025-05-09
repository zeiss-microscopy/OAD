# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_workflow_tools.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################
# import asyncio
# import sys
# import os
from zen_api.workflows.v3beta import (
    JobTemplateInfo,
    WorkflowServiceStub,
    WorkflowServiceGetAvailableJobTemplatesRequest,
    WorkflowServiceIsJobTemplateLoadedRequest,
    WorkflowServiceIsJobRunningRequest,
    WorkflowServiceRunJobRequest,
    JobStatus,
    WorkflowServiceGetStatusRequest,
    WorkflowServiceRegisterOnStatusChangedRequest,
    WorkflowServiceLoadJobTemplateRequest,
)

from zen_api.workflows.v1beta import (
    JobResourcesServiceStub,
    JobResourcesServiceSetIntegerValueRequest,
    JobResourcesServiceSetFloatValueRequest,
    JobResourcesServiceGetAvailableResourcesRequest,
    # JobResourcesServiceSetDoubleValueRequest,
    JobResourcesServiceSetBooleanValueRequest,
    JobResourcesServiceSetStringValueRequest,
    # JobResourcesServiceGetLongValueRequest
)

from zenapi_tools import set_logging
from typing import List, Optional, Dict

logger = set_logging()


def print_job_template(job_template: JobTemplateInfo) -> None:
    """
    Prints the details of a job template.

    Parameters:
        job_template (JobTemplateInfo): The job template to print.

    Returns:
        None
    """
    print(f"    - {job_template.name}:")
    print(f"        - Description: {job_template.description}")
    print(f"        - Category: {job_template.category}")
    print(f"        - Subcategory: {job_template.subcategory}")


async def get_job_templates(
    workflow_service: WorkflowServiceStub, category="", subcategory=""
) -> List[JobTemplateInfo]:
    """
    Retrieves the available job templates from the workflow service.

    Args:
        workflow_service (WorkflowServiceStub): The workflow service to retrieve job templates from.
        category (str, optional): The category of job templates to filter by. Defaults to "".
        subcategory (str, optional): The subcategory of job templates to filter by. Defaults to "".

    Returns:
        List[JobTemplateInfo]: A list of available job templates.
    """
    response = await workflow_service.get_available_job_templates(
        WorkflowServiceGetAvailableJobTemplatesRequest(
            category=category, subcategory=subcategory
        )
    )
    return response.job_templates


async def get_all_job_templates(workflow_service: WorkflowServiceStub) -> None:
    """
    Asynchronously retrieves all job templates from the specified workflow service.
    Parameters:
    - workflow_service (WorkflowServiceStub): The workflow service to retrieve job templates from.
    Returns:
    None
    """
    job_templates = await get_job_templates(workflow_service)

    print("All job templates:")
    for job_template in job_templates:
        print_job_template(job_template)
    print()


async def get_zen_api_job_templates(workflow_service: WorkflowServiceStub):
    """
    Retrieves the ZEN API job templates from the specified workflow service.
    Parameters:
    - workflow_service (WorkflowServiceStub): The workflow service to retrieve the job templates from.
    Returns:
    - List[JobTemplate]: A list of ZEN API job templates.
    Raises:
    - SomeException: If an error occurs while retrieving the job templates.
    """
    job_templates = await get_job_templates(workflow_service, category="ZEN API")

    print("ZEN API job templates:")
    for job_template in job_templates:
        print_job_template(job_template)
    print()


async def get_resource_ids(job_resources_service: JobResourcesServiceStub) -> List[str]:
    """
    Retrieves the available resource IDs from the job resources service.

    Parameters:
    - job_resources_service (JobResourcesServiceStub): The job resources service to retrieve resource IDs from.

    Returns:
    - List[str]: A list of available resource IDs.
    """
    response = await job_resources_service.get_available_resources(
        JobResourcesServiceGetAvailableResourcesRequest()
    )
    return response.resource_ids


async def is_job_template_loaded(workflow_service: WorkflowServiceStub) -> bool:
    """
    Check if the job template is loaded.

    Parameters:
    - workflow_service (WorkflowServiceStub): The workflow service stub.

    Returns:
    - bool: True if the job template is loaded, False otherwise.
    """
    request = WorkflowServiceIsJobTemplateLoadedRequest()
    response = await workflow_service.is_job_template_loaded(request)
    return response.is_job_template_loaded


async def is_job_running(workflow_service: WorkflowServiceStub) -> bool:
    """
    Check if a job is currently running.

    Parameters:
    - workflow_service (WorkflowServiceStub): The workflow service stub.

    Returns:
    - bool: True if a job is running, False otherwise.
    """
    request = WorkflowServiceIsJobRunningRequest()
    response = await workflow_service.is_job_running(request)
    return response.is_job_running


async def get_status(workflow_service: WorkflowServiceStub) -> JobStatus:
    """
    Get the status of a job using the provided workflow service.

    Parameters:
    - workflow_service (WorkflowServiceStub): The workflow service to use for retrieving the status.

    Returns:
    - JobStatus: The status of the job.
    """
    request = WorkflowServiceGetStatusRequest()
    response = await workflow_service.get_status(request)
    return response.job_status


async def monitor_status(workflow_service: WorkflowServiceStub) -> None:
    """
    Monitors the status of a workflow.
    Args:
        workflow_service (WorkflowServiceStub): The workflow service stub.
    Returns:
        None
    """
    request = WorkflowServiceRegisterOnStatusChangedRequest()
    async for response in workflow_service.register_on_status_changed(
        request, timeout=10
    ):
        logger.info(f"--> Status changed to: {response.job_status}")

        if response.job_status == JobStatus.NOT_LOADED:
            break


async def run_job(
    workflow_service: WorkflowServiceStub,
    job_template_name: str,
    job_resources_service: Optional[JobResourcesServiceStub] = None,
    parameters: Optional[Dict] = None,
    result_path: Optional[str] = None,
    verbose: bool = False,
) -> None:
    """
    Runs a job using the specified workflow service and job template.
    Args:
        workflow_service (WorkflowServiceStub): The workflow service to use for running the job.
        job_template_name (str): The name of the job template to load.
        job_resources_service (Optional[JobResourcesServiceStub], optional): The job resources service to use for modifying job parameters. Defaults to None.
        parameters (Optional[Dict], optional): The parameters to modify in the job template. Defaults to None.
        result_path (Optional[str], optional): The result path for the job template. Defaults to None.
        verbose (bool, optional): Whether to log additional information during the job execution. Defaults to False.
    Raises:
        TypeError: If the type of a parameter is not supported.
    Returns:
        None: This function does not return anything.
    """

    # Initial status
    if verbose:
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

    # show the resource_ids of the current job
    resources_ids = await get_job_resource_ids(job_resources_service)

    for id in resources_ids:
        logger.info(f"ResourceId found: {id}")

    # modify job parameters
    if parameters is not None:

        for k, v in parameters.items():

            if k in resources_ids:

                if isinstance(v, int):

                    request = JobResourcesServiceSetIntegerValueRequest(
                        resource_id=k, value=v
                    )
                    await job_resources_service.set_integer_value(request)

                elif isinstance(v, float):

                    request = JobResourcesServiceSetFloatValueRequest(
                        resource_id=k, value=v
                    )
                    await job_resources_service.set_float_value(request)

                elif isinstance(v, bool):

                    request = JobResourcesServiceSetBooleanValueRequest(
                        resource_id=k, value=v
                    )
                    await job_resources_service.set_boolean_value(request)

                elif isinstance(v, str):

                    request = JobResourcesServiceSetStringValueRequest(
                        resource_id=k, value=v
                    )
                    await job_resources_service.set_string_value(request)

                else:
                    raise TypeError(f"The type of {k} is not supported")

                logger.info(f"Updated parameter: {k} --> {v}")

    if verbose:
        loaded = await is_job_template_loaded(workflow_service)
        logger.info(f"Is job template loaded: {loaded}")

        status = await get_status(workflow_service)
        logger.info(f"Status after loading the job template: {status}")

        # Run job
        running = await is_job_running(workflow_service)
        logger.info(f"Is job running: {running}")

    logger.info("Running loaded job template...")
    request = WorkflowServiceRunJobRequest()
    await workflow_service.run_job(request)
    logger.info("Job execution completed")

    if verbose:
        loaded = await is_job_template_loaded(workflow_service)
        logger.info(f"Is job template loaded: {loaded}")

        running = await is_job_running(workflow_service)
        logger.info(f"Is job running: {running}")

        status = await get_status(workflow_service)
        logger.info(f"Status after running the loaded job template: {status}")


async def get_job_resource_ids(
    job_resources_service: JobResourcesServiceGetAvailableResourcesRequest,
) -> List[str]:
    """
    Retrieves the resource IDs of the current job.
    Parameters:
    - job_resources_service: An instance of JobResourcesServiceGetAvailableResourcesRequest.
    Returns:
    - A list of resource IDs.
    """

    # show the resource_ids of the current job
    resources = await job_resources_service.get_available_resources(
        JobResourcesServiceGetAvailableResourcesRequest()
    )

    return resources.resources
