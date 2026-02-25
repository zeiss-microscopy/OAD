# ZEN API Documentation

ZEN Release 3.14 - Spring 2026 Version:-2026.05.1

## Table of Contents

- [zen\_api/acquisition/v1beta/experiment\_descriptor.proto](#zen_api/acquisition/v1beta/experiment_descriptor.proto)
  - [ExperimentDescriptor](#zen_api.acquisition.v1beta.ExperimentDescriptor)
- [zen\_api/acquisition/v1beta/experiment\_service.proto](#zen_api/acquisition/v1beta/experiment_service.proto)
  - [ExperimentServiceCloneRequest](#zen_api.acquisition.v1beta.ExperimentServiceCloneRequest)
  - [ExperimentServiceCloneResponse](#zen_api.acquisition.v1beta.ExperimentServiceCloneResponse)
  - [ExperimentServiceDeleteRequest](#zen_api.acquisition.v1beta.ExperimentServiceDeleteRequest)
  - [ExperimentServiceDeleteResponse](#zen_api.acquisition.v1beta.ExperimentServiceDeleteResponse)
  - [ExperimentServiceExportRequest](#zen_api.acquisition.v1beta.ExperimentServiceExportRequest)
  - [ExperimentServiceExportResponse](#zen_api.acquisition.v1beta.ExperimentServiceExportResponse)
  - [ExperimentServiceGetAvailableExperimentsRequest](#zen_api.acquisition.v1beta.ExperimentServiceGetAvailableExperimentsRequest)
  - [ExperimentServiceGetAvailableExperimentsResponse](#zen_api.acquisition.v1beta.ExperimentServiceGetAvailableExperimentsResponse)
  - [ExperimentServiceGetImageOutputPathRequest](#zen_api.acquisition.v1beta.ExperimentServiceGetImageOutputPathRequest)
  - [ExperimentServiceGetImageOutputPathResponse](#zen_api.acquisition.v1beta.ExperimentServiceGetImageOutputPathResponse)
  - [ExperimentServiceGetStatusRequest](#zen_api.acquisition.v1beta.ExperimentServiceGetStatusRequest)
  - [ExperimentServiceGetStatusResponse](#zen_api.acquisition.v1beta.ExperimentServiceGetStatusResponse)
  - [ExperimentServiceImportRequest](#zen_api.acquisition.v1beta.ExperimentServiceImportRequest)
  - [ExperimentServiceImportResponse](#zen_api.acquisition.v1beta.ExperimentServiceImportResponse)
  - [ExperimentServiceLoadRequest](#zen_api.acquisition.v1beta.ExperimentServiceLoadRequest)
  - [ExperimentServiceLoadResponse](#zen_api.acquisition.v1beta.ExperimentServiceLoadResponse)
  - [ExperimentServiceRegisterOnStatusChangedRequest](#zen_api.acquisition.v1beta.ExperimentServiceRegisterOnStatusChangedRequest)
  - [ExperimentServiceRegisterOnStatusChangedResponse](#zen_api.acquisition.v1beta.ExperimentServiceRegisterOnStatusChangedResponse)
  - [ExperimentServiceRunExperimentRequest](#zen_api.acquisition.v1beta.ExperimentServiceRunExperimentRequest)
  - [ExperimentServiceRunExperimentResponse](#zen_api.acquisition.v1beta.ExperimentServiceRunExperimentResponse)
  - [ExperimentServiceRunSnapRequest](#zen_api.acquisition.v1beta.ExperimentServiceRunSnapRequest)
  - [ExperimentServiceRunSnapResponse](#zen_api.acquisition.v1beta.ExperimentServiceRunSnapResponse)
  - [ExperimentServiceSaveRequest](#zen_api.acquisition.v1beta.ExperimentServiceSaveRequest)
  - [ExperimentServiceSaveResponse](#zen_api.acquisition.v1beta.ExperimentServiceSaveResponse)
  - [ExperimentServiceStartContinuousRequest](#zen_api.acquisition.v1beta.ExperimentServiceStartContinuousRequest)
  - [ExperimentServiceStartExperimentRequest](#zen_api.acquisition.v1beta.ExperimentServiceStartExperimentRequest)
  - [ExperimentServiceStartExperimentResponse](#zen_api.acquisition.v1beta.ExperimentServiceStartExperimentResponse)
  - [ExperimentServiceStartLiveRequest](#zen_api.acquisition.v1beta.ExperimentServiceStartLiveRequest)
  - [ExperimentServiceStartSnapRequest](#zen_api.acquisition.v1beta.ExperimentServiceStartSnapRequest)
  - [ExperimentServiceStartSnapResponse](#zen_api.acquisition.v1beta.ExperimentServiceStartSnapResponse)
  - [ExperimentServiceStopRequest](#zen_api.acquisition.v1beta.ExperimentServiceStopRequest)
  - [ExperimentServiceStopResponse](#zen_api.acquisition.v1beta.ExperimentServiceStopResponse)
  - [ExperimentService](#zen_api.acquisition.v1beta.ExperimentService)
- [zen\_api/acquisition/v1beta/experiment\_status.proto](#zen_api/acquisition/v1beta/experiment_status.proto)
  - [ExperimentStatus](#zen_api.acquisition.v1beta.ExperimentStatus)
- [zen\_api/acquisition/v1beta/experiment\_streaming\_service.proto](#zen_api/acquisition/v1beta/experiment_streaming_service.proto)
  - [ExperimentStreamingServiceMonitorAllExperimentsRequest](#zen_api.acquisition.v1beta.ExperimentStreamingServiceMonitorAllExperimentsRequest)
  - [ExperimentStreamingServiceMonitorAllExperimentsResponse](#zen_api.acquisition.v1beta.ExperimentStreamingServiceMonitorAllExperimentsResponse)
  - [ExperimentStreamingServiceMonitorExperimentRequest](#zen_api.acquisition.v1beta.ExperimentStreamingServiceMonitorExperimentRequest)
  - [ExperimentStreamingServiceMonitorExperimentResponse](#zen_api.acquisition.v1beta.ExperimentStreamingServiceMonitorExperimentResponse)
  - [ExperimentStreamingService](#zen_api.acquisition.v1beta.ExperimentStreamingService)
- [zen\_api/acquisition/v1beta/frame\_data.proto](#zen_api/acquisition/v1beta/frame_data.proto)
  - [FrameData](#zen_api.acquisition.v1beta.FrameData)
- [zen\_api/acquisition/v1beta/frame\_pixel\_data.proto](#zen_api/acquisition/v1beta/frame_pixel_data.proto)
  - [FramePixelData](#zen_api.acquisition.v1beta.FramePixelData)
- [zen\_api/acquisition/v1beta/frame\_position.proto](#zen_api/acquisition/v1beta/frame_position.proto)
  - [FramePosition](#zen_api.acquisition.v1beta.FramePosition)
- [zen\_api/acquisition/v1beta/frame\_stage\_position.proto](#zen_api/acquisition/v1beta/frame_stage_position.proto)
  - [FrameStagePosition](#zen_api.acquisition.v1beta.FrameStagePosition)
- [zen\_api/acquisition/v1beta/pixel\_type.proto](#zen_api/acquisition/v1beta/pixel_type.proto)
  - [PixelType](#zen_api.acquisition.v1beta.PixelType)
- [zen\_api/acquisition/v1beta/scaling.proto](#zen_api/acquisition/v1beta/scaling.proto)
  - [Scaling](#zen_api.acquisition.v1beta.Scaling)
- [zen\_api/application/v1/composition\_service.proto](#zen_api/application/v1/composition_service.proto)
  - [CompositionServiceCreateModuleRequest](#zen_api.application.v1.CompositionServiceCreateModuleRequest)
  - [CompositionServiceCreateModuleResponse](#zen_api.application.v1.CompositionServiceCreateModuleResponse)
  - [CompositionServiceIsModuleAvailableRequest](#zen_api.application.v1.CompositionServiceIsModuleAvailableRequest)
  - [IsModuleAvailableResponse](#zen_api.application.v1.IsModuleAvailableResponse)
  - [CompositionService](#zen_api.application.v1.CompositionService)
- [zen\_api/common/v1/double\_frame.proto](#zen_api/common/v1/double_frame.proto)
  - [DoubleFrame](#zen_api.common.v1.DoubleFrame)
- [zen\_api/common/v1/double\_point.proto](#zen_api/common/v1/double_point.proto)
  - [DoublePoint](#zen_api.common.v1.DoublePoint)
- [zen\_api/common/v1/double\_size.proto](#zen_api/common/v1/double_size.proto)
  - [DoubleSize](#zen_api.common.v1.DoubleSize)
- [zen\_api/common/v1/int\_point.proto](#zen_api/common/v1/int_point.proto)
  - [IntPoint](#zen_api.common.v1.IntPoint)
- [zen\_api/common/v1/int\_size.proto](#zen_api/common/v1/int_size.proto)
  - [IntSize](#zen_api.common.v1.IntSize)
- [zen\_api/hardware/v1/axis\_identifier.proto](#zen_api/hardware/v1/axis_identifier.proto)
  - [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier)
- [zen\_api/hardware/v1/simple\_stage\_service.proto](#zen_api/hardware/v1/simple_stage_service.proto)
  - [SimpleStageServiceGetAccelerationRequest](#zen_api.hardware.v1.SimpleStageServiceGetAccelerationRequest)
  - [SimpleStageServiceGetAccelerationResponse](#zen_api.hardware.v1.SimpleStageServiceGetAccelerationResponse)
  - [SimpleStageServiceGetPositionRequest](#zen_api.hardware.v1.SimpleStageServiceGetPositionRequest)
  - [SimpleStageServiceGetPositionResponse](#zen_api.hardware.v1.SimpleStageServiceGetPositionResponse)
  - [SimpleStageServiceGetSpeedRequest](#zen_api.hardware.v1.SimpleStageServiceGetSpeedRequest)
  - [SimpleStageServiceGetSpeedResponse](#zen_api.hardware.v1.SimpleStageServiceGetSpeedResponse)
  - [SimpleStageServiceMoveToRequest](#zen_api.hardware.v1.SimpleStageServiceMoveToRequest)
  - [SimpleStageServiceMoveToResponse](#zen_api.hardware.v1.SimpleStageServiceMoveToResponse)
  - [SimpleStageServiceSetAccelerationRequest](#zen_api.hardware.v1.SimpleStageServiceSetAccelerationRequest)
  - [SimpleStageServiceSetAccelerationResponse](#zen_api.hardware.v1.SimpleStageServiceSetAccelerationResponse)
  - [SimpleStageServiceSetSpeedRequest](#zen_api.hardware.v1.SimpleStageServiceSetSpeedRequest)
  - [SimpleStageServiceSetSpeedResponse](#zen_api.hardware.v1.SimpleStageServiceSetSpeedResponse)
  - [SimpleStageServiceStopRequest](#zen_api.hardware.v1.SimpleStageServiceStopRequest)
  - [SimpleStageServiceStopResponse](#zen_api.hardware.v1.SimpleStageServiceStopResponse)
  - [SimpleStageService](#zen_api.hardware.v1.SimpleStageService)
- [zen\_api/hardware/v1/stage\_axis.proto](#zen_api/hardware/v1/stage_axis.proto)
  - [StageAxis](#zen_api.hardware.v1.StageAxis)
- [zen\_api/hardware/v1/stage\_motion\_state.proto](#zen_api/hardware/v1/stage_motion_state.proto)
  - [StageMotionState](#zen_api.hardware.v1.StageMotionState)
- [zen\_api/hardware/v1/stage\_service.proto](#zen_api/hardware/v1/stage_service.proto)
  - [StageServiceAxisVelocityResponse](#zen_api.hardware.v1.StageServiceAxisVelocityResponse)
  - [StageServiceGetAvailableStageAxisRequest](#zen_api.hardware.v1.StageServiceGetAvailableStageAxisRequest)
  - [StageServiceGetAvailableStageAxisResponse](#zen_api.hardware.v1.StageServiceGetAvailableStageAxisResponse)
  - [StageServiceGetAxisPositionRequest](#zen_api.hardware.v1.StageServiceGetAxisPositionRequest)
  - [StageServiceGetAxisPositionResponse](#zen_api.hardware.v1.StageServiceGetAxisPositionResponse)
  - [StageServiceGetAxisVelocityRequest](#zen_api.hardware.v1.StageServiceGetAxisVelocityRequest)
  - [StageServiceGetAxisVelocityResponse](#zen_api.hardware.v1.StageServiceGetAxisVelocityResponse)
  - [StageServiceGetStageMotionStateRequest](#zen_api.hardware.v1.StageServiceGetStageMotionStateRequest)
  - [StageServiceGetStageMotionStateResponse](#zen_api.hardware.v1.StageServiceGetStageMotionStateResponse)
  - [StageServiceGetStagePositionRequest](#zen_api.hardware.v1.StageServiceGetStagePositionRequest)
  - [StageServiceGetStagePositionResponse](#zen_api.hardware.v1.StageServiceGetStagePositionResponse)
  - [StageServiceGetStageStateRequest](#zen_api.hardware.v1.StageServiceGetStageStateRequest)
  - [StageServiceGetStageStateResponse](#zen_api.hardware.v1.StageServiceGetStageStateResponse)
  - [StageServiceGetStageVelocityRequest](#zen_api.hardware.v1.StageServiceGetStageVelocityRequest)
  - [StageServiceGetStageVelocityResponse](#zen_api.hardware.v1.StageServiceGetStageVelocityResponse)
  - [StageServiceInitializeStageRequest](#zen_api.hardware.v1.StageServiceInitializeStageRequest)
  - [StageServiceInitializeStageResponse](#zen_api.hardware.v1.StageServiceInitializeStageResponse)
  - [StageServiceMoveToRequest](#zen_api.hardware.v1.StageServiceMoveToRequest)
  - [StageServiceMoveToResponse](#zen_api.hardware.v1.StageServiceMoveToResponse)
  - [StageServiceRegisterOnStageMotionStateChangedRequest](#zen_api.hardware.v1.StageServiceRegisterOnStageMotionStateChangedRequest)
  - [StageServiceRegisterOnStageMotionStateChangedResponse](#zen_api.hardware.v1.StageServiceRegisterOnStageMotionStateChangedResponse)
  - [StageServiceRegisterOnStagePositionChangedRequest](#zen_api.hardware.v1.StageServiceRegisterOnStagePositionChangedRequest)
  - [StageServiceRegisterOnStagePositionChangedResponse](#zen_api.hardware.v1.StageServiceRegisterOnStagePositionChangedResponse)
  - [StageServiceRegisterOnStageStateChangedRequest](#zen_api.hardware.v1.StageServiceRegisterOnStageStateChangedRequest)
  - [StageServiceRegisterOnStageStateChangedResponse](#zen_api.hardware.v1.StageServiceRegisterOnStageStateChangedResponse)
  - [StageServiceRegisterOnStageVelocityChangedRequest](#zen_api.hardware.v1.StageServiceRegisterOnStageVelocityChangedRequest)
  - [StageServiceRegisterOnStageVelocityChangedResponse](#zen_api.hardware.v1.StageServiceRegisterOnStageVelocityChangedResponse)
  - [StageServiceStopRequest](#zen_api.hardware.v1.StageServiceStopRequest)
  - [StageServiceStopResponse](#zen_api.hardware.v1.StageServiceStopResponse)
  - [StageService](#zen_api.hardware.v1.StageService)
- [zen\_api/hardware/v1/stage\_state.proto](#zen_api/hardware/v1/stage_state.proto)
  - [StageState](#zen_api.hardware.v1.StageState)
- [zen\_api/workflows/v1/start\_job\_options.proto](#zen_api/workflows/v1/start_job_options.proto)
  - [StartJobOptions](#zen_api.workflows.v1.StartJobOptions)
- [zen\_api/workflows/v1beta/job\_resources\_service.proto](#zen_api/workflows/v1beta/job_resources_service.proto)
  - [JobResourcesServiceGetAvailableResourcesRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetAvailableResourcesRequest)
  - [JobResourcesServiceGetAvailableResourcesResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetAvailableResourcesResponse)
  - [JobResourcesServiceGetBooleanValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetBooleanValueRequest)
  - [JobResourcesServiceGetBooleanValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetBooleanValueResponse)
  - [JobResourcesServiceGetDateTimeValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetDateTimeValueRequest)
  - [JobResourcesServiceGetDateTimeValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetDateTimeValueResponse)
  - [JobResourcesServiceGetDateValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetDateValueRequest)
  - [JobResourcesServiceGetDateValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetDateValueResponse)
  - [JobResourcesServiceGetDoubleValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetDoubleValueRequest)
  - [JobResourcesServiceGetDoubleValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetDoubleValueResponse)
  - [JobResourcesServiceGetFloatValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetFloatValueRequest)
  - [JobResourcesServiceGetFloatValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetFloatValueResponse)
  - [JobResourcesServiceGetIntegerValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetIntegerValueRequest)
  - [JobResourcesServiceGetIntegerValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetIntegerValueResponse)
  - [JobResourcesServiceGetLongValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetLongValueRequest)
  - [JobResourcesServiceGetLongValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetLongValueResponse)
  - [JobResourcesServiceGetStringValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetStringValueRequest)
  - [JobResourcesServiceGetStringValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetStringValueResponse)
  - [JobResourcesServiceGetTimeValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetTimeValueRequest)
  - [JobResourcesServiceGetTimeValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetTimeValueResponse)
  - [JobResourcesServiceHasResourceRequest](#zen_api.workflows.v1beta.JobResourcesServiceHasResourceRequest)
  - [JobResourcesServiceHasResourceResponse](#zen_api.workflows.v1beta.JobResourcesServiceHasResourceResponse)
  - [JobResourcesServiceIsJobLoadedRequest](#zen_api.workflows.v1beta.JobResourcesServiceIsJobLoadedRequest)
  - [JobResourcesServiceIsJobLoadedResponse](#zen_api.workflows.v1beta.JobResourcesServiceIsJobLoadedResponse)
  - [JobResourcesServiceSetBooleanValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetBooleanValueRequest)
  - [JobResourcesServiceSetBooleanValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetBooleanValueResponse)
  - [JobResourcesServiceSetDateTimeValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetDateTimeValueRequest)
  - [JobResourcesServiceSetDateTimeValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetDateTimeValueResponse)
  - [JobResourcesServiceSetDateValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetDateValueRequest)
  - [JobResourcesServiceSetDateValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetDateValueResponse)
  - [JobResourcesServiceSetDoubleValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetDoubleValueRequest)
  - [JobResourcesServiceSetDoubleValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetDoubleValueResponse)
  - [JobResourcesServiceSetFloatValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetFloatValueRequest)
  - [JobResourcesServiceSetFloatValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetFloatValueResponse)
  - [JobResourcesServiceSetIntegerValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetIntegerValueRequest)
  - [JobResourcesServiceSetIntegerValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetIntegerValueResponse)
  - [JobResourcesServiceSetLongValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetLongValueRequest)
  - [JobResourcesServiceSetLongValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetLongValueResponse)
  - [JobResourcesServiceSetStringValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetStringValueRequest)
  - [JobResourcesServiceSetStringValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetStringValueResponse)
  - [JobResourcesServiceSetTimeValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetTimeValueRequest)
  - [JobResourcesServiceSetTimeValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetTimeValueResponse)
  - [JobResourcesService](#zen_api.workflows.v1beta.JobResourcesService)
- [zen\_api/workflows/v2/job\_info.proto](#zen_api/workflows/v2/job_info.proto)
  - [JobInfo](#zen_api.workflows.v2.JobInfo)
- [zen\_api/workflows/v2/job\_status.proto](#zen_api/workflows/v2/job_status.proto)
  - [JobStatus](#zen_api.workflows.v2.JobStatus)
- [zen\_api/workflows/v2/workflow\_service.proto](#zen_api/workflows/v2/workflow_service.proto)
  - [WorkflowServiceGetJobInfoRequest](#zen_api.workflows.v2.WorkflowServiceGetJobInfoRequest)
  - [WorkflowServiceGetJobInfoResponse](#zen_api.workflows.v2.WorkflowServiceGetJobInfoResponse)
  - [WorkflowServiceStartJobRequest](#zen_api.workflows.v2.WorkflowServiceStartJobRequest)
  - [WorkflowServiceStartJobResponse](#zen_api.workflows.v2.WorkflowServiceStartJobResponse)
  - [WorkflowServiceStopJobRequest](#zen_api.workflows.v2.WorkflowServiceStopJobRequest)
  - [WorkflowServiceStopJobResponse](#zen_api.workflows.v2.WorkflowServiceStopJobResponse)
  - [WorkflowServiceWaitJobRequest](#zen_api.workflows.v2.WorkflowServiceWaitJobRequest)
  - [WorkflowServiceWaitJobResponse](#zen_api.workflows.v2.WorkflowServiceWaitJobResponse)
  - [WorkflowService](#zen_api.workflows.v2.WorkflowService)
- [zen\_api/workflows/v3beta/job\_status.proto](#zen_api/workflows/v3beta/job_status.proto)
  - [JobStatus](#zen_api.workflows.v3beta.JobStatus)
- [zen\_api/workflows/v3beta/job\_template\_info.proto](#zen_api/workflows/v3beta/job_template_info.proto)
  - [JobTemplateInfo](#zen_api.workflows.v3beta.JobTemplateInfo)
- [zen\_api/workflows/v3beta/workflow\_service.proto](#zen_api/workflows/v3beta/workflow_service.proto)
  - [WorkflowServiceGetAvailableJobTemplatesRequest](#zen_api.workflows.v3beta.WorkflowServiceGetAvailableJobTemplatesRequest)
  - [WorkflowServiceGetAvailableJobTemplatesResponse](#zen_api.workflows.v3beta.WorkflowServiceGetAvailableJobTemplatesResponse)
  - [WorkflowServiceGetStatusRequest](#zen_api.workflows.v3beta.WorkflowServiceGetStatusRequest)
  - [WorkflowServiceGetStatusResponse](#zen_api.workflows.v3beta.WorkflowServiceGetStatusResponse)
  - [WorkflowServiceIsJobRunningRequest](#zen_api.workflows.v3beta.WorkflowServiceIsJobRunningRequest)
  - [WorkflowServiceIsJobRunningResponse](#zen_api.workflows.v3beta.WorkflowServiceIsJobRunningResponse)
  - [WorkflowServiceIsJobTemplateLoadedRequest](#zen_api.workflows.v3beta.WorkflowServiceIsJobTemplateLoadedRequest)
  - [WorkflowServiceIsJobTemplateLoadedResponse](#zen_api.workflows.v3beta.WorkflowServiceIsJobTemplateLoadedResponse)
  - [WorkflowServiceLoadJobTemplateRequest](#zen_api.workflows.v3beta.WorkflowServiceLoadJobTemplateRequest)
  - [WorkflowServiceLoadJobTemplateResponse](#zen_api.workflows.v3beta.WorkflowServiceLoadJobTemplateResponse)
  - [WorkflowServiceRegisterOnStatusChangedRequest](#zen_api.workflows.v3beta.WorkflowServiceRegisterOnStatusChangedRequest)
  - [WorkflowServiceRegisterOnStatusChangedResponse](#zen_api.workflows.v3beta.WorkflowServiceRegisterOnStatusChangedResponse)
  - [WorkflowServiceRunJobRequest](#zen_api.workflows.v3beta.WorkflowServiceRunJobRequest)
  - [WorkflowServiceRunJobResponse](#zen_api.workflows.v3beta.WorkflowServiceRunJobResponse)
  - [WorkflowServiceStartJobRequest](#zen_api.workflows.v3beta.WorkflowServiceStartJobRequest)
  - [WorkflowServiceStartJobResponse](#zen_api.workflows.v3beta.WorkflowServiceStartJobResponse)
  - [WorkflowServiceStopJobRequest](#zen_api.workflows.v3beta.WorkflowServiceStopJobRequest)
  - [WorkflowServiceStopJobResponse](#zen_api.workflows.v3beta.WorkflowServiceStopJobResponse)
  - [WorkflowServiceUnloadJobTemplateRequest](#zen_api.workflows.v3beta.WorkflowServiceUnloadJobTemplateRequest)
  - [WorkflowServiceUnloadJobTemplateResponse](#zen_api.workflows.v3beta.WorkflowServiceUnloadJobTemplateResponse)
  - [WorkflowServiceWaitJobRequest](#zen_api.workflows.v3beta.WorkflowServiceWaitJobRequest)
  - [WorkflowServiceWaitJobResponse](#zen_api.workflows.v3beta.WorkflowServiceWaitJobResponse)
  - [WorkflowService](#zen_api.workflows.v3beta.WorkflowService)
- [zen\_api/em/hardware/v1/acquisition\_response\_type.proto](#zen_api/em/hardware/v1/acquisition_response_type.proto)
  - [AcquisitionResponseType](#zen_api.em.hardware.v1.AcquisitionResponseType)
- [zen\_api/em/hardware/v1/acquisition\_service.proto](#zen_api/em/hardware/v1/acquisition_service.proto)
  - [AcquisitionServiceGetExternalScanSourceRequest](#zen_api.em.hardware.v1.AcquisitionServiceGetExternalScanSourceRequest)
  - [AcquisitionServiceGetExternalScanSourceResponse](#zen_api.em.hardware.v1.AcquisitionServiceGetExternalScanSourceResponse)
  - [AcquisitionServiceSetExternalScanSourceRequest](#zen_api.em.hardware.v1.AcquisitionServiceSetExternalScanSourceRequest)
  - [AcquisitionServiceSetExternalScanSourceResponse](#zen_api.em.hardware.v1.AcquisitionServiceSetExternalScanSourceResponse)
  - [AcquisitionService](#zen_api.em.hardware.v1.AcquisitionService)
- [zen\_api/em/hardware/v1/acquisition\_settings.proto](#zen_api/em/hardware/v1/acquisition_settings.proto)
  - [AcquisitionSettings](#zen_api.em.hardware.v1.AcquisitionSettings)
- [zen\_api/em/hardware/v1/acquisition\_status.proto](#zen_api/em/hardware/v1/acquisition_status.proto)
  - [AcquisitionStatus](#zen_api.em.hardware.v1.AcquisitionStatus)
- [zen\_api/em/hardware/v1/beam\_state.proto](#zen_api/em/hardware/v1/beam_state.proto)
  - [BeamState](#zen_api.em.hardware.v1.BeamState)
- [zen\_api/em/hardware/v1/camera\_acquisition\_settings.proto](#zen_api/em/hardware/v1/camera_acquisition_settings.proto)
  - [CameraAcquisitionSettings](#zen_api.em.hardware.v1.CameraAcquisitionSettings)
- [zen\_api/em/hardware/v1/camera\_acquisition\_status.proto](#zen_api/em/hardware/v1/camera_acquisition_status.proto)
  - [CameraAcquisitionStatus](#zen_api.em.hardware.v1.CameraAcquisitionStatus)
- [zen\_api/em/hardware/v1/camera\_service.proto](#zen_api/em/hardware/v1/camera_service.proto)
  - [CameraServiceGetAcquisitionStatusRequest](#zen_api.em.hardware.v1.CameraServiceGetAcquisitionStatusRequest)
  - [CameraServiceGetAcquisitionStatusResponse](#zen_api.em.hardware.v1.CameraServiceGetAcquisitionStatusResponse)
  - [CameraServiceGetAvailableCamerasRequest](#zen_api.em.hardware.v1.CameraServiceGetAvailableCamerasRequest)
  - [CameraServiceGetAvailableCamerasResponse](#zen_api.em.hardware.v1.CameraServiceGetAvailableCamerasResponse)
  - [CameraServiceGetBrightnessRequest](#zen_api.em.hardware.v1.CameraServiceGetBrightnessRequest)
  - [CameraServiceGetBrightnessResponse](#zen_api.em.hardware.v1.CameraServiceGetBrightnessResponse)
  - [CameraServiceGetCcdModeRequest](#zen_api.em.hardware.v1.CameraServiceGetCcdModeRequest)
  - [CameraServiceGetCcdModeResponse](#zen_api.em.hardware.v1.CameraServiceGetCcdModeResponse)
  - [CameraServiceGetContrastRequest](#zen_api.em.hardware.v1.CameraServiceGetContrastRequest)
  - [CameraServiceGetContrastResponse](#zen_api.em.hardware.v1.CameraServiceGetContrastResponse)
  - [CameraServiceRegisterOnAcquisitionStatusChangedRequest](#zen_api.em.hardware.v1.CameraServiceRegisterOnAcquisitionStatusChangedRequest)
  - [CameraServiceRegisterOnAcquisitionStatusChangedResponse](#zen_api.em.hardware.v1.CameraServiceRegisterOnAcquisitionStatusChangedResponse)
  - [CameraServiceRegisterOnBrightnessChangedRequest](#zen_api.em.hardware.v1.CameraServiceRegisterOnBrightnessChangedRequest)
  - [CameraServiceRegisterOnBrightnessChangedResponse](#zen_api.em.hardware.v1.CameraServiceRegisterOnBrightnessChangedResponse)
  - [CameraServiceRegisterOnCcdModeChangedRequest](#zen_api.em.hardware.v1.CameraServiceRegisterOnCcdModeChangedRequest)
  - [CameraServiceRegisterOnCcdModeChangedResponse](#zen_api.em.hardware.v1.CameraServiceRegisterOnCcdModeChangedResponse)
  - [CameraServiceRegisterOnContrastChangedRequest](#zen_api.em.hardware.v1.CameraServiceRegisterOnContrastChangedRequest)
  - [CameraServiceRegisterOnContrastChangedResponse](#zen_api.em.hardware.v1.CameraServiceRegisterOnContrastChangedResponse)
  - [CameraServiceSetBrightnessRequest](#zen_api.em.hardware.v1.CameraServiceSetBrightnessRequest)
  - [CameraServiceSetBrightnessResponse](#zen_api.em.hardware.v1.CameraServiceSetBrightnessResponse)
  - [CameraServiceSetCcdModeRequest](#zen_api.em.hardware.v1.CameraServiceSetCcdModeRequest)
  - [CameraServiceSetCcdModeResponse](#zen_api.em.hardware.v1.CameraServiceSetCcdModeResponse)
  - [CameraServiceSetContrastRequest](#zen_api.em.hardware.v1.CameraServiceSetContrastRequest)
  - [CameraServiceSetContrastResponse](#zen_api.em.hardware.v1.CameraServiceSetContrastResponse)
  - [CameraServiceStartLiveAcquisitionRequest](#zen_api.em.hardware.v1.CameraServiceStartLiveAcquisitionRequest)
  - [CameraServiceStartLiveAcquisitionResponse](#zen_api.em.hardware.v1.CameraServiceStartLiveAcquisitionResponse)
  - [CameraServiceStartSingleAcquisitionRequest](#zen_api.em.hardware.v1.CameraServiceStartSingleAcquisitionRequest)
  - [CameraServiceStartSingleAcquisitionResponse](#zen_api.em.hardware.v1.CameraServiceStartSingleAcquisitionResponse)
  - [CameraServiceStopLiveAcquisitionRequest](#zen_api.em.hardware.v1.CameraServiceStopLiveAcquisitionRequest)
  - [CameraServiceStopLiveAcquisitionResponse](#zen_api.em.hardware.v1.CameraServiceStopLiveAcquisitionResponse)
  - [CameraService](#zen_api.em.hardware.v1.CameraService)
- [zen\_api/em/hardware/v1/ccd\_mode.proto](#zen_api/em/hardware/v1/ccd_mode.proto)
  - [CcdMode](#zen_api.em.hardware.v1.CcdMode)
- [zen\_api/em/hardware/v1/command\_id.proto](#zen_api/em/hardware/v1/command_id.proto)
  - [CommandId](#zen_api.em.hardware.v1.CommandId)
- [zen\_api/em/hardware/v1/detector\_service.proto](#zen_api/em/hardware/v1/detector_service.proto)
  - [DetectorServiceGetAvailableDetectorsRequest](#zen_api.em.hardware.v1.DetectorServiceGetAvailableDetectorsRequest)
  - [DetectorServiceGetAvailableDetectorsResponse](#zen_api.em.hardware.v1.DetectorServiceGetAvailableDetectorsResponse)
  - [DetectorServiceGetBrightnessRequest](#zen_api.em.hardware.v1.DetectorServiceGetBrightnessRequest)
  - [DetectorServiceGetBrightnessResponse](#zen_api.em.hardware.v1.DetectorServiceGetBrightnessResponse)
  - [DetectorServiceGetContrastRequest](#zen_api.em.hardware.v1.DetectorServiceGetContrastRequest)
  - [DetectorServiceGetContrastResponse](#zen_api.em.hardware.v1.DetectorServiceGetContrastResponse)
  - [DetectorServiceRegisterOnBrightnessChangedRequest](#zen_api.em.hardware.v1.DetectorServiceRegisterOnBrightnessChangedRequest)
  - [DetectorServiceRegisterOnBrightnessChangedResponse](#zen_api.em.hardware.v1.DetectorServiceRegisterOnBrightnessChangedResponse)
  - [DetectorServiceRegisterOnContrastChangedRequest](#zen_api.em.hardware.v1.DetectorServiceRegisterOnContrastChangedRequest)
  - [DetectorServiceRegisterOnContrastChangedResponse](#zen_api.em.hardware.v1.DetectorServiceRegisterOnContrastChangedResponse)
  - [DetectorServiceSetBrightnessRequest](#zen_api.em.hardware.v1.DetectorServiceSetBrightnessRequest)
  - [DetectorServiceSetBrightnessResponse](#zen_api.em.hardware.v1.DetectorServiceSetBrightnessResponse)
  - [DetectorServiceSetContrastRequest](#zen_api.em.hardware.v1.DetectorServiceSetContrastRequest)
  - [DetectorServiceSetContrastResponse](#zen_api.em.hardware.v1.DetectorServiceSetContrastResponse)
  - [DetectorService](#zen_api.em.hardware.v1.DetectorService)
- [zen\_api/em/hardware/v1/electron\_column\_service.proto](#zen_api/em/hardware/v1/electron_column_service.proto)
  - [ElectronColumnServiceGetActualVoltageRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetActualVoltageRequest)
  - [ElectronColumnServiceGetActualVoltageResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetActualVoltageResponse)
  - [ElectronColumnServiceGetApertureAlignRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetApertureAlignRequest)
  - [ElectronColumnServiceGetApertureAlignResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetApertureAlignResponse)
  - [ElectronColumnServiceGetBeamBlankerStateRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamBlankerStateRequest)
  - [ElectronColumnServiceGetBeamBlankerStateResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamBlankerStateResponse)
  - [ElectronColumnServiceGetBeamShiftLimitsRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamShiftLimitsRequest)
  - [ElectronColumnServiceGetBeamShiftLimitsResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamShiftLimitsResponse)
  - [ElectronColumnServiceGetBeamShiftRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamShiftRequest)
  - [ElectronColumnServiceGetBeamShiftResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamShiftResponse)
  - [ElectronColumnServiceGetBeamStateRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamStateRequest)
  - [ElectronColumnServiceGetBeamStateResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamStateResponse)
  - [ElectronColumnServiceGetBoosterVoltageRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetBoosterVoltageRequest)
  - [ElectronColumnServiceGetBoosterVoltageResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetBoosterVoltageResponse)
  - [ElectronColumnServiceGetEhtOffsetLimitsRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetEhtOffsetLimitsRequest)
  - [ElectronColumnServiceGetEhtOffsetLimitsResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetEhtOffsetLimitsResponse)
  - [ElectronColumnServiceGetEhtOffsetRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetEhtOffsetRequest)
  - [ElectronColumnServiceGetEhtOffsetResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetEhtOffsetResponse)
  - [ElectronColumnServiceGetFocusLimitsRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetFocusLimitsRequest)
  - [ElectronColumnServiceGetFocusLimitsResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetFocusLimitsResponse)
  - [ElectronColumnServiceGetFocusRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetFocusRequest)
  - [ElectronColumnServiceGetFocusResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetFocusResponse)
  - [ElectronColumnServiceGetFovLimitsRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovLimitsRequest)
  - [ElectronColumnServiceGetFovLimitsResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovLimitsResponse)
  - [ElectronColumnServiceGetFovRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovRequest)
  - [ElectronColumnServiceGetFovResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovResponse)
  - [ElectronColumnServiceGetFovRotationLimitsRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovRotationLimitsRequest)
  - [ElectronColumnServiceGetFovRotationLimitsResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovRotationLimitsResponse)
  - [ElectronColumnServiceGetFovRotationRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovRotationRequest)
  - [ElectronColumnServiceGetFovRotationResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovRotationResponse)
  - [ElectronColumnServiceGetObjectiveCurrentRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetObjectiveCurrentRequest)
  - [ElectronColumnServiceGetObjectiveCurrentResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetObjectiveCurrentResponse)
  - [ElectronColumnServiceGetProbeCurrentRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetProbeCurrentRequest)
  - [ElectronColumnServiceGetProbeCurrentResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetProbeCurrentResponse)
  - [ElectronColumnServiceGetSemiAngleRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetSemiAngleRequest)
  - [ElectronColumnServiceGetSemiAngleResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetSemiAngleResponse)
  - [ElectronColumnServiceGetSpotSizeRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetSpotSizeRequest)
  - [ElectronColumnServiceGetSpotSizeResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetSpotSizeResponse)
  - [ElectronColumnServiceGetStigmatorRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetStigmatorRequest)
  - [ElectronColumnServiceGetStigmatorResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetStigmatorResponse)
  - [ElectronColumnServiceGetTargetVoltageRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetTargetVoltageRequest)
  - [ElectronColumnServiceGetTargetVoltageResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetTargetVoltageResponse)
  - [ElectronColumnServiceGetVoltageLimitsRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetVoltageLimitsRequest)
  - [ElectronColumnServiceGetVoltageLimitsResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetVoltageLimitsResponse)
  - [ElectronColumnServiceGoToStandbyRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGoToStandbyRequest)
  - [ElectronColumnServiceGoToStandbyResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGoToStandbyResponse)
  - [ElectronColumnServiceRegisterOnApertureAlignChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnApertureAlignChangedRequest)
  - [ElectronColumnServiceRegisterOnApertureAlignChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnApertureAlignChangedResponse)
  - [ElectronColumnServiceRegisterOnBeamBlankerStateChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnBeamBlankerStateChangedRequest)
  - [ElectronColumnServiceRegisterOnBeamBlankerStateChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnBeamBlankerStateChangedResponse)
  - [ElectronColumnServiceRegisterOnBeamShiftChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnBeamShiftChangedRequest)
  - [ElectronColumnServiceRegisterOnBeamShiftChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnBeamShiftChangedResponse)
  - [ElectronColumnServiceRegisterOnBeamStateChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnBeamStateChangedRequest)
  - [ElectronColumnServiceRegisterOnBeamStateChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnBeamStateChangedResponse)
  - [ElectronColumnServiceRegisterOnFocusChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnFocusChangedRequest)
  - [ElectronColumnServiceRegisterOnFocusChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnFocusChangedResponse)
  - [ElectronColumnServiceRegisterOnFovChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnFovChangedRequest)
  - [ElectronColumnServiceRegisterOnFovChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnFovChangedResponse)
  - [ElectronColumnServiceRegisterOnFovRotationChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnFovRotationChangedRequest)
  - [ElectronColumnServiceRegisterOnFovRotationChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnFovRotationChangedResponse)
  - [ElectronColumnServiceRegisterOnProbeCurrentChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnProbeCurrentChangedRequest)
  - [ElectronColumnServiceRegisterOnProbeCurrentChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnProbeCurrentChangedResponse)
  - [ElectronColumnServiceRegisterOnSemiAngleChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnSemiAngleChangedRequest)
  - [ElectronColumnServiceRegisterOnSemiAngleChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnSemiAngleChangedResponse)
  - [ElectronColumnServiceRegisterOnSpotSizeChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnSpotSizeChangedRequest)
  - [ElectronColumnServiceRegisterOnSpotSizeChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnSpotSizeChangedResponse)
  - [ElectronColumnServiceRegisterOnStigmatorChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnStigmatorChangedRequest)
  - [ElectronColumnServiceRegisterOnStigmatorChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnStigmatorChangedResponse)
  - [ElectronColumnServiceRegisterOnVoltageChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnVoltageChangedRequest)
  - [ElectronColumnServiceRegisterOnVoltageChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnVoltageChangedResponse)
  - [ElectronColumnServiceSetApertureAlignRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetApertureAlignRequest)
  - [ElectronColumnServiceSetApertureAlignResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetApertureAlignResponse)
  - [ElectronColumnServiceSetBeamBlankerStateRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetBeamBlankerStateRequest)
  - [ElectronColumnServiceSetBeamBlankerStateResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetBeamBlankerStateResponse)
  - [ElectronColumnServiceSetBeamShiftRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetBeamShiftRequest)
  - [ElectronColumnServiceSetBeamShiftResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetBeamShiftResponse)
  - [ElectronColumnServiceSetEhtOffsetRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetEhtOffsetRequest)
  - [ElectronColumnServiceSetEhtOffsetResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetEhtOffsetResponse)
  - [ElectronColumnServiceSetFocusRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetFocusRequest)
  - [ElectronColumnServiceSetFocusResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetFocusResponse)
  - [ElectronColumnServiceSetFovRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetFovRequest)
  - [ElectronColumnServiceSetFovResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetFovResponse)
  - [ElectronColumnServiceSetFovRotationRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetFovRotationRequest)
  - [ElectronColumnServiceSetFovRotationResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetFovRotationResponse)
  - [ElectronColumnServiceSetObjectiveCurrentRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetObjectiveCurrentRequest)
  - [ElectronColumnServiceSetObjectiveCurrentResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetObjectiveCurrentResponse)
  - [ElectronColumnServiceSetProbeCurrentRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetProbeCurrentRequest)
  - [ElectronColumnServiceSetProbeCurrentResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetProbeCurrentResponse)
  - [ElectronColumnServiceSetStigmatorRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetStigmatorRequest)
  - [ElectronColumnServiceSetStigmatorResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetStigmatorResponse)
  - [ElectronColumnServiceSetVoltageRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetVoltageRequest)
  - [ElectronColumnServiceSetVoltageResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetVoltageResponse)
  - [ElectronColumnServiceTurnOffRequest](#zen_api.em.hardware.v1.ElectronColumnServiceTurnOffRequest)
  - [ElectronColumnServiceTurnOffResponse](#zen_api.em.hardware.v1.ElectronColumnServiceTurnOffResponse)
  - [ElectronColumnServiceTurnOnRequest](#zen_api.em.hardware.v1.ElectronColumnServiceTurnOnRequest)
  - [ElectronColumnServiceTurnOnResponse](#zen_api.em.hardware.v1.ElectronColumnServiceTurnOnResponse)
  - [ElectronColumnService](#zen_api.em.hardware.v1.ElectronColumnService)
- [zen\_api/em/hardware/v1/em\_stage\_service.proto](#zen_api/em/hardware/v1/em_stage_service.proto)
  - [EmStageServiceGetAxisBacklashModeRequest](#zen_api.em.hardware.v1.EmStageServiceGetAxisBacklashModeRequest)
  - [EmStageServiceGetAxisLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceGetAxisLimitsRequest)
  - [EmStageServiceGetAxisUserLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceGetAxisUserLimitsRequest)
  - [EmStageServiceGetAxisVelocityLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceGetAxisVelocityLimitsRequest)
  - [EmStageServiceGetStageBacklashModesRequest](#zen_api.em.hardware.v1.EmStageServiceGetStageBacklashModesRequest)
  - [EmStageServiceGetStageFastRequest](#zen_api.em.hardware.v1.EmStageServiceGetStageFastRequest)
  - [EmStageServiceGetStageLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceGetStageLimitsRequest)
  - [EmStageServiceGetStageUserLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceGetStageUserLimitsRequest)
  - [EmStageServiceGetStageVelocityLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceGetStageVelocityLimitsRequest)
  - [EmStageServiceSetAxisBacklashModeRequest](#zen_api.em.hardware.v1.EmStageServiceSetAxisBacklashModeRequest)
  - [EmStageServiceSetAxisUserLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceSetAxisUserLimitsRequest)
  - [EmStageServiceSetAxisVelocityRequest](#zen_api.em.hardware.v1.EmStageServiceSetAxisVelocityRequest)
  - [EmStageServiceSetStageBacklashModesRequest](#zen_api.em.hardware.v1.EmStageServiceSetStageBacklashModesRequest)
  - [EmStageServiceSetStageFastRequest](#zen_api.em.hardware.v1.EmStageServiceSetStageFastRequest)
  - [EmStageServiceSetStageUserLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceSetStageUserLimitsRequest)
  - [StageServiceAxisBacklashModeResponse](#zen_api.em.hardware.v1.StageServiceAxisBacklashModeResponse)
  - [StageServiceAxisUserLimitsResponse](#zen_api.em.hardware.v1.StageServiceAxisUserLimitsResponse)
  - [StageServiceGetAxisBacklashModeResponse](#zen_api.em.hardware.v1.StageServiceGetAxisBacklashModeResponse)
  - [StageServiceGetAxisLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetAxisLimitsResponse)
  - [StageServiceGetAxisUserLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetAxisUserLimitsResponse)
  - [StageServiceGetAxisVelocityLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetAxisVelocityLimitsResponse)
  - [StageServiceGetStageBacklashModesResponse](#zen_api.em.hardware.v1.StageServiceGetStageBacklashModesResponse)
  - [StageServiceGetStageFastResponse](#zen_api.em.hardware.v1.StageServiceGetStageFastResponse)
  - [StageServiceGetStageLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetStageLimitsResponse)
  - [StageServiceGetStageUserLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetStageUserLimitsResponse)
  - [StageServiceGetStageVelocityLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetStageVelocityLimitsResponse)
  - [StageServiceSetAxisBacklashModeResponse](#zen_api.em.hardware.v1.StageServiceSetAxisBacklashModeResponse)
  - [StageServiceSetAxisUserLimitsResponse](#zen_api.em.hardware.v1.StageServiceSetAxisUserLimitsResponse)
  - [StageServiceSetAxisVelocityResponse](#zen_api.em.hardware.v1.StageServiceSetAxisVelocityResponse)
  - [StageServiceSetStageBacklashModesResponse](#zen_api.em.hardware.v1.StageServiceSetStageBacklashModesResponse)
  - [StageServiceSetStageFastResponse](#zen_api.em.hardware.v1.StageServiceSetStageFastResponse)
  - [StageServiceSetStageUserLimitsResponse](#zen_api.em.hardware.v1.StageServiceSetStageUserLimitsResponse)
  - [EmStageService](#zen_api.em.hardware.v1.EmStageService)
- [zen\_api/em/hardware/v1/extended\_acquisition\_settings.proto](#zen_api/em/hardware/v1/extended_acquisition_settings.proto)
  - [ExtendedAcquisitionSettings](#zen_api.em.hardware.v1.ExtendedAcquisitionSettings)
- [zen\_api/em/hardware/v1/external\_procedure\_service.proto](#zen_api/em/hardware/v1/external_procedure_service.proto)
  - [ExternalProcedureServiceRegisterExternalProcedureRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceRegisterExternalProcedureRequest)
  - [ExternalProcedureServiceRegisterExternalProcedureResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceRegisterExternalProcedureResponse)
  - [ExternalProcedureServiceReportCommandFailureRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceReportCommandFailureRequest)
  - [ExternalProcedureServiceReportCommandFailureResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceReportCommandFailureResponse)
  - [ExternalProcedureServiceReportCommandSuccessRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceReportCommandSuccessRequest)
  - [ExternalProcedureServiceReportCommandSuccessResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceReportCommandSuccessResponse)
  - [ExternalProcedureServiceReportInitializationErrorRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceReportInitializationErrorRequest)
  - [ExternalProcedureServiceReportInitializationErrorResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceReportInitializationErrorResponse)
  - [ExternalProcedureServiceReportProgressRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceReportProgressRequest)
  - [ExternalProcedureServiceReportProgressResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceReportProgressResponse)
  - [ExternalProcedureServiceReportReadyRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceReportReadyRequest)
  - [ExternalProcedureServiceReportReadyResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceReportReadyResponse)
  - [ExternalProcedureServiceReportStatusRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceReportStatusRequest)
  - [ExternalProcedureServiceReportStatusResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceReportStatusResponse)
  - [ExternalProcedureService](#zen_api.em.hardware.v1.ExternalProcedureService)
- [zen\_api/em/hardware/v1/illumination\_service.proto](#zen_api/em/hardware/v1/illumination_service.proto)
  - [IlluminationServiceGetIlluminationIRRequest](#zen_api.em.hardware.v1.IlluminationServiceGetIlluminationIRRequest)
  - [IlluminationServiceGetIlluminationIRResponse](#zen_api.em.hardware.v1.IlluminationServiceGetIlluminationIRResponse)
  - [IlluminationServiceGetIlluminationWhiteRequest](#zen_api.em.hardware.v1.IlluminationServiceGetIlluminationWhiteRequest)
  - [IlluminationServiceGetIlluminationWhiteResponse](#zen_api.em.hardware.v1.IlluminationServiceGetIlluminationWhiteResponse)
  - [IlluminationServiceRegisterOnIlluminationIRChangedRequest](#zen_api.em.hardware.v1.IlluminationServiceRegisterOnIlluminationIRChangedRequest)
  - [IlluminationServiceRegisterOnIlluminationIRChangedResponse](#zen_api.em.hardware.v1.IlluminationServiceRegisterOnIlluminationIRChangedResponse)
  - [IlluminationServiceRegisterOnIlluminationWhiteChangedRequest](#zen_api.em.hardware.v1.IlluminationServiceRegisterOnIlluminationWhiteChangedRequest)
  - [IlluminationServiceRegisterOnIlluminationWhiteChangedResponse](#zen_api.em.hardware.v1.IlluminationServiceRegisterOnIlluminationWhiteChangedResponse)
  - [IlluminationServiceSetIlluminationIRRequest](#zen_api.em.hardware.v1.IlluminationServiceSetIlluminationIRRequest)
  - [IlluminationServiceSetIlluminationIRResponse](#zen_api.em.hardware.v1.IlluminationServiceSetIlluminationIRResponse)
  - [IlluminationServiceSetIlluminationWhiteRequest](#zen_api.em.hardware.v1.IlluminationServiceSetIlluminationWhiteRequest)
  - [IlluminationServiceSetIlluminationWhiteResponse](#zen_api.em.hardware.v1.IlluminationServiceSetIlluminationWhiteResponse)
  - [IlluminationService](#zen_api.em.hardware.v1.IlluminationService)
- [zen\_api/em/hardware/v1/simple\_acquisition\_service.proto](#zen_api/em/hardware/v1/simple_acquisition_service.proto)
  - [SimpleAcquisitionServiceAcquireExtendedSingleFrameRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceAcquireExtendedSingleFrameRequest)
  - [SimpleAcquisitionServiceAcquireExtendedSingleFrameResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceAcquireExtendedSingleFrameResponse)
  - [SimpleAcquisitionServiceAcquireSingleFrameRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceAcquireSingleFrameRequest)
  - [SimpleAcquisitionServiceAcquireSingleFrameResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceAcquireSingleFrameResponse)
  - [SimpleAcquisitionServiceChangeDwellTimeRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceChangeDwellTimeRequest)
  - [SimpleAcquisitionServiceChangeDwellTimeResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceChangeDwellTimeResponse)
  - [SimpleAcquisitionServiceGetAcquisitionStatusRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceGetAcquisitionStatusRequest)
  - [SimpleAcquisitionServiceGetAcquisitionStatusResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceGetAcquisitionStatusResponse)
  - [SimpleAcquisitionServiceGetBrightnessRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceGetBrightnessRequest)
  - [SimpleAcquisitionServiceGetBrightnessResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceGetBrightnessResponse)
  - [SimpleAcquisitionServiceGetContrastRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceGetContrastRequest)
  - [SimpleAcquisitionServiceGetContrastResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceGetContrastResponse)
  - [SimpleAcquisitionServiceRegisterOnAcquisitionStatusChangedRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceRegisterOnAcquisitionStatusChangedRequest)
  - [SimpleAcquisitionServiceRegisterOnAcquisitionStatusChangedResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceRegisterOnAcquisitionStatusChangedResponse)
  - [SimpleAcquisitionServiceSetBrightnessRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceSetBrightnessRequest)
  - [SimpleAcquisitionServiceSetBrightnessResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceSetBrightnessResponse)
  - [SimpleAcquisitionServiceSetContrastRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceSetContrastRequest)
  - [SimpleAcquisitionServiceSetContrastResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceSetContrastResponse)
  - [SimpleAcquisitionServiceStartExtendedLiveAcquisitionRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceStartExtendedLiveAcquisitionRequest)
  - [SimpleAcquisitionServiceStartExtendedLiveAcquisitionResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceStartExtendedLiveAcquisitionResponse)
  - [SimpleAcquisitionServiceStartLiveAcquisitionRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceStartLiveAcquisitionRequest)
  - [SimpleAcquisitionServiceStartLiveAcquisitionResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceStartLiveAcquisitionResponse)
  - [SimpleAcquisitionServiceStopLiveAcquisitionRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceStopLiveAcquisitionRequest)
  - [SimpleAcquisitionServiceStopLiveAcquisitionResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceStopLiveAcquisitionResponse)
  - [SimpleAcquisitionService](#zen_api.em.hardware.v1.SimpleAcquisitionService)
- [zen\_api/em/hardware/v1/specimen\_current\_monitor\_service.proto](#zen_api/em/hardware/v1/specimen_current_monitor_service.proto)
  - [SpecimenCurrentMonitorServiceGetSpecimenCurrentRequest](#zen_api.em.hardware.v1.SpecimenCurrentMonitorServiceGetSpecimenCurrentRequest)
  - [SpecimenCurrentMonitorServiceGetSpecimenCurrentResponse](#zen_api.em.hardware.v1.SpecimenCurrentMonitorServiceGetSpecimenCurrentResponse)
  - [SpecimenCurrentMonitorServiceRegisterOnSpecimenCurrentChangedRequest](#zen_api.em.hardware.v1.SpecimenCurrentMonitorServiceRegisterOnSpecimenCurrentChangedRequest)
  - [SpecimenCurrentMonitorServiceRegisterOnSpecimenCurrentChangedResponse](#zen_api.em.hardware.v1.SpecimenCurrentMonitorServiceRegisterOnSpecimenCurrentChangedResponse)
  - [SpecimenCurrentMonitorService](#zen_api.em.hardware.v1.SpecimenCurrentMonitorService)
- [zen\_api/em/hardware/v1/stage\_backlash\_mode.proto](#zen_api/em/hardware/v1/stage_backlash_mode.proto)
  - [StageBacklashMode](#zen_api.em.hardware.v1.StageBacklashMode)
- [zen\_api/em/hardware/v1/vacuum\_mode.proto](#zen_api/em/hardware/v1/vacuum_mode.proto)
  - [VacuumMode](#zen_api.em.hardware.v1.VacuumMode)
- [zen\_api/em/hardware/v1/vacuum\_service.proto](#zen_api/em/hardware/v1/vacuum_service.proto)
  - [VacuumServiceCloseValveRequest](#zen_api.em.hardware.v1.VacuumServiceCloseValveRequest)
  - [VacuumServiceCloseValveResponse](#zen_api.em.hardware.v1.VacuumServiceCloseValveResponse)
  - [VacuumServiceGetAvailableVacuumModesRequest](#zen_api.em.hardware.v1.VacuumServiceGetAvailableVacuumModesRequest)
  - [VacuumServiceGetAvailableVacuumModesResponse](#zen_api.em.hardware.v1.VacuumServiceGetAvailableVacuumModesResponse)
  - [VacuumServiceGetAvailableValvesRequest](#zen_api.em.hardware.v1.VacuumServiceGetAvailableValvesRequest)
  - [VacuumServiceGetAvailableValvesResponse](#zen_api.em.hardware.v1.VacuumServiceGetAvailableValvesResponse)
  - [VacuumServiceGetChamberPressureRequest](#zen_api.em.hardware.v1.VacuumServiceGetChamberPressureRequest)
  - [VacuumServiceGetChamberPressureResponse](#zen_api.em.hardware.v1.VacuumServiceGetChamberPressureResponse)
  - [VacuumServiceGetTargetChamberPressureRequest](#zen_api.em.hardware.v1.VacuumServiceGetTargetChamberPressureRequest)
  - [VacuumServiceGetTargetChamberPressureResponse](#zen_api.em.hardware.v1.VacuumServiceGetTargetChamberPressureResponse)
  - [VacuumServiceGetVacuumModeRequest](#zen_api.em.hardware.v1.VacuumServiceGetVacuumModeRequest)
  - [VacuumServiceGetVacuumModeResponse](#zen_api.em.hardware.v1.VacuumServiceGetVacuumModeResponse)
  - [VacuumServiceGetVacuumStateRequest](#zen_api.em.hardware.v1.VacuumServiceGetVacuumStateRequest)
  - [VacuumServiceGetVacuumStateResponse](#zen_api.em.hardware.v1.VacuumServiceGetVacuumStateResponse)
  - [VacuumServiceGetValveStateRequest](#zen_api.em.hardware.v1.VacuumServiceGetValveStateRequest)
  - [VacuumServiceGetValveStateResponse](#zen_api.em.hardware.v1.VacuumServiceGetValveStateResponse)
  - [VacuumServiceOpenValveRequest](#zen_api.em.hardware.v1.VacuumServiceOpenValveRequest)
  - [VacuumServiceOpenValveResponse](#zen_api.em.hardware.v1.VacuumServiceOpenValveResponse)
  - [VacuumServicePumpRequest](#zen_api.em.hardware.v1.VacuumServicePumpRequest)
  - [VacuumServicePumpResponse](#zen_api.em.hardware.v1.VacuumServicePumpResponse)
  - [VacuumServiceRegisterOnChamberPressureChangedRequest](#zen_api.em.hardware.v1.VacuumServiceRegisterOnChamberPressureChangedRequest)
  - [VacuumServiceRegisterOnChamberPressureChangedResponse](#zen_api.em.hardware.v1.VacuumServiceRegisterOnChamberPressureChangedResponse)
  - [VacuumServiceRegisterOnTargetChamberPressureChangedRequest](#zen_api.em.hardware.v1.VacuumServiceRegisterOnTargetChamberPressureChangedRequest)
  - [VacuumServiceRegisterOnTargetChamberPressureChangedResponse](#zen_api.em.hardware.v1.VacuumServiceRegisterOnTargetChamberPressureChangedResponse)
  - [VacuumServiceRegisterOnVacuumModeChangedRequest](#zen_api.em.hardware.v1.VacuumServiceRegisterOnVacuumModeChangedRequest)
  - [VacuumServiceRegisterOnVacuumModeChangedResponse](#zen_api.em.hardware.v1.VacuumServiceRegisterOnVacuumModeChangedResponse)
  - [VacuumServiceRegisterOnVacuumStateChangedRequest](#zen_api.em.hardware.v1.VacuumServiceRegisterOnVacuumStateChangedRequest)
  - [VacuumServiceRegisterOnVacuumStateChangedResponse](#zen_api.em.hardware.v1.VacuumServiceRegisterOnVacuumStateChangedResponse)
  - [VacuumServiceRegisterOnValveStateChangedRequest](#zen_api.em.hardware.v1.VacuumServiceRegisterOnValveStateChangedRequest)
  - [VacuumServiceRegisterOnValveStateChangedResponse](#zen_api.em.hardware.v1.VacuumServiceRegisterOnValveStateChangedResponse)
  - [VacuumServiceSetTargetChamberPressureRequest](#zen_api.em.hardware.v1.VacuumServiceSetTargetChamberPressureRequest)
  - [VacuumServiceSetTargetChamberPressureResponse](#zen_api.em.hardware.v1.VacuumServiceSetTargetChamberPressureResponse)
  - [VacuumServiceSetVacuumModeRequest](#zen_api.em.hardware.v1.VacuumServiceSetVacuumModeRequest)
  - [VacuumServiceSetVacuumModeResponse](#zen_api.em.hardware.v1.VacuumServiceSetVacuumModeResponse)
  - [VacuumServiceVentRequest](#zen_api.em.hardware.v1.VacuumServiceVentRequest)
  - [VacuumServiceVentResponse](#zen_api.em.hardware.v1.VacuumServiceVentResponse)
  - [VacuumService](#zen_api.em.hardware.v1.VacuumService)
- [zen\_api/em/hardware/v1/vacuum\_state.proto](#zen_api/em/hardware/v1/vacuum_state.proto)
  - [VacuumState](#zen_api.em.hardware.v1.VacuumState)
- [zen\_api/em/hardware/v1/valve.proto](#zen_api/em/hardware/v1/valve.proto)
  - [Valve](#zen_api.em.hardware.v1.Valve)
- [zen\_api/em/hardware/v1/valve\_state.proto](#zen_api/em/hardware/v1/valve_state.proto)
  - [ValveState](#zen_api.em.hardware.v1.ValveState)
- [zen\_api/em/workflow/v1/create\_workflow\_service.proto](#zen_api/em/workflow/v1/create_workflow_service.proto)
  - [CreateWorkflowServiceAddAbsoluteTiltingActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddAbsoluteTiltingActionRequest)
  - [CreateWorkflowServiceAddAbsoluteTiltingActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddAbsoluteTiltingActionResponse)
  - [CreateWorkflowServiceAddAcquireNavCamImageActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddAcquireNavCamImageActionRequest)
  - [CreateWorkflowServiceAddAcquireNavCamImageActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddAcquireNavCamImageActionResponse)
  - [CreateWorkflowServiceAddAcquireStoreImageActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddAcquireStoreImageActionRequest)
  - [CreateWorkflowServiceAddAcquireStoreImageActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddAcquireStoreImageActionResponse)
  - [CreateWorkflowServiceAddChangeBeamStateActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddChangeBeamStateActionRequest)
  - [CreateWorkflowServiceAddChangeBeamStateActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddChangeBeamStateActionResponse)
  - [CreateWorkflowServiceAddChangeCurrentActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddChangeCurrentActionRequest)
  - [CreateWorkflowServiceAddChangeCurrentActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddChangeCurrentActionResponse)
  - [CreateWorkflowServiceAddChangeEhtActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddChangeEhtActionRequest)
  - [CreateWorkflowServiceAddChangeEhtActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddChangeEhtActionResponse)
  - [CreateWorkflowServiceAddEdsAcquisitionSettingsParameterActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddEdsAcquisitionSettingsParameterActionRequest)
  - [CreateWorkflowServiceAddEdsAcquisitionSettingsParameterActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddEdsAcquisitionSettingsParameterActionResponse)
  - [CreateWorkflowServiceAddFocusAndFovActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddFocusAndFovActionRequest)
  - [CreateWorkflowServiceAddFocusAndFovActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddFocusAndFovActionResponse)
  - [CreateWorkflowServiceAddGoToStoredPositionActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddGoToStoredPositionActionRequest)
  - [CreateWorkflowServiceAddGoToStoredPositionActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddGoToStoredPositionActionResponse)
  - [CreateWorkflowServiceAddInitializeActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddInitializeActionRequest)
  - [CreateWorkflowServiceAddInitializeActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddInitializeActionResponse)
  - [CreateWorkflowServiceAddMoveStageRelativeActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddMoveStageRelativeActionRequest)
  - [CreateWorkflowServiceAddMoveStageRelativeActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddMoveStageRelativeActionResponse)
  - [CreateWorkflowServiceAddPositionControlledTiltActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddPositionControlledTiltActionRequest)
  - [CreateWorkflowServiceAddPositionControlledTiltActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddPositionControlledTiltActionResponse)
  - [CreateWorkflowServiceAddRestoreFibProbeActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddRestoreFibProbeActionRequest)
  - [CreateWorkflowServiceAddRestoreFibProbeActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddRestoreFibProbeActionResponse)
  - [CreateWorkflowServiceAddSetFibProbeActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSetFibProbeActionRequest)
  - [CreateWorkflowServiceAddSetFibProbeActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSetFibProbeActionResponse)
  - [CreateWorkflowServiceAddSetFibWithValuesActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSetFibWithValuesActionRequest)
  - [CreateWorkflowServiceAddSetFibWithValuesActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSetFibWithValuesActionResponse)
  - [CreateWorkflowServiceAddSetVacuumParameterActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSetVacuumParameterActionRequest)
  - [CreateWorkflowServiceAddSetVacuumParameterActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSetVacuumParameterActionResponse)
  - [CreateWorkflowServiceAddSpotParameterActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSpotParameterActionRequest)
  - [CreateWorkflowServiceAddSpotParameterActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSpotParameterActionResponse)
  - [CreateWorkflowServiceAddStoreFibProbeActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddStoreFibProbeActionRequest)
  - [CreateWorkflowServiceAddStoreFibProbeActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddStoreFibProbeActionResponse)
  - [CreateWorkflowServiceAddTouchAlarmGeneratorActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddTouchAlarmGeneratorActionRequest)
  - [CreateWorkflowServiceAddTouchAlarmGeneratorActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddTouchAlarmGeneratorActionResponse)
  - [CreateWorkflowServiceAddVacuumCommandActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddVacuumCommandActionRequest)
  - [CreateWorkflowServiceAddVacuumCommandActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddVacuumCommandActionResponse)
  - [CreateWorkflowService](#zen_api.em.workflow.v1.CreateWorkflowService)
- [zen\_api/em/workflow/v1/eds\_acquisition\_mode.proto](#zen_api/em/workflow/v1/eds_acquisition_mode.proto)
  - [EdsAcquisitionMode](#zen_api.em.workflow.v1.EdsAcquisitionMode)
- [zen\_api/em/workflow/v1/eds\_spectrum\_acquisition\_settings.proto](#zen_api/em/workflow/v1/eds_spectrum_acquisition_settings.proto)
  - [EdsSpectrumAcquisitionSettings](#zen_api.em.workflow.v1.EdsSpectrumAcquisitionSettings)
- [zen\_api/em/workflow/v1/em\_region\_of\_interest.proto](#zen_api/em/workflow/v1/em_region_of_interest.proto)
  - [EmRegionOfInterest](#zen_api.em.workflow.v1.EmRegionOfInterest)
- [zen\_api/em/workflow/v1/run\_workflow\_service.proto](#zen_api/em/workflow/v1/run_workflow_service.proto)
  - [RunWorkflowServiceBreakRequest](#zen_api.em.workflow.v1.RunWorkflowServiceBreakRequest)
  - [RunWorkflowServiceBreakResponse](#zen_api.em.workflow.v1.RunWorkflowServiceBreakResponse)
  - [RunWorkflowServiceDefineAndRunCompleteWorkflowRequest](#zen_api.em.workflow.v1.RunWorkflowServiceDefineAndRunCompleteWorkflowRequest)
  - [RunWorkflowServiceDefineAndRunCompleteWorkflowResponse](#zen_api.em.workflow.v1.RunWorkflowServiceDefineAndRunCompleteWorkflowResponse)
  - [RunWorkflowServiceGetWorkflowByIdRequest](#zen_api.em.workflow.v1.RunWorkflowServiceGetWorkflowByIdRequest)
  - [RunWorkflowServiceGetWorkflowByIdResponse](#zen_api.em.workflow.v1.RunWorkflowServiceGetWorkflowByIdResponse)
  - [RunWorkflowServiceGetWorkflowStateRequest](#zen_api.em.workflow.v1.RunWorkflowServiceGetWorkflowStateRequest)
  - [RunWorkflowServiceGetWorkflowStateResponse](#zen_api.em.workflow.v1.RunWorkflowServiceGetWorkflowStateResponse)
  - [RunWorkflowServiceNextRequest](#zen_api.em.workflow.v1.RunWorkflowServiceNextRequest)
  - [RunWorkflowServiceNextResponse](#zen_api.em.workflow.v1.RunWorkflowServiceNextResponse)
  - [RunWorkflowServicePauseRequest](#zen_api.em.workflow.v1.RunWorkflowServicePauseRequest)
  - [RunWorkflowServicePauseResponse](#zen_api.em.workflow.v1.RunWorkflowServicePauseResponse)
  - [RunWorkflowServiceRegisterOnActionExecutionIdChangedRequest](#zen_api.em.workflow.v1.RunWorkflowServiceRegisterOnActionExecutionIdChangedRequest)
  - [RunWorkflowServiceRegisterOnActionExecutionIdChangedResponse](#zen_api.em.workflow.v1.RunWorkflowServiceRegisterOnActionExecutionIdChangedResponse)
  - [RunWorkflowServiceRegisterOnWorkflowStateChangedRequest](#zen_api.em.workflow.v1.RunWorkflowServiceRegisterOnWorkflowStateChangedRequest)
  - [RunWorkflowServiceRegisterOnWorkflowStateChangedResponse](#zen_api.em.workflow.v1.RunWorkflowServiceRegisterOnWorkflowStateChangedResponse)
  - [RunWorkflowServiceResumeRequest](#zen_api.em.workflow.v1.RunWorkflowServiceResumeRequest)
  - [RunWorkflowServiceResumeResponse](#zen_api.em.workflow.v1.RunWorkflowServiceResumeResponse)
  - [RunWorkflowServiceRunWorkflowRequest](#zen_api.em.workflow.v1.RunWorkflowServiceRunWorkflowRequest)
  - [RunWorkflowServiceRunWorkflowResponse](#zen_api.em.workflow.v1.RunWorkflowServiceRunWorkflowResponse)
  - [RunWorkflowServiceSetNormalModeRequest](#zen_api.em.workflow.v1.RunWorkflowServiceSetNormalModeRequest)
  - [RunWorkflowServiceSetNormalModeResponse](#zen_api.em.workflow.v1.RunWorkflowServiceSetNormalModeResponse)
  - [RunWorkflowServiceSetStepModeRequest](#zen_api.em.workflow.v1.RunWorkflowServiceSetStepModeRequest)
  - [RunWorkflowServiceSetStepModeResponse](#zen_api.em.workflow.v1.RunWorkflowServiceSetStepModeResponse)
  - [RunWorkflowServiceStartRequest](#zen_api.em.workflow.v1.RunWorkflowServiceStartRequest)
  - [RunWorkflowServiceStartResponse](#zen_api.em.workflow.v1.RunWorkflowServiceStartResponse)
  - [RunWorkflowServiceStepRequest](#zen_api.em.workflow.v1.RunWorkflowServiceStepRequest)
  - [RunWorkflowServiceStepResponse](#zen_api.em.workflow.v1.RunWorkflowServiceStepResponse)
  - [RunWorkflowServiceStopEmergencyRequest](#zen_api.em.workflow.v1.RunWorkflowServiceStopEmergencyRequest)
  - [RunWorkflowServiceStopEmergencyResponse](#zen_api.em.workflow.v1.RunWorkflowServiceStopEmergencyResponse)
  - [RunWorkflowServiceStopRequest](#zen_api.em.workflow.v1.RunWorkflowServiceStopRequest)
  - [RunWorkflowServiceStopResponse](#zen_api.em.workflow.v1.RunWorkflowServiceStopResponse)
  - [RunWorkflowService](#zen_api.em.workflow.v1.RunWorkflowService)
- [zen\_api/em/workflow/v1/vacuum\_parameter.proto](#zen_api/em/workflow/v1/vacuum_parameter.proto)
  - [VacuumParameter](#zen_api.em.workflow.v1.VacuumParameter)
- [zen\_api/em/workflow/v1/workflow\_admin\_service.proto](#zen_api/em/workflow/v1/workflow_admin_service.proto)
  - [WorkflowAdminServiceDeleteWorkflowByIdRequest](#zen_api.em.workflow.v1.WorkflowAdminServiceDeleteWorkflowByIdRequest)
  - [WorkflowAdminServiceDeleteWorkflowByIdResponse](#zen_api.em.workflow.v1.WorkflowAdminServiceDeleteWorkflowByIdResponse)
  - [WorkflowAdminServiceGetAvailableWorkflowIdsRequest](#zen_api.em.workflow.v1.WorkflowAdminServiceGetAvailableWorkflowIdsRequest)
  - [WorkflowAdminServiceGetAvailableWorkflowIdsResponse](#zen_api.em.workflow.v1.WorkflowAdminServiceGetAvailableWorkflowIdsResponse)
  - [WorkflowAdminService](#zen_api.em.workflow.v1.WorkflowAdminService)
- [zen\_api/em/workflow/v1/workflow\_state.proto](#zen_api/em/workflow/v1/workflow_state.proto)
  - [WorkflowState](#zen_api.em.workflow.v1.WorkflowState)
- [zen\_api/lm/acquisition/v1/autofocus\_contrast\_measure.proto](#zen_api/lm/acquisition/v1/autofocus_contrast_measure.proto)
  - [AutofocusContrastMeasure](#zen_api.lm.acquisition.v1.AutofocusContrastMeasure)
- [zen\_api/lm/acquisition/v1/autofocus\_mode.proto](#zen_api/lm/acquisition/v1/autofocus_mode.proto)
  - [AutofocusMode](#zen_api.lm.acquisition.v1.AutofocusMode)
- [zen\_api/lm/acquisition/v1/autofocus\_sampling.proto](#zen_api/lm/acquisition/v1/autofocus_sampling.proto)
  - [AutofocusSampling](#zen_api.lm.acquisition.v1.AutofocusSampling)
- [zen\_api/lm/acquisition/v1/channel\_info.proto](#zen_api/lm/acquisition/v1/channel_info.proto)
  - [ChannelInfo](#zen_api.lm.acquisition.v1.ChannelInfo)
- [zen\_api/lm/acquisition/v1/definite\_focus\_service.proto](#zen_api/lm/acquisition/v1/definite_focus_service.proto)
  - [DefiniteFocusServiceFindSurfaceRequest](#zen_api.lm.acquisition.v1.DefiniteFocusServiceFindSurfaceRequest)
  - [DefiniteFocusServiceFindSurfaceResponse](#zen_api.lm.acquisition.v1.DefiniteFocusServiceFindSurfaceResponse)
  - [DefiniteFocusServiceLockFocusRequest](#zen_api.lm.acquisition.v1.DefiniteFocusServiceLockFocusRequest)
  - [DefiniteFocusServiceLockFocusResponse](#zen_api.lm.acquisition.v1.DefiniteFocusServiceLockFocusResponse)
  - [DefiniteFocusServiceRecallFocusRequest](#zen_api.lm.acquisition.v1.DefiniteFocusServiceRecallFocusRequest)
  - [DefiniteFocusServiceRecallFocusResponse](#zen_api.lm.acquisition.v1.DefiniteFocusServiceRecallFocusResponse)
  - [DefiniteFocusServiceStoreFocusRequest](#zen_api.lm.acquisition.v1.DefiniteFocusServiceStoreFocusRequest)
  - [DefiniteFocusServiceStoreFocusResponse](#zen_api.lm.acquisition.v1.DefiniteFocusServiceStoreFocusResponse)
  - [DefiniteFocusServiceUnlockFocusRequest](#zen_api.lm.acquisition.v1.DefiniteFocusServiceUnlockFocusRequest)
  - [DefiniteFocusServiceUnlockFocusResponse](#zen_api.lm.acquisition.v1.DefiniteFocusServiceUnlockFocusResponse)
  - [DefiniteFocusService](#zen_api.lm.acquisition.v1.DefiniteFocusService)
- [zen\_api/lm/acquisition/v1/experiment\_sw\_autofocus\_service.proto](#zen_api/lm/acquisition/v1/experiment_sw_autofocus_service.proto)
  - [ExperimentSwAutofocusServiceExportRequest](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceExportRequest)
  - [ExperimentSwAutofocusServiceExportResponse](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceExportResponse)
  - [ExperimentSwAutofocusServiceFindAutoFocusRequest](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceFindAutoFocusRequest)
  - [ExperimentSwAutofocusServiceFindAutoFocusResponse](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceFindAutoFocusResponse)
  - [ExperimentSwAutofocusServiceGetAutofocusParametersRequest](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceGetAutofocusParametersRequest)
  - [ExperimentSwAutofocusServiceGetAutofocusParametersResponse](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceGetAutofocusParametersResponse)
  - [ExperimentSwAutofocusServiceImportRequest](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceImportRequest)
  - [ExperimentSwAutofocusServiceImportResponse](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceImportResponse)
  - [ExperimentSwAutofocusServiceSetAutofocusParametersRequest](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceSetAutofocusParametersRequest)
  - [ExperimentSwAutofocusServiceSetAutofocusParametersResponse](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceSetAutofocusParametersResponse)
  - [ExperimentSwAutofocusService](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusService)
- [zen\_api/lm/acquisition/v1/position3d.proto](#zen_api/lm/acquisition/v1/position3d.proto)
  - [Position3d](#zen_api.lm.acquisition.v1.Position3d)
- [zen\_api/lm/acquisition/v1/region\_contour.proto](#zen_api/lm/acquisition/v1/region_contour.proto)
  - [RegionContour](#zen_api.lm.acquisition.v1.RegionContour)
  - [RegionEllipse](#zen_api.lm.acquisition.v1.RegionEllipse)
  - [RegionPolygon](#zen_api.lm.acquisition.v1.RegionPolygon)
  - [RegionRectangle](#zen_api.lm.acquisition.v1.RegionRectangle)
- [zen\_api/lm/acquisition/v1/region\_point.proto](#zen_api/lm/acquisition/v1/region_point.proto)
  - [RegionPoint](#zen_api.lm.acquisition.v1.RegionPoint)
- [zen\_api/lm/acquisition/v1/region\_rect.proto](#zen_api/lm/acquisition/v1/region_rect.proto)
  - [RegionRect](#zen_api.lm.acquisition.v1.RegionRect)
- [zen\_api/lm/acquisition/v1/tiles\_service.proto](#zen_api/lm/acquisition/v1/tiles_service.proto)
  - [TilesServiceAddEllipseTileRegionRequest](#zen_api.lm.acquisition.v1.TilesServiceAddEllipseTileRegionRequest)
  - [TilesServiceAddEllipseTileRegionResponse](#zen_api.lm.acquisition.v1.TilesServiceAddEllipseTileRegionResponse)
  - [TilesServiceAddPolygonTileRegionRequest](#zen_api.lm.acquisition.v1.TilesServiceAddPolygonTileRegionRequest)
  - [TilesServiceAddPolygonTileRegionResponse](#zen_api.lm.acquisition.v1.TilesServiceAddPolygonTileRegionResponse)
  - [TilesServiceAddPositionsRequest](#zen_api.lm.acquisition.v1.TilesServiceAddPositionsRequest)
  - [TilesServiceAddPositionsResponse](#zen_api.lm.acquisition.v1.TilesServiceAddPositionsResponse)
  - [TilesServiceAddRectangleTileRegionRequest](#zen_api.lm.acquisition.v1.TilesServiceAddRectangleTileRegionRequest)
  - [TilesServiceAddRectangleTileRegionResponse](#zen_api.lm.acquisition.v1.TilesServiceAddRectangleTileRegionResponse)
  - [TilesServiceClearRequest](#zen_api.lm.acquisition.v1.TilesServiceClearRequest)
  - [TilesServiceClearResponse](#zen_api.lm.acquisition.v1.TilesServiceClearResponse)
  - [TilesServiceIsTilesExperimentRequest](#zen_api.lm.acquisition.v1.TilesServiceIsTilesExperimentRequest)
  - [TilesServiceIsTilesExperimentResponse](#zen_api.lm.acquisition.v1.TilesServiceIsTilesExperimentResponse)
  - [TilesService](#zen_api.lm.acquisition.v1.TilesService)
- [zen\_api/lm/acquisition/v1/time\_series\_info.proto](#zen_api/lm/acquisition/v1/time_series_info.proto)
  - [TimeSeriesInfo](#zen_api.lm.acquisition.v1.TimeSeriesInfo)
- [zen\_api/lm/acquisition/v1/time\_series\_service.proto](#zen_api/lm/acquisition/v1/time_series_service.proto)
  - [TimeSeriesServiceGetTimeSeriesInfoRequest](#zen_api.lm.acquisition.v1.TimeSeriesServiceGetTimeSeriesInfoRequest)
  - [TimeSeriesServiceGetTimeSeriesInfoResponse](#zen_api.lm.acquisition.v1.TimeSeriesServiceGetTimeSeriesInfoResponse)
  - [TimeSeriesServiceSetTimeSeriesInfoRequest](#zen_api.lm.acquisition.v1.TimeSeriesServiceSetTimeSeriesInfoRequest)
  - [TimeSeriesServiceSetTimeSeriesInfoResponse](#zen_api.lm.acquisition.v1.TimeSeriesServiceSetTimeSeriesInfoResponse)
  - [TimeSeriesService](#zen_api.lm.acquisition.v1.TimeSeriesService)
- [zen\_api/lm/acquisition/v1/time\_series\_service\_time\_series\_info.proto](#zen_api/lm/acquisition/v1/time_series_service_time_series_info.proto)
  - [TimeSeriesServiceTimeSeriesInfo](#zen_api.lm.acquisition.v1.TimeSeriesServiceTimeSeriesInfo)
- [zen\_api/lm/acquisition/v1/time\_series\_service\_time\_unit.proto](#zen_api/lm/acquisition/v1/time_series_service_time_unit.proto)
  - [TimeSeriesServiceTimeUnit](#zen_api.lm.acquisition.v1.TimeSeriesServiceTimeUnit)
- [zen\_api/lm/acquisition/v1/time\_series\_service\_time\_unit\_extended.proto](#zen_api/lm/acquisition/v1/time_series_service_time_unit_extended.proto)
  - [TimeSeriesServiceTimeUnitExtended](#zen_api.lm.acquisition.v1.TimeSeriesServiceTimeUnitExtended)
- [zen\_api/lm/acquisition/v1/time\_unit.proto](#zen_api/lm/acquisition/v1/time_unit.proto)
  - [TimeUnit](#zen_api.lm.acquisition.v1.TimeUnit)
- [zen\_api/lm/acquisition/v1/time\_unit\_extended.proto](#zen_api/lm/acquisition/v1/time_unit_extended.proto)
  - [TimeUnitExtended](#zen_api.lm.acquisition.v1.TimeUnitExtended)
- [zen\_api/lm/acquisition/v1/track\_info.proto](#zen_api/lm/acquisition/v1/track_info.proto)
  - [TrackInfo](#zen_api.lm.acquisition.v1.TrackInfo)
- [zen\_api/lm/acquisition/v1/track\_service.proto](#zen_api/lm/acquisition/v1/track_service.proto)
  - [TrackServiceActivateChannelRequest](#zen_api.lm.acquisition.v1.TrackServiceActivateChannelRequest)
  - [TrackServiceActivateChannelResponse](#zen_api.lm.acquisition.v1.TrackServiceActivateChannelResponse)
  - [TrackServiceActivateTrackRequest](#zen_api.lm.acquisition.v1.TrackServiceActivateTrackRequest)
  - [TrackServiceActivateTrackResponse](#zen_api.lm.acquisition.v1.TrackServiceActivateTrackResponse)
  - [TrackServiceDeactivateChannelRequest](#zen_api.lm.acquisition.v1.TrackServiceDeactivateChannelRequest)
  - [TrackServiceDeactivateChannelResponse](#zen_api.lm.acquisition.v1.TrackServiceDeactivateChannelResponse)
  - [TrackServiceDeactivateTrackRequest](#zen_api.lm.acquisition.v1.TrackServiceDeactivateTrackRequest)
  - [TrackServiceDeactivateTrackResponse](#zen_api.lm.acquisition.v1.TrackServiceDeactivateTrackResponse)
  - [TrackServiceGetTrackInfoRequest](#zen_api.lm.acquisition.v1.TrackServiceGetTrackInfoRequest)
  - [TrackServiceGetTrackInfoResponse](#zen_api.lm.acquisition.v1.TrackServiceGetTrackInfoResponse)
  - [TrackService](#zen_api.lm.acquisition.v1.TrackService)
- [zen\_api/lm/acquisition/v1/zstack\_service.proto](#zen_api/lm/acquisition/v1/zstack_service.proto)
  - [ZStackServiceGetZStackInfoRequest](#zen_api.lm.acquisition.v1.ZStackServiceGetZStackInfoRequest)
  - [ZStackServiceGetZStackInfoResponse](#zen_api.lm.acquisition.v1.ZStackServiceGetZStackInfoResponse)
  - [ZStackServiceIsZStackExperimentRequest](#zen_api.lm.acquisition.v1.ZStackServiceIsZStackExperimentRequest)
  - [ZStackServiceIsZStackExperimentResponse](#zen_api.lm.acquisition.v1.ZStackServiceIsZStackExperimentResponse)
  - [ZStackServiceModifyZStackCenterRangeRequest](#zen_api.lm.acquisition.v1.ZStackServiceModifyZStackCenterRangeRequest)
  - [ZStackServiceModifyZStackCenterRangeResponse](#zen_api.lm.acquisition.v1.ZStackServiceModifyZStackCenterRangeResponse)
  - [ZStackServiceModifyZStackFirstLastRequest](#zen_api.lm.acquisition.v1.ZStackServiceModifyZStackFirstLastRequest)
  - [ZStackServiceModifyZStackFirstLastResponse](#zen_api.lm.acquisition.v1.ZStackServiceModifyZStackFirstLastResponse)
  - [ZStackService](#zen_api.lm.acquisition.v1.ZStackService)
- [zen\_api/lm/acquisition/v2/region\_contour.proto](#zen_api/lm/acquisition/v2/region_contour.proto)
  - [RegionContour](#zen_api.lm.acquisition.v2.RegionContour)
  - [RegionEllipse](#zen_api.lm.acquisition.v2.RegionEllipse)
  - [RegionPolygon](#zen_api.lm.acquisition.v2.RegionPolygon)
  - [RegionRectangle](#zen_api.lm.acquisition.v2.RegionRectangle)
- [zen\_api/lm/acquisition/v2/region\_point.proto](#zen_api/lm/acquisition/v2/region_point.proto)
  - [RegionPoint](#zen_api.lm.acquisition.v2.RegionPoint)
- [zen\_api/lm/acquisition/v2/region\_rect.proto](#zen_api/lm/acquisition/v2/region_rect.proto)
  - [RegionRect](#zen_api.lm.acquisition.v2.RegionRect)
- [zen\_api/lm/hardware/v1/configured\_container\_info.proto](#zen_api/lm/hardware/v1/configured_container_info.proto)
  - [ConfiguredContainerInfo](#zen_api.lm.hardware.v1.ConfiguredContainerInfo)
- [zen\_api/lm/hardware/v1/focus\_service.proto](#zen_api/lm/hardware/v1/focus_service.proto)
  - [FocusServiceGetAccelerationRequest](#zen_api.lm.hardware.v1.FocusServiceGetAccelerationRequest)
  - [FocusServiceGetAccelerationResponse](#zen_api.lm.hardware.v1.FocusServiceGetAccelerationResponse)
  - [FocusServiceGetPositionRequest](#zen_api.lm.hardware.v1.FocusServiceGetPositionRequest)
  - [FocusServiceGetPositionResponse](#zen_api.lm.hardware.v1.FocusServiceGetPositionResponse)
  - [FocusServiceGetSpeedRequest](#zen_api.lm.hardware.v1.FocusServiceGetSpeedRequest)
  - [FocusServiceGetSpeedResponse](#zen_api.lm.hardware.v1.FocusServiceGetSpeedResponse)
  - [FocusServiceMoveToRequest](#zen_api.lm.hardware.v1.FocusServiceMoveToRequest)
  - [FocusServiceMoveToResponse](#zen_api.lm.hardware.v1.FocusServiceMoveToResponse)
  - [FocusServiceSetAccelerationRequest](#zen_api.lm.hardware.v1.FocusServiceSetAccelerationRequest)
  - [FocusServiceSetAccelerationResponse](#zen_api.lm.hardware.v1.FocusServiceSetAccelerationResponse)
  - [FocusServiceSetSpeedRequest](#zen_api.lm.hardware.v1.FocusServiceSetSpeedRequest)
  - [FocusServiceSetSpeedResponse](#zen_api.lm.hardware.v1.FocusServiceSetSpeedResponse)
  - [FocusServiceStopRequest](#zen_api.lm.hardware.v1.FocusServiceStopRequest)
  - [FocusServiceStopResponse](#zen_api.lm.hardware.v1.FocusServiceStopResponse)
  - [FocusService](#zen_api.lm.hardware.v1.FocusService)
- [zen\_api/lm/hardware/v1/sample\_carrier\_service.proto](#zen_api/lm/hardware/v1/sample_carrier_service.proto)
  - [SampleCarrierServiceActivateContainerRangeRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceActivateContainerRangeRequest)
  - [SampleCarrierServiceActivateContainerRangeResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceActivateContainerRangeResponse)
  - [SampleCarrierServiceActivateContainerRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceActivateContainerRequest)
  - [SampleCarrierServiceActivateContainerResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceActivateContainerResponse)
  - [SampleCarrierServiceActivateContainersRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceActivateContainersRequest)
  - [SampleCarrierServiceActivateContainersResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceActivateContainersResponse)
  - [SampleCarrierServiceDeactivateContainerRangeRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceDeactivateContainerRangeRequest)
  - [SampleCarrierServiceDeactivateContainerRangeResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceDeactivateContainerRangeResponse)
  - [SampleCarrierServiceDeactivateContainerRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceDeactivateContainerRequest)
  - [SampleCarrierServiceDeactivateContainerResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceDeactivateContainerResponse)
  - [SampleCarrierServiceDeactivateContainersRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceDeactivateContainersRequest)
  - [SampleCarrierServiceDeactivateContainersResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceDeactivateContainersResponse)
  - [SampleCarrierServiceGetConfiguredContainersRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceGetConfiguredContainersRequest)
  - [SampleCarrierServiceGetConfiguredContainersResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceGetConfiguredContainersResponse)
  - [SampleCarrierServiceGetCurrentContainerRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceGetCurrentContainerRequest)
  - [SampleCarrierServiceGetCurrentContainerResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceGetCurrentContainerResponse)
  - [SampleCarrierServiceGetInfoRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceGetInfoRequest)
  - [SampleCarrierServiceGetInfoResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceGetInfoResponse)
  - [SampleCarrierServiceMoveToContainerRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceMoveToContainerRequest)
  - [SampleCarrierServiceMoveToContainerResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceMoveToContainerResponse)
  - [SampleCarrierService](#zen_api.lm.hardware.v1.SampleCarrierService)
- [zen\_api/lm/hardware/v2/camera\_service.proto](#zen_api/lm/hardware/v2/camera_service.proto)
  - [CameraServiceConfigureCameraRequest](#zen_api.lm.hardware.v2.CameraServiceConfigureCameraRequest)
  - [CameraServiceConfigureCameraResponse](#zen_api.lm.hardware.v2.CameraServiceConfigureCameraResponse)
  - [CameraServiceGetAllCamerasResponse](#zen_api.lm.hardware.v2.CameraServiceGetAllCamerasResponse)
  - [CameraServiceGetCameraRequest](#zen_api.lm.hardware.v2.CameraServiceGetCameraRequest)
  - [CameraServiceGetCameraResponse](#zen_api.lm.hardware.v2.CameraServiceGetCameraResponse)
  - [CameraServiceGetCamerasRequest](#zen_api.lm.hardware.v2.CameraServiceGetCamerasRequest)
  - [CameraService](#zen_api.lm.hardware.v2.CameraService)
- [zen\_api/lm/hardware/v2/filter\_data.proto](#zen_api/lm/hardware/v2/filter_data.proto)
  - [FilterData](#zen_api.lm.hardware.v2.FilterData)
- [zen\_api/lm/hardware/v2/filter\_wheel\_service.proto](#zen_api/lm/hardware/v2/filter_wheel_service.proto)
  - [FilterWheelServiceGetFiltersRequest](#zen_api.lm.hardware.v2.FilterWheelServiceGetFiltersRequest)
  - [FilterWheelServiceGetFiltersResponse](#zen_api.lm.hardware.v2.FilterWheelServiceGetFiltersResponse)
  - [FilterWheelServiceGetPositionRequest](#zen_api.lm.hardware.v2.FilterWheelServiceGetPositionRequest)
  - [FilterWheelServiceGetPositionResponse](#zen_api.lm.hardware.v2.FilterWheelServiceGetPositionResponse)
  - [FilterWheelServiceMoveToRequest](#zen_api.lm.hardware.v2.FilterWheelServiceMoveToRequest)
  - [FilterWheelServiceMoveToResponse](#zen_api.lm.hardware.v2.FilterWheelServiceMoveToResponse)
  - [FilterWheelService](#zen_api.lm.hardware.v2.FilterWheelService)
- [zen\_api/lm/hardware/v2/focus\_service.proto](#zen_api/lm/hardware/v2/focus_service.proto)
  - [FocusServiceGetAccelerationRequest](#zen_api.lm.hardware.v2.FocusServiceGetAccelerationRequest)
  - [FocusServiceGetAccelerationResponse](#zen_api.lm.hardware.v2.FocusServiceGetAccelerationResponse)
  - [FocusServiceGetPositionRequest](#zen_api.lm.hardware.v2.FocusServiceGetPositionRequest)
  - [FocusServiceGetPositionResponse](#zen_api.lm.hardware.v2.FocusServiceGetPositionResponse)
  - [FocusServiceGetSpeedRequest](#zen_api.lm.hardware.v2.FocusServiceGetSpeedRequest)
  - [FocusServiceGetSpeedResponse](#zen_api.lm.hardware.v2.FocusServiceGetSpeedResponse)
  - [FocusServiceMoveToRequest](#zen_api.lm.hardware.v2.FocusServiceMoveToRequest)
  - [FocusServiceMoveToResponse](#zen_api.lm.hardware.v2.FocusServiceMoveToResponse)
  - [FocusServiceSetAccelerationRequest](#zen_api.lm.hardware.v2.FocusServiceSetAccelerationRequest)
  - [FocusServiceSetAccelerationResponse](#zen_api.lm.hardware.v2.FocusServiceSetAccelerationResponse)
  - [FocusServiceSetSpeedRequest](#zen_api.lm.hardware.v2.FocusServiceSetSpeedRequest)
  - [FocusServiceSetSpeedResponse](#zen_api.lm.hardware.v2.FocusServiceSetSpeedResponse)
  - [FocusServiceStopRequest](#zen_api.lm.hardware.v2.FocusServiceStopRequest)
  - [FocusServiceStopResponse](#zen_api.lm.hardware.v2.FocusServiceStopResponse)
  - [FocusService](#zen_api.lm.hardware.v2.FocusService)
- [zen\_api/lm/hardware/v2/get\_camera\_data.proto](#zen_api/lm/hardware/v2/get_camera_data.proto)
  - [GetCameraData](#zen_api.lm.hardware.v2.GetCameraData)
- [zen\_api/lm/hardware/v2/objective\_changer\_immersion\_types.proto](#zen_api/lm/hardware/v2/objective_changer_immersion_types.proto)
  - [ObjectiveChangerImmersionTypes](#zen_api.lm.hardware.v2.ObjectiveChangerImmersionTypes)
- [zen\_api/lm/hardware/v2/objective\_changer\_service.proto](#zen_api/lm/hardware/v2/objective_changer_service.proto)
  - [ObjectiveChangerServiceGetObjectivesRequest](#zen_api.lm.hardware.v2.ObjectiveChangerServiceGetObjectivesRequest)
  - [ObjectiveChangerServiceGetObjectivesResponse](#zen_api.lm.hardware.v2.ObjectiveChangerServiceGetObjectivesResponse)
  - [ObjectiveChangerServiceGetPositionRequest](#zen_api.lm.hardware.v2.ObjectiveChangerServiceGetPositionRequest)
  - [ObjectiveChangerServiceGetPositionResponse](#zen_api.lm.hardware.v2.ObjectiveChangerServiceGetPositionResponse)
  - [ObjectiveChangerServiceMoveToRequest](#zen_api.lm.hardware.v2.ObjectiveChangerServiceMoveToRequest)
  - [ObjectiveChangerServiceMoveToResponse](#zen_api.lm.hardware.v2.ObjectiveChangerServiceMoveToResponse)
  - [ObjectiveChangerService](#zen_api.lm.hardware.v2.ObjectiveChangerService)
- [zen\_api/lm/hardware/v2/objective\_data.proto](#zen_api/lm/hardware/v2/objective_data.proto)
  - [ObjectiveData](#zen_api.lm.hardware.v2.ObjectiveData)
- [zen\_api/lm/hardware/v2/optovar\_data.proto](#zen_api/lm/hardware/v2/optovar_data.proto)
  - [OptovarData](#zen_api.lm.hardware.v2.OptovarData)
- [zen\_api/lm/hardware/v2/optovar\_service.proto](#zen_api/lm/hardware/v2/optovar_service.proto)
  - [OptovarServiceGetOptovarsRequest](#zen_api.lm.hardware.v2.OptovarServiceGetOptovarsRequest)
  - [OptovarServiceGetOptovarsResponse](#zen_api.lm.hardware.v2.OptovarServiceGetOptovarsResponse)
  - [OptovarServiceGetPositionRequest](#zen_api.lm.hardware.v2.OptovarServiceGetPositionRequest)
  - [OptovarServiceGetPositionResponse](#zen_api.lm.hardware.v2.OptovarServiceGetPositionResponse)
  - [OptovarServiceMoveToRequest](#zen_api.lm.hardware.v2.OptovarServiceMoveToRequest)
  - [OptovarServiceMoveToResponse](#zen_api.lm.hardware.v2.OptovarServiceMoveToResponse)
  - [OptovarService](#zen_api.lm.hardware.v2.OptovarService)
- [zen\_api/lm/hardware/v2/reflector\_changer\_service.proto](#zen_api/lm/hardware/v2/reflector_changer_service.proto)
  - [ReflectorChangerServiceGetPositionRequest](#zen_api.lm.hardware.v2.ReflectorChangerServiceGetPositionRequest)
  - [ReflectorChangerServiceGetPositionResponse](#zen_api.lm.hardware.v2.ReflectorChangerServiceGetPositionResponse)
  - [ReflectorChangerServiceGetReflectorsRequest](#zen_api.lm.hardware.v2.ReflectorChangerServiceGetReflectorsRequest)
  - [ReflectorChangerServiceGetReflectorsResponse](#zen_api.lm.hardware.v2.ReflectorChangerServiceGetReflectorsResponse)
  - [ReflectorChangerServiceMoveToRequest](#zen_api.lm.hardware.v2.ReflectorChangerServiceMoveToRequest)
  - [ReflectorChangerServiceMoveToResponse](#zen_api.lm.hardware.v2.ReflectorChangerServiceMoveToResponse)
  - [ReflectorChangerService](#zen_api.lm.hardware.v2.ReflectorChangerService)
- [zen\_api/lm/hardware/v2/reflector\_data.proto](#zen_api/lm/hardware/v2/reflector_data.proto)
  - [ReflectorData](#zen_api.lm.hardware.v2.ReflectorData)
- [zen\_api/lm/hardware/v2/set\_camera\_data.proto](#zen_api/lm/hardware/v2/set_camera_data.proto)
  - [SetCameraData](#zen_api.lm.hardware.v2.SetCameraData)
- [zen\_api/lm/live\_scan/v1/live\_scan\_service.proto](#zen_api/lm/live_scan/v1/live_scan_service.proto)
  - [LiveScanServiceEjectTrayRequest](#zen_api.lm.live_scan.v1.LiveScanServiceEjectTrayRequest)
  - [LiveScanServiceEjectTrayResponse](#zen_api.lm.live_scan.v1.LiveScanServiceEjectTrayResponse)
  - [LiveScanServiceGetConfigurationRequest](#zen_api.lm.live_scan.v1.LiveScanServiceGetConfigurationRequest)
  - [LiveScanServiceGetConfigurationResponse](#zen_api.lm.live_scan.v1.LiveScanServiceGetConfigurationResponse)
  - [LiveScanServiceLoadTrayAndPrescanRequest](#zen_api.lm.live_scan.v1.LiveScanServiceLoadTrayAndPrescanRequest)
  - [LiveScanServiceLoadTrayAndPrescanResponse](#zen_api.lm.live_scan.v1.LiveScanServiceLoadTrayAndPrescanResponse)
  - [LiveScanServiceSetConfigurationRequest](#zen_api.lm.live_scan.v1.LiveScanServiceSetConfigurationRequest)
  - [LiveScanServiceSetConfigurationResponse](#zen_api.lm.live_scan.v1.LiveScanServiceSetConfigurationResponse)
  - [LiveScanService](#zen_api.lm.live_scan.v1.LiveScanService)
- [zen\_api/lm/live\_scan/v1/live\_scan\_service\_configuration.proto](#zen_api/lm/live_scan/v1/live_scan_service_configuration.proto)
  - [LiveScanServiceConfiguration](#zen_api.lm.live_scan.v1.LiveScanServiceConfiguration)
- [zen\_api/lm/slide\_scan/v1/channel\_settings.proto](#zen_api/lm/slide_scan/v1/channel_settings.proto)
  - [ChannelSettings](#zen_api.lm.slide_scan.v1.ChannelSettings)
- [zen\_api/lm/slide\_scan/v1/information\_base.proto](#zen_api/lm/slide_scan/v1/information_base.proto)
  - [InformationBase](#zen_api.lm.slide_scan.v1.InformationBase)
  - [MagazineInformation](#zen_api.lm.slide_scan.v1.MagazineInformation)
  - [SimpleInformation](#zen_api.lm.slide_scan.v1.SimpleInformation)
  - [SlideScanSystemInformation](#zen_api.lm.slide_scan.v1.SlideScanSystemInformation)
- [zen\_api/lm/slide\_scan/v1/profile\_information.proto](#zen_api/lm/slide_scan/v1/profile_information.proto)
  - [ProfileInformation](#zen_api.lm.slide_scan.v1.ProfileInformation)
- [zen\_api/lm/slide\_scan/v1/region\_definition.proto](#zen_api/lm/slide_scan/v1/region_definition.proto)
  - [RegionDefinition](#zen_api.lm.slide_scan.v1.RegionDefinition)
- [zen\_api/lm/slide\_scan/v1/response\_code.proto](#zen_api/lm/slide_scan/v1/response_code.proto)
  - [ResponseCode](#zen_api.lm.slide_scan.v1.ResponseCode)
- [zen\_api/lm/slide\_scan/v1/response\_type.proto](#zen_api/lm/slide_scan/v1/response_type.proto)
  - [ResponseType](#zen_api.lm.slide_scan.v1.ResponseType)
- [zen\_api/lm/slide\_scan/v1/scan\_profile\_options\_override.proto](#zen_api/lm/slide_scan/v1/scan_profile_options_override.proto)
  - [ScanProfileOptionsOverride](#zen_api.lm.slide_scan.v1.ScanProfileOptionsOverride)
- [zen\_api/lm/slide\_scan/v1/slide\_information.proto](#zen_api/lm/slide_scan/v1/slide_information.proto)
  - [SlideInformation](#zen_api.lm.slide_scan.v1.SlideInformation)
- [zen\_api/lm/slide\_scan/v1/slide\_position\_information.proto](#zen_api/lm/slide_scan/v1/slide_position_information.proto)
  - [SlidePositionInformation](#zen_api.lm.slide_scan.v1.SlidePositionInformation)
- [zen\_api/lm/slide\_scan/v1/slide\_scan\_service.proto](#zen_api/lm/slide_scan/v1/slide_scan_service.proto)
  - [GeneralResponse](#zen_api.lm.slide_scan.v1.GeneralResponse)
  - [SlideScanServiceGetChannelSettingsRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceGetChannelSettingsRequest)
  - [SlideScanServiceGetChannelSettingsResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceGetChannelSettingsResponse)
  - [SlideScanServiceGetMagazineStateRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceGetMagazineStateRequest)
  - [SlideScanServiceGetMagazineStateResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceGetMagazineStateResponse)
  - [SlideScanServiceGetStorageFolderRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceGetStorageFolderRequest)
  - [SlideScanServiceGetStorageFolderResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceGetStorageFolderResponse)
  - [SlideScanServiceObserveRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceObserveRequest)
  - [SlideScanServiceObserveResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceObserveResponse)
  - [SlideScanServiceResetSlideStatesRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceResetSlideStatesRequest)
  - [SlideScanServiceResetSlideStatesResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceResetSlideStatesResponse)
  - [SlideScanServiceSetStorageFolderRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceSetStorageFolderRequest)
  - [SlideScanServiceSetStorageFolderResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceSetStorageFolderResponse)
  - [SlideScanServiceStartScanPreviewRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceStartScanPreviewRequest)
  - [SlideScanServiceStartScanPreviewResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceStartScanPreviewResponse)
  - [SlideScanServiceStartScanProfileRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceStartScanProfileRequest)
  - [SlideScanServiceStartScanProfileResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceStartScanProfileResponse)
  - [SlideScanServiceStopScanPreviewRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceStopScanPreviewRequest)
  - [SlideScanServiceStopScanPreviewResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceStopScanPreviewResponse)
  - [SlideScanServiceStopScanProfileRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceStopScanProfileRequest)
  - [SlideScanServiceStopScanProfileResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceStopScanProfileResponse)
  - [SlideScanServiceUnmarkSlidesRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceUnmarkSlidesRequest)
  - [SlideScanServiceUnmarkSlidesResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceUnmarkSlidesResponse)
  - [SlideScanService](#zen_api.lm.slide_scan.v1.SlideScanService)
- [zen\_api/lm/slide\_scan/v1/slide\_state.proto](#zen_api/lm/slide_scan/v1/slide_state.proto)
  - [SlideState](#zen_api.lm.slide_scan.v1.SlideState)
- [zen\_api/lm/slide\_scan/v1/tray\_information.proto](#zen_api/lm/slide_scan/v1/tray_information.proto)
  - [TrayInformation](#zen_api.lm.slide_scan.v1.TrayInformation)
- [zen\_api/lm/slide\_scan/v1/tray\_slot\_state.proto](#zen_api/lm/slide_scan/v1/tray_slot_state.proto)
  - [TraySlotState](#zen_api.lm.slide_scan.v1.TraySlotState)
- [zen\_api/lm/slide\_scan/v1/tray\_type.proto](#zen_api/lm/slide_scan/v1/tray_type.proto)
  - [TrayType](#zen_api.lm.slide_scan.v1.TrayType)
- [zen\_api/lm/slide\_scan/v1/tray\_working\_state.proto](#zen_api/lm/slide_scan/v1/tray_working_state.proto)
  - [TrayWorkingState](#zen_api.lm.slide_scan.v1.TrayWorkingState)
- [Scalar Value Types](#scalar-value-types)

## zen\_api/acquisition/v1beta/experiment\_descriptor.proto

[Top](#title)

### ExperimentDescriptor

Descriptors for experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| name | [string](#string) |  | Experiment name. |

## zen\_api/acquisition/v1beta/experiment\_service.proto

[Top](#title)

### ExperimentServiceCloneRequest

The ExperimentServiceCloneRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Id of the experiment to be cloned. |

### ExperimentServiceCloneResponse

Response object of the method for cloning an experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment id which is used to reference the cloned experiment. |

### ExperimentServiceDeleteRequest

The ExperimentServiceDeleteRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_name | [string](#string) |  | Name of the experiment to be deleted. |

### ExperimentServiceDeleteResponse

The ExperimentServiceDeleteResponse class.

### ExperimentServiceExportRequest

The ExperimentServiceExportRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |

### ExperimentServiceExportResponse

Response object of the method for exporting an experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| xml | [string](#string) |  | Xml string of experiment. |

### ExperimentServiceGetAvailableExperimentsRequest

The ExperimentServiceGetAvailableExperimentsRequest class.

### ExperimentServiceGetAvailableExperimentsResponse

Response object of available experiments.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiments | [ExperimentDescriptor](#zen_api.acquisition.v1beta.ExperimentDescriptor) | repeated | List of available experiments. |

### ExperimentServiceGetImageOutputPathRequest

The ExperimentServiceGetImageOutputPathRequest class.

### ExperimentServiceGetImageOutputPathResponse

Response object of the method for getting the image output path.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| image\_output\_path | [string](#string) |  | The image output path. |

### ExperimentServiceGetStatusRequest

The ExperimentServiceGetStatusRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | ID of an experiment for which status is requested. If ID is provided, the status can be retrieved for both active and finished experiments. If ID is not provided, status of one of the active experiments is returned. If ID is not provided and there are no active experiments, an exception is thrown. |

### ExperimentServiceGetStatusResponse

Response object representing the status of an experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| status | [ExperimentStatus](#zen_api.acquisition.v1beta.ExperimentStatus) |  | The experiment status. |

### ExperimentServiceImportRequest

The ExperimentServiceImportRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| xml\_string | [string](#string) |  | Xml string of the experiment. |

### ExperimentServiceImportResponse

Response object of the method for importing an experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment id which is used to reference the imported experiment. |

### ExperimentServiceLoadRequest

The ExperimentServiceLoadRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_name | [string](#string) |  | Name of the experiment. |

### ExperimentServiceLoadResponse

Response object of the method for loading an experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment id which is used to reference the loaded experiment. |

### ExperimentServiceRegisterOnStatusChangedRequest

The ExperimentServiceRegisterOnStatusChangedRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | ID of an active experiment for which status is monitored. If ID is not provided, status of one of the active experiments is monitored. |

### ExperimentServiceRegisterOnStatusChangedResponse

Response object representing the status of an experiment.

It contains full set of status information, which can consist a single or multiple new states.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| status | [ExperimentStatus](#zen_api.acquisition.v1beta.ExperimentStatus) |  | The experiment status. |

### ExperimentServiceRunExperimentRequest

The ExperimentServiceRunExperimentRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |
| output\_name | [string](#string) |  | Optional name of the experiment's output. If a null or an empty name is provided, the output name will be created automatically, otherwise the output name must be in a format of a file name without a file extension. |

### ExperimentServiceRunExperimentResponse

Information about execution of an experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| output\_name | [string](#string) |  | The name of the experiment's output (in a format of a file name without a file extension). |

### ExperimentServiceRunSnapRequest

The ExperimentServiceRunSnapRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |
| output\_name | [string](#string) |  | Optional name of the experiment's output. If a null or an empty name is provided, the output name will be created automatically, otherwise the output name must be in a format of a file name without a file extension. |

### ExperimentServiceRunSnapResponse

Information about execution of a snap experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| output\_name | [string](#string) |  | The name of the snap's output (in a format of a file name without a file extension). |

### ExperimentServiceSaveRequest

The ExperimentServiceSaveRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |
| experiment\_name | [string](#string) |  | Name to be used when saving the experiment. |
| allow\_override | [bool](#bool) |  | Allow override of already existing experiment with the same name. |

### ExperimentServiceSaveResponse

The ExperimentServiceSaveResponse class.

### ExperimentServiceStartContinuousRequest

The ExperimentServiceStartContinuousRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |

### ExperimentServiceStartExperimentRequest

The ExperimentServiceStartExperimentRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |
| output\_name | [string](#string) |  | Optional name of the experiment's output. If a null or an empty name is provided, the output name will be created automatically, otherwise the output name must be in a format of a file name without a file extension. |

### ExperimentServiceStartExperimentResponse

Information about execution of an experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| output\_name | [string](#string) |  | The name of the experiment's output (in a format of a file name without a file extension). |

### ExperimentServiceStartLiveRequest

The ExperimentServiceStartLiveRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |
| track\_index | [google.protobuf.Int32Value](https://protobuf.dev/reference/protobuf/google.protobuf/#int32-value) |  | Optional track index. When index is not provided the first selected or activated track (in that order) will be used, but when the index is provided the track with than index will be selected. The track index starts with "0". |

### ExperimentServiceStartSnapRequest

The ExperimentServiceStartSnapRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |
| output\_name | [string](#string) |  | Optional name of the experiment's output. If a null or an empty name is provided, the output name will be created automatically, otherwise the output name must be in a format of a file name without a file extension. |

### ExperimentServiceStartSnapResponse

Information about execution of a snap experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| output\_name | [string](#string) |  | The name of the snap's output (in a format of a file name without a file extension). |

### ExperimentServiceStopRequest

The ExperimentServiceStopRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | ID of an experiment to stop or an empty GUID to stop one of the active experiments. |

### ExperimentServiceStopResponse

Information about execution of an experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The ID of the experiment which is used to reference the stopped experiment. |

### ExperimentService

The IExperimentService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | Clone | [ExperimentServiceCloneRequest](#zen_api.acquisition.v1beta.ExperimentServiceCloneRequest) | [ExperimentServiceCloneResponse](#zen_api.acquisition.v1beta.ExperimentServiceCloneResponse) | Clones an already loaded experiment. Useful when one wants to clone an experiment before modifying it in order to preserve the original experiment. This method returns the info needed to reference the cloned experiment. |
|  | Delete | [ExperimentServiceDeleteRequest](#zen_api.acquisition.v1beta.ExperimentServiceDeleteRequest) | [ExperimentServiceDeleteResponse](#zen_api.acquisition.v1beta.ExperimentServiceDeleteResponse) | Deletes an experiment file from the predefined location on disk. It does not delete the corresponding loaded experiment instance. |
|  | Export | [ExperimentServiceExportRequest](#zen_api.acquisition.v1beta.ExperimentServiceExportRequest) | [ExperimentServiceExportResponse](#zen_api.acquisition.v1beta.ExperimentServiceExportResponse) | Returns xml representation of an experiment. |
|  | GetAvailableExperiments | [ExperimentServiceGetAvailableExperimentsRequest](#zen_api.acquisition.v1beta.ExperimentServiceGetAvailableExperimentsRequest) | [ExperimentServiceGetAvailableExperimentsResponse](#zen_api.acquisition.v1beta.ExperimentServiceGetAvailableExperimentsResponse) | Retrieves a list of all available experiments of the system. |
|  | GetImageOutputPath | [ExperimentServiceGetImageOutputPathRequest](#zen_api.acquisition.v1beta.ExperimentServiceGetImageOutputPathRequest) | [ExperimentServiceGetImageOutputPathResponse](#zen_api.acquisition.v1beta.ExperimentServiceGetImageOutputPathResponse) | Gets the location where the images will be stored on the machine where ZEN Client is running. |
|  | GetStatus | [ExperimentServiceGetStatusRequest](#zen_api.acquisition.v1beta.ExperimentServiceGetStatusRequest) | [ExperimentServiceGetStatusResponse](#zen_api.acquisition.v1beta.ExperimentServiceGetStatusResponse) | Gets status of an experiment. The information is updated in interval (several times per seconds). As a result, some status updates could be skipped. |
|  | Import | [ExperimentServiceImportRequest](#zen_api.acquisition.v1beta.ExperimentServiceImportRequest) | [ExperimentServiceImportResponse](#zen_api.acquisition.v1beta.ExperimentServiceImportResponse) | Imports an experiment from the provided experiment xml string. This method returns the info needed to reference the imported experiment. |
|  | Load | [ExperimentServiceLoadRequest](#zen_api.acquisition.v1beta.ExperimentServiceLoadRequest) | [ExperimentServiceLoadResponse](#zen_api.acquisition.v1beta.ExperimentServiceLoadResponse) | Loads an experiment from the available experiments. Consequently, the experiment is ready to be executed or modified. This method returns the info needed to reference the loaded experiment. |
|  | RegisterOnStatusChanged | [ExperimentServiceRegisterOnStatusChangedRequest](#zen_api.acquisition.v1beta.ExperimentServiceRegisterOnStatusChangedRequest) | [ExperimentServiceRegisterOnStatusChangedResponse](#zen_api.acquisition.v1beta.ExperimentServiceRegisterOnStatusChangedResponse) stream | Register on experiment status changed events. The information is updated in interval (several times per seconds). As a result, some status updates could be skipped. The notifications can be retrieved for experiments which are active at the time the method is invoked. If the method is invoked after an experiment is finished, the call will throw an exception. |
|  | RunExperiment | [ExperimentServiceRunExperimentRequest](#zen_api.acquisition.v1beta.ExperimentServiceRunExperimentRequest) | [ExperimentServiceRunExperimentResponse](#zen_api.acquisition.v1beta.ExperimentServiceRunExperimentResponse) | Executes an experiment and waits until the experiment execution is finished. This means that the method will block until the experiment was successfully completed, it fails, or it is cancelled. If the call is interrupted (e.g., caller is not available anymore) the experiment will be stopped. |
|  | RunSnap | [ExperimentServiceRunSnapRequest](#zen_api.acquisition.v1beta.ExperimentServiceRunSnapRequest) | [ExperimentServiceRunSnapResponse](#zen_api.acquisition.v1beta.ExperimentServiceRunSnapResponse) | Acquires a single snap image with the activated channels in the specified experiment and waits until the process of acquiring snap is finished. This means that the method will block until the experiment was successfully completed, it fails, or it is cancelled. If the call is interrupted (e.g., caller is not available anymore) the snap will be stopped. |
|  | Save | [ExperimentServiceSaveRequest](#zen_api.acquisition.v1beta.ExperimentServiceSaveRequest) | [ExperimentServiceSaveResponse](#zen_api.acquisition.v1beta.ExperimentServiceSaveResponse) | Saves a loaded experiment to the predefined location on disk. |
|  | StartContinuous | [ExperimentServiceStartContinuousRequest](#zen_api.acquisition.v1beta.ExperimentServiceStartContinuousRequest) | [.google.protobuf.Empty](https://protobuf.dev/reference/protobuf/google.protobuf/#empty) | Starts the continuous with the activated channels in the specified experiment and waits for the acquisition to start. After that point continuous will run until it is explicitly stopped or it fails - even if the caller is not available anymore. |
|  | StartExperiment | [ExperimentServiceStartExperimentRequest](#zen_api.acquisition.v1beta.ExperimentServiceStartExperimentRequest) | [ExperimentServiceStartExperimentResponse](#zen_api.acquisition.v1beta.ExperimentServiceStartExperimentResponse) | Starts the process of executing an experiment and waits for the acquisition to start. After that point the experiment will either run to completion (successful or not) or until it is explicitly stopped - even if the caller is not available anymore. |
|  | StartLive | [ExperimentServiceStartLiveRequest](#zen_api.acquisition.v1beta.ExperimentServiceStartLiveRequest) | [.google.protobuf.Empty](https://protobuf.dev/reference/protobuf/google.protobuf/#empty) | Starts live with the requested track in the specified experiment and waits for the acquisition to start. After that point live will run until it is explicitly stopped or it fails - even if the caller is not available anymore. |
|  | StartSnap | [ExperimentServiceStartSnapRequest](#zen_api.acquisition.v1beta.ExperimentServiceStartSnapRequest) | [ExperimentServiceStartSnapResponse](#zen_api.acquisition.v1beta.ExperimentServiceStartSnapResponse) | Starts the process of acquiring a single snap image with the activated channels in the specified experiment and waits for the acquisition to start. After that point the snap will either run to completion (successful or not) or until it is explicitly stopped - even if the caller is not available anymore. |
|  | Stop | [ExperimentServiceStopRequest](#zen_api.acquisition.v1beta.ExperimentServiceStopRequest) | [ExperimentServiceStopResponse](#zen_api.acquisition.v1beta.ExperimentServiceStopResponse) | Stops the specified experiment or one of the active experiments if the experiment ID is not provided. This will stop any type of experiment (i.e., experiment, snap, continuous, live) if it is active and known to this service. This method returns the info needed to reference the stopped experiment. |

## zen\_api/acquisition/v1beta/experiment\_status.proto

[Top](#title)

### ExperimentStatus

Status of an experiment.

The index properties are 0-based.

If a value is 0 or -1 it means the value is not initialized or

the running experiment does not have the corresponding dimension.

In case of indices, 0 value can also refer to the first element.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| tiles\_index | [int32](#int32) |  | The current or already acquired (depending of the dimension order) tiles position index of the currently acquired scene. |
| tiles\_count | [int32](#int32) |  | The tiles count of the currently acquired scene. |
| cumulated\_tiles\_count | [int32](#int32) |  | The total tiles count of all scenes. |
| scenes\_index | [int32](#int32) |  | The current or already acquired (depending of the dimension order) scene index (= tile region/position index). |
| scenes\_count | [int32](#int32) |  | The total scene count (= tile region/position count). |
| time\_points\_index | [int32](#int32) |  | The current or already acquired (depending of the dimension order) time point index in time series. |
| time\_points\_count | [int32](#int32) |  | The number of time points in time series. |
| zstack\_slices\_index | [int32](#int32) |  | The current or already acquired (depending of the dimension order) z-stack slice index. |
| zstack\_slices\_count | [int32](#int32) |  | The total count of z-stack slices. |
| channels\_index | [int32](#int32) |  | The current or already acquired (depending of the dimension order) channel index. |
| channels\_count | [int32](#int32) |  | The total channel count. |
| images\_acquired\_index | [int32](#int32) |  | The number of acquired images over all dimensions (channels, time series, z-stack, cumulated tiles). |
| images\_count | [int32](#int32) |  | The images count over all dimensions (channels, time series, z-stack, cumulated tiles). This value is relevant only for acquisition where end is determined (standard experiment and Snap), therefore it is not relevant for Continuous and Live. |
| is\_experiment\_running | [bool](#bool) |  | A value indicating whether the experiment is currently running. |
| is\_acquisition\_running | [bool](#bool) |  | A value indicating whether an acquisition is currently running. |
| total\_elapsed\_time | [google.protobuf.Duration](https://protobuf.dev/reference/protobuf/google.protobuf/#duration) |  | The total time that elapsed since the start of the running experiment. |

## zen\_api/acquisition/v1beta/experiment\_streaming\_service.proto

[Top](#title)

### ExperimentStreamingServiceMonitorAllExperimentsRequest

The ExperimentStreamingServiceMonitorAllExperimentsRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| channel\_index | [google.protobuf.Int32Value](https://protobuf.dev/reference/protobuf/google.protobuf/#int32-value) |  | Optional parameter for filtering by specific channel. If the channel index is provided, then only that channel will be monitored, but if the channel index is not provided, then all channels will be monitored. |
| enable\_raw\_data | [bool](#bool) |  | Value indicating whether the streamed frame data contains raw frames as received from the acquisition (when set), which can be either full or partial frames (e.g., in general LM cameras produce full frames and LSM and EM detectors produce partial frames/lines). Otherwise (when not set) the streamed frame data contains only full frames, which means that in the case of partial frames/lines, they would be assembled into full frames. |

### ExperimentStreamingServiceMonitorAllExperimentsResponse

Response object of the method for monitoring all experiments.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| frame\_data | [FrameData](#zen_api.acquisition.v1beta.FrameData) |  | The experiment's frame data. |

### ExperimentStreamingServiceMonitorExperimentRequest

The ExperimentStreamingServiceMonitorExperimentRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | ID of the experiment to monitor. |
| channel\_index | [google.protobuf.Int32Value](https://protobuf.dev/reference/protobuf/google.protobuf/#int32-value) |  | Optional parameter for filtering by specific channel. If the channel index is provided, then only that channel will be monitored, but if the channel index is not provided, then all channels will be monitored. |
| enable\_raw\_data | [bool](#bool) |  | Value indicating whether the streamed frame data contains raw frames as received from the acquisition (when set), which can be either full or partial frames (e.g., in general LM cameras produce full frames and LSM and EM detectors produce partial frames/lines). Otherwise (when not set) the streamed frame data contains only full frames, which means that in the case of partial frames/lines, they would be assembled into full frames. |

### ExperimentStreamingServiceMonitorExperimentResponse

Response object of the method for monitoring an experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| frame\_data | [FrameData](#zen_api.acquisition.v1beta.FrameData) |  | The experiment's frame data. |

### ExperimentStreamingService

The IExperimentStreamingService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | MonitorAllExperiments | [ExperimentStreamingServiceMonitorAllExperimentsRequest](#zen_api.acquisition.v1beta.ExperimentStreamingServiceMonitorAllExperimentsRequest) | [ExperimentStreamingServiceMonitorAllExperimentsResponse](#zen_api.acquisition.v1beta.ExperimentStreamingServiceMonitorAllExperimentsResponse) stream | Starts monitoring all experiments. |
|  | MonitorExperiment | [ExperimentStreamingServiceMonitorExperimentRequest](#zen_api.acquisition.v1beta.ExperimentStreamingServiceMonitorExperimentRequest) | [ExperimentStreamingServiceMonitorExperimentResponse](#zen_api.acquisition.v1beta.ExperimentStreamingServiceMonitorExperimentResponse) stream | Starts monitoring the specified experiment. |

## zen\_api/acquisition/v1beta/frame\_data.proto

[Top](#title)

### FrameData

A simple container for the frame data. This can contain either a full frame or only a part

of it (e.g., in case of partial acquisition when working with EM and LSM).

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The ID of the experiment. |
| frame\_number | [int32](#int32) |  | The frame sequence number. One frame can represent either a single image taken by the camera or one full scan in case of partial acquisition. One frame can also contain multiple channels if they are acquired in the same image or scan. |
| frame\_position | [FramePosition](#zen_api.acquisition.v1beta.FramePosition) |  | The position of the full frame. |
| frame\_size | [zen\_api.common.v1.IntSize](#zen_api.common.v1.IntSize) |  | The size of the full frame (in pixels). |
| frame\_stage\_position | [FrameStagePosition](#zen_api.acquisition.v1beta.FrameStagePosition) |  | The stage position of the acquired full frame. |
| scaling | [Scaling](#zen_api.acquisition.v1beta.Scaling) |  | The scaling of the frame. |
| pixel\_data | [FramePixelData](#zen_api.acquisition.v1beta.FramePixelData) |  | The pixel data of the frame. This can contain either the pixels of a full frame or only a part of it (e.g., a line or a rectangle in case of partial acquisition when working with EM and LSM). |

## zen\_api/acquisition/v1beta/frame\_pixel\_data.proto

[Top](#title)

### FramePixelData

A simple container for the frame pixel data. This can contain either the pixels of a full

frame or only a part of it (e.g., a line or a rectangle in case of partial acquisition when

working with EM and LSM).

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| start\_position | [zen\_api.common.v1.IntPoint](#zen_api.common.v1.IntPoint) |  | The start position (in pixels) of the pixel data in the frame. Together with the size property, this represents the rectangle where the pixels are located inside the full frame. For ordinary acquisition this will be the top left corner of the frame, but for partial acquisition this can be any position inside the full frame relative to the top left corner. |
| size | [zen\_api.common.v1.IntSize](#zen_api.common.v1.IntSize) |  | Size (in pixels) of the pixel data. Together with the start position property, this represents the rectangle where the pixels are located inside the full frame. For ordinary acquisition this will be the full frame size, but for partial acquisition this can be just one part of the full frame. |
| pixel\_type | [PixelType](#zen_api.acquisition.v1beta.PixelType) |  | The pixel type of the frame. |
| raw\_data | [bytes](#bytes) |  | The raw pixel data. The value of individual pixels is contained in this container. The pixel values need to be extracted from the raw byte data. The number of bits needed to extract a single pixel from the raw byte data and the format it is stored in is determined by the pixel type property. |

## zen\_api/acquisition/v1beta/frame\_position.proto

[Top](#title)

### FramePosition

Defines the position of the frame in multiple dimensions.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [int32](#int32) |  | The pixel index in X direction of the top left corner of the frame. |
| y | [int32](#int32) |  | The pixel index in Y direction of the top left corner of the frame. |
| z | [int32](#int32) |  | The Z slice index of the of the frame. |
| t | [int32](#int32) |  | The time point of the frame in a sequentially acquired series of data. Note that this doesn't represents the exact time of acquisition but only the sequence of the acquired image. |
| s | [int32](#int32) |  | The scene index. |
| m | [int32](#int32) |  | The mosaic tile index. |
| c | [int32](#int32) |  | The channel index in a multi-channel data set. |
| h | [int32](#int32) |  | The raw data index. |

## zen\_api/acquisition/v1beta/frame\_stage\_position.proto

[Top](#title)

### FrameStagePosition

Defines the stage position of the acquired frame.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The stage position in X direction (unit: m). |
| y | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The stage position in Y direction (unit: m). |
| z | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The stage position in Z direction (unit: m). |

## zen\_api/acquisition/v1beta/pixel\_type.proto

[Top](#title)

### PixelType

Pixel type of image data.

| Name | Number | Description |
| --- | --- | --- |
| PIXEL\_TYPE\_UNSPECIFIED | 0 | Default value if status is not specified. |
| PIXEL\_TYPE\_GRAY8 | 1 | 8 bit unsigned. |
| PIXEL\_TYPE\_GRAY16 | 2 | 16 bit unsigned. |
| PIXEL\_TYPE\_BGR24 | 4 | 8 bit triples, representing the color channels Blue, Green and Red. |
| PIXEL\_TYPE\_BGR48 | 5 | 16 bit triples, representing the color channels Blue, Green and Red. |

## zen\_api/acquisition/v1beta/scaling.proto

[Top](#title)

### Scaling

Defines the scaling of the acquired frame.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [double](#double) |  | The scaling in X dimension (unit: m/pixel). |
| y | [double](#double) |  | The scaling in Y dimension (unit: m/pixel). |

## zen\_api/application/v1/composition\_service.proto

[Top](#title)

### CompositionServiceCreateModuleRequest

The CompositionServiceCreateModuleRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| module\_id | [string](#string) |  | The id of the module. |
| display\_name | [string](#string) |  | The display name of the module. |
| description | [string](#string) |  | The description of the module. |
| license\_string | [string](#string) |  | The license string. |
| minimum\_required\_version | [string](#string) |  | The minimum required feature version. |

### CompositionServiceCreateModuleResponse

The CompositionServiceCreateModuleResponse class.

### CompositionServiceIsModuleAvailableRequest

The CompositionServiceIsModuleAvailableRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| module\_id | [string](#string) |  | The module id. |

### IsModuleAvailableResponse

Response object of the method for checking the availability state of a composition module.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| is\_available | [bool](#bool) |  | A value indicating whether the module is available or not. |

### CompositionService

The ICompositionService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | CreateModule | [CompositionServiceCreateModuleRequest](#zen_api.application.v1.CompositionServiceCreateModuleRequest) | [CompositionServiceCreateModuleResponse](#zen_api.application.v1.CompositionServiceCreateModuleResponse) | Creates a module and adds it to the selected profile. With this method, a client can 'inject' a new module at runtime (e.g. via OAD script or ZEN API). After adding the module, it will appear as optional module of the selected profile just as any other module. The Module Manager can be used to verify this. After adding the module, the client can make use of the 'normal' license infrastructure to check the avaiability of the newly added module. Note: A module is available, if the module is licensed AND the user has enabled it (via the Module Manager). In case a module gets added via this method, the module is enabled by default. |
|  | IsModuleAvailable | [CompositionServiceIsModuleAvailableRequest](#zen_api.application.v1.CompositionServiceIsModuleAvailableRequest) | [IsModuleAvailableResponse](#zen_api.application.v1.IsModuleAvailableResponse) | Returns the availability state of the given module. |

## zen\_api/common/v1/double\_frame.proto

[Top](#title)

### DoubleFrame

Double-based frame.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| start\_point | [DoublePoint](#zen_api.common.v1.DoublePoint) |  | The start point. |
| size | [DoubleSize](#zen_api.common.v1.DoubleSize) |  | The size. |

## zen\_api/common/v1/double\_point.proto

[Top](#title)

### DoublePoint

Double-based point object.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [double](#double) |  | The coordinate X of a point. |
| y | [double](#double) |  | The coordinate Y of a point. |

## zen\_api/common/v1/double\_size.proto

[Top](#title)

### DoubleSize

Double-based size.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| width | [double](#double) |  | The width. |
| height | [double](#double) |  | The height. |

## zen\_api/common/v1/int\_point.proto

[Top](#title)

### IntPoint

Integer-based point.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [int32](#int32) |  | The coordinate X of a point. |
| y | [int32](#int32) |  | The coordinate Y of a point. |

## zen\_api/common/v1/int\_size.proto

[Top](#title)

### IntSize

Integer-based size.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| width | [int32](#int32) |  | The width. |
| height | [int32](#int32) |  | The height. |

## zen\_api/hardware/v1/axis\_identifier.proto

[Top](#title)

### AxisIdentifier

Unique identifier for axis.

| Name | Number | Description |
| --- | --- | --- |
| AXIS\_IDENTIFIER\_UNSPECIFIED | 0 | Default enum value. |
| AXIS\_IDENTIFIER\_X | 1 | X axis (translation axis). Controlled by length, default unit is meters. |
| AXIS\_IDENTIFIER\_Y | 2 | Y axis (translation axis). Controlled by length, default unit is meters. |
| AXIS\_IDENTIFIER\_Z | 3 | Z axis (translation axis). Controlled by length, default unit is meters. |
| AXIS\_IDENTIFIER\_R | 4 | R axis (rotation axis). Controlled by angle, default unit is radians. |
| AXIS\_IDENTIFIER\_T | 5 | T axis (rotation axis). Controlled by angle, default unit is radians. |
| AXIS\_IDENTIFIER\_M | 6 | M axis (translation axis). Controlled by length, default unit is meters. |

## zen\_api/hardware/v1/simple\_stage\_service.proto

[Top](#title)

### SimpleStageServiceGetAccelerationRequest

The SimpleStageServiceGetAccelerationRequest class.

### SimpleStageServiceGetAccelerationResponse

Acceleration of the stage.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [double](#double) |  | The X component of the acceleration in %. |
| y | [double](#double) |  | The Y component of the acceleration in %. |

### SimpleStageServiceGetPositionRequest

The SimpleStageServiceGetPositionRequest class.

### SimpleStageServiceGetPositionResponse

Position of the stage.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [double](#double) |  | The X component of the position in meters. |
| y | [double](#double) |  | The Y component of the position in meters. |

### SimpleStageServiceGetSpeedRequest

The SimpleStageServiceGetSpeedRequest class.

### SimpleStageServiceGetSpeedResponse

Speed of the stage.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [double](#double) |  | The X component of the speed in %. |
| y | [double](#double) |  | The Y component of the speed in %. |

### SimpleStageServiceMoveToRequest

The SimpleStageServiceMoveToRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | Target position x in meters. Leave out if x position should not be changed. |
| y | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | Target position y in meters. Leave out if y position should not be changed. |

### SimpleStageServiceMoveToResponse

Describes the result of a Stage.MoveTo request.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| position\_changed | [bool](#bool) |  | A value indicating whether the position was changed. |

### SimpleStageServiceSetAccelerationRequest

The SimpleStageServiceSetAccelerationRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| acceleration\_x | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | Acceleration in x direction in percent, i.e. values from range [0;100]. |
| acceleration\_y | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | Acceleration in y direction in percent, i.e. values from range [0;100]. |

### SimpleStageServiceSetAccelerationResponse

The SimpleStageServiceSetAccelerationResponse class.

### SimpleStageServiceSetSpeedRequest

The SimpleStageServiceSetSpeedRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| speed\_x | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | Speed in x direction in percent, i.e. values from range [0;100]. |
| speed\_y | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | Speed in y direction in percent, i.e. values from range [0;100]. |

### SimpleStageServiceSetSpeedResponse

The SimpleStageServiceSetSpeedResponse class.

### SimpleStageServiceStopRequest

The SimpleStageServiceStopRequest class.

### SimpleStageServiceStopResponse

The SimpleStageServiceStopResponse class.

### SimpleStageService

The ISimpleStageService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetAcceleration | [SimpleStageServiceGetAccelerationRequest](#zen_api.hardware.v1.SimpleStageServiceGetAccelerationRequest) | [SimpleStageServiceGetAccelerationResponse](#zen_api.hardware.v1.SimpleStageServiceGetAccelerationResponse) | Gets the acceleration of the stage. |
|  | GetPosition | [SimpleStageServiceGetPositionRequest](#zen_api.hardware.v1.SimpleStageServiceGetPositionRequest) | [SimpleStageServiceGetPositionResponse](#zen_api.hardware.v1.SimpleStageServiceGetPositionResponse) | Gets the current stage position. |
|  | GetSpeed | [SimpleStageServiceGetSpeedRequest](#zen_api.hardware.v1.SimpleStageServiceGetSpeedRequest) | [SimpleStageServiceGetSpeedResponse](#zen_api.hardware.v1.SimpleStageServiceGetSpeedResponse) | Gets the speed of the stage. |
|  | MoveTo | [SimpleStageServiceMoveToRequest](#zen_api.hardware.v1.SimpleStageServiceMoveToRequest) | [SimpleStageServiceMoveToResponse](#zen_api.hardware.v1.SimpleStageServiceMoveToResponse) | Moves the stage to the given position. Is a value for a dimension is no supplied, the position in that dimension it is kept as is. |
|  | SetAcceleration | [SimpleStageServiceSetAccelerationRequest](#zen_api.hardware.v1.SimpleStageServiceSetAccelerationRequest) | [SimpleStageServiceSetAccelerationResponse](#zen_api.hardware.v1.SimpleStageServiceSetAccelerationResponse) | Sets the acceleration of the stage in percent. |
|  | SetSpeed | [SimpleStageServiceSetSpeedRequest](#zen_api.hardware.v1.SimpleStageServiceSetSpeedRequest) | [SimpleStageServiceSetSpeedResponse](#zen_api.hardware.v1.SimpleStageServiceSetSpeedResponse) | Sets the speed of the stage in percent. |
|  | Stop | [SimpleStageServiceStopRequest](#zen_api.hardware.v1.SimpleStageServiceStopRequest) | [SimpleStageServiceStopResponse](#zen_api.hardware.v1.SimpleStageServiceStopResponse) | Stops the stage if it is moving. |

## zen\_api/hardware/v1/stage\_axis.proto

[Top](#title)

### StageAxis

Abstract representation of an arbitrary axis.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| position | [double](#double) |  | The position of the axis in meters or radians. |

## zen\_api/hardware/v1/stage\_motion\_state.proto

[Top](#title)

### StageMotionState

Stage motion state for ZenApi.

| Name | Number | Description |
| --- | --- | --- |
| STAGE\_MOTION\_STATE\_UNSPECIFIED | 0 | Default enum value. |
| STAGE\_MOTION\_STATE\_UNKNOWN | 1 | Should not occur in a well configured system. |
| STAGE\_MOTION\_STATE\_ERROR | 2 | The stage cannot perform any task. Software restart and/or physical intervention is required. |
| STAGE\_MOTION\_STATE\_IDLE | 3 | The stage is not moving. |
| STAGE\_MOTION\_STATE\_MOVING | 4 | The stage is in motion. |

## zen\_api/hardware/v1/stage\_service.proto

[Top](#title)

### StageServiceAxisVelocityResponse

Abstract representation of an arbitrary axis and it's velocity.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| velocity | [double](#double) |  | The velocity of the axis in meters per second or radians per second. |

### StageServiceGetAvailableStageAxisRequest

The StageServiceGetAvailableStageAxisRequest class.

### StageServiceGetAvailableStageAxisResponse

Response object of available stage axis.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| available\_axis | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) | repeated |  |

### StageServiceGetAxisPositionRequest

The StageServiceGetAxisPositionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_id | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The requested axis. |

### StageServiceGetAxisPositionResponse

Abstract representation of an arbitrary axis.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| position | [double](#double) |  | The position of the axis in meters or radians. |

### StageServiceGetAxisVelocityRequest

The StageServiceGetAxisVelocityRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_id | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The requested axis. |

### StageServiceGetAxisVelocityResponse

Abstract representation of an arbitrary axis and it's velocity.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| velocity | [double](#double) |  | The velocity of the axis in meters per second or radians per second. |

### StageServiceGetStageMotionStateRequest

The StageServiceGetStageMotionStateRequest class.

### StageServiceGetStageMotionStateResponse

StageMotionState enum response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| state | [StageMotionState](#zen_api.hardware.v1.StageMotionState) |  | The available axis and their positions. |

### StageServiceGetStagePositionRequest

The StageServiceGetStagePositionRequest class.

### StageServiceGetStagePositionResponse

Response object of stage axis positions.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_positions | [StageAxis](#zen_api.hardware.v1.StageAxis) | repeated | The available axis and their positions. |

### StageServiceGetStageStateRequest

The StageServiceGetStageStateRequest class.

### StageServiceGetStageStateResponse

StageState enum response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| state | [StageState](#zen_api.hardware.v1.StageState) |  | The stage state. |

### StageServiceGetStageVelocityRequest

The StageServiceGetStageVelocityRequest class.

### StageServiceGetStageVelocityResponse

Response object of stage axis velocities.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_velocities | [StageServiceAxisVelocityResponse](#zen_api.hardware.v1.StageServiceAxisVelocityResponse) | repeated | The available axis and their velocities. |

### StageServiceInitializeStageRequest

The StageServiceInitializeStageRequest class.

### StageServiceInitializeStageResponse

Response object of the initialize stage method.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to initialize the stage succeeded or not. |

### StageServiceMoveToRequest

The StageServiceMoveToRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_to\_move | [StageAxis](#zen_api.hardware.v1.StageAxis) | repeated | The stage axis that should move. The position is in meters. |

### StageServiceMoveToResponse

Response object of the MoveStage method.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to move the stage succeeded or not. |

### StageServiceRegisterOnStageMotionStateChangedRequest

The StageServiceRegisterOnStageMotionStateChangedRequest class.

### StageServiceRegisterOnStageMotionStateChangedResponse

StageMotionState enum response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| state | [StageMotionState](#zen_api.hardware.v1.StageMotionState) |  | The stage motion state. |

### StageServiceRegisterOnStagePositionChangedRequest

The StageServiceRegisterOnStagePositionChangedRequest class.

### StageServiceRegisterOnStagePositionChangedResponse

Abstract representation of an arbitrary axis.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| position | [double](#double) |  | The position of the axis in meters or radians. |

### StageServiceRegisterOnStageStateChangedRequest

The StageServiceRegisterOnStageStateChangedRequest class.

### StageServiceRegisterOnStageStateChangedResponse

StageState enum response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| state | [StageState](#zen_api.hardware.v1.StageState) |  | The stage state. |

### StageServiceRegisterOnStageVelocityChangedRequest

The StageServiceRegisterOnStageVelocityChangedRequest class.

### StageServiceRegisterOnStageVelocityChangedResponse

Abstract representation of an arbitrary axis and it's velocity.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| velocity | [double](#double) |  | The velocity of the axis in meters per second or radians per second. |

### StageServiceStopRequest

The StageServiceStopRequest class.

### StageServiceStopResponse

The StageServiceStopResponse class.

### StageService

The IStageService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetAvailableStageAxis | [StageServiceGetAvailableStageAxisRequest](#zen_api.hardware.v1.StageServiceGetAvailableStageAxisRequest) | [StageServiceGetAvailableStageAxisResponse](#zen_api.hardware.v1.StageServiceGetAvailableStageAxisResponse) | Retrieves all available stage axis on this system. |
|  | GetAxisPosition | [StageServiceGetAxisPositionRequest](#zen_api.hardware.v1.StageServiceGetAxisPositionRequest) | [StageServiceGetAxisPositionResponse](#zen_api.hardware.v1.StageServiceGetAxisPositionResponse) | Gets the current position of an axis of the stage. |
|  | GetAxisVelocity | [StageServiceGetAxisVelocityRequest](#zen_api.hardware.v1.StageServiceGetAxisVelocityRequest) | [StageServiceGetAxisVelocityResponse](#zen_api.hardware.v1.StageServiceGetAxisVelocityResponse) | Gets the current velocity of an axis of the stage. |
|  | GetStageMotionState | [StageServiceGetStageMotionStateRequest](#zen_api.hardware.v1.StageServiceGetStageMotionStateRequest) | [StageServiceGetStageMotionStateResponse](#zen_api.hardware.v1.StageServiceGetStageMotionStateResponse) | Retrieves the current stage motion state. |
|  | GetStagePosition | [StageServiceGetStagePositionRequest](#zen_api.hardware.v1.StageServiceGetStagePositionRequest) | [StageServiceGetStagePositionResponse](#zen_api.hardware.v1.StageServiceGetStagePositionResponse) | Retrieves the current stage position. This will return the positions of all available axis.. |
|  | GetStageState | [StageServiceGetStageStateRequest](#zen_api.hardware.v1.StageServiceGetStageStateRequest) | [StageServiceGetStageStateResponse](#zen_api.hardware.v1.StageServiceGetStageStateResponse) | Retrieves the current stage state. |
|  | GetStageVelocity | [StageServiceGetStageVelocityRequest](#zen_api.hardware.v1.StageServiceGetStageVelocityRequest) | [StageServiceGetStageVelocityResponse](#zen_api.hardware.v1.StageServiceGetStageVelocityResponse) | Retrieves the current stage velocity. This will return the velocity of all available axis. |
|  | InitializeStage | [StageServiceInitializeStageRequest](#zen_api.hardware.v1.StageServiceInitializeStageRequest) | [StageServiceInitializeStageResponse](#zen_api.hardware.v1.StageServiceInitializeStageResponse) | Starts an initialization routine for the stage to initialize all stage axis. This may take a while and the stage is moving in this time. |
|  | MoveTo | [StageServiceMoveToRequest](#zen_api.hardware.v1.StageServiceMoveToRequest) | [StageServiceMoveToResponse](#zen_api.hardware.v1.StageServiceMoveToResponse) | Moves the stage. |
|  | RegisterOnStageMotionStateChanged | [StageServiceRegisterOnStageMotionStateChangedRequest](#zen_api.hardware.v1.StageServiceRegisterOnStageMotionStateChangedRequest) | [StageServiceRegisterOnStageMotionStateChangedResponse](#zen_api.hardware.v1.StageServiceRegisterOnStageMotionStateChangedResponse) stream | Notification about changes of the stage motion state. |
|  | RegisterOnStagePositionChanged | [StageServiceRegisterOnStagePositionChangedRequest](#zen_api.hardware.v1.StageServiceRegisterOnStagePositionChangedRequest) | [StageServiceRegisterOnStagePositionChangedResponse](#zen_api.hardware.v1.StageServiceRegisterOnStagePositionChangedResponse) stream | Notification about changes of all stage axis positions. |
|  | RegisterOnStageStateChanged | [StageServiceRegisterOnStageStateChangedRequest](#zen_api.hardware.v1.StageServiceRegisterOnStageStateChangedRequest) | [StageServiceRegisterOnStageStateChangedResponse](#zen_api.hardware.v1.StageServiceRegisterOnStageStateChangedResponse) stream | Notification about changes of the stage state. |
|  | RegisterOnStageVelocityChanged | [StageServiceRegisterOnStageVelocityChangedRequest](#zen_api.hardware.v1.StageServiceRegisterOnStageVelocityChangedRequest) | [StageServiceRegisterOnStageVelocityChangedResponse](#zen_api.hardware.v1.StageServiceRegisterOnStageVelocityChangedResponse) stream | Notification about changes of all stage axis velocities. |
|  | Stop | [StageServiceStopRequest](#zen_api.hardware.v1.StageServiceStopRequest) | [StageServiceStopResponse](#zen_api.hardware.v1.StageServiceStopResponse) | Immediately stops the stage. |

## zen\_api/hardware/v1/stage\_state.proto

[Top](#title)

### StageState

Stage state for ZenApi.

| Name | Number | Description |
| --- | --- | --- |
| STAGE\_STATE\_UNSPECIFIED | 0 | Default enum value. |
| STAGE\_STATE\_UNKNOWN | 1 | Should not occur in a well configured system. |
| STAGE\_STATE\_ERROR | 2 | The stage cannot perform any task. Software restart and/or physical intervention is required. |
| STAGE\_STATE\_NORMAL | 3 | The state is functioning normally and can be used. |
| STAGE\_STATE\_INITIALIZING | 4 | The stage is in the process of reinitializing one or more axes, should not be used, and will ignore value sets and commands other than stop. |
| STAGE\_STATE\_INITIALIZATION\_NEEDED | 5 | The stage will respond to motion commands, but positions may be reported erroneously, and the stage should be initialized before further use. |

## zen\_api/workflows/v1/start\_job\_options.proto

[Top](#title)

### StartJobOptions

Start Job options.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| result\_path | [string](#string) |  | A value indicating a path for saving a Job results in the file system. -- If value is given than Job output will be copied to given path in filesystem and not uploaded to ZEN Archive. Have to be in the Windows-supported directory path format (local drive or network share). -- If value is null (or empty/whitespace) than Job output will be uploaded to ZEN Archive and not copied to anywhere. |

## zen\_api/workflows/v1beta/job\_resources\_service.proto

[Top](#title)

### JobResourcesServiceGetAvailableResourcesRequest

The JobResourcesServiceGetAvailableResourcesRequest class.

### JobResourcesServiceGetAvailableResourcesResponse

Response containing the list of all available resource workflow parameters.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resources | [string](#string) | repeated | The list of all available resource workflow parameters. |

### JobResourcesServiceGetBooleanValueRequest

The JobResourcesServiceGetBooleanValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |

### JobResourcesServiceGetBooleanValueResponse

Response containing the resource's value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [bool](#bool) |  | The resource's value. |

### JobResourcesServiceGetDateTimeValueRequest

The JobResourcesServiceGetDateTimeValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |

### JobResourcesServiceGetDateTimeValueResponse

Response containing the resource's value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [string](#string) |  | The resource's date and time string value in ISO 8601 format. |

### JobResourcesServiceGetDateValueRequest

The JobResourcesServiceGetDateValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |

### JobResourcesServiceGetDateValueResponse

Response containing the resource's value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [string](#string) |  | The resource's date string value in ISO 8601 format. |

### JobResourcesServiceGetDoubleValueRequest

The JobResourcesServiceGetDoubleValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |

### JobResourcesServiceGetDoubleValueResponse

Response containing the resource's value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [double](#double) |  | The resource's value. |

### JobResourcesServiceGetFloatValueRequest

The JobResourcesServiceGetFloatValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |

### JobResourcesServiceGetFloatValueResponse

Response containing the resource's value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [float](#float) |  | The resource's value. |

### JobResourcesServiceGetIntegerValueRequest

The JobResourcesServiceGetIntegerValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |

### JobResourcesServiceGetIntegerValueResponse

Response containing the resource's value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [int32](#int32) |  | The resource's value. |

### JobResourcesServiceGetLongValueRequest

The JobResourcesServiceGetLongValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |

### JobResourcesServiceGetLongValueResponse

Response containing the resource's value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [int64](#int64) |  | The resource's value. |

### JobResourcesServiceGetStringValueRequest

The JobResourcesServiceGetStringValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |

### JobResourcesServiceGetStringValueResponse

Response containing the resource's value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [string](#string) |  | The resource's value. |

### JobResourcesServiceGetTimeValueRequest

The JobResourcesServiceGetTimeValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |

### JobResourcesServiceGetTimeValueResponse

Response containing the resource's value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [string](#string) |  | The resource's time string value in ISO 8601 format. |

### JobResourcesServiceHasResourceRequest

The JobResourcesServiceHasResourceRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |

### JobResourcesServiceHasResourceResponse

Response containing information if the current job has a resource with the specified ID.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| has\_resource | [bool](#bool) |  | A value indicating whether the current job has a resource with the specified ID. |

### JobResourcesServiceIsJobLoadedRequest

The JobResourcesServiceIsJobLoadedRequest class.

### JobResourcesServiceIsJobLoadedResponse

Response containing information if a job is loaded.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| is\_job\_loaded | [bool](#bool) |  | A value indicating whether a job is loaded. |

### JobResourcesServiceSetBooleanValueRequest

The JobResourcesServiceSetBooleanValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |
| value | [bool](#bool) |  | The resource's value. |

### JobResourcesServiceSetBooleanValueResponse

The JobResourcesServiceSetBooleanValueResponse class.

### JobResourcesServiceSetDateTimeValueRequest

The JobResourcesServiceSetDateTimeValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |
| value | [string](#string) |  | The resource's value. |

### JobResourcesServiceSetDateTimeValueResponse

The JobResourcesServiceSetDateTimeValueResponse class.

### JobResourcesServiceSetDateValueRequest

The JobResourcesServiceSetDateValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |
| value | [string](#string) |  | The resource's value. |

### JobResourcesServiceSetDateValueResponse

The JobResourcesServiceSetDateValueResponse class.

### JobResourcesServiceSetDoubleValueRequest

The JobResourcesServiceSetDoubleValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |
| value | [double](#double) |  | The resource's value. |

### JobResourcesServiceSetDoubleValueResponse

The JobResourcesServiceSetDoubleValueResponse class.

### JobResourcesServiceSetFloatValueRequest

The JobResourcesServiceSetFloatValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |
| value | [float](#float) |  | The resource's value. |

### JobResourcesServiceSetFloatValueResponse

The JobResourcesServiceSetFloatValueResponse class.

### JobResourcesServiceSetIntegerValueRequest

The JobResourcesServiceSetIntegerValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |
| value | [int32](#int32) |  | The resource's value. |

### JobResourcesServiceSetIntegerValueResponse

The JobResourcesServiceSetIntegerValueResponse class.

### JobResourcesServiceSetLongValueRequest

The JobResourcesServiceSetLongValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |
| value | [int64](#int64) |  | The resource's value. |

### JobResourcesServiceSetLongValueResponse

The JobResourcesServiceSetLongValueResponse class.

### JobResourcesServiceSetStringValueRequest

The JobResourcesServiceSetStringValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |
| value | [string](#string) |  | The resource's value. |

### JobResourcesServiceSetStringValueResponse

The JobResourcesServiceSetStringValueResponse class.

### JobResourcesServiceSetTimeValueRequest

The JobResourcesServiceSetTimeValueRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| resource\_id | [string](#string) |  | The ID of the resource. |
| value | [string](#string) |  | The resource's value. |

### JobResourcesServiceSetTimeValueResponse

The JobResourcesServiceSetTimeValueResponse class.

### JobResourcesService

The IJobResourcesService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetAvailableResources | [JobResourcesServiceGetAvailableResourcesRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetAvailableResourcesRequest) | [JobResourcesServiceGetAvailableResourcesResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetAvailableResourcesResponse) | Retrieves a list of all available resource workflow parameters. |
|  | GetBooleanValue | [JobResourcesServiceGetBooleanValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetBooleanValueRequest) | [JobResourcesServiceGetBooleanValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetBooleanValueResponse) | Gets the value of the resource with the specified ID from the current job as a boolean value. |
|  | GetDateTimeValue | [JobResourcesServiceGetDateTimeValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetDateTimeValueRequest) | [JobResourcesServiceGetDateTimeValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetDateTimeValueResponse) | Gets the value of the resource with the specified ID from the current job as a date and time string value in ISO 8601 format. |
|  | GetDateValue | [JobResourcesServiceGetDateValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetDateValueRequest) | [JobResourcesServiceGetDateValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetDateValueResponse) | Gets the value of the resource with the specified ID from the current job as a date string value in ISO 8601 format. |
|  | GetDoubleValue | [JobResourcesServiceGetDoubleValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetDoubleValueRequest) | [JobResourcesServiceGetDoubleValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetDoubleValueResponse) | Gets the value of the resource with the specified ID from the current job as a double precision floating point value. |
|  | GetFloatValue | [JobResourcesServiceGetFloatValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetFloatValueRequest) | [JobResourcesServiceGetFloatValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetFloatValueResponse) | Gets the value of the resource with the specified ID from the current job as a single precision floating point value. |
|  | GetIntegerValue | [JobResourcesServiceGetIntegerValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetIntegerValueRequest) | [JobResourcesServiceGetIntegerValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetIntegerValueResponse) | Gets the value of the resource with the specified ID from the current job as an integer value. |
|  | GetLongValue | [JobResourcesServiceGetLongValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetLongValueRequest) | [JobResourcesServiceGetLongValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetLongValueResponse) | Gets the value of the resource with the specified ID from the current job as a long integer value. |
|  | GetStringValue | [JobResourcesServiceGetStringValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetStringValueRequest) | [JobResourcesServiceGetStringValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetStringValueResponse) | Gets the value of the resource with the specified ID from the current job as a string value. |
|  | GetTimeValue | [JobResourcesServiceGetTimeValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetTimeValueRequest) | [JobResourcesServiceGetTimeValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetTimeValueResponse) | Gets the value of the resource with the specified ID from the current job as a time string value in ISO 8601 format. |
|  | HasResource | [JobResourcesServiceHasResourceRequest](#zen_api.workflows.v1beta.JobResourcesServiceHasResourceRequest) | [JobResourcesServiceHasResourceResponse](#zen_api.workflows.v1beta.JobResourcesServiceHasResourceResponse) | Checks if the current job has a resource with the specified ID. |
|  | IsJobLoaded | [JobResourcesServiceIsJobLoadedRequest](#zen_api.workflows.v1beta.JobResourcesServiceIsJobLoadedRequest) | [JobResourcesServiceIsJobLoadedResponse](#zen_api.workflows.v1beta.JobResourcesServiceIsJobLoadedResponse) | Checks if a job is loaded. |
|  | SetBooleanValue | [JobResourcesServiceSetBooleanValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetBooleanValueRequest) | [JobResourcesServiceSetBooleanValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetBooleanValueResponse) | Sets the value of the resource with the specified ID in the current job as a boolean value or creates the resource if it doesn't exist. |
|  | SetDateTimeValue | [JobResourcesServiceSetDateTimeValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetDateTimeValueRequest) | [JobResourcesServiceSetDateTimeValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetDateTimeValueResponse) | Sets the value of the resource with the specified ID in the current job as a date and time string value in ISO 8601 format or creates the resource if it doesn't exist. |
|  | SetDateValue | [JobResourcesServiceSetDateValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetDateValueRequest) | [JobResourcesServiceSetDateValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetDateValueResponse) | Sets the value of the resource with the specified ID in the current job as a date string value in ISO 8601 format or creates the resource if it doesn't exist. |
|  | SetDoubleValue | [JobResourcesServiceSetDoubleValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetDoubleValueRequest) | [JobResourcesServiceSetDoubleValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetDoubleValueResponse) | Sets the value of the resource with the specified ID in the current job as a double precision floating point value or creates the resource if it doesn't exist. |
|  | SetFloatValue | [JobResourcesServiceSetFloatValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetFloatValueRequest) | [JobResourcesServiceSetFloatValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetFloatValueResponse) | Sets the value of the resource with the specified ID in the current job as a single precision floating point value or creates the resource if it doesn't exist. |
|  | SetIntegerValue | [JobResourcesServiceSetIntegerValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetIntegerValueRequest) | [JobResourcesServiceSetIntegerValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetIntegerValueResponse) | Sets the value of the resource with the specified ID in the current job as an integer value or creates the resource if it doesn't exist. |
|  | SetLongValue | [JobResourcesServiceSetLongValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetLongValueRequest) | [JobResourcesServiceSetLongValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetLongValueResponse) | Sets the value of the resource with the specified ID in the current job as a long integer value or creates the resource if it doesn't exist. |
|  | SetStringValue | [JobResourcesServiceSetStringValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetStringValueRequest) | [JobResourcesServiceSetStringValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetStringValueResponse) | Sets the value of the resource with the specified ID in the current job as a string value or creates the resource if it doesn't exist. |
|  | SetTimeValue | [JobResourcesServiceSetTimeValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetTimeValueRequest) | [JobResourcesServiceSetTimeValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetTimeValueResponse) | Sets the value of the resource with the specified ID in the current job as a time string value in ISO 8601 format or creates the resource if it doesn't exist. |

## zen\_api/workflows/v2/job\_info.proto

[Top](#title)

### JobInfo

Information about Job executed by the workflow runner contains a real-time updates and Job's events with Job state.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| job\_id | [string](#string) |  | A Job unique runtime ID. |
| create\_date | [google.protobuf.Timestamp](https://protobuf.dev/reference/protobuf/google.protobuf/#timestamp) |  | A date and time when JobInfo was created. |
| status | [JobStatus](#zen_api.workflows.v2.JobStatus) |  | A Job execution state. |
| start\_options | [zen\_api.workflows.v1.StartJobOptions](#zen_api.workflows.v1.StartJobOptions) |  | A Job starting options. |

## zen\_api/workflows/v2/job\_status.proto

[Top](#title)

### JobStatus

Runtime status of the Job.

| Name | Number | Description |
| --- | --- | --- |
| JOB\_STATUS\_UNSPECIFIED | 0 | Default value if status is not specified. |
| JOB\_STATUS\_RUNNING | 1 | Job is currently executed by the workflow runner. |
| JOB\_STATUS\_PAUSED | 2 | Job execution is paused (not supported for now and reserved only for future purposes for saving numeration sequence). |
| JOB\_STATUS\_COMPLETED | 3 | Job execution is successfully completed. |
| JOB\_STATUS\_FAILED | 4 | Job execution was failed. |
| JOB\_STATUS\_CANCELLED | 5 | Job execution was interrupted (cancelled). |
| JOB\_STATUS\_PENDING | 6 | Job is created but still not started and waiting for beginning of execution. |

## zen\_api/workflows/v2/workflow\_service.proto

[Top](#title)

### WorkflowServiceGetJobInfoRequest

The WorkflowServiceGetJobInfoRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| job\_id | [string](#string) |  | Target Job ID. |

### WorkflowServiceGetJobInfoResponse

Response object representing the job info.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| job\_info | [JobInfo](#zen_api.workflows.v2.JobInfo) |  | The job info. |

### WorkflowServiceStartJobRequest

The WorkflowServiceStartJobRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| job\_name | [string](#string) |  | Job display name. |
| options | [zen\_api.workflows.v1.StartJobOptions](#zen_api.workflows.v1.StartJobOptions) |  | Job starting options. |

### WorkflowServiceStartJobResponse

Response object representing the starting of a job.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| job\_info | [JobInfo](#zen_api.workflows.v2.JobInfo) |  | The job info. |

### WorkflowServiceStopJobRequest

The WorkflowServiceStopJobRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| job\_id | [string](#string) |  | Target Job ID. |

### WorkflowServiceStopJobResponse

The WorkflowServiceStopJobResponse class.

### WorkflowServiceWaitJobRequest

The WorkflowServiceWaitJobRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| job\_id | [string](#string) |  | Target Job ID. |

### WorkflowServiceWaitJobResponse

The WorkflowServiceWaitJobResponse class.

### WorkflowService

The IWorkflowService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetJobInfo | [WorkflowServiceGetJobInfoRequest](#zen_api.workflows.v2.WorkflowServiceGetJobInfoRequest) | [WorkflowServiceGetJobInfoResponse](#zen_api.workflows.v2.WorkflowServiceGetJobInfoResponse) | Get Job information. |
|  | StartJob | [WorkflowServiceStartJobRequest](#zen_api.workflows.v2.WorkflowServiceStartJobRequest) | [WorkflowServiceStartJobResponse](#zen_api.workflows.v2.WorkflowServiceStartJobResponse) | Start Job execution. |
|  | StopJob | [WorkflowServiceStopJobRequest](#zen_api.workflows.v2.WorkflowServiceStopJobRequest) | [WorkflowServiceStopJobResponse](#zen_api.workflows.v2.WorkflowServiceStopJobResponse) | Stop the Job execution. |
|  | WaitJob | [WorkflowServiceWaitJobRequest](#zen_api.workflows.v2.WorkflowServiceWaitJobRequest) | [WorkflowServiceWaitJobResponse](#zen_api.workflows.v2.WorkflowServiceWaitJobResponse) | Wait for the Job execution will be finished. |

## zen\_api/workflows/v3beta/job\_status.proto

[Top](#title)

### JobStatus

Enumerates possible job statuses.

| Name | Number | Description |
| --- | --- | --- |
| JOB\_STATUS\_UNSPECIFIED | 0 | Default enum value. |
| JOB\_STATUS\_NOT\_LOADED | 1 | Job template is not loaded. |
| JOB\_STATUS\_LOADED | 2 | Job template is loaded. |
| JOB\_STATUS\_RUNNING | 3 | Job is running. |
| JOB\_STATUS\_FINALIZING | 4 | Finalizing job results after the job was completed successfully. |
| JOB\_STATUS\_ARCHIVING | 5 | Archiving job results after they were finalized. |
| JOB\_STATUS\_COMPLETED | 6 | Job was completed successfully. |
| JOB\_STATUS\_ABORTED | 7 | Job was aborted. |
| JOB\_STATUS\_CANCELED | 8 | Job was canceled. |

## zen\_api/workflows/v3beta/job\_template\_info.proto

[Top](#title)

### JobTemplateInfo

Contains information about a job template.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| name | [string](#string) |  | The job template's name. |
| description | [string](#string) |  | The job template's description. |
| category | [string](#string) |  | The job template's category. |
| subcategory | [string](#string) |  | The job template's subcategory. |

## zen\_api/workflows/v3beta/workflow\_service.proto

[Top](#title)

### WorkflowServiceGetAvailableJobTemplatesRequest

The WorkflowServiceGetAvailableJobTemplatesRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| category | [string](#string) |  | Optional filter for job templates. If category is provided then only job templates that are in the specified category will be listed. |
| subcategory | [string](#string) |  | Optional filter for job templates. If subcategory is provided then only job templates that are in the specified subcategory will be listed. |

### WorkflowServiceGetAvailableJobTemplatesResponse

Represents a list of all available job templates.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| job\_templates | [JobTemplateInfo](#zen_api.workflows.v3beta.JobTemplateInfo) | repeated | The available job templates. |

### WorkflowServiceGetStatusRequest

The WorkflowServiceGetStatusRequest class.

### WorkflowServiceGetStatusResponse

Response containing the job status.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| job\_status | [JobStatus](#zen_api.workflows.v3beta.JobStatus) |  | The job status. |

### WorkflowServiceIsJobRunningRequest

The WorkflowServiceIsJobRunningRequest class.

### WorkflowServiceIsJobRunningResponse

Response object representing the return value of IsJobRunning() method of the

Workflow service.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| is\_job\_running | [bool](#bool) |  | A value indicating whether the loaded job is currently running. |

### WorkflowServiceIsJobTemplateLoadedRequest

The WorkflowServiceIsJobTemplateLoadedRequest class.

### WorkflowServiceIsJobTemplateLoadedResponse

Response object representing the return value of IsJobTemplateLoaded() method of the

Workflow service.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| is\_job\_template\_loaded | [bool](#bool) |  | A value indicating whether a job template is loaded. |

### WorkflowServiceLoadJobTemplateRequest

The WorkflowServiceLoadJobTemplateRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| job\_template\_name | [string](#string) |  | The name of the job template. |
| result\_path | [string](#string) |  | Optional parameter for storing the result outside of ZEN archive. If provided the job result will be stored in the selected location and will not be uploaded to the archive. |

### WorkflowServiceLoadJobTemplateResponse

The WorkflowServiceLoadJobTemplateResponse class.

### WorkflowServiceRegisterOnStatusChangedRequest

The WorkflowServiceRegisterOnStatusChangedRequest class.

### WorkflowServiceRegisterOnStatusChangedResponse

Response containing the job status.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| job\_status | [JobStatus](#zen_api.workflows.v3beta.JobStatus) |  | The job status. |

### WorkflowServiceRunJobRequest

The WorkflowServiceRunJobRequest class.

### WorkflowServiceRunJobResponse

Response object representing the return value of RunJob() method of the Workflow service.

### WorkflowServiceStartJobRequest

The WorkflowServiceStartJobRequest class.

### WorkflowServiceStartJobResponse

The WorkflowServiceStartJobResponse class.

### WorkflowServiceStopJobRequest

The WorkflowServiceStopJobRequest class.

### WorkflowServiceStopJobResponse

Response object representing the return value of StopJob() method of the Workflow service.

### WorkflowServiceUnloadJobTemplateRequest

The WorkflowServiceUnloadJobTemplateRequest class.

### WorkflowServiceUnloadJobTemplateResponse

The WorkflowServiceUnloadJobTemplateResponse class.

### WorkflowServiceWaitJobRequest

The WorkflowServiceWaitJobRequest class.

### WorkflowServiceWaitJobResponse

Response object representing the return value of WaitJob() method of the Workflow service.

### WorkflowService

The IWorkflowService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetAvailableJobTemplates | [WorkflowServiceGetAvailableJobTemplatesRequest](#zen_api.workflows.v3beta.WorkflowServiceGetAvailableJobTemplatesRequest) | [WorkflowServiceGetAvailableJobTemplatesResponse](#zen_api.workflows.v3beta.WorkflowServiceGetAvailableJobTemplatesResponse) | Retrieves a list of all available job templates. |
|  | GetStatus | [WorkflowServiceGetStatusRequest](#zen_api.workflows.v3beta.WorkflowServiceGetStatusRequest) | [WorkflowServiceGetStatusResponse](#zen_api.workflows.v3beta.WorkflowServiceGetStatusResponse) | Gets the job status. |
|  | IsJobRunning | [WorkflowServiceIsJobRunningRequest](#zen_api.workflows.v3beta.WorkflowServiceIsJobRunningRequest) | [WorkflowServiceIsJobRunningResponse](#zen_api.workflows.v3beta.WorkflowServiceIsJobRunningResponse) | Checks if the loaded job is currently running. |
|  | IsJobTemplateLoaded | [WorkflowServiceIsJobTemplateLoadedRequest](#zen_api.workflows.v3beta.WorkflowServiceIsJobTemplateLoadedRequest) | [WorkflowServiceIsJobTemplateLoadedResponse](#zen_api.workflows.v3beta.WorkflowServiceIsJobTemplateLoadedResponse) | Checks if a job template is loaded. |
|  | LoadJobTemplate | [WorkflowServiceLoadJobTemplateRequest](#zen_api.workflows.v3beta.WorkflowServiceLoadJobTemplateRequest) | [WorkflowServiceLoadJobTemplateResponse](#zen_api.workflows.v3beta.WorkflowServiceLoadJobTemplateResponse) | Loads a job template and prepares it for execution. |
|  | RegisterOnStatusChanged | [WorkflowServiceRegisterOnStatusChangedRequest](#zen_api.workflows.v3beta.WorkflowServiceRegisterOnStatusChangedRequest) | [WorkflowServiceRegisterOnStatusChangedResponse](#zen_api.workflows.v3beta.WorkflowServiceRegisterOnStatusChangedResponse) stream | Register on job status changed events. |
|  | RunJob | [WorkflowServiceRunJobRequest](#zen_api.workflows.v3beta.WorkflowServiceRunJobRequest) | [WorkflowServiceRunJobResponse](#zen_api.workflows.v3beta.WorkflowServiceRunJobResponse) | Runs the loaded job template to completion. |
|  | StartJob | [WorkflowServiceStartJobRequest](#zen_api.workflows.v3beta.WorkflowServiceStartJobRequest) | [WorkflowServiceStartJobResponse](#zen_api.workflows.v3beta.WorkflowServiceStartJobResponse) | Starts the loaded job template but it doesn't wait for it to complete. |
|  | StopJob | [WorkflowServiceStopJobRequest](#zen_api.workflows.v3beta.WorkflowServiceStopJobRequest) | [WorkflowServiceStopJobResponse](#zen_api.workflows.v3beta.WorkflowServiceStopJobResponse) | Stops the currently running job and waits for it to complete. |
|  | UnloadJobTemplate | [WorkflowServiceUnloadJobTemplateRequest](#zen_api.workflows.v3beta.WorkflowServiceUnloadJobTemplateRequest) | [WorkflowServiceUnloadJobTemplateResponse](#zen_api.workflows.v3beta.WorkflowServiceUnloadJobTemplateResponse) | Unloads the loaded job template. |
|  | WaitJob | [WorkflowServiceWaitJobRequest](#zen_api.workflows.v3beta.WorkflowServiceWaitJobRequest) | [WorkflowServiceWaitJobResponse](#zen_api.workflows.v3beta.WorkflowServiceWaitJobResponse) | Waits for currently running job to complete. |

## zen\_api/em/hardware/v1/acquisition\_response\_type.proto

[Top](#title)

### AcquisitionResponseType

Indicates the type of response returned by the camera live image acquisition stream.

| Name | Number | Description |
| --- | --- | --- |
| ACQUISITION\_RESPONSE\_TYPE\_UNSPECIFIED | 0 | Unspecified type. |
| ACQUISITION\_RESPONSE\_TYPE\_FRAME\_START | 1 | The response is the first data buffer of a new frame. The response will include the image meta-data. |
| ACQUISITION\_RESPONSE\_TYPE\_FRAME\_CONTINUATION | 2 | The response is a continuation of the previous frame. The response will not include the image meta-data. |

## zen\_api/em/hardware/v1/acquisition\_service.proto

[Top](#title)

### AcquisitionServiceGetExternalScanSourceRequest

The AcquisitionServiceGetExternalScanSourceRequest class.

### AcquisitionServiceGetExternalScanSourceResponse

Response object representing the external scan source identifier.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| source | [int64](#int64) |  | The external scan source identifier. |

### AcquisitionServiceSetExternalScanSourceRequest

The AcquisitionServiceSetExternalScanSourceRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| source | [int64](#int64) |  | The external scan source identifier. Source = 0: Internal scan control Source = 1, 2, 3, 4: External scan configuration |

### AcquisitionServiceSetExternalScanSourceResponse

Response object representing the external scan source identifier after setting.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| source | [int64](#int64) |  | The external scan source identifier. |
| success | [bool](#bool) |  | A value indicating whether the operation succeeded. |

### AcquisitionService

The IAcquisitionService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetExternalScanSource | [AcquisitionServiceGetExternalScanSourceRequest](#zen_api.em.hardware.v1.AcquisitionServiceGetExternalScanSourceRequest) | [AcquisitionServiceGetExternalScanSourceResponse](#zen_api.em.hardware.v1.AcquisitionServiceGetExternalScanSourceResponse) | Gets the external scan source identifier. Specifies which external source is used for scan control when external scan is enabled. |
|  | SetExternalScanSource | [AcquisitionServiceSetExternalScanSourceRequest](#zen_api.em.hardware.v1.AcquisitionServiceSetExternalScanSourceRequest) | [AcquisitionServiceSetExternalScanSourceResponse](#zen_api.em.hardware.v1.AcquisitionServiceSetExternalScanSourceResponse) | Sets the external scan source identifier. Specifies which external source to use for scan control when external scan is enabled. |

## zen\_api/em/hardware/v1/acquisition\_settings.proto

[Top](#title)

### AcquisitionSettings

Request object to set the simple acquisition settings.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| detector\_name | [string](#string) |  | The detector to use. Null will take the detector from the previous acquisition. |
| width | [int32](#int32) |  | The image width in pixels. |
| height | [int32](#int32) |  | The image height in pixels. |
| dwell\_time | [double](#double) |  | The dwell time in seconds. The closest dwell time to the selected one will be chosen. |
| frame\_averages | [int32](#int32) |  | The number of frames to average. 1 means no averaging. |
| line\_averages | [int32](#int32) |  | The number of lines to average. 1 means no averaging. |

## zen\_api/em/hardware/v1/acquisition\_status.proto

[Top](#title)

### AcquisitionStatus

Acquisition states.

| Name | Number | Description |
| --- | --- | --- |
| ACQUISITION\_STATUS\_UNSPECIFIED | 0 | Default enum value. |
| ACQUISITION\_STATUS\_IDLE | 1 | No acquisition task is running, available for next acquisition. |
| ACQUISITION\_STATUS\_BUSY | 2 | Acquisition hardware is occupied by another task. No acquisition possible at the moment. |
| ACQUISITION\_STATUS\_LIVE\_RUNNING | 3 | Live acquisition is currently running. |
| ACQUISITION\_STATUS\_ACQUISITION\_RUNNING | 4 | Acquisition task is currently running. |

## zen\_api/em/hardware/v1/beam\_state.proto

[Top](#title)

### BeamState

Possible beam operating states.

| Name | Number | Description |
| --- | --- | --- |
| BEAM\_STATE\_UNSPECIFIED | 0 | Default enum value. |
| BEAM\_STATE\_UNKNOWN | 1 | Unknown indicates that this variable hasn't been assigned yet. This value should never occur. If you read this value, it's a bug. |
| BEAM\_STATE\_ERROR | 2 | There is an error with the Gun or EHT and the beam cannot be used. |
| BEAM\_STATE\_OFF | 3 | EHT is off. On FE-SEMs, the gun may be on, gun interfaces must be checked to discover gun state. On C-SEMs the EHT and gun are off, and there is no current on the filament. |
| BEAM\_STATE\_TURNING\_ON | 4 | The EHT (and gun for C-SEM) is turning on. |
| BEAM\_STATE\_ON | 5 | Gun is on. Filament (if it exists) has full current. EHT is on. The beam can be used. |
| BEAM\_STATE\_GOING\_TO\_STANDBY | 6 | The beam is going into the standby state. |
| BEAM\_STATE\_STANDBY | 7 | Not all devices support this mode. This represents an intermediate state. The EVO and the FIB have standby states. |
| BEAM\_STATE\_TURNING\_OFF | 8 | The EHT is ramping down. On C-SEM, the gun and filament may also be shutting down. |

## zen\_api/em/hardware/v1/camera\_acquisition\_settings.proto

[Top](#title)

### CameraAcquisitionSettings

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_name | [string](#string) |  | The camera to use. |
| width | [int32](#int32) |  | The image width in pixels. |
| height | [int32](#int32) |  | The image height in pixels. |

## zen\_api/em/hardware/v1/camera\_acquisition\_status.proto

[Top](#title)

### CameraAcquisitionStatus

Acquisition states.

| Name | Number | Description |
| --- | --- | --- |
| CAMERA\_ACQUISITION\_STATUS\_UNSPECIFIED | 0 | Default enum value. |
| CAMERA\_ACQUISITION\_STATUS\_UNKNOWN | 1 | Should not occur in an initialized system. |
| CAMERA\_ACQUISITION\_STATUS\_ERROR | 2 | The image acquisition device is in an error state and cannot be used. |
| CAMERA\_ACQUISITION\_STATUS\_IDLE | 3 | The image acquisition device is ready to perform a task. |
| CAMERA\_ACQUISITION\_STATUS\_BUSY | 4 | The image acquisition device is busy with other tasks and cannot be used for image acquisition. |
| CAMERA\_ACQUISITION\_STATUS\_LIVE\_ACQUISITION | 5 | The system is performing a scan and will continue until explicitly asked to stop. We use the term "Live" instead of "Continuous" because in ZIS, "Continuous" means "a time series of snaps with no delay between and no scheduled end". |
| CAMERA\_ACQUISITION\_STATUS\_SINGLE\_ACQUISITION | 6 | The system is performing a scan that has a scheduled termination such as "at the end of the frame". |

## zen\_api/em/hardware/v1/camera\_service.proto

[Top](#title)

### CameraServiceGetAcquisitionStatusRequest

The CameraServiceGetAcquisitionStatusRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_id | [string](#string) |  | The camera ID. |

### CameraServiceGetAcquisitionStatusResponse

Response object for the get acquisition state.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| status | [CameraAcquisitionStatus](#zen_api.em.hardware.v1.CameraAcquisitionStatus) |  | The acquisition status. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### CameraServiceGetAvailableCamerasRequest

The CameraServiceGetAvailableCamerasRequest class.

### CameraServiceGetAvailableCamerasResponse

Response object representing a list of available cameras.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_names | [string](#string) | repeated | The available cameras on the system. |

### CameraServiceGetBrightnessRequest

The CameraServiceGetBrightnessRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_id | [string](#string) |  | The camera ID. |

### CameraServiceGetBrightnessResponse

Response object for the get brightness.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| brightness | [double](#double) |  | The brightness. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### CameraServiceGetCcdModeRequest

The CameraServiceGetCcdModeRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_id | [string](#string) |  | The camera ID. |

### CameraServiceGetCcdModeResponse

Response object for the get CCD mode.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| mode | [CcdMode](#zen_api.em.hardware.v1.CcdMode) |  | The CCD mode. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### CameraServiceGetContrastRequest

The CameraServiceGetContrastRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_id | [string](#string) |  | The camera ID. |

### CameraServiceGetContrastResponse

Response object for the get contrast.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| contrast | [double](#double) |  | The contrast. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### CameraServiceRegisterOnAcquisitionStatusChangedRequest

The CameraServiceRegisterOnAcquisitionStatusChangedRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_id | [string](#string) |  | The camera ID. |

### CameraServiceRegisterOnAcquisitionStatusChangedResponse

Response object for the get acquisition state.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| status | [CameraAcquisitionStatus](#zen_api.em.hardware.v1.CameraAcquisitionStatus) |  | The acquisition status. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### CameraServiceRegisterOnBrightnessChangedRequest

The CameraServiceRegisterOnBrightnessChangedRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_id | [string](#string) |  | The camera ID. |

### CameraServiceRegisterOnBrightnessChangedResponse

Response object for the get brightness.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| brightness | [double](#double) |  | The brightness. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### CameraServiceRegisterOnCcdModeChangedRequest

The CameraServiceRegisterOnCcdModeChangedRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_id | [string](#string) |  | The camera ID. |

### CameraServiceRegisterOnCcdModeChangedResponse

Response object for the get CCD mode.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| mode | [CcdMode](#zen_api.em.hardware.v1.CcdMode) |  | The CCD mode. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### CameraServiceRegisterOnContrastChangedRequest

The CameraServiceRegisterOnContrastChangedRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_id | [string](#string) |  | The camera ID. |

### CameraServiceRegisterOnContrastChangedResponse

Response object for the get contrast.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| contrast | [double](#double) |  | The contrast. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### CameraServiceSetBrightnessRequest

The CameraServiceSetBrightnessRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_id | [string](#string) |  | The camera ID. |
| brightness | [double](#double) |  | The brightness to set[0..100]%. |

### CameraServiceSetBrightnessResponse

Response object for the set brightness.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| brightness | [double](#double) |  | The brightness. |
| success | [bool](#bool) |  | A value indicating whether setting the brightness was successful. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### CameraServiceSetCcdModeRequest

The CameraServiceSetCcdModeRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_id | [string](#string) |  | The camera ID. |
| mode | [CcdMode](#zen_api.em.hardware.v1.CcdMode) |  | The CCD mode to set. |

### CameraServiceSetCcdModeResponse

Response object for the set CCD mode.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| mode | [CcdMode](#zen_api.em.hardware.v1.CcdMode) |  | The CCD mode. |
| success | [bool](#bool) |  | A value indicating whether setting the CCD mode was successful. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### CameraServiceSetContrastRequest

The CameraServiceSetContrastRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_id | [string](#string) |  | The camera ID. |
| contrast | [double](#double) |  | The contrast to set[0..100]%. |

### CameraServiceSetContrastResponse

Response object for the set contrast.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| contrast | [double](#double) |  | The contrast. |
| success | [bool](#bool) |  | A value indicating whether setting the contrast was successful. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### CameraServiceStartLiveAcquisitionRequest

The CameraServiceStartLiveAcquisitionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| settings | [CameraAcquisitionSettings](#zen_api.em.hardware.v1.CameraAcquisitionSettings) |  | The imaging settings used to acquire multiple frames. |

### CameraServiceStartLiveAcquisitionResponse

Response object of the camera live image acquisition.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| result\_type | [AcquisitionResponseType](#zen_api.em.hardware.v1.AcquisitionResponseType) |  | A value indicating the type of response returned by the camera live image acquisition stream. |
| width | [int32](#int32) |  | The overall width of the image. This is only valid when the ResultType is FrameStart, otherwise it will be set to zero and not transmitted. |
| height | [int32](#int32) |  | The overall height of the image. This is only valid when the ResultType is FrameStart, otherwise it will be set to zero and not transmitted. |
| bytes\_per\_pixel | [uint32](#uint32) |  | The number of bytes per pixel. This is only valid when the ResultType is FrameStart, otherwise it will be set to zero and not transmitted. |
| total\_image\_size | [int32](#int32) |  | The total size of the image. This is only valid when the ResultType is FrameStart, otherwise it will be set to zero and not transmitted. |
| image\_data | [bytes](#bytes) |  | The data buffer of this part of the image. This may be less than the total image size, in which case the client should expect more data to follow. |

### CameraServiceStartSingleAcquisitionRequest

The CameraServiceStartSingleAcquisitionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| settings | [CameraAcquisitionSettings](#zen_api.em.hardware.v1.CameraAcquisitionSettings) |  | The imaging settings used to acquire a frame. |

### CameraServiceStartSingleAcquisitionResponse

Response object of the camera single image acquisition.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| result\_type | [AcquisitionResponseType](#zen_api.em.hardware.v1.AcquisitionResponseType) |  | A value indicating the type of response returned by the camera live image acquisition stream. |
| width | [int32](#int32) |  | The overall width of the image. This is only valid when the ResultType is FrameStart, otherwise it will be set to zero and not transmitted. |
| height | [int32](#int32) |  | The overall height of the image. This is only valid when the ResultType is FrameStart, otherwise it will be set to zero and not transmitted. |
| bytes\_per\_pixel | [uint32](#uint32) |  | The number of bytes per pixel. This is only valid when the ResultType is FrameStart, otherwise it will be set to zero and not transmitted. |
| total\_image\_size | [int32](#int32) |  | The total size of the image. This is only valid when the ResultType is FrameStart, otherwise it will be set to zero and not transmitted. |
| image\_data | [bytes](#bytes) |  | The data buffer of this part of the image. This may be less than the total image size, in which case the client should expect more data to follow. |

### CameraServiceStopLiveAcquisitionRequest

The CameraServiceStopLiveAcquisitionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera\_id | [string](#string) |  | The camera ID. |

### CameraServiceStopLiveAcquisitionResponse

Response object of the camera stop acquisition.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to acquire an image succeeded or not. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### CameraService

The ICameraService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetAcquisitionStatus | [CameraServiceGetAcquisitionStatusRequest](#zen_api.em.hardware.v1.CameraServiceGetAcquisitionStatusRequest) | [CameraServiceGetAcquisitionStatusResponse](#zen_api.em.hardware.v1.CameraServiceGetAcquisitionStatusResponse) | Gets the acquisition status for the specified camera. |
|  | GetAvailableCameras | [CameraServiceGetAvailableCamerasRequest](#zen_api.em.hardware.v1.CameraServiceGetAvailableCamerasRequest) | [CameraServiceGetAvailableCamerasResponse](#zen_api.em.hardware.v1.CameraServiceGetAvailableCamerasResponse) | Gets the available cameras/ |
|  | GetBrightness | [CameraServiceGetBrightnessRequest](#zen_api.em.hardware.v1.CameraServiceGetBrightnessRequest) | [CameraServiceGetBrightnessResponse](#zen_api.em.hardware.v1.CameraServiceGetBrightnessResponse) | Gets the brightness for the specified camera. |
|  | GetCcdMode | [CameraServiceGetCcdModeRequest](#zen_api.em.hardware.v1.CameraServiceGetCcdModeRequest) | [CameraServiceGetCcdModeResponse](#zen_api.em.hardware.v1.CameraServiceGetCcdModeResponse) | Gets the CCD mode for the specified camera. |
|  | GetContrast | [CameraServiceGetContrastRequest](#zen_api.em.hardware.v1.CameraServiceGetContrastRequest) | [CameraServiceGetContrastResponse](#zen_api.em.hardware.v1.CameraServiceGetContrastResponse) | Gets the contrast for the specified camera. |
|  | RegisterOnAcquisitionStatusChanged | [CameraServiceRegisterOnAcquisitionStatusChangedRequest](#zen_api.em.hardware.v1.CameraServiceRegisterOnAcquisitionStatusChangedRequest) | [CameraServiceRegisterOnAcquisitionStatusChangedResponse](#zen_api.em.hardware.v1.CameraServiceRegisterOnAcquisitionStatusChangedResponse) stream | Registers a subscriber on acquisition status changes for the specified camera. |
|  | RegisterOnBrightnessChanged | [CameraServiceRegisterOnBrightnessChangedRequest](#zen_api.em.hardware.v1.CameraServiceRegisterOnBrightnessChangedRequest) | [CameraServiceRegisterOnBrightnessChangedResponse](#zen_api.em.hardware.v1.CameraServiceRegisterOnBrightnessChangedResponse) stream | Registers a subscriber on brightness changes for the specified camera. |
|  | RegisterOnCcdModeChanged | [CameraServiceRegisterOnCcdModeChangedRequest](#zen_api.em.hardware.v1.CameraServiceRegisterOnCcdModeChangedRequest) | [CameraServiceRegisterOnCcdModeChangedResponse](#zen_api.em.hardware.v1.CameraServiceRegisterOnCcdModeChangedResponse) stream | Registers a subscriber on CCD mode changes for the specified camera. |
|  | RegisterOnContrastChanged | [CameraServiceRegisterOnContrastChangedRequest](#zen_api.em.hardware.v1.CameraServiceRegisterOnContrastChangedRequest) | [CameraServiceRegisterOnContrastChangedResponse](#zen_api.em.hardware.v1.CameraServiceRegisterOnContrastChangedResponse) stream | Registers a subscriber on contrast changes for the specified camera. |
|  | SetBrightness | [CameraServiceSetBrightnessRequest](#zen_api.em.hardware.v1.CameraServiceSetBrightnessRequest) | [CameraServiceSetBrightnessResponse](#zen_api.em.hardware.v1.CameraServiceSetBrightnessResponse) | Sets the brightness for the specified camera. |
|  | SetCcdMode | [CameraServiceSetCcdModeRequest](#zen_api.em.hardware.v1.CameraServiceSetCcdModeRequest) | [CameraServiceSetCcdModeResponse](#zen_api.em.hardware.v1.CameraServiceSetCcdModeResponse) | Sets the CCD mode for the specified camera. |
|  | SetContrast | [CameraServiceSetContrastRequest](#zen_api.em.hardware.v1.CameraServiceSetContrastRequest) | [CameraServiceSetContrastResponse](#zen_api.em.hardware.v1.CameraServiceSetContrastResponse) | Sets the contrast for the specified camera. |
|  | StartLiveAcquisition | [CameraServiceStartLiveAcquisitionRequest](#zen_api.em.hardware.v1.CameraServiceStartLiveAcquisitionRequest) | [CameraServiceStartLiveAcquisitionResponse](#zen_api.em.hardware.v1.CameraServiceStartLiveAcquisitionResponse) stream | Starts a live acquisition with the given settings. |
|  | StartSingleAcquisition | [CameraServiceStartSingleAcquisitionRequest](#zen_api.em.hardware.v1.CameraServiceStartSingleAcquisitionRequest) | [CameraServiceStartSingleAcquisitionResponse](#zen_api.em.hardware.v1.CameraServiceStartSingleAcquisitionResponse) stream | Starts a single frame acquisition for the specified camera. The image is streamed to the same destination as live acquisition. |
|  | StopLiveAcquisition | [CameraServiceStopLiveAcquisitionRequest](#zen_api.em.hardware.v1.CameraServiceStopLiveAcquisitionRequest) | [CameraServiceStopLiveAcquisitionResponse](#zen_api.em.hardware.v1.CameraServiceStopLiveAcquisitionResponse) | Stops any ongoing live acquisition. Only has an effect if ZenApi.EM.Hardware.V1.ICameraApi.GetAcquisitionStatus(System.String) returns ZenApi.EM.Hardware.V1.AcquisitionStatus.LiveRunning. |

## zen\_api/em/hardware/v1/ccd\_mode.proto

[Top](#title)

### CcdMode

The CCD mode enumeration.

| Name | Number | Description |
| --- | --- | --- |
| CCD\_MODE\_UNSPECIFIED | 0 | Default enum value. |
| CCD\_MODE\_OFF | 1 | Illumination is off. |
| CCD\_MODE\_AUTO | 2 | Illumination mode is determined based on detector selection. |
| CCD\_MODE\_GREYSCALE | 3 | Illumination is Infra-red, producing greyscale images. |
| CCD\_MODE\_COLOR | 4 | Illumination is White light, producing color images. |

## zen\_api/em/hardware/v1/command\_id.proto

[Top](#title)

### CommandId

| Name | Number | Description |
| --- | --- | --- |
| COMMAND\_ID\_UNSPECIFIED | 0 | framework required, not used for communication. |
| COMMAND\_ID\_EXECUTE | 1 | The external procedure is currently executing. |
| COMMAND\_ID\_STOP | 2 | The external procedure is about to stop it's execution. |
| COMMAND\_ID\_PAUSE | 3 | The external procedure is paused from execution. |
| COMMAND\_ID\_CONTINUE | 4 | The external procedure is continued from pause. |
| COMMAND\_ID\_CLOSE | 5 | The external procedure is about to close . |

## zen\_api/em/hardware/v1/detector\_service.proto

[Top](#title)

### DetectorServiceGetAvailableDetectorsRequest

The DetectorServiceGetAvailableDetectorsRequest class.

### DetectorServiceGetAvailableDetectorsResponse

Response object representing a list of available detectors.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| detector\_names | [string](#string) | repeated | The available detectors on the system. |

### DetectorServiceGetBrightnessRequest

The DetectorServiceGetBrightnessRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| detector\_name | [string](#string) |  | The unique name of the detector to control as string. Must be part of ZenApi.EM.Hardware.V1.IDetectorApi.GetAvailableDetectors. |

### DetectorServiceGetBrightnessResponse

Response object representing a detector brightness value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| brightness | [double](#double) |  | The brightness in percentage [0, 100]. |

### DetectorServiceGetContrastRequest

The DetectorServiceGetContrastRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| detector\_name | [string](#string) |  | The unique name of the detector to control as string. Must be part of ZenApi.EM.Hardware.V1.IDetectorApi.GetAvailableDetectors. |

### DetectorServiceGetContrastResponse

Response object representing a detector contrast value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| contrast | [double](#double) |  | The contrast in percentage [0, 100]. |

### DetectorServiceRegisterOnBrightnessChangedRequest

The DetectorServiceRegisterOnBrightnessChangedRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| detector\_name | [string](#string) |  | The unique name of the detector to control as string. Must be part of ZenApi.EM.Hardware.V1.IDetectorApi.GetAvailableDetectors. |

### DetectorServiceRegisterOnBrightnessChangedResponse

Response object representing a detector brightness value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| brightness | [double](#double) |  | The brightness in percentage [0, 100]. |

### DetectorServiceRegisterOnContrastChangedRequest

The DetectorServiceRegisterOnContrastChangedRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| detector\_name | [string](#string) |  | The unique name of the detector to control as string. Must be part of ZenApi.EM.Hardware.V1.IDetectorApi.GetAvailableDetectors. |

### DetectorServiceRegisterOnContrastChangedResponse

Response object representing a detector contrast value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| contrast | [double](#double) |  | The contrast in percentage [0, 100]. |

### DetectorServiceSetBrightnessRequest

The DetectorServiceSetBrightnessRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| detector\_name | [string](#string) |  | The unique name of the detector to control as string. Must be part of ZenApi.EM.Hardware.V1.IDetectorApi.GetAvailableDetectors. |
| brightness | [double](#double) |  | The brightness value to apply in percentage [0, 1]. |

### DetectorServiceSetBrightnessResponse

Response object representing a detector brightness value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| brightness | [double](#double) |  | The brightness in percentage [0, 100]. |

### DetectorServiceSetContrastRequest

The DetectorServiceSetContrastRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| detector\_name | [string](#string) |  | The unique name of the detector to control as string. Must be part of ZenApi.EM.Hardware.V1.IDetectorApi.GetAvailableDetectors. |
| contrast | [double](#double) |  | The contrast value to apply in percentage [0, 1]. |

### DetectorServiceSetContrastResponse

Response object representing a detector contrast value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| contrast | [double](#double) |  | The contrast in percentage [0, 100]. |

### DetectorService

The IDetectorService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetAvailableDetectors | [DetectorServiceGetAvailableDetectorsRequest](#zen_api.em.hardware.v1.DetectorServiceGetAvailableDetectorsRequest) | [DetectorServiceGetAvailableDetectorsResponse](#zen_api.em.hardware.v1.DetectorServiceGetAvailableDetectorsResponse) | Retrieves a list of all available detectors of the system. Their name serves as an identifier for this API service. |
|  | GetBrightness | [DetectorServiceGetBrightnessRequest](#zen_api.em.hardware.v1.DetectorServiceGetBrightnessRequest) | [DetectorServiceGetBrightnessResponse](#zen_api.em.hardware.v1.DetectorServiceGetBrightnessResponse) | Retrieves the brightness value applied to a specific detector in percentage. |
|  | GetContrast | [DetectorServiceGetContrastRequest](#zen_api.em.hardware.v1.DetectorServiceGetContrastRequest) | [DetectorServiceGetContrastResponse](#zen_api.em.hardware.v1.DetectorServiceGetContrastResponse) | Retrieves the contrast value applied to a specific detector in percentage. |
|  | RegisterOnBrightnessChanged | [DetectorServiceRegisterOnBrightnessChangedRequest](#zen_api.em.hardware.v1.DetectorServiceRegisterOnBrightnessChangedRequest) | [DetectorServiceRegisterOnBrightnessChangedResponse](#zen_api.em.hardware.v1.DetectorServiceRegisterOnBrightnessChangedResponse) stream | Registers a subscriber on brightness changes of a specific detector. |
|  | RegisterOnContrastChanged | [DetectorServiceRegisterOnContrastChangedRequest](#zen_api.em.hardware.v1.DetectorServiceRegisterOnContrastChangedRequest) | [DetectorServiceRegisterOnContrastChangedResponse](#zen_api.em.hardware.v1.DetectorServiceRegisterOnContrastChangedResponse) stream | Registers a subscriber on contrast changes of a specific detector. |
|  | SetBrightness | [DetectorServiceSetBrightnessRequest](#zen_api.em.hardware.v1.DetectorServiceSetBrightnessRequest) | [DetectorServiceSetBrightnessResponse](#zen_api.em.hardware.v1.DetectorServiceSetBrightnessResponse) | Applies a brightness value to a specified detector. The brightness value is applied immediately and has to be in [0, 1]. |
|  | SetContrast | [DetectorServiceSetContrastRequest](#zen_api.em.hardware.v1.DetectorServiceSetContrastRequest) | [DetectorServiceSetContrastResponse](#zen_api.em.hardware.v1.DetectorServiceSetContrastResponse) | Applies a contrast value to a specified detector. The contrast value is applied immediately and has to be in [0, 1]. |

## zen\_api/em/hardware/v1/electron\_column\_service.proto

[Top](#title)

### ElectronColumnServiceGetActualVoltageRequest

The ElectronColumnServiceGetActualVoltageRequest class.

### ElectronColumnServiceGetActualVoltageResponse

Response object representing the eht/voltage.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| voltage | [double](#double) |  | The eht/voltage in volts. |

### ElectronColumnServiceGetApertureAlignRequest

The ElectronColumnServiceGetApertureAlignRequest class.

### ElectronColumnServiceGetApertureAlignResponse

Response object describing the aperture align values.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [double](#double) |  | The x aperture align in percentage. |
| y | [double](#double) |  | The y aperture align in percentage. |

### ElectronColumnServiceGetBeamBlankerStateRequest

The ElectronColumnServiceGetBeamBlankerStateRequest class.

### ElectronColumnServiceGetBeamBlankerStateResponse

Response object representing the beam blanker.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| is\_beam\_blanked | [bool](#bool) |  | A value indicating whether the beam is blanked. |

### ElectronColumnServiceGetBeamShiftLimitsRequest

The ElectronColumnServiceGetBeamShiftLimitsRequest class.

### ElectronColumnServiceGetBeamShiftLimitsResponse

Response object representing the beam shift limits.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| beam\_shift\_xmin | [double](#double) |  | The minimum beam shift X in meters. |
| beam\_shift\_xmax | [double](#double) |  | The maximum beam shift X in meters. |
| beam\_shift\_ymin | [double](#double) |  | The minimum beam shift Y in meters. |
| beam\_shift\_ymax | [double](#double) |  | The maximum beam shift Y in meters. |

### ElectronColumnServiceGetBeamShiftRequest

The ElectronColumnServiceGetBeamShiftRequest class.

### ElectronColumnServiceGetBeamShiftResponse

Response object describing the beam shift values.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| shift\_x | [double](#double) |  | The x beam shift in meters. |
| shift\_y | [double](#double) |  | The y beam shift in meters. |

### ElectronColumnServiceGetBeamStateRequest

The ElectronColumnServiceGetBeamStateRequest class.

### ElectronColumnServiceGetBeamStateResponse

BeamState enum wrapper.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| state | [BeamState](#zen_api.em.hardware.v1.BeamState) |  | The beam state. |
| task\_success | [bool](#bool) |  | A value indicating whether the task to change beam state succeeded or not. |

### ElectronColumnServiceGetBoosterVoltageRequest

The ElectronColumnServiceGetBoosterVoltageRequest class.

### ElectronColumnServiceGetBoosterVoltageResponse

Response object representing the booster voltage.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| booster\_voltage | [double](#double) |  | The booster voltage in volts. |
| success | [bool](#bool) |  | A value indicating whether getting the booster voltage was successful. |

### ElectronColumnServiceGetEhtOffsetLimitsRequest

The ElectronColumnServiceGetEhtOffsetLimitsRequest class.

### ElectronColumnServiceGetEhtOffsetLimitsResponse

Response object representing the eht offset response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| minimum | [double](#double) |  | The minimum eht offset in volts. |
| maximum | [double](#double) |  | The maximum eht offset in volts. |
| success | [bool](#bool) |  | A value indicating whether geetting the eht offset limits was successful. |

### ElectronColumnServiceGetEhtOffsetRequest

The ElectronColumnServiceGetEhtOffsetRequest class.

### ElectronColumnServiceGetEhtOffsetResponse

Response object representing the eht offset.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| eht\_offset | [double](#double) |  | The eht offset in volts. |
| success | [bool](#bool) |  | A value indicating whether gets or sets of the eht offset was successful. |

### ElectronColumnServiceGetFocusLimitsRequest

The ElectronColumnServiceGetFocusLimitsRequest class.

### ElectronColumnServiceGetFocusLimitsResponse

Response object representing the column focus.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| focus\_min | [double](#double) |  | The minimum focus in meters. |
| focus\_max | [double](#double) |  | The maximum focus in meters. |

### ElectronColumnServiceGetFocusRequest

The ElectronColumnServiceGetFocusRequest class.

### ElectronColumnServiceGetFocusResponse

Response object representing the column focus.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| focus | [double](#double) |  | The focus in meters. |

### ElectronColumnServiceGetFovLimitsRequest

The ElectronColumnServiceGetFovLimitsRequest class.

### ElectronColumnServiceGetFovLimitsResponse

Response object representing the field of view limits.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| minimum | [double](#double) |  | The minimum field of view in meters. |
| maximum | [double](#double) |  | The maximum field of view in meters. |

### ElectronColumnServiceGetFovRequest

The ElectronColumnServiceGetFovRequest class.

### ElectronColumnServiceGetFovResponse

Response object representing the field of view expansion.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| fov | [double](#double) |  | The fov expansion in meters. |

### ElectronColumnServiceGetFovRotationLimitsRequest

The ElectronColumnServiceGetFovRotationLimitsRequest class.

### ElectronColumnServiceGetFovRotationLimitsResponse

Response object representing the field of view rotation limits.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| minimum | [double](#double) |  | The minimum field of view rotation in radians. |
| maximum | [double](#double) |  | The maximum field of view rotation in radians. |

### ElectronColumnServiceGetFovRotationRequest

The ElectronColumnServiceGetFovRotationRequest class.

### ElectronColumnServiceGetFovRotationResponse

Response object representing the field of view rotation.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| rotation | [double](#double) |  | The field of view rotation in radians. |

### ElectronColumnServiceGetObjectiveCurrentRequest

The ElectronColumnServiceGetObjectiveCurrentRequest class.

### ElectronColumnServiceGetObjectiveCurrentResponse

Response object representing the objective current.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| objective\_current | [double](#double) |  | The objective current in amperes. |
| success | [bool](#bool) |  | A value indicating whether getting the objective current was successful. |

### ElectronColumnServiceGetProbeCurrentRequest

The ElectronColumnServiceGetProbeCurrentRequest class.

### ElectronColumnServiceGetProbeCurrentResponse

Response object representing the probe current.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| probe\_current | [double](#double) |  | The probe current value in Amps. |

### ElectronColumnServiceGetSemiAngleRequest

The ElectronColumnServiceGetSemiAngleRequest class.

### ElectronColumnServiceGetSemiAngleResponse

Response object describing the semi angle value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| angle | [double](#double) |  | The semi angle in radians. |

### ElectronColumnServiceGetSpotSizeRequest

The ElectronColumnServiceGetSpotSizeRequest class.

### ElectronColumnServiceGetSpotSizeResponse

Response object representing the spot size.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| spot\_size | [double](#double) |  | The spot size in meters. |

### ElectronColumnServiceGetStigmatorRequest

The ElectronColumnServiceGetStigmatorRequest class.

### ElectronColumnServiceGetStigmatorResponse

Response object representing the stigmator value of the electron column.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| stigmator\_x | [double](#double) |  | The stigmator x in percent [0,1]. |
| stigmator\_y | [double](#double) |  | The stigmator y in percent [0,1]. |

### ElectronColumnServiceGetTargetVoltageRequest

The ElectronColumnServiceGetTargetVoltageRequest class.

### ElectronColumnServiceGetTargetVoltageResponse

Response object representing the eht/voltage.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| voltage | [double](#double) |  | The eht/voltage in volts. |

### ElectronColumnServiceGetVoltageLimitsRequest

The ElectronColumnServiceGetVoltageLimitsRequest class.

### ElectronColumnServiceGetVoltageLimitsResponse

Response object representing the voltage limits.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| minimum | [double](#double) |  | The minimum voltage in volts. |
| maximum | [double](#double) |  | The maximum voltage in volts. |

### ElectronColumnServiceGoToStandbyRequest

The ElectronColumnServiceGoToStandbyRequest class.

### ElectronColumnServiceGoToStandbyResponse

BeamState enum wrapper.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| state | [BeamState](#zen_api.em.hardware.v1.BeamState) |  | The beam state. |
| task\_success | [bool](#bool) |  | A value indicating whether the task to change beam state succeeded or not. |

### ElectronColumnServiceRegisterOnApertureAlignChangedRequest

The ElectronColumnServiceRegisterOnApertureAlignChangedRequest class.

### ElectronColumnServiceRegisterOnApertureAlignChangedResponse

Response object describing the aperture align values.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [double](#double) |  | The x aperture align in percentage. |
| y | [double](#double) |  | The y aperture align in percentage. |

### ElectronColumnServiceRegisterOnBeamBlankerStateChangedRequest

The ElectronColumnServiceRegisterOnBeamBlankerStateChangedRequest class.

### ElectronColumnServiceRegisterOnBeamBlankerStateChangedResponse

Response object representing the beam blanker.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| is\_beam\_blanked | [bool](#bool) |  | A value indicating whether the beam is blanked. |

### ElectronColumnServiceRegisterOnBeamShiftChangedRequest

The ElectronColumnServiceRegisterOnBeamShiftChangedRequest class.

### ElectronColumnServiceRegisterOnBeamShiftChangedResponse

Response object describing the beam shift values.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| shift\_x | [double](#double) |  | The x beam shift in meters. |
| shift\_y | [double](#double) |  | The y beam shift in meters. |

### ElectronColumnServiceRegisterOnBeamStateChangedRequest

The ElectronColumnServiceRegisterOnBeamStateChangedRequest class.

### ElectronColumnServiceRegisterOnBeamStateChangedResponse

BeamState enum wrapper.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| state | [BeamState](#zen_api.em.hardware.v1.BeamState) |  | The beam state. |
| task\_success | [bool](#bool) |  | A value indicating whether the task to change beam state succeeded or not. |

### ElectronColumnServiceRegisterOnFocusChangedRequest

The ElectronColumnServiceRegisterOnFocusChangedRequest class.

### ElectronColumnServiceRegisterOnFocusChangedResponse

Response object representing the column focus.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| focus | [double](#double) |  | The focus in meters. |

### ElectronColumnServiceRegisterOnFovChangedRequest

The ElectronColumnServiceRegisterOnFovChangedRequest class.

### ElectronColumnServiceRegisterOnFovChangedResponse

Response object representing the field of view expansion.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| fov | [double](#double) |  | The fov expansion in meters. |

### ElectronColumnServiceRegisterOnFovRotationChangedRequest

The ElectronColumnServiceRegisterOnFovRotationChangedRequest class.

### ElectronColumnServiceRegisterOnFovRotationChangedResponse

Response object representing the field of view rotation.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| rotation | [double](#double) |  | The field of view rotation in radians. |

### ElectronColumnServiceRegisterOnProbeCurrentChangedRequest

The ElectronColumnServiceRegisterOnProbeCurrentChangedRequest class.

### ElectronColumnServiceRegisterOnProbeCurrentChangedResponse

Response object representing the probe current.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| probe\_current | [double](#double) |  | The probe current value in Amps. |

### ElectronColumnServiceRegisterOnSemiAngleChangedRequest

The ElectronColumnServiceRegisterOnSemiAngleChangedRequest class.

### ElectronColumnServiceRegisterOnSemiAngleChangedResponse

Response object describing the semi angle values.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| angle | [double](#double) |  | The semi angle in radians. |

### ElectronColumnServiceRegisterOnSpotSizeChangedRequest

The ElectronColumnServiceRegisterOnSpotSizeChangedRequest class.

### ElectronColumnServiceRegisterOnSpotSizeChangedResponse

Response object representing the spot size.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| spot\_size | [double](#double) |  | The spot size in meters. |

### ElectronColumnServiceRegisterOnStigmatorChangedRequest

The ElectronColumnServiceRegisterOnStigmatorChangedRequest class.

### ElectronColumnServiceRegisterOnStigmatorChangedResponse

Response object representing stigmator changes of the electron column.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| stigmator\_x | [double](#double) |  | The stigmator x in percent [0,1]. |
| stigmator\_y | [double](#double) |  | The stigmator y in percent [0,1]. |

### ElectronColumnServiceRegisterOnVoltageChangedRequest

The ElectronColumnServiceRegisterOnVoltageChangedRequest class.

### ElectronColumnServiceRegisterOnVoltageChangedResponse

Response object representing the eht/voltage.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| voltage | [double](#double) |  | The eht/voltage in volts. |

### ElectronColumnServiceSetApertureAlignRequest

The ElectronColumnServiceSetApertureAlignRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The new aperture align x in percentage. null if it should not be changed. |
| y | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The new aperture align y in percentage. null if it should not be changed. |

### ElectronColumnServiceSetApertureAlignResponse

Response object describing the aperture align values.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [double](#double) |  | The x aperture align in percentage. |
| y | [double](#double) |  | The y aperture align in percentage. |
| success | [bool](#bool) |  | A value indicating whether setting of the aperture alignment was successful. |

### ElectronColumnServiceSetBeamBlankerStateRequest

The ElectronColumnServiceSetBeamBlankerStateRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| blank\_beam | [bool](#bool) |  | True blanks beam, false unblanks beam. |

### ElectronColumnServiceSetBeamBlankerStateResponse

Response object representing the electron column beam blanker.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| beam\_blanked | [bool](#bool) |  | The beam blanker. |

### ElectronColumnServiceSetBeamShiftRequest

The ElectronColumnServiceSetBeamShiftRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| xshift | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The new beam shift x in meters. null if it should not be changed. |
| yshift | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The new beam shift y in meters. null if it should not be changed. |

### ElectronColumnServiceSetBeamShiftResponse

Response object describing the beam shift values.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| shift\_x | [double](#double) |  | The x beam shift in meters. |
| shift\_y | [double](#double) |  | The y beam shift in meters. |

### ElectronColumnServiceSetEhtOffsetRequest

The ElectronColumnServiceSetEhtOffsetRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| eht\_offset | [double](#double) |  | The eht offset. |

### ElectronColumnServiceSetEhtOffsetResponse

Response object representing the eht offset response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| eht\_offset | [double](#double) |  | The eht offset in volts. |
| success | [bool](#bool) |  | A value indicating whether gets or sets of the eht offset was successful. |

### ElectronColumnServiceSetFocusRequest

The ElectronColumnServiceSetFocusRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| focus | [double](#double) |  | The new focus in meters. |

### ElectronColumnServiceSetFocusResponse

Response object representing the column focus.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| focus | [double](#double) |  | The focus in meters. |

### ElectronColumnServiceSetFovRequest

The ElectronColumnServiceSetFovRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| fov | [double](#double) |  | The size of the new FOV in meters. |

### ElectronColumnServiceSetFovResponse

Response object representing the field of view expansion.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| fov | [double](#double) |  | The fov expansion in meters. |

### ElectronColumnServiceSetFovRotationRequest

The ElectronColumnServiceSetFovRotationRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| fov\_rotation | [double](#double) |  | The rotation in radians, clockwise. |

### ElectronColumnServiceSetFovRotationResponse

Response object representing the field of view rotation.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| rotation | [double](#double) |  | The field of view rotation in radians. |

### ElectronColumnServiceSetObjectiveCurrentRequest

The ElectronColumnServiceSetObjectiveCurrentRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| objective\_current | [double](#double) |  | The objective current in amperes. |

### ElectronColumnServiceSetObjectiveCurrentResponse

Response object representing the objective current response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| objective\_current | [double](#double) |  | The ObjectiveCurrent in amperes. |
| success | [bool](#bool) |  | A value indicating whether setting the objective current was successful. |

### ElectronColumnServiceSetProbeCurrentRequest

The ElectronColumnServiceSetProbeCurrentRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| current\_amps | [double](#double) |  | Probe current in Ampere. |

### ElectronColumnServiceSetProbeCurrentResponse

Response object representing the probe current.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| success | [bool](#bool) |  | A value indicating whether setting the probe current was successful. |
| probe\_current | [double](#double) |  | The probe current value in Amps. |

### ElectronColumnServiceSetStigmatorRequest

The ElectronColumnServiceSetStigmatorRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| stigmator\_x | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The stigmator x value in percent [0, 1] or null if is not supposed to change. |
| stigmator\_y | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The stigmator y value in percent [0, 1] or null if is not supposed to change. |

### ElectronColumnServiceSetStigmatorResponse

Response object representing the stigmator set value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| stigmator\_x | [double](#double) |  | The stigmator x in percent [0,1]. |
| stigmator\_y | [double](#double) |  | The stigmator y in percent [0,1]. |

### ElectronColumnServiceSetVoltageRequest

The ElectronColumnServiceSetVoltageRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| voltage | [double](#double) |  | The new eht/voltage in volts. |

### ElectronColumnServiceSetVoltageResponse

Response object representing the eht/voltage.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| voltage | [double](#double) |  | The eht/voltage in volts. |

### ElectronColumnServiceTurnOffRequest

The ElectronColumnServiceTurnOffRequest class.

### ElectronColumnServiceTurnOffResponse

BeamState enum wrapper.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| state | [BeamState](#zen_api.em.hardware.v1.BeamState) |  | The beam state. |
| task\_success | [bool](#bool) |  | A value indicating whether the task to change beam state succeeded or not. |

### ElectronColumnServiceTurnOnRequest

The ElectronColumnServiceTurnOnRequest class.

### ElectronColumnServiceTurnOnResponse

BeamState enum wrapper.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| state | [BeamState](#zen_api.em.hardware.v1.BeamState) |  | The beam state. |
| task\_success | [bool](#bool) |  | A value indicating whether the task to change beam state succeeded or not. |

### ElectronColumnService

The IElectronColumnService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetActualVoltage | [ElectronColumnServiceGetActualVoltageRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetActualVoltageRequest) | [ElectronColumnServiceGetActualVoltageResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetActualVoltageResponse) | Retrieves the current eht/voltage. |
|  | GetApertureAlign | [ElectronColumnServiceGetApertureAlignRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetApertureAlignRequest) | [ElectronColumnServiceGetApertureAlignResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetApertureAlignResponse) | Gets the aperture align in percentage. |
|  | GetBeamBlankerState | [ElectronColumnServiceGetBeamBlankerStateRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamBlankerStateRequest) | [ElectronColumnServiceGetBeamBlankerStateResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamBlankerStateResponse) | Gets the beam blanker state. |
|  | GetBeamShift | [ElectronColumnServiceGetBeamShiftRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamShiftRequest) | [ElectronColumnServiceGetBeamShiftResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamShiftResponse) | Gets the current beam shift in meters. |
|  | GetBeamShiftLimits | [ElectronColumnServiceGetBeamShiftLimitsRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamShiftLimitsRequest) | [ElectronColumnServiceGetBeamShiftLimitsResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamShiftLimitsResponse) | Gets the limits of the beam shiftin meters. |
|  | GetBeamState | [ElectronColumnServiceGetBeamStateRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamStateRequest) | [ElectronColumnServiceGetBeamStateResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetBeamStateResponse) | Retrieves the current beam working state. |
|  | GetBoosterVoltage | [ElectronColumnServiceGetBoosterVoltageRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetBoosterVoltageRequest) | [ElectronColumnServiceGetBoosterVoltageResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetBoosterVoltageResponse) | Gets the booster voltage in volts. |
|  | GetEhtOffset | [ElectronColumnServiceGetEhtOffsetRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetEhtOffsetRequest) | [ElectronColumnServiceGetEhtOffsetResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetEhtOffsetResponse) | Gets the eht offset in volts. |
|  | GetEhtOffsetLimits | [ElectronColumnServiceGetEhtOffsetLimitsRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetEhtOffsetLimitsRequest) | [ElectronColumnServiceGetEhtOffsetLimitsResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetEhtOffsetLimitsResponse) | Gets the limits of the eht offset in volts. |
|  | GetFocus | [ElectronColumnServiceGetFocusRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetFocusRequest) | [ElectronColumnServiceGetFocusResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetFocusResponse) | Gets the current focus (working distance) in meters. |
|  | GetFocusLimits | [ElectronColumnServiceGetFocusLimitsRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetFocusLimitsRequest) | [ElectronColumnServiceGetFocusLimitsResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetFocusLimitsResponse) | Gets the limits of the current focus (working distance) in meters. |
|  | GetFov | [ElectronColumnServiceGetFovRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovRequest) | [ElectronColumnServiceGetFovResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovResponse) | Retrieves the current Field Of View. |
|  | GetFovLimits | [ElectronColumnServiceGetFovLimitsRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovLimitsRequest) | [ElectronColumnServiceGetFovLimitsResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovLimitsResponse) | Gets the limits of the Field Of View in meters. |
|  | GetFovRotation | [ElectronColumnServiceGetFovRotationRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovRotationRequest) | [ElectronColumnServiceGetFovRotationResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovRotationResponse) | Gets the rotation of the Field Of View. |
|  | GetFovRotationLimits | [ElectronColumnServiceGetFovRotationLimitsRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovRotationLimitsRequest) | [ElectronColumnServiceGetFovRotationLimitsResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetFovRotationLimitsResponse) | Gets the limits of the Field Of View rotation in radians. |
|  | GetObjectiveCurrent | [ElectronColumnServiceGetObjectiveCurrentRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetObjectiveCurrentRequest) | [ElectronColumnServiceGetObjectiveCurrentResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetObjectiveCurrentResponse) | Gets the objective current in amperes. The objective current controls the strength of the magnetic field of the lens. |
|  | GetProbeCurrent | [ElectronColumnServiceGetProbeCurrentRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetProbeCurrentRequest) | [ElectronColumnServiceGetProbeCurrentResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetProbeCurrentResponse) | Get the probe current. |
|  | GetSemiAngle | [ElectronColumnServiceGetSemiAngleRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetSemiAngleRequest) | [ElectronColumnServiceGetSemiAngleResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetSemiAngleResponse) | Gets the current semi angle in radians. |
|  | GetSpotSize | [ElectronColumnServiceGetSpotSizeRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetSpotSizeRequest) | [ElectronColumnServiceGetSpotSizeResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetSpotSizeResponse) | Gets the spot size in meters. |
|  | GetStigmator | [ElectronColumnServiceGetStigmatorRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetStigmatorRequest) | [ElectronColumnServiceGetStigmatorResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetStigmatorResponse) | Gets the current stigmator x and y values in percent [0, 1]. |
|  | GetTargetVoltage | [ElectronColumnServiceGetTargetVoltageRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetTargetVoltageRequest) | [ElectronColumnServiceGetTargetVoltageResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetTargetVoltageResponse) | Retrieves the target eht/voltage. |
|  | GetVoltageLimits | [ElectronColumnServiceGetVoltageLimitsRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGetVoltageLimitsRequest) | [ElectronColumnServiceGetVoltageLimitsResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGetVoltageLimitsResponse) | Gets the limits of the voltage (EHT) in volts. |
|  | GoToStandby | [ElectronColumnServiceGoToStandbyRequest](#zen_api.em.hardware.v1.ElectronColumnServiceGoToStandbyRequest) | [ElectronColumnServiceGoToStandbyResponse](#zen_api.em.hardware.v1.ElectronColumnServiceGoToStandbyResponse) | Bring the column into standby mode. This call triggers the column to go into standby mode. Emission will still be on. |
|  | RegisterOnApertureAlignChanged | [ElectronColumnServiceRegisterOnApertureAlignChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnApertureAlignChangedRequest) | [ElectronColumnServiceRegisterOnApertureAlignChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnApertureAlignChangedResponse) stream | Register on aperture align changed events. |
|  | RegisterOnBeamBlankerStateChanged | [ElectronColumnServiceRegisterOnBeamBlankerStateChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnBeamBlankerStateChangedRequest) | [ElectronColumnServiceRegisterOnBeamBlankerStateChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnBeamBlankerStateChangedResponse) stream | Register on the beam blanker state changed events. |
|  | RegisterOnBeamShiftChanged | [ElectronColumnServiceRegisterOnBeamShiftChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnBeamShiftChangedRequest) | [ElectronColumnServiceRegisterOnBeamShiftChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnBeamShiftChangedResponse) stream | Register on column beam shift changed events. |
|  | RegisterOnBeamStateChanged | [ElectronColumnServiceRegisterOnBeamStateChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnBeamStateChangedRequest) | [ElectronColumnServiceRegisterOnBeamStateChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnBeamStateChangedResponse) stream | Register on beam state changed events. |
|  | RegisterOnFocusChanged | [ElectronColumnServiceRegisterOnFocusChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnFocusChangedRequest) | [ElectronColumnServiceRegisterOnFocusChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnFocusChangedResponse) stream | Register on column focus (working distance) changed events. |
|  | RegisterOnFovChanged | [ElectronColumnServiceRegisterOnFovChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnFovChangedRequest) | [ElectronColumnServiceRegisterOnFovChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnFovChangedResponse) stream | Register on column FOV changed events. |
|  | RegisterOnFovRotationChanged | [ElectronColumnServiceRegisterOnFovRotationChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnFovRotationChangedRequest) | [ElectronColumnServiceRegisterOnFovRotationChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnFovRotationChangedResponse) stream | Register on FOV rotation changed events. |
|  | RegisterOnProbeCurrentChanged | [ElectronColumnServiceRegisterOnProbeCurrentChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnProbeCurrentChangedRequest) | [ElectronColumnServiceRegisterOnProbeCurrentChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnProbeCurrentChangedResponse) stream | Register on column probe current changed events. |
|  | RegisterOnSemiAngleChanged | [ElectronColumnServiceRegisterOnSemiAngleChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnSemiAngleChangedRequest) | [ElectronColumnServiceRegisterOnSemiAngleChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnSemiAngleChangedResponse) stream | Register on column semi angle changed events. |
|  | RegisterOnSpotSizeChanged | [ElectronColumnServiceRegisterOnSpotSizeChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnSpotSizeChangedRequest) | [ElectronColumnServiceRegisterOnSpotSizeChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnSpotSizeChangedResponse) stream | Register on beam spot size changed events. |
|  | RegisterOnStigmatorChanged | [ElectronColumnServiceRegisterOnStigmatorChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnStigmatorChangedRequest) | [ElectronColumnServiceRegisterOnStigmatorChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnStigmatorChangedResponse) stream | Register on stigmator x and y changed events. |
|  | RegisterOnVoltageChanged | [ElectronColumnServiceRegisterOnVoltageChangedRequest](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnVoltageChangedRequest) | [ElectronColumnServiceRegisterOnVoltageChangedResponse](#zen_api.em.hardware.v1.ElectronColumnServiceRegisterOnVoltageChangedResponse) stream | Register on column (current/actual) eht/voltage changed events. |
|  | SetApertureAlign | [ElectronColumnServiceSetApertureAlignRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetApertureAlignRequest) | [ElectronColumnServiceSetApertureAlignResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetApertureAlignResponse) | Sets the eht offset. |
|  | SetBeamBlankerState | [ElectronColumnServiceSetBeamBlankerStateRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetBeamBlankerStateRequest) | [ElectronColumnServiceSetBeamBlankerStateResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetBeamBlankerStateResponse) | Sets the beam blanker state. |
|  | SetBeamShift | [ElectronColumnServiceSetBeamShiftRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetBeamShiftRequest) | [ElectronColumnServiceSetBeamShiftResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetBeamShiftResponse) | Set the beam shift of this column. Values can be null if they should not be updated. |
|  | SetEhtOffset | [ElectronColumnServiceSetEhtOffsetRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetEhtOffsetRequest) | [ElectronColumnServiceSetEhtOffsetResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetEhtOffsetResponse) | Sets the eht offset. |
|  | SetFocus | [ElectronColumnServiceSetFocusRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetFocusRequest) | [ElectronColumnServiceSetFocusResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetFocusResponse) | Applies a new focus (working distance) to the column. |
|  | SetFov | [ElectronColumnServiceSetFovRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetFovRequest) | [ElectronColumnServiceSetFovResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetFovResponse) | Applies a new FOV. |
|  | SetFovRotation | [ElectronColumnServiceSetFovRotationRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetFovRotationRequest) | [ElectronColumnServiceSetFovRotationResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetFovRotationResponse) | Rotates the Field Of View. If scan rotation is not enabled, it would be enabled. |
|  | SetObjectiveCurrent | [ElectronColumnServiceSetObjectiveCurrentRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetObjectiveCurrentRequest) | [ElectronColumnServiceSetObjectiveCurrentResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetObjectiveCurrentResponse) | Sets the objective current, that controlls the strength of the magnetic field of the lens. |
|  | SetProbeCurrent | [ElectronColumnServiceSetProbeCurrentRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetProbeCurrentRequest) | [ElectronColumnServiceSetProbeCurrentResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetProbeCurrentResponse) | Set the probe current. |
|  | SetStigmator | [ElectronColumnServiceSetStigmatorRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetStigmatorRequest) | [ElectronColumnServiceSetStigmatorResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetStigmatorResponse) | Applies a new stigmator x and / or y value to the column. |
|  | SetVoltage | [ElectronColumnServiceSetVoltageRequest](#zen_api.em.hardware.v1.ElectronColumnServiceSetVoltageRequest) | [ElectronColumnServiceSetVoltageResponse](#zen_api.em.hardware.v1.ElectronColumnServiceSetVoltageResponse) | Applies a new target eht/voltage to the column. |
|  | TurnOff | [ElectronColumnServiceTurnOffRequest](#zen_api.em.hardware.v1.ElectronColumnServiceTurnOffRequest) | [ElectronColumnServiceTurnOffResponse](#zen_api.em.hardware.v1.ElectronColumnServiceTurnOffResponse) | Turns the column off. This call initiates ramping down of emission and brings the column into off state. |
|  | TurnOn | [ElectronColumnServiceTurnOnRequest](#zen_api.em.hardware.v1.ElectronColumnServiceTurnOnRequest) | [ElectronColumnServiceTurnOnResponse](#zen_api.em.hardware.v1.ElectronColumnServiceTurnOnResponse) | Bring the column into working mode. This call initiates ramping of emission and brings the column into working condition. |

## zen\_api/em/hardware/v1/em\_stage\_service.proto

[Top](#title)

### EmStageServiceGetAxisBacklashModeRequest

The EmStageServiceGetAxisBacklashModeRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_id | [zen\_api.hardware.v1.AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |

### EmStageServiceGetAxisLimitsRequest

The EmStageServiceGetAxisLimitsRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_id | [zen\_api.hardware.v1.AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |

### EmStageServiceGetAxisUserLimitsRequest

The EmStageServiceGetAxisUserLimitsRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_id | [zen\_api.hardware.v1.AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |

### EmStageServiceGetAxisVelocityLimitsRequest

The EmStageServiceGetAxisVelocityLimitsRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_id | [zen\_api.hardware.v1.AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |

### EmStageServiceGetStageBacklashModesRequest

The EmStageServiceGetStageBacklashModesRequest class.

### EmStageServiceGetStageFastRequest

The EmStageServiceGetStageFastRequest class.

### EmStageServiceGetStageLimitsRequest

The EmStageServiceGetStageLimitsRequest class.

### EmStageServiceGetStageUserLimitsRequest

The EmStageServiceGetStageUserLimitsRequest class.

### EmStageServiceGetStageVelocityLimitsRequest

The EmStageServiceGetStageVelocityLimitsRequest class.

### EmStageServiceSetAxisBacklashModeRequest

The EmStageServiceSetAxisBacklashModeRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_id | [zen\_api.hardware.v1.AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| mode | [StageBacklashMode](#zen_api.em.hardware.v1.StageBacklashMode) |  | The backlash mode to set. |

### EmStageServiceSetAxisUserLimitsRequest

The EmStageServiceSetAxisUserLimitsRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_id | [zen\_api.hardware.v1.AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| lower\_limit | [double](#double) |  | The lower User limit in meters. Range [-1.0 : 1.0 m] |
| upper\_limit | [double](#double) |  | The upper User limit in meters. Range [-1.0 : 1.0 m] |

### EmStageServiceSetAxisVelocityRequest

The EmStageServiceSetAxisVelocityRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_id | [zen\_api.hardware.v1.AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| velocity | [double](#double) |  | The target velocity in meters per second or radians per second. |

### EmStageServiceSetStageBacklashModesRequest

The EmStageServiceSetStageBacklashModesRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_backlash\_modes | [StageServiceAxisBacklashModeResponse](#zen_api.em.hardware.v1.StageServiceAxisBacklashModeResponse) | repeated | Array of axis backlash modes to set. |

### EmStageServiceSetStageFastRequest

The EmStageServiceSetStageFastRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| stage\_fast | [bool](#bool) |  | The new stage fast status. |

### EmStageServiceSetStageUserLimitsRequest

The EmStageServiceSetStageUserLimitsRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_user\_limits | [StageServiceAxisUserLimitsResponse](#zen_api.em.hardware.v1.StageServiceAxisUserLimitsResponse) | repeated | Array of axis User limits to set. |

### StageServiceAxisBacklashModeResponse

Request object for setting axis backlash mode.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis | [zen\_api.hardware.v1.AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| mode | [StageBacklashMode](#zen_api.em.hardware.v1.StageBacklashMode) |  | The backlash mode. |

### StageServiceAxisUserLimitsResponse

Request object for setting axis soft limits.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis | [zen\_api.hardware.v1.AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| lower\_limit | [double](#double) |  | The lower soft limit in meters or radians. |
| upper\_limit | [double](#double) |  | The upper soft limit in meters or radians. |

### StageServiceGetAxisBacklashModeResponse

Response object for axis backlash mode.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis | [zen\_api.hardware.v1.AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| mode | [StageBacklashMode](#zen_api.em.hardware.v1.StageBacklashMode) |  | The backlash mode. |

### StageServiceGetAxisLimitsResponse

Response object for axis position limits.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis | [zen\_api.hardware.v1.AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| minimum | [double](#double) |  | The minimum position in meters or radians. |
| maximum | [double](#double) |  | The maximum position in meters or radians. |

### StageServiceGetAxisUserLimitsResponse

Response object for axis soft limits.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis | [zen\_api.hardware.v1.AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| lower\_limit | [double](#double) |  | The lower soft limit in meters or radians. |
| upper\_limit | [double](#double) |  | The upper soft limit in meters or radians. |

### StageServiceGetAxisVelocityLimitsResponse

Response object for axis velocity limits.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis | [zen\_api.hardware.v1.AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |  | The axis identifier. |
| minimum | [double](#double) |  | The minimum velocity in meters per second or radians per second. |
| maximum | [double](#double) |  | The maximum velocity in meters per second or radians per second. |

### StageServiceGetStageBacklashModesResponse

Response object for stage backlash modes.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_backlash\_modes | [StageServiceGetAxisBacklashModeResponse](#zen_api.em.hardware.v1.StageServiceGetAxisBacklashModeResponse) | repeated | The available axes and their backlash modes. |

### StageServiceGetStageFastResponse

Response object representing the column focus.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| stage\_fast | [bool](#bool) |  | A value indicating whether stage fast is enabled. |

### StageServiceGetStageLimitsResponse

Response object for stage position limits.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_limits | [StageServiceGetAxisLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetAxisLimitsResponse) | repeated | The available axes and their position limits. |

### StageServiceGetStageUserLimitsResponse

Response object for stage soft limits.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_soft\_limits | [StageServiceGetAxisUserLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetAxisUserLimitsResponse) | repeated | The available axes and their soft limits. |

### StageServiceGetStageVelocityLimitsResponse

Response object for stage velocity limits.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| axis\_velocity\_limits | [StageServiceGetAxisVelocityLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetAxisVelocityLimitsResponse) | repeated | The available axes and their velocity limits. |

### StageServiceSetAxisBacklashModeResponse

Response object for setting axis backlash mode.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| success | [bool](#bool) |  | A value indicating whether the operation succeeded. |

### StageServiceSetAxisUserLimitsResponse

Response object for setting axis soft limits.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| success | [bool](#bool) |  | A value indicating whether the operation succeeded. |

### StageServiceSetAxisVelocityResponse

Response object for setting axis velocity.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| success | [bool](#bool) |  | A value indicating whether the operation succeeded. |

### StageServiceSetStageBacklashModesResponse

Response object for setting stage backlash modes.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| success | [bool](#bool) |  | A value indicating whether the operation succeeded. |

### StageServiceSetStageFastResponse

Response object representing the column focus.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| stage\_fast | [bool](#bool) |  | A value indicating whether the stage fast status as a boolean. |

### StageServiceSetStageUserLimitsResponse

Response object for setting stage user limits.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| success | [bool](#bool) |  | A value indicating whether the operation succeeded. |

### EmStageService

The IEmStageService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetAxisBacklashMode | [EmStageServiceGetAxisBacklashModeRequest](#zen_api.em.hardware.v1.EmStageServiceGetAxisBacklashModeRequest) | [StageServiceGetAxisBacklashModeResponse](#zen_api.em.hardware.v1.StageServiceGetAxisBacklashModeResponse) | Gets the backlash mode for a specific stage axis. |
|  | GetAxisLimits | [EmStageServiceGetAxisLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceGetAxisLimitsRequest) | [StageServiceGetAxisLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetAxisLimitsResponse) | Gets the position limits (minimum and maximum) for a specific stage axis. |
|  | GetAxisUserLimits | [EmStageServiceGetAxisUserLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceGetAxisUserLimitsRequest) | [StageServiceGetAxisUserLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetAxisUserLimitsResponse) | Gets the User limits (upper and lower) for a specific stage axis. |
|  | GetAxisVelocityLimits | [EmStageServiceGetAxisVelocityLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceGetAxisVelocityLimitsRequest) | [StageServiceGetAxisVelocityLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetAxisVelocityLimitsResponse) | Gets the velocity limits (minimum and maximum) for a specific stage axis. |
|  | GetStageBacklashModes | [EmStageServiceGetStageBacklashModesRequest](#zen_api.em.hardware.v1.EmStageServiceGetStageBacklashModesRequest) | [StageServiceGetStageBacklashModesResponse](#zen_api.em.hardware.v1.StageServiceGetStageBacklashModesResponse) | Gets the backlash modes for all available stage axes. |
|  | GetStageFast | [EmStageServiceGetStageFastRequest](#zen_api.em.hardware.v1.EmStageServiceGetStageFastRequest) | [StageServiceGetStageFastResponse](#zen_api.em.hardware.v1.StageServiceGetStageFastResponse) | Gets the stage fast status. |
|  | GetStageLimits | [EmStageServiceGetStageLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceGetStageLimitsRequest) | [StageServiceGetStageLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetStageLimitsResponse) | Gets the position limits for all available stage axes. |
|  | GetStageUserLimits | [EmStageServiceGetStageUserLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceGetStageUserLimitsRequest) | [StageServiceGetStageUserLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetStageUserLimitsResponse) | Gets the User limits for all available stage axes. |
|  | GetStageVelocityLimits | [EmStageServiceGetStageVelocityLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceGetStageVelocityLimitsRequest) | [StageServiceGetStageVelocityLimitsResponse](#zen_api.em.hardware.v1.StageServiceGetStageVelocityLimitsResponse) | Gets the velocity limits for all available stage axes. |
|  | SetAxisBacklashMode | [EmStageServiceSetAxisBacklashModeRequest](#zen_api.em.hardware.v1.EmStageServiceSetAxisBacklashModeRequest) | [StageServiceSetAxisBacklashModeResponse](#zen_api.em.hardware.v1.StageServiceSetAxisBacklashModeResponse) | Sets the backlash mode for a specific stage axis. |
|  | SetAxisUserLimits | [EmStageServiceSetAxisUserLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceSetAxisUserLimitsRequest) | [StageServiceSetAxisUserLimitsResponse](#zen_api.em.hardware.v1.StageServiceSetAxisUserLimitsResponse) | Sets the User limits for a specific stage axis. |
|  | SetAxisVelocity | [EmStageServiceSetAxisVelocityRequest](#zen_api.em.hardware.v1.EmStageServiceSetAxisVelocityRequest) | [StageServiceSetAxisVelocityResponse](#zen_api.em.hardware.v1.StageServiceSetAxisVelocityResponse) | Sets the target velocity for a specific stage axis. |
|  | SetStageBacklashModes | [EmStageServiceSetStageBacklashModesRequest](#zen_api.em.hardware.v1.EmStageServiceSetStageBacklashModesRequest) | [StageServiceSetStageBacklashModesResponse](#zen_api.em.hardware.v1.StageServiceSetStageBacklashModesResponse) | Sets the backlash modes for multiple stage axes. |
|  | SetStageFast | [EmStageServiceSetStageFastRequest](#zen_api.em.hardware.v1.EmStageServiceSetStageFastRequest) | [StageServiceSetStageFastResponse](#zen_api.em.hardware.v1.StageServiceSetStageFastResponse) | Applies a new stage fast status. |
|  | SetStageUserLimits | [EmStageServiceSetStageUserLimitsRequest](#zen_api.em.hardware.v1.EmStageServiceSetStageUserLimitsRequest) | [StageServiceSetStageUserLimitsResponse](#zen_api.em.hardware.v1.StageServiceSetStageUserLimitsResponse) | Sets the User limits for multiple stage axes. |

## zen\_api/em/hardware/v1/extended\_acquisition\_settings.proto

[Top](#title)

### ExtendedAcquisitionSettings

Request object to set the simple acquisition settings.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| detector\_name | [string](#string) |  | The detector to use. Null will take the detector from the previous acquisition. |
| width | [int32](#int32) |  | The image width in pixels. |
| height | [int32](#int32) |  | The image height in pixels. |
| dwell\_time | [double](#double) |  | The dwell time in seconds. The closest dwell time to the selected one will be chosen. |
| frame\_averages | [int32](#int32) |  | The number of frames to average. 1 means no averaging. |
| line\_averages | [int32](#int32) |  | The number of lines to average. 1 means no averaging. |
| scan\_size\_x | [double](#double) |  | The relative size of the scan field in x direction proportional to the full field of view, where the FOV equals 1. Range (0, 1]. |
| scan\_size\_y | [double](#double) |  | The relative size of the scan field in y direction proportional to the full field of view, where the FOV equals 1. Range (0, 1]. |
| scan\_center\_x | [double](#double) |  | The relative position of the scan field in x direction proportional to the full field of view, where the optical axis is at (0,0) and the FOV ranges from -0.5 to 0.5. Range (-0.5, 0.5). |
| scan\_center\_y | [double](#double) |  | The relative position of the scan field in y direction proportional to the full field of view, where the optical axis is at (0,0) and the FOV ranges from -0.5 to 0.5. Range (-0.5, 0.5). |

## zen\_api/em/hardware/v1/external\_procedure\_service.proto

[Top](#title)

### ExternalProcedureServiceRegisterExternalProcedureRequest

The ExternalProcedureServiceRegisterExternalProcedureRequest class.

### ExternalProcedureServiceRegisterExternalProcedureResponse

transfer object definition used to send commands to external procedures

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| parameters | [string](#string) | repeated | An array of string parameters, may be empty |
| id | [string](#string) |  | The System.Guid of the external procedure the command is for, needs to be filtered by external procedures, as all procedures use the same channel to listen for commands default value could not be applied: 00000000-0000-0000-0000-000000000000 |
| command\_id | [CommandId](#zen_api.em.hardware.v1.CommandId) |  | The ZenApi.EM.Hardware.V1.ExternalProcedureServiceRegisterExternalProcedureResponse.CommandId telling the external procedure what to do |

### ExternalProcedureServiceReportCommandFailureRequest

The ExternalProcedureServiceReportCommandFailureRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| id | [string](#string) |  | the System.Guid of a given running script a command has been send to. default value could not be applied: 00000000-0000-0000-0000-000000000000 |
| command\_id | [CommandId](#zen_api.em.hardware.v1.CommandId) |  | the ZenApi.EM.Hardware.V1.CommandId of a given command. |

### ExternalProcedureServiceReportCommandFailureResponse

The ExternalProcedureServiceReportCommandFailureResponse class.

### ExternalProcedureServiceReportCommandSuccessRequest

The ExternalProcedureServiceReportCommandSuccessRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| id | [string](#string) |  | the System.Guid of a given running script a command has been send to. default value could not be applied: 00000000-0000-0000-0000-000000000000 |
| command\_id | [CommandId](#zen_api.em.hardware.v1.CommandId) |  | the ZenApi.EM.Hardware.V1.CommandId of a given command. |

### ExternalProcedureServiceReportCommandSuccessResponse

The ExternalProcedureServiceReportCommandSuccessResponse class.

### ExternalProcedureServiceReportInitializationErrorRequest

The ExternalProcedureServiceReportInitializationErrorRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| id | [string](#string) |  | the id as System.Guid of the external procedure. default value could not be applied: 00000000-0000-0000-0000-000000000000 |
| error\_message | [string](#string) |  | a System.String error message. |

### ExternalProcedureServiceReportInitializationErrorResponse

The ExternalProcedureServiceReportInitializationErrorResponse class.

### ExternalProcedureServiceReportProgressRequest

The ExternalProcedureServiceReportProgressRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| id | [string](#string) |  | the id as System.Guid of the external procedure. default value could not be applied: 00000000-0000-0000-0000-000000000000 |
| progress | [double](#double) |  | The progress to be reported i the range [0, 1]. Alternatively, -1 for undetermined progress. |

### ExternalProcedureServiceReportProgressResponse

The ExternalProcedureServiceReportProgressResponse class.

### ExternalProcedureServiceReportReadyRequest

The ExternalProcedureServiceReportReadyRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| id | [string](#string) |  | the id as System.Guid of the external procedure. default value could not be applied: 00000000-0000-0000-0000-000000000000 |
| error\_message | [string](#string) |  | a nullable System.String to report an error during the execution of the last run. |

### ExternalProcedureServiceReportReadyResponse

The ExternalProcedureServiceReportReadyResponse class.

### ExternalProcedureServiceReportStatusRequest

The ExternalProcedureServiceReportStatusRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| id | [string](#string) |  | the id as System.Guid of the external procedure. default value could not be applied: 00000000-0000-0000-0000-000000000000 |
| message | [string](#string) |  | the System.String to be reported. |

### ExternalProcedureServiceReportStatusResponse

The ExternalProcedureServiceReportStatusResponse class.

### ExternalProcedureService

The IExternalProcedureService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | RegisterExternalProcedure | [ExternalProcedureServiceRegisterExternalProcedureRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceRegisterExternalProcedureRequest) | [ExternalProcedureServiceRegisterExternalProcedureResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceRegisterExternalProcedureResponse) stream | Registers the caller to get notified about ZenApi.EM.Hardware.V1.ExternalProcedureServiceRegisterExternalProcedureResponse's (for all external procedures; filtering must be done by the caller). |
|  | ReportCommandFailure | [ExternalProcedureServiceReportCommandFailureRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceReportCommandFailureRequest) | [ExternalProcedureServiceReportCommandFailureResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceReportCommandFailureResponse) | Reports the failure of execution of the given ZenApi.EM.Hardware.V1.ExternalProcedureServiceRegisterExternalProcedureResponse. |
|  | ReportCommandSuccess | [ExternalProcedureServiceReportCommandSuccessRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceReportCommandSuccessRequest) | [ExternalProcedureServiceReportCommandSuccessResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceReportCommandSuccessResponse) | Reports the successful execution of the given ZenApi.EM.Hardware.V1.ExternalProcedureServiceRegisterExternalProcedureResponse. |
|  | ReportInitializationError | [ExternalProcedureServiceReportInitializationErrorRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceReportInitializationErrorRequest) | [ExternalProcedureServiceReportInitializationErrorResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceReportInitializationErrorResponse) | Reports an error that has occurred during the initialization of an external procedure, leads to error state. |
|  | ReportProgress | [ExternalProcedureServiceReportProgressRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceReportProgressRequest) | [ExternalProcedureServiceReportProgressResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceReportProgressResponse) | reports the progress of the external procedure with the given id. |
|  | ReportReady | [ExternalProcedureServiceReportReadyRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceReportReadyRequest) | [ExternalProcedureServiceReportReadyResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceReportReadyResponse) | Reports, that the external procedure with the given id is ready to be executed. |
|  | ReportStatus | [ExternalProcedureServiceReportStatusRequest](#zen_api.em.hardware.v1.ExternalProcedureServiceReportStatusRequest) | [ExternalProcedureServiceReportStatusResponse](#zen_api.em.hardware.v1.ExternalProcedureServiceReportStatusResponse) | reports a status message to zen. |

## zen\_api/em/hardware/v1/illumination\_service.proto

[Top](#title)

### IlluminationServiceGetIlluminationIRRequest

The IlluminationServiceGetIlluminationIRRequest class.

### IlluminationServiceGetIlluminationIRResponse

Response object for the illuminator get illumination IR.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| illumination\_ir | [double](#double) |  | The illumination IR. |

### IlluminationServiceGetIlluminationWhiteRequest

The IlluminationServiceGetIlluminationWhiteRequest class.

### IlluminationServiceGetIlluminationWhiteResponse

Response object for the illuminator get illumination white.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| illumination\_white | [double](#double) |  | The illumination white. |

### IlluminationServiceRegisterOnIlluminationIRChangedRequest

The IlluminationServiceRegisterOnIlluminationIRChangedRequest class.

### IlluminationServiceRegisterOnIlluminationIRChangedResponse

Response object for register on illumination IR changed.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| illumination\_ir | [double](#double) |  | The illumination IR. |

### IlluminationServiceRegisterOnIlluminationWhiteChangedRequest

The IlluminationServiceRegisterOnIlluminationWhiteChangedRequest class.

### IlluminationServiceRegisterOnIlluminationWhiteChangedResponse

Response object for register on illumination white changed.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| illumination\_white | [double](#double) |  | The illumination white. |

### IlluminationServiceSetIlluminationIRRequest

The IlluminationServiceSetIlluminationIRRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| illumination\_ir | [double](#double) |  | The illumination IR value to set [0..100]%. |

### IlluminationServiceSetIlluminationIRResponse

Response object for the illuminator set illumination IR.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| illumination\_ir | [double](#double) |  | The illumination IR. |
| success | [bool](#bool) |  | A value indicating whether setting the brightness was successful. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### IlluminationServiceSetIlluminationWhiteRequest

The IlluminationServiceSetIlluminationWhiteRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| illumination\_white | [double](#double) |  | The illumination white value to set [0..100]%. |

### IlluminationServiceSetIlluminationWhiteResponse

Response object for the illuminator set illumination white.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| illumination\_white | [double](#double) |  | The illumination white. |
| success | [bool](#bool) |  | A value indicating whether setting the brightness was successful. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### IlluminationService

The IIlluminationService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetIlluminationIR | [IlluminationServiceGetIlluminationIRRequest](#zen_api.em.hardware.v1.IlluminationServiceGetIlluminationIRRequest) | [IlluminationServiceGetIlluminationIRResponse](#zen_api.em.hardware.v1.IlluminationServiceGetIlluminationIRResponse) | Gets the illumination IR value. Returns the current illumination IR value [0..100]%. |
|  | GetIlluminationWhite | [IlluminationServiceGetIlluminationWhiteRequest](#zen_api.em.hardware.v1.IlluminationServiceGetIlluminationWhiteRequest) | [IlluminationServiceGetIlluminationWhiteResponse](#zen_api.em.hardware.v1.IlluminationServiceGetIlluminationWhiteResponse) | Gets the illumination white value. Returns the current illumination white value [0..100]%. |
|  | RegisterOnIlluminationIRChanged | [IlluminationServiceRegisterOnIlluminationIRChangedRequest](#zen_api.em.hardware.v1.IlluminationServiceRegisterOnIlluminationIRChangedRequest) | [IlluminationServiceRegisterOnIlluminationIRChangedResponse](#zen_api.em.hardware.v1.IlluminationServiceRegisterOnIlluminationIRChangedResponse) stream | Registers a subscriber on illumination IR changes. returns the current illumination IR value [0..100]%. |
|  | RegisterOnIlluminationWhiteChanged | [IlluminationServiceRegisterOnIlluminationWhiteChangedRequest](#zen_api.em.hardware.v1.IlluminationServiceRegisterOnIlluminationWhiteChangedRequest) | [IlluminationServiceRegisterOnIlluminationWhiteChangedResponse](#zen_api.em.hardware.v1.IlluminationServiceRegisterOnIlluminationWhiteChangedResponse) stream | Registers a subscriber on illumination white changes. Returns the current illumination white value [0..100]%. |
|  | SetIlluminationIR | [IlluminationServiceSetIlluminationIRRequest](#zen_api.em.hardware.v1.IlluminationServiceSetIlluminationIRRequest) | [IlluminationServiceSetIlluminationIRResponse](#zen_api.em.hardware.v1.IlluminationServiceSetIlluminationIRResponse) | Sets the illumination IR value. Returns the current illumination IR value [0..100]%. |
|  | SetIlluminationWhite | [IlluminationServiceSetIlluminationWhiteRequest](#zen_api.em.hardware.v1.IlluminationServiceSetIlluminationWhiteRequest) | [IlluminationServiceSetIlluminationWhiteResponse](#zen_api.em.hardware.v1.IlluminationServiceSetIlluminationWhiteResponse) | Sets the illumination white value. Returns the current illumination white value [0..100]%. |

## zen\_api/em/hardware/v1/simple\_acquisition\_service.proto

[Top](#title)

### SimpleAcquisitionServiceAcquireExtendedSingleFrameRequest

The SimpleAcquisitionServiceAcquireExtendedSingleFrameRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| settings | [ExtendedAcquisitionSettings](#zen_api.em.hardware.v1.ExtendedAcquisitionSettings) |  | The imaging settings used to acquire a frame. |

### SimpleAcquisitionServiceAcquireExtendedSingleFrameResponse

Response object of the AcquireExtendedSingleFrame method of the ZenApi.EM.Hardware.V1.ISimpleAcquisitionApi.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to initialize the stage succeeded or not. |
| width | [int32](#int32) |  | The width in pixels of the image. |
| height | [int32](#int32) |  | The height in pixels of the image. |
| image\_data | [bytes](#bytes) |  | The image raw data, 1 frame. Frame data as 16 bit per pixel, #pixels = ZenApi.EM.Hardware.V1.SimpleAcquisitionServiceAcquireExtendedSingleFrameResponse.Width \* ZenApi.EM.Hardware.V1.SimpleAcquisitionServiceAcquireExtendedSingleFrameResponse.Height. Total length in byte = #pixels \* 2. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### SimpleAcquisitionServiceAcquireSingleFrameRequest

The SimpleAcquisitionServiceAcquireSingleFrameRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| settings | [AcquisitionSettings](#zen_api.em.hardware.v1.AcquisitionSettings) |  | The imaging settings used to acquire a frame. |

### SimpleAcquisitionServiceAcquireSingleFrameResponse

Response object of the AcquireSingleFrame method of the ZenApi.EM.Hardware.V1.ISimpleAcquisitionApi.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to initialize the stage succeeded or not. |
| width | [int32](#int32) |  | The width in pixels of the image. |
| height | [int32](#int32) |  | The height in pixels of the image. |
| image\_data | [bytes](#bytes) |  | The image raw data, 1 frame. Frame data as 16 bit per pixel, #pixels = ZenApi.EM.Hardware.V1.SimpleAcquisitionServiceAcquireSingleFrameResponse.Width \* ZenApi.EM.Hardware.V1.SimpleAcquisitionServiceAcquireSingleFrameResponse.Height. Total length in byte = #pixels \* 2. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### SimpleAcquisitionServiceChangeDwellTimeRequest

The SimpleAcquisitionServiceChangeDwellTimeRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| dwell\_seconds | [double](#double) |  | The new dwell time in seconds. Must be in [25e-9, 107] and only multiples of 25e-9s are supported. |

### SimpleAcquisitionServiceChangeDwellTimeResponse

Response object representing the current acquisition status.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to initialize the stage succeeded or not. |

### SimpleAcquisitionServiceGetAcquisitionStatusRequest

The SimpleAcquisitionServiceGetAcquisitionStatusRequest class.

### SimpleAcquisitionServiceGetAcquisitionStatusResponse

Response object representing the current acquisition status.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| status | [AcquisitionStatus](#zen_api.em.hardware.v1.AcquisitionStatus) |  | A value indicating whether the task to initialize the stage succeeded or not. |

### SimpleAcquisitionServiceGetBrightnessRequest

The SimpleAcquisitionServiceGetBrightnessRequest class.

### SimpleAcquisitionServiceGetBrightnessResponse

Response object representing a detector brightness value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| brightness | [double](#double) |  | The brightness in percentage [0, 100]. |

### SimpleAcquisitionServiceGetContrastRequest

The SimpleAcquisitionServiceGetContrastRequest class.

### SimpleAcquisitionServiceGetContrastResponse

Response object representing a detector contrast value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| contrast | [double](#double) |  | The contrast in percentage [0, 100]. |

### SimpleAcquisitionServiceRegisterOnAcquisitionStatusChangedRequest

The SimpleAcquisitionServiceRegisterOnAcquisitionStatusChangedRequest class.

### SimpleAcquisitionServiceRegisterOnAcquisitionStatusChangedResponse

Response object representing the current acquisition status.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| status | [AcquisitionStatus](#zen_api.em.hardware.v1.AcquisitionStatus) |  | A value indicating whether the task to initialize the stage succeeded or not. |

### SimpleAcquisitionServiceSetBrightnessRequest

The SimpleAcquisitionServiceSetBrightnessRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| brightness | [double](#double) |  | The brightness value to apply in percentage [0, 1]. |

### SimpleAcquisitionServiceSetBrightnessResponse

Response object representing a detector brightness value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| brightness | [double](#double) |  | The brightness in percentage [0, 100]. |

### SimpleAcquisitionServiceSetContrastRequest

The SimpleAcquisitionServiceSetContrastRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| contrast | [double](#double) |  | The contrast value to apply in percentage [0, 1]. |

### SimpleAcquisitionServiceSetContrastResponse

Response object representing a detector contrast value.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| contrast | [double](#double) |  | The contrast in percentage [0, 100]. |

### SimpleAcquisitionServiceStartExtendedLiveAcquisitionRequest

The SimpleAcquisitionServiceStartExtendedLiveAcquisitionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| settings | [ExtendedAcquisitionSettings](#zen_api.em.hardware.v1.ExtendedAcquisitionSettings) |  | The imaging settings used to acquire multiple frames. |

### SimpleAcquisitionServiceStartExtendedLiveAcquisitionResponse

Response object of the StartExtendedLiveAcquisition method of the ZenApi.EM.Hardware.V1.ISimpleAcquisitionApi.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to acquire an image succeeded or not. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### SimpleAcquisitionServiceStartLiveAcquisitionRequest

The SimpleAcquisitionServiceStartLiveAcquisitionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| settings | [AcquisitionSettings](#zen_api.em.hardware.v1.AcquisitionSettings) |  | The imaging settings used to acquire multiple frames. |

### SimpleAcquisitionServiceStartLiveAcquisitionResponse

Response object of the StartLiveAcquisition method of the ZenApi.EM.Hardware.V1.ISimpleAcquisitionApi.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to acquire an image succeeded or not. |
| message | [string](#string) |  | A string message for display to the customer in failure case. This is only for display purpose and the message may change. Empty string on success. |

### SimpleAcquisitionServiceStopLiveAcquisitionRequest

The SimpleAcquisitionServiceStopLiveAcquisitionRequest class.

### SimpleAcquisitionServiceStopLiveAcquisitionResponse

The SimpleAcquisitionServiceStopLiveAcquisitionResponse class.

### SimpleAcquisitionService

The ISimpleAcquisitionService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | AcquireExtendedSingleFrame | [SimpleAcquisitionServiceAcquireExtendedSingleFrameRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceAcquireExtendedSingleFrameRequest) | [SimpleAcquisitionServiceAcquireExtendedSingleFrameResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceAcquireExtendedSingleFrameResponse) | Call to start single channel acquisition of a single frame with given settings. The task returned represents the ongoing acquisition. The resulting image is send once the acquisition completed. |
|  | AcquireSingleFrame | [SimpleAcquisitionServiceAcquireSingleFrameRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceAcquireSingleFrameRequest) | [SimpleAcquisitionServiceAcquireSingleFrameResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceAcquireSingleFrameResponse) | Call to start single channel acquisition of a single frame with given settings. The task returned represents the ongoing acquisition. The resulting image is send once the acquisition completed. |
|  | ChangeDwellTime | [SimpleAcquisitionServiceChangeDwellTimeRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceChangeDwellTimeRequest) | [SimpleAcquisitionServiceChangeDwellTimeResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceChangeDwellTimeResponse) | Changes the dwell time for any ongoing acquisition task. |
|  | GetAcquisitionStatus | [SimpleAcquisitionServiceGetAcquisitionStatusRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceGetAcquisitionStatusRequest) | [SimpleAcquisitionServiceGetAcquisitionStatusResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceGetAcquisitionStatusResponse) | Retrieves the current state of the acquisition hardware. Allows to deduce if the hardware is available for a new acquisition, is blocked by some other task, or acquires currently images. |
|  | GetBrightness | [SimpleAcquisitionServiceGetBrightnessRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceGetBrightnessRequest) | [SimpleAcquisitionServiceGetBrightnessResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceGetBrightnessResponse) | Retrieves the brightness value applied to a specific detector in percentage. |
|  | GetContrast | [SimpleAcquisitionServiceGetContrastRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceGetContrastRequest) | [SimpleAcquisitionServiceGetContrastResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceGetContrastResponse) | Retrieves the contrast value applied to a specific detector in percentage. |
|  | RegisterOnAcquisitionStatusChanged | [SimpleAcquisitionServiceRegisterOnAcquisitionStatusChangedRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceRegisterOnAcquisitionStatusChangedRequest) | [SimpleAcquisitionServiceRegisterOnAcquisitionStatusChangedResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceRegisterOnAcquisitionStatusChangedResponse) stream | Subscribes to acquisition status changed events. |
|  | SetBrightness | [SimpleAcquisitionServiceSetBrightnessRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceSetBrightnessRequest) | [SimpleAcquisitionServiceSetBrightnessResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceSetBrightnessResponse) | Applies a brightness value to a specified detector. The brightness value is applied immediately and has to be in [0, 1]. |
|  | SetContrast | [SimpleAcquisitionServiceSetContrastRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceSetContrastRequest) | [SimpleAcquisitionServiceSetContrastResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceSetContrastResponse) | Applies a contrast value to a specified detector. The contrast value is applied immediately and has to be in [0, 1]. |
|  | StartExtendedLiveAcquisition | [SimpleAcquisitionServiceStartExtendedLiveAcquisitionRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceStartExtendedLiveAcquisitionRequest) | [SimpleAcquisitionServiceStartExtendedLiveAcquisitionResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceStartExtendedLiveAcquisitionResponse) | This starts a live single channel acquisition with the given settings. |
|  | StartLiveAcquisition | [SimpleAcquisitionServiceStartLiveAcquisitionRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceStartLiveAcquisitionRequest) | [SimpleAcquisitionServiceStartLiveAcquisitionResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceStartLiveAcquisitionResponse) | This starts a live single channel acquisition with the given settings. |
|  | StopLiveAcquisition | [SimpleAcquisitionServiceStopLiveAcquisitionRequest](#zen_api.em.hardware.v1.SimpleAcquisitionServiceStopLiveAcquisitionRequest) | [SimpleAcquisitionServiceStopLiveAcquisitionResponse](#zen_api.em.hardware.v1.SimpleAcquisitionServiceStopLiveAcquisitionResponse) | Stops any ongoing live acquisition. Has only an effect if ZenApi.EM.Hardware.V1.ISimpleAcquisitionApi.GetAcquisitionStatus returns ZenApi.EM.Hardware.V1.AcquisitionStatus.LiveRunning. |

## zen\_api/em/hardware/v1/specimen\_current\_monitor\_service.proto

[Top](#title)

### SpecimenCurrentMonitorServiceGetSpecimenCurrentRequest

The SpecimenCurrentMonitorServiceGetSpecimenCurrentRequest class.

### SpecimenCurrentMonitorServiceGetSpecimenCurrentResponse

Response object for specimen current.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| current | [double](#double) |  | The specimen current value in amperes. |

### SpecimenCurrentMonitorServiceRegisterOnSpecimenCurrentChangedRequest

The SpecimenCurrentMonitorServiceRegisterOnSpecimenCurrentChangedRequest class.

### SpecimenCurrentMonitorServiceRegisterOnSpecimenCurrentChangedResponse

Response object for specimen current changed notification.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| current | [double](#double) |  | The specimen current value in amperes. |

### SpecimenCurrentMonitorService

The ISpecimenCurrentMonitorService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetSpecimenCurrent | [SpecimenCurrentMonitorServiceGetSpecimenCurrentRequest](#zen_api.em.hardware.v1.SpecimenCurrentMonitorServiceGetSpecimenCurrentRequest) | [SpecimenCurrentMonitorServiceGetSpecimenCurrentResponse](#zen_api.em.hardware.v1.SpecimenCurrentMonitorServiceGetSpecimenCurrentResponse) | Gets the current specimen current in amperes. |
|  | RegisterOnSpecimenCurrentChanged | [SpecimenCurrentMonitorServiceRegisterOnSpecimenCurrentChangedRequest](#zen_api.em.hardware.v1.SpecimenCurrentMonitorServiceRegisterOnSpecimenCurrentChangedRequest) | [SpecimenCurrentMonitorServiceRegisterOnSpecimenCurrentChangedResponse](#zen_api.em.hardware.v1.SpecimenCurrentMonitorServiceRegisterOnSpecimenCurrentChangedResponse) stream | Register on specimen current changed events. |

## zen\_api/em/hardware/v1/stage\_backlash\_mode.proto

[Top](#title)

### StageBacklashMode

Stage backlash mode enumeration.

| Name | Number | Description |
| --- | --- | --- |
| STAGE\_BACKLASH\_MODE\_UNSPECIFIED | 0 | Unknown indicates that this variable hasn't been assigned yet. |
| STAGE\_BACKLASH\_MODE\_DISABLED | 1 | Stage backlash is disabled. |
| STAGE\_BACKLASH\_MODE\_POSITIVE | 2 | Stage backlash is enabled in the positive direction. |
| STAGE\_BACKLASH\_MODE\_NEGATIVE | 3 | Stage backlash is enabled in the negative direction. |
| STAGE\_BACKLASH\_MODE\_BOTH\_DIRECTIONS\_POSITIVE | 4 | Stage backlash is positive in both positive and negative directions. |
| STAGE\_BACKLASH\_MODE\_BOTH\_DIRECTIONS\_NEGATIVE | 5 | Stage backlash is negative in both directions. |

## zen\_api/em/hardware/v1/vacuum\_mode.proto

[Top](#title)

### VacuumMode

Possible vacuum modes supported by our tools.

| Name | Number | Description |
| --- | --- | --- |
| VACUUM\_MODE\_UNSPECIFIED | 0 | Default enum value. |
| VACUUM\_MODE\_HIGH\_VACUUM | 1 | Standard vacuum mode is ZenApi.EM.Hardware.V1.VacuumMode.HighVacuum. Target chamber pressure can not be adjusted. |
| VACUUM\_MODE\_VARIABLE\_PRESSURE | 2 | The optional ZenApi.EM.Hardware.V1.VacuumMode.VariablePressure mode allows to specify a target chamber pressure. |

## zen\_api/em/hardware/v1/vacuum\_service.proto

[Top](#title)

### VacuumServiceCloseValveRequest

The VacuumServiceCloseValveRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| valve | [Valve](#zen_api.em.hardware.v1.Valve) |  | The valve identifier of the valve to close. |

### VacuumServiceCloseValveResponse

Response object of ZenApi.EM.Hardware.V1.IVacuumApi.CloseValve(ZenApi.EM.Hardware.V1.Valve,System.Threading.CancellationToken) method.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to close a valve succeeded or not. |

### VacuumServiceGetAvailableVacuumModesRequest

The VacuumServiceGetAvailableVacuumModesRequest class.

### VacuumServiceGetAvailableVacuumModesResponse

AvailableVacuumModes enum collection response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| available\_modes | [VacuumMode](#zen_api.em.hardware.v1.VacuumMode) | repeated |  |

### VacuumServiceGetAvailableValvesRequest

The VacuumServiceGetAvailableValvesRequest class.

### VacuumServiceGetAvailableValvesResponse

AvailableValves enum collection response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| available\_valves | [Valve](#zen_api.em.hardware.v1.Valve) | repeated |  |

### VacuumServiceGetChamberPressureRequest

The VacuumServiceGetChamberPressureRequest class.

### VacuumServiceGetChamberPressureResponse

Response to represent the chamber pressure.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| pressure | [double](#double) |  | The chamber pressure in [pascal]. |

### VacuumServiceGetTargetChamberPressureRequest

The VacuumServiceGetTargetChamberPressureRequest class.

### VacuumServiceGetTargetChamberPressureResponse

Response to represent the chamber pressure.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| pressure | [double](#double) |  | The chamber pressure in [pascal]. |

### VacuumServiceGetVacuumModeRequest

The VacuumServiceGetVacuumModeRequest class.

### VacuumServiceGetVacuumModeResponse

VacuumMode enum response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| mode | [VacuumMode](#zen_api.em.hardware.v1.VacuumMode) |  | The vacuum mode. |

### VacuumServiceGetVacuumStateRequest

The VacuumServiceGetVacuumStateRequest class.

### VacuumServiceGetVacuumStateResponse

VacuumState enum response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| state | [VacuumState](#zen_api.em.hardware.v1.VacuumState) |  | The vacuum state. |

### VacuumServiceGetValveStateRequest

The VacuumServiceGetValveStateRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| valve | [Valve](#zen_api.em.hardware.v1.Valve) |  | The valve to get the status of. |

### VacuumServiceGetValveStateResponse

ValveState enum response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| valve | [Valve](#zen_api.em.hardware.v1.Valve) |  | The valve identifier. |
| state | [ValveState](#zen_api.em.hardware.v1.ValveState) |  | The valves state. |

### VacuumServiceOpenValveRequest

The VacuumServiceOpenValveRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| valve | [Valve](#zen_api.em.hardware.v1.Valve) |  | The valve identifier of the valve to open. |

### VacuumServiceOpenValveResponse

Response object of ZenApi.EM.Hardware.V1.IVacuumApi.OpenValve(ZenApi.EM.Hardware.V1.Valve,System.Threading.CancellationToken) method.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to open a valve succeeded or not. |

### VacuumServicePumpRequest

The VacuumServicePumpRequest class.

### VacuumServicePumpResponse

Response object of the ZenApi.EM.Hardware.V1.IVacuumApi.Pump(System.Threading.CancellationToken) method.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to pump the chamber succeeded or not. |

### VacuumServiceRegisterOnChamberPressureChangedRequest

The VacuumServiceRegisterOnChamberPressureChangedRequest class.

### VacuumServiceRegisterOnChamberPressureChangedResponse

Response to represent the chamber pressure.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| pressure | [double](#double) |  | The chamber pressure in [pascal]. |

### VacuumServiceRegisterOnTargetChamberPressureChangedRequest

The VacuumServiceRegisterOnTargetChamberPressureChangedRequest class.

### VacuumServiceRegisterOnTargetChamberPressureChangedResponse

Response to represent the chamber pressure.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| pressure | [double](#double) |  | The chamber pressure in [pascal]. |

### VacuumServiceRegisterOnVacuumModeChangedRequest

The VacuumServiceRegisterOnVacuumModeChangedRequest class.

### VacuumServiceRegisterOnVacuumModeChangedResponse

VacuumMode enum response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| mode | [VacuumMode](#zen_api.em.hardware.v1.VacuumMode) |  | The vacuum mode. |

### VacuumServiceRegisterOnVacuumStateChangedRequest

The VacuumServiceRegisterOnVacuumStateChangedRequest class.

### VacuumServiceRegisterOnVacuumStateChangedResponse

VacuumState enum response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| state | [VacuumState](#zen_api.em.hardware.v1.VacuumState) |  | The vacuum state. |

### VacuumServiceRegisterOnValveStateChangedRequest

The VacuumServiceRegisterOnValveStateChangedRequest class.

### VacuumServiceRegisterOnValveStateChangedResponse

ValveState enum response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| valve | [Valve](#zen_api.em.hardware.v1.Valve) |  | The valve identifier. |
| state | [ValveState](#zen_api.em.hardware.v1.ValveState) |  | The valves state. |

### VacuumServiceSetTargetChamberPressureRequest

The VacuumServiceSetTargetChamberPressureRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| target\_pressure | [double](#double) |  | The target chamber pressure if in ZenApi.EM.Hardware.V1.VacuumMode.VariablePressure mode in [pascal]. |

### VacuumServiceSetTargetChamberPressureResponse

Response object of the ZenApi.EM.Hardware.V1.IVacuumApi.SetTargetChamberPressure(System.Double,System.Threading.CancellationToken) method.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to set the chamber pressure succeeded or not. |

### VacuumServiceSetVacuumModeRequest

The VacuumServiceSetVacuumModeRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| mode | [VacuumMode](#zen_api.em.hardware.v1.VacuumMode) |  | The ZenApi.EM.Hardware.V1.VacuumMode to apply. |

### VacuumServiceSetVacuumModeResponse

Response object of the ZenApi.EM.Hardware.V1.IVacuumApi.SetVacuumMode(ZenApi.EM.Hardware.V1.VacuumMode,System.Threading.CancellationToken) method.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to set the vacuum mode succeeded or not. |

### VacuumServiceVentRequest

The VacuumServiceVentRequest class.

### VacuumServiceVentResponse

Response object of ZenApi.EM.Hardware.V1.IVacuumApi.Vent(System.Threading.CancellationToken) method.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to vent the chamber succeeded or not. |

### VacuumService

The IVacuumService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | CloseValve | [VacuumServiceCloseValveRequest](#zen_api.em.hardware.v1.VacuumServiceCloseValveRequest) | [VacuumServiceCloseValveResponse](#zen_api.em.hardware.v1.VacuumServiceCloseValveResponse) | Closes a valve on the system. |
|  | GetAvailableVacuumModes | [VacuumServiceGetAvailableVacuumModesRequest](#zen_api.em.hardware.v1.VacuumServiceGetAvailableVacuumModesRequest) | [VacuumServiceGetAvailableVacuumModesResponse](#zen_api.em.hardware.v1.VacuumServiceGetAvailableVacuumModesResponse) | Retrieves a collection of available vacuum modes, like HV and VP. Available modes depend on the tool configuration and don't change during runtime. Note: TargetChamberPressure functionality is only working for VP mode. |
|  | GetAvailableValves | [VacuumServiceGetAvailableValvesRequest](#zen_api.em.hardware.v1.VacuumServiceGetAvailableValvesRequest) | [VacuumServiceGetAvailableValvesResponse](#zen_api.em.hardware.v1.VacuumServiceGetAvailableValvesResponse) | Retrieves all available valves of the system that can be controlled. Possible values are listed in ZenApi.EM.Hardware.V1.Valve enumeration. |
|  | GetChamberPressure | [VacuumServiceGetChamberPressureRequest](#zen_api.em.hardware.v1.VacuumServiceGetChamberPressureRequest) | [VacuumServiceGetChamberPressureResponse](#zen_api.em.hardware.v1.VacuumServiceGetChamberPressureResponse) | Retrieves the current chamber pressure in [pascal]. |
|  | GetTargetChamberPressure | [VacuumServiceGetTargetChamberPressureRequest](#zen_api.em.hardware.v1.VacuumServiceGetTargetChamberPressureRequest) | [VacuumServiceGetTargetChamberPressureResponse](#zen_api.em.hardware.v1.VacuumServiceGetTargetChamberPressureResponse) | Retrieves the target chamber pressure for ZenApi.EM.Hardware.V1.VacuumMode.VariablePressure mode. Unspecified return value on non VP configurations. |
|  | GetVacuumMode | [VacuumServiceGetVacuumModeRequest](#zen_api.em.hardware.v1.VacuumServiceGetVacuumModeRequest) | [VacuumServiceGetVacuumModeResponse](#zen_api.em.hardware.v1.VacuumServiceGetVacuumModeResponse) | Retrieves the currently active Vacuum Mode. |
|  | GetVacuumState | [VacuumServiceGetVacuumStateRequest](#zen_api.em.hardware.v1.VacuumServiceGetVacuumStateRequest) | [VacuumServiceGetVacuumStateResponse](#zen_api.em.hardware.v1.VacuumServiceGetVacuumStateResponse) | Retrieves the current vacuum state. |
|  | GetValveState | [VacuumServiceGetValveStateRequest](#zen_api.em.hardware.v1.VacuumServiceGetValveStateRequest) | [VacuumServiceGetValveStateResponse](#zen_api.em.hardware.v1.VacuumServiceGetValveStateResponse) | Retrieves the current state of a valve. Only states of available valves are defined. See ZenApi.EM.Hardware.V1.IVacuumApi.GetAvailableValves. |
|  | OpenValve | [VacuumServiceOpenValveRequest](#zen_api.em.hardware.v1.VacuumServiceOpenValveRequest) | [VacuumServiceOpenValveResponse](#zen_api.em.hardware.v1.VacuumServiceOpenValveResponse) | Opens a valve on the system. |
|  | Pump | [VacuumServicePumpRequest](#zen_api.em.hardware.v1.VacuumServicePumpRequest) | [VacuumServicePumpResponse](#zen_api.em.hardware.v1.VacuumServicePumpResponse) | Starts the pumping process to evacuate the chamber and install a stable vacuum. |
|  | RegisterOnChamberPressureChanged | [VacuumServiceRegisterOnChamberPressureChangedRequest](#zen_api.em.hardware.v1.VacuumServiceRegisterOnChamberPressureChangedRequest) | [VacuumServiceRegisterOnChamberPressureChangedResponse](#zen_api.em.hardware.v1.VacuumServiceRegisterOnChamberPressureChangedResponse) stream | Notifications on chamber pressure. Events are fired every time the current chamber pressure changes. |
|  | RegisterOnTargetChamberPressureChanged | [VacuumServiceRegisterOnTargetChamberPressureChangedRequest](#zen_api.em.hardware.v1.VacuumServiceRegisterOnTargetChamberPressureChangedRequest) | [VacuumServiceRegisterOnTargetChamberPressureChangedResponse](#zen_api.em.hardware.v1.VacuumServiceRegisterOnTargetChamberPressureChangedResponse) stream | Notifications about changes to the target chamber pressure value. Only enabled on systems supporting ZenApi.EM.Hardware.V1.VacuumMode.VariablePressure mode. |
|  | RegisterOnVacuumModeChanged | [VacuumServiceRegisterOnVacuumModeChangedRequest](#zen_api.em.hardware.v1.VacuumServiceRegisterOnVacuumModeChangedRequest) | [VacuumServiceRegisterOnVacuumModeChangedResponse](#zen_api.em.hardware.v1.VacuumServiceRegisterOnVacuumModeChangedResponse) stream | Notification about changes of the active vacuum mode. See ZenApi.EM.Hardware.V1.VacuumMode. |
|  | RegisterOnVacuumStateChanged | [VacuumServiceRegisterOnVacuumStateChangedRequest](#zen_api.em.hardware.v1.VacuumServiceRegisterOnVacuumStateChangedRequest) | [VacuumServiceRegisterOnVacuumStateChangedResponse](#zen_api.em.hardware.v1.VacuumServiceRegisterOnVacuumStateChangedResponse) stream | Notification about changes of the vacuum system state. See ZenApi.EM.Hardware.V1.VacuumState. |
|  | RegisterOnValveStateChanged | [VacuumServiceRegisterOnValveStateChangedRequest](#zen_api.em.hardware.v1.VacuumServiceRegisterOnValveStateChangedRequest) | [VacuumServiceRegisterOnValveStateChangedResponse](#zen_api.em.hardware.v1.VacuumServiceRegisterOnValveStateChangedResponse) stream | Notifications about any valves state changes. |
|  | SetTargetChamberPressure | [VacuumServiceSetTargetChamberPressureRequest](#zen_api.em.hardware.v1.VacuumServiceSetTargetChamberPressureRequest) | [VacuumServiceSetTargetChamberPressureResponse](#zen_api.em.hardware.v1.VacuumServiceSetTargetChamberPressureResponse) | Sets and if in ZenApi.EM.Hardware.V1.VacuumMode.VariablePressure also applies a new chamber pressure. |
|  | SetVacuumMode | [VacuumServiceSetVacuumModeRequest](#zen_api.em.hardware.v1.VacuumServiceSetVacuumModeRequest) | [VacuumServiceSetVacuumModeResponse](#zen_api.em.hardware.v1.VacuumServiceSetVacuumModeResponse) | Sets the active vacuum mode. No op if the vacuum mode does not change, otherwise the process to switch to the other vacuum mode is initiated. |
|  | Vent | [VacuumServiceVentRequest](#zen_api.em.hardware.v1.VacuumServiceVentRequest) | [VacuumServiceVentResponse](#zen_api.em.hardware.v1.VacuumServiceVentResponse) | Starts the venting process to vent the chamber and allow the chamber door to be opened. |

## zen\_api/em/hardware/v1/vacuum\_state.proto

[Top](#title)

### VacuumState

Possible states of the vacuum system.

TODO enum states must be reviewed by application, maybe Christian Hendrich

what is really needed on customer side, keep it simple

| Name | Number | Description |
| --- | --- | --- |
| VACUUM\_STATE\_UNSPECIFIED | 0 | Default enum value. |
| VACUUM\_STATE\_READY | 1 | Vacuum is ready. |
| VACUUM\_STATE\_NOT\_READY | 2 | Vacuum is not ready. Maybe vented, pumping, venting, ... |

## zen\_api/em/hardware/v1/valve.proto

[Top](#title)

### Valve

Enumeration of all possibles valves to control.

| Name | Number | Description |
| --- | --- | --- |
| VALVE\_UNSPECIFIED | 0 | The default enum value. |
| VALVE\_SEM\_ISOLATION\_VALVE | 1 | SEM column chamber isolation valve. |
| VALVE\_FIB\_ISOLATION\_VALVE | 2 | FIB column chamber isolation valve. |

## zen\_api/em/hardware/v1/valve\_state.proto

[Top](#title)

### ValveState

Possible states of any valve.

TODO enum states must be reviewed by application, maybe Christian Hendrich

what is really needed on customer side, keep it simple

| Name | Number | Description |
| --- | --- | --- |
| VALVE\_STATE\_UNSPECIFIED | 0 | Default enum value. |
| VALVE\_STATE\_OPEN | 1 | Valve is open. |
| VALVE\_STATE\_CLOSED | 2 | Valve is closed. |

## zen\_api/em/workflow/v1/create\_workflow\_service.proto

[Top](#title)

### CreateWorkflowServiceAddAbsoluteTiltingActionRequest

The CreateWorkflowServiceAddAbsoluteTiltingActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| tilt\_angle | [double](#double) |  | The angle in degrees to which the tilting should occur. Defaults to 0 if not specified. |

### CreateWorkflowServiceAddAbsoluteTiltingActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddAcquireNavCamImageActionRequest

The CreateWorkflowServiceAddAcquireNavCamImageActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| em\_region\_of\_interest | [EmRegionOfInterest](#zen_api.em.workflow.v1.EmRegionOfInterest) |  | An ZenApi.EM.Workflow.V1.EmRegionOfInterest object specifying the region of interest for the NavCam image acquisition. |
| file\_name | [string](#string) |  | The name of the file where the acquired NavCam image will be saved. |

### CreateWorkflowServiceAddAcquireNavCamImageActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddAcquireStoreImageActionRequest

The CreateWorkflowServiceAddAcquireStoreImageActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| em\_region\_of\_interest | [EmRegionOfInterest](#zen_api.em.workflow.v1.EmRegionOfInterest) |  | An ZenApi.EM.Workflow.V1.EmRegionOfInterest object specifying the region of interest for the image acquisition. |
| image\_key | [string](#string) |  | A unique key identifier for the image to be stored. |
| position\_name | [string](#string) |  | An optional name for the position associated with the image acquisition. Default is an empty string. |
| xoffset | [double](#double) |  | An optional X-coordinate offset for the image acquisition. Default is System.Double.NaN. |
| yoffset | [double](#double) |  | An optional Y-coordinate offset for the image acquisition. Default is System.Double.NaN. |
| file\_name | [string](#string) |  | An optional file name for storing the acquired image. Default is an empty string. |

### CreateWorkflowServiceAddAcquireStoreImageActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddChangeBeamStateActionRequest

The CreateWorkflowServiceAddChangeBeamStateActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| desired\_state | [zen\_api.em.hardware.v1.BeamState](#zen_api.em.hardware.v1.BeamState) |  | The desired state of the beam, specified as a ZenApi.EM.Hardware.V1.BeamState enumeration. |

### CreateWorkflowServiceAddChangeBeamStateActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddChangeCurrentActionRequest

The CreateWorkflowServiceAddChangeCurrentActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| target\_current | [double](#double) |  | The target current level to which the current should be adjusted. |

### CreateWorkflowServiceAddChangeCurrentActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddChangeEhtActionRequest

The CreateWorkflowServiceAddChangeEhtActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| target\_voltage | [double](#double) |  | The target voltage level to which the EHT should be changed. |

### CreateWorkflowServiceAddChangeEhtActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddEdsAcquisitionSettingsParameterActionRequest

The CreateWorkflowServiceAddEdsAcquisitionSettingsParameterActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | The unique identifier of the workflow to which the EDS acquisition settings action will be appended. |
| acquisition\_settings | [EdsSpectrumAcquisitionSettings](#zen_api.em.workflow.v1.EdsSpectrumAcquisitionSettings) |  | The EDS acquisition settings to be applied, provided as an ZenApi.EM.Workflow.V1.EdsSpectrumAcquisitionSettings interface. |

### CreateWorkflowServiceAddEdsAcquisitionSettingsParameterActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddFocusAndFovActionRequest

The CreateWorkflowServiceAddFocusAndFovActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| focus | [double](#double) |  | The focus value to be set. |
| fov | [double](#double) |  | The field of view value to be set. |
| is\_sem | [bool](#bool) |  | A boolean indicating whether the setting is for a SEM (true) or not (false). |

### CreateWorkflowServiceAddFocusAndFovActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddGoToStoredPositionActionRequest

The CreateWorkflowServiceAddGoToStoredPositionActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| id | [int32](#int32) |  | Id of the stage position stored. |

### CreateWorkflowServiceAddGoToStoredPositionActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddInitializeActionRequest

The CreateWorkflowServiceAddInitializeActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |

### CreateWorkflowServiceAddInitializeActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddMoveStageRelativeActionRequest

The CreateWorkflowServiceAddMoveStageRelativeActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| axis\_to\_move | [zen\_api.hardware.v1.StageAxis](#zen_api.hardware.v1.StageAxis) | repeated | The stage axis that should move. The position is in meters. |

### CreateWorkflowServiceAddMoveStageRelativeActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddPositionControlledTiltActionRequest

The CreateWorkflowServiceAddPositionControlledTiltActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| start\_angle | [double](#double) |  | The starting angle in degrees for the tilt action. |
| target\_angle | [double](#double) |  | The target angle in degrees the tilt action aims to reach. |
| large\_step | [double](#double) |  | The size of the large step in degrees for tilting. |
| small\_step | [double](#double) |  | The size of the small step in degrees for finer tilting adjustments. |

### CreateWorkflowServiceAddPositionControlledTiltActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddRestoreFibProbeActionRequest

The CreateWorkflowServiceAddRestoreFibProbeActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| fib\_probe\_storage\_name | [string](#string) |  | The name of the storage location from which the FIB probe state will be restored. |

### CreateWorkflowServiceAddRestoreFibProbeActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddSetFibProbeActionRequest

The CreateWorkflowServiceAddSetFibProbeActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| probe\_name | [string](#string) |  | The name of the FIB probe to be set. |

### CreateWorkflowServiceAddSetFibProbeActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddSetFibWithValuesActionRequest

The CreateWorkflowServiceAddSetFibWithValuesActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| voltage | [string](#string) |  | The voltage value to set for the FIB. |
| current | [string](#string) |  | The current value to set for the FIB. |

### CreateWorkflowServiceAddSetFibWithValuesActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddSetVacuumParameterActionRequest

The CreateWorkflowServiceAddSetVacuumParameterActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| vacuum\_parameter | [VacuumParameter](#zen_api.em.workflow.v1.VacuumParameter) |  | The vacuum parameter to be set, specified as a ZenApi.EM.Workflow.V1.VacuumParameter enumeration. |
| value | [double](#double) |  | The value to which the specified vacuum parameter should be set. |

### CreateWorkflowServiceAddSetVacuumParameterActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddSpotParameterActionRequest

The CreateWorkflowServiceAddSpotParameterActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| spot\_id | [string](#string) |  | The identifier of the spot to be configured. |
| position\_x | [double](#double) |  | The X-coordinate of the beam position for the spot. |
| position\_y | [double](#double) |  | The Y-coordinate of the beam position for the spot. |

### CreateWorkflowServiceAddSpotParameterActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddStoreFibProbeActionRequest

The CreateWorkflowServiceAddStoreFibProbeActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| fib\_probe\_storage\_name | [string](#string) |  | The name for the storage location of the FIB probe state. |

### CreateWorkflowServiceAddStoreFibProbeActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddTouchAlarmGeneratorActionRequest

The CreateWorkflowServiceAddTouchAlarmGeneratorActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| disable\_alarm | [bool](#bool) |  | A boolean indicating whether to disable (true) or enable (false) the touch alarm. |

### CreateWorkflowServiceAddTouchAlarmGeneratorActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowServiceAddVacuumCommandActionRequest

The CreateWorkflowServiceAddVacuumCommandActionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow to which action should be added. |
| command | [string](#string) |  | The vacuum command to be sent. |

### CreateWorkflowServiceAddVacuumCommandActionResponse

ActionResponse response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which was created. |

### CreateWorkflowService

The ICreateWorkflowService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | AddAbsoluteTiltingAction | [CreateWorkflowServiceAddAbsoluteTiltingActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddAbsoluteTiltingActionRequest) | [CreateWorkflowServiceAddAbsoluteTiltingActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddAbsoluteTiltingActionResponse) | Creates an absolute tilting action. |
|  | AddAcquireNavCamImageAction | [CreateWorkflowServiceAddAcquireNavCamImageActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddAcquireNavCamImageActionRequest) | [CreateWorkflowServiceAddAcquireNavCamImageActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddAcquireNavCamImageActionResponse) | Creates an action to acquire a navigation camera image for a specified region of interest in an automated engine workflow. This method generates an action for capturing a NavCam image based on the provided EM region of interest and appends it to an existing workflow. |
|  | AddAcquireStoreImageAction | [CreateWorkflowServiceAddAcquireStoreImageActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddAcquireStoreImageActionRequest) | [CreateWorkflowServiceAddAcquireStoreImageActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddAcquireStoreImageActionResponse) | Creates an action to acquire and store an image based on a specified region of interest in an automated engine workflow. This method generates an action for capturing and storing an image, including optional position and offset parameters, and appends it to an existing workflow. |
|  | AddChangeBeamStateAction | [CreateWorkflowServiceAddChangeBeamStateActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddChangeBeamStateActionRequest) | [CreateWorkflowServiceAddChangeBeamStateActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddChangeBeamStateActionResponse) | Creates an action to change the beam state in an automated engine workflow. This method generates a beam state change action based on the desired state and appends it to an existing workflow. |
|  | AddChangeCurrentAction | [CreateWorkflowServiceAddChangeCurrentActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddChangeCurrentActionRequest) | [CreateWorkflowServiceAddChangeCurrentActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddChangeCurrentActionResponse) | Creates an action to change the current level in an automated engine workflow. This method generates a current change action based on the specified target current and appends it to an existing workflow. |
|  | AddChangeEhtAction | [CreateWorkflowServiceAddChangeEhtActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddChangeEhtActionRequest) | [CreateWorkflowServiceAddChangeEhtActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddChangeEhtActionResponse) | Creates an action to change the EHT voltage in an automated engine workflow. This method generates an EHT voltage change action and appends it to an existing workflow. |
|  | AddEdsAcquisitionSettingsParameterAction | [CreateWorkflowServiceAddEdsAcquisitionSettingsParameterActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddEdsAcquisitionSettingsParameterActionRequest) | [CreateWorkflowServiceAddEdsAcquisitionSettingsParameterActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddEdsAcquisitionSettingsParameterActionResponse) | Creates an action to set Energy-Dispersive X-ray Spectroscopy (EDS) acquisition settings in an automated engine workflow. This method generates an action for configuring EDS acquisition settings and appends it to an existing workflow. |
|  | AddFocusAndFovAction | [CreateWorkflowServiceAddFocusAndFovActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddFocusAndFovActionRequest) | [CreateWorkflowServiceAddFocusAndFovActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddFocusAndFovActionResponse) | Creates an action to adjust the focus and field of view (FOV) in an automated engine workflow. This method generates an action for setting focus and FOV values, and appends it to an existing workflow. |
|  | AddGoToStoredPositionAction | [CreateWorkflowServiceAddGoToStoredPositionActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddGoToStoredPositionActionRequest) | [CreateWorkflowServiceAddGoToStoredPositionActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddGoToStoredPositionActionResponse) | Adds an action that moves the stage to a stored point. |
|  | AddInitializeAction | [CreateWorkflowServiceAddInitializeActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddInitializeActionRequest) | [CreateWorkflowServiceAddInitializeActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddInitializeActionResponse) | Add action that initializes the stage. |
|  | AddMoveStageRelativeAction | [CreateWorkflowServiceAddMoveStageRelativeActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddMoveStageRelativeActionRequest) | [CreateWorkflowServiceAddMoveStageRelativeActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddMoveStageRelativeActionResponse) | Add Move Stage Relative action to the specified workflow. The action will be added at the last position of the specified workflow. When specified workflow is not present, it will be automatically created. |
|  | AddPositionControlledTiltAction | [CreateWorkflowServiceAddPositionControlledTiltActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddPositionControlledTiltActionRequest) | [CreateWorkflowServiceAddPositionControlledTiltActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddPositionControlledTiltActionResponse) | Creates a position-controlled tilt action as part of an automated engine workflow. This method generates an action based on specified tilt angles and step sizes, and appends it to a given workflow. When specified workflow is not present, it will be automatically created. |
|  | AddRestoreFibProbeAction | [CreateWorkflowServiceAddRestoreFibProbeActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddRestoreFibProbeActionRequest) | [CreateWorkflowServiceAddRestoreFibProbeActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddRestoreFibProbeActionResponse) | Creates an action to restore the FIB probe to a previously stored state in an automated engine workflow. This method generates an action for restoring the FIB probe configuration from a named storage and appends it to an existing workflow. |
|  | AddSetFibProbeAction | [CreateWorkflowServiceAddSetFibProbeActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSetFibProbeActionRequest) | [CreateWorkflowServiceAddSetFibProbeActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSetFibProbeActionResponse) | Creates an action to set a specific FIB probe in an automated engine workflow. This method generates an action to configure the FIB system to use a specified probe and appends it to an existing workflow. |
|  | AddSetFibWithValuesAction | [CreateWorkflowServiceAddSetFibWithValuesActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSetFibWithValuesActionRequest) | [CreateWorkflowServiceAddSetFibWithValuesActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSetFibWithValuesActionResponse) | Creates an action to set the FIB with specified voltage and current values in an automated engine workflow. This method generates an action for setting the FIB parameters and appends it to an existing workflow. |
|  | AddSetVacuumParameterAction | [CreateWorkflowServiceAddSetVacuumParameterActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSetVacuumParameterActionRequest) | [CreateWorkflowServiceAddSetVacuumParameterActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSetVacuumParameterActionResponse) | Creates an action to set a specific vacuum parameter in an automated engine workflow. This method generates an action to adjust a vacuum parameter to a specified value and appends it to an existing workflow. |
|  | AddSpotParameterAction | [CreateWorkflowServiceAddSpotParameterActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSpotParameterActionRequest) | [CreateWorkflowServiceAddSpotParameterActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddSpotParameterActionResponse) | Creates an action to set parameters for a specific spot in an automated engine workflow. This method generates an action to configure a beam spot with a given ID and beam position, using specified X and Y coordinates, and appends it to an existing workflow. |
|  | AddStoreFibProbeAction | [CreateWorkflowServiceAddStoreFibProbeActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddStoreFibProbeActionRequest) | [CreateWorkflowServiceAddStoreFibProbeActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddStoreFibProbeActionResponse) | Creates an action to store the current state of the FIB probe in an automated engine workflow. This method generates an action for storing the FIB probe configuration and appends it to an existing workflow. |
|  | AddTouchAlarmGeneratorAction | [CreateWorkflowServiceAddTouchAlarmGeneratorActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddTouchAlarmGeneratorActionRequest) | [CreateWorkflowServiceAddTouchAlarmGeneratorActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddTouchAlarmGeneratorActionResponse) | Creates an action to enable or disable the touch alarm in an automated engine workflow. This method generates an action for toggling the touch alarm state and appends it to an existing workflow. |
|  | AddVacuumCommandAction | [CreateWorkflowServiceAddVacuumCommandActionRequest](#zen_api.em.workflow.v1.CreateWorkflowServiceAddVacuumCommandActionRequest) | [CreateWorkflowServiceAddVacuumCommandActionResponse](#zen_api.em.workflow.v1.CreateWorkflowServiceAddVacuumCommandActionResponse) | Creates an action to send a vacuum command in an automated engine workflow. This method generates an action for sending a specified vacuum command and appends it to an existing workflow. |

## zen\_api/em/workflow/v1/eds\_acquisition\_mode.proto

[Top](#title)

### EdsAcquisitionMode

Enum indicating the acquisition mode.

| Name | Number | Description |
| --- | --- | --- |
| EDS\_ACQUISITION\_MODE\_UNSPECIFIED | 0 | Default enum value. |
| EDS\_ACQUISITION\_MODE\_AUTO | 1 | Auto selection of acquisition mode which is Counts. Acquisition continues until enough counts are collected in the spectrum. |
| EDS\_ACQUISITION\_MODE\_LIVE\_TIME | 2 | Acquire EDS data for a period of live time. This is the time for which the system is processing counts into the spectrum. |
| EDS\_ACQUISITION\_MODE\_COUNTS | 3 | Acquisition continues until enough counts are collected in the spectrum. |

## zen\_api/em/workflow/v1/eds\_spectrum\_acquisition\_settings.proto

[Top](#title)

### EdsSpectrumAcquisitionSettings

EDS spectrum acquisition setting.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| acquisition\_counts | [int32](#int32) |  | The acquisition counts. |
| acquisition\_time | [double](#double) |  | The acquisition time in seconds. |
| acquisition\_mode | [EdsAcquisitionMode](#zen_api.em.workflow.v1.EdsAcquisitionMode) |  | A value indicating whether the acquisition mode (live time or counts). |

## zen\_api/em/workflow/v1/em\_region\_of\_interest.proto

[Top](#title)

### EmRegionOfInterest

The EM region of interest settings.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| position\_x | [double](#double) |  | The X-coordinate of the region's position. |
| position\_y | [double](#double) |  | The Y-coordinate of the region's position. |
| width | [double](#double) |  | The width of the region. |
| height | [double](#double) |  | The height of the region. |

## zen\_api/em/workflow/v1/run\_workflow\_service.proto

[Top](#title)

### RunWorkflowServiceBreakRequest

The RunWorkflowServiceBreakRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| break\_elements | [string](#string) |  | List of elements, that shall be skipped. |

### RunWorkflowServiceBreakResponse

The RunWorkflowServiceBreakResponse class.

### RunWorkflowServiceDefineAndRunCompleteWorkflowRequest

The RunWorkflowServiceDefineAndRunCompleteWorkflowRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_definition | [string](#string) |  | Complete and consistent definition of the workflow which should be executed. |

### RunWorkflowServiceDefineAndRunCompleteWorkflowResponse

Response object of the RunWorkflow method.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to run workflow succeeded or not. |

### RunWorkflowServiceGetWorkflowByIdRequest

The RunWorkflowServiceGetWorkflowByIdRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow which should be returned. |

### RunWorkflowServiceGetWorkflowByIdResponse

Response object of the GetWorkflow method.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow | [string](#string) |  | A value with workflow xml. |

### RunWorkflowServiceGetWorkflowStateRequest

The RunWorkflowServiceGetWorkflowStateRequest class.

### RunWorkflowServiceGetWorkflowStateResponse

Response object of the RunWorkflowApi.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_state | [WorkflowState](#zen_api.em.workflow.v1.WorkflowState) |  | A Workflow state value. |

### RunWorkflowServiceNextRequest

The RunWorkflowServiceNextRequest class.

### RunWorkflowServiceNextResponse

The RunWorkflowServiceNextResponse class.

### RunWorkflowServicePauseRequest

The RunWorkflowServicePauseRequest class.

### RunWorkflowServicePauseResponse

The RunWorkflowServicePauseResponse class.

### RunWorkflowServiceRegisterOnActionExecutionIdChangedRequest

The RunWorkflowServiceRegisterOnActionExecutionIdChangedRequest class.

### RunWorkflowServiceRegisterOnActionExecutionIdChangedResponse

ActionExecutionId response.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| action\_id | [string](#string) |  | The action id which is curently executed. |

### RunWorkflowServiceRegisterOnWorkflowStateChangedRequest

The RunWorkflowServiceRegisterOnWorkflowStateChangedRequest class.

### RunWorkflowServiceRegisterOnWorkflowStateChangedResponse

Response object of the RunWorkflowApi.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_state | [WorkflowState](#zen_api.em.workflow.v1.WorkflowState) |  | A Workflow state value. |

### RunWorkflowServiceResumeRequest

The RunWorkflowServiceResumeRequest class.

### RunWorkflowServiceResumeResponse

The RunWorkflowServiceResumeResponse class.

### RunWorkflowServiceRunWorkflowRequest

The RunWorkflowServiceRunWorkflowRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow which should be executed. |

### RunWorkflowServiceRunWorkflowResponse

Response object of the RunWorkflow method.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| task\_success | [bool](#bool) |  | A value indicating whether the task to run workflow succeeded or not. |

### RunWorkflowServiceSetNormalModeRequest

The RunWorkflowServiceSetNormalModeRequest class.

### RunWorkflowServiceSetNormalModeResponse

The RunWorkflowServiceSetNormalModeResponse class.

### RunWorkflowServiceSetStepModeRequest

The RunWorkflowServiceSetStepModeRequest class.

### RunWorkflowServiceSetStepModeResponse

The RunWorkflowServiceSetStepModeResponse class.

### RunWorkflowServiceStartRequest

The RunWorkflowServiceStartRequest class.

### RunWorkflowServiceStartResponse

The RunWorkflowServiceStartResponse class.

### RunWorkflowServiceStepRequest

The RunWorkflowServiceStepRequest class.

### RunWorkflowServiceStepResponse

The RunWorkflowServiceStepResponse class.

### RunWorkflowServiceStopEmergencyRequest

The RunWorkflowServiceStopEmergencyRequest class.

### RunWorkflowServiceStopEmergencyResponse

The RunWorkflowServiceStopEmergencyResponse class.

### RunWorkflowServiceStopRequest

The RunWorkflowServiceStopRequest class.

### RunWorkflowServiceStopResponse

The RunWorkflowServiceStopResponse class.

### RunWorkflowService

The IRunWorkflowService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | Break | [RunWorkflowServiceBreakRequest](#zen_api.em.workflow.v1.RunWorkflowServiceBreakRequest) | [RunWorkflowServiceBreakResponse](#zen_api.em.workflow.v1.RunWorkflowServiceBreakResponse) | Execution of Break command. |
|  | DefineAndRunCompleteWorkflow | [RunWorkflowServiceDefineAndRunCompleteWorkflowRequest](#zen_api.em.workflow.v1.RunWorkflowServiceDefineAndRunCompleteWorkflowRequest) | [RunWorkflowServiceDefineAndRunCompleteWorkflowResponse](#zen_api.em.workflow.v1.RunWorkflowServiceDefineAndRunCompleteWorkflowResponse) | Trigger a run of the complete workflow. |
|  | GetWorkflowById | [RunWorkflowServiceGetWorkflowByIdRequest](#zen_api.em.workflow.v1.RunWorkflowServiceGetWorkflowByIdRequest) | [RunWorkflowServiceGetWorkflowByIdResponse](#zen_api.em.workflow.v1.RunWorkflowServiceGetWorkflowByIdResponse) | Retrieves the workflow by the given id. If workflow is not yet defined an Empty.String will be returned. |
|  | GetWorkflowState | [RunWorkflowServiceGetWorkflowStateRequest](#zen_api.em.workflow.v1.RunWorkflowServiceGetWorkflowStateRequest) | [RunWorkflowServiceGetWorkflowStateResponse](#zen_api.em.workflow.v1.RunWorkflowServiceGetWorkflowStateResponse) | Gets Workflow State. |
|  | Next | [RunWorkflowServiceNextRequest](#zen_api.em.workflow.v1.RunWorkflowServiceNextRequest) | [RunWorkflowServiceNextResponse](#zen_api.em.workflow.v1.RunWorkflowServiceNextResponse) | Execution of Next command. |
|  | Pause | [RunWorkflowServicePauseRequest](#zen_api.em.workflow.v1.RunWorkflowServicePauseRequest) | [RunWorkflowServicePauseResponse](#zen_api.em.workflow.v1.RunWorkflowServicePauseResponse) | Trigger pauses the currently running workflow. |
|  | RegisterOnActionExecutionIdChanged | [RunWorkflowServiceRegisterOnActionExecutionIdChangedRequest](#zen_api.em.workflow.v1.RunWorkflowServiceRegisterOnActionExecutionIdChangedRequest) | [RunWorkflowServiceRegisterOnActionExecutionIdChangedResponse](#zen_api.em.workflow.v1.RunWorkflowServiceRegisterOnActionExecutionIdChangedResponse) stream | Notification about change of the currently executed action id. |
|  | RegisterOnWorkflowStateChanged | [RunWorkflowServiceRegisterOnWorkflowStateChangedRequest](#zen_api.em.workflow.v1.RunWorkflowServiceRegisterOnWorkflowStateChangedRequest) | [RunWorkflowServiceRegisterOnWorkflowStateChangedResponse](#zen_api.em.workflow.v1.RunWorkflowServiceRegisterOnWorkflowStateChangedResponse) stream | Notification about change of the Workflow state. |
|  | Resume | [RunWorkflowServiceResumeRequest](#zen_api.em.workflow.v1.RunWorkflowServiceResumeRequest) | [RunWorkflowServiceResumeResponse](#zen_api.em.workflow.v1.RunWorkflowServiceResumeResponse) | Trigger resumes the currently paused workflow. |
|  | RunWorkflow | [RunWorkflowServiceRunWorkflowRequest](#zen_api.em.workflow.v1.RunWorkflowServiceRunWorkflowRequest) | [RunWorkflowServiceRunWorkflowResponse](#zen_api.em.workflow.v1.RunWorkflowServiceRunWorkflowResponse) | Trigger a run of the specified workflow. |
|  | SetNormalMode | [RunWorkflowServiceSetNormalModeRequest](#zen_api.em.workflow.v1.RunWorkflowServiceSetNormalModeRequest) | [RunWorkflowServiceSetNormalModeResponse](#zen_api.em.workflow.v1.RunWorkflowServiceSetNormalModeResponse) | Execution of set normal / step mode command. |
|  | SetStepMode | [RunWorkflowServiceSetStepModeRequest](#zen_api.em.workflow.v1.RunWorkflowServiceSetStepModeRequest) | [RunWorkflowServiceSetStepModeResponse](#zen_api.em.workflow.v1.RunWorkflowServiceSetStepModeResponse) | Execution of set normal / step mode command. |
|  | Start | [RunWorkflowServiceStartRequest](#zen_api.em.workflow.v1.RunWorkflowServiceStartRequest) | [RunWorkflowServiceStartResponse](#zen_api.em.workflow.v1.RunWorkflowServiceStartResponse) | Trigger starts the stopped workflow. |
|  | Step | [RunWorkflowServiceStepRequest](#zen_api.em.workflow.v1.RunWorkflowServiceStepRequest) | [RunWorkflowServiceStepResponse](#zen_api.em.workflow.v1.RunWorkflowServiceStepResponse) | Execution of Step command in step mode. |
|  | Stop | [RunWorkflowServiceStopRequest](#zen_api.em.workflow.v1.RunWorkflowServiceStopRequest) | [RunWorkflowServiceStopResponse](#zen_api.em.workflow.v1.RunWorkflowServiceStopResponse) | Trigger stops the currently running workflow. The workflow not necessary was started from API. |
|  | StopEmergency | [RunWorkflowServiceStopEmergencyRequest](#zen_api.em.workflow.v1.RunWorkflowServiceStopEmergencyRequest) | [RunWorkflowServiceStopEmergencyResponse](#zen_api.em.workflow.v1.RunWorkflowServiceStopEmergencyResponse) | Trigger stops emergency. |

## zen\_api/em/workflow/v1/vacuum\_parameter.proto

[Top](#title)

### VacuumParameter

List of parameters that can be called on the Vacuum.

| Name | Number | Description |
| --- | --- | --- |
| VACUUM\_PARAMETER\_UNSPECIFIED | 0 | Default enum value. |
| VACUUM\_PARAMETER\_VARIABLE\_PRESSURE\_TARGET | 1 | Variable pressure. |

## zen\_api/em/workflow/v1/workflow\_admin\_service.proto

[Top](#title)

### WorkflowAdminServiceDeleteWorkflowByIdRequest

The WorkflowAdminServiceDeleteWorkflowByIdRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_id | [string](#string) |  | Identifier of the workflow which should be deleted. |

### WorkflowAdminServiceDeleteWorkflowByIdResponse

The WorkflowAdminServiceDeleteWorkflowByIdResponse class.

### WorkflowAdminServiceGetAvailableWorkflowIdsRequest

The WorkflowAdminServiceGetAvailableWorkflowIdsRequest class.

### WorkflowAdminServiceGetAvailableWorkflowIdsResponse

Response object of the GetAvailableWorkflowsIds method.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| workflow\_ids | [string](#string) | repeated | A value with workflow xml. |

### WorkflowAdminService

The IWorkflowAdminService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | DeleteWorkflowById | [WorkflowAdminServiceDeleteWorkflowByIdRequest](#zen_api.em.workflow.v1.WorkflowAdminServiceDeleteWorkflowByIdRequest) | [WorkflowAdminServiceDeleteWorkflowByIdResponse](#zen_api.em.workflow.v1.WorkflowAdminServiceDeleteWorkflowByIdResponse) | Delete specified workflow by workflowId. |
|  | GetAvailableWorkflowIds | [WorkflowAdminServiceGetAvailableWorkflowIdsRequest](#zen_api.em.workflow.v1.WorkflowAdminServiceGetAvailableWorkflowIdsRequest) | [WorkflowAdminServiceGetAvailableWorkflowIdsResponse](#zen_api.em.workflow.v1.WorkflowAdminServiceGetAvailableWorkflowIdsResponse) | Gets all available workflowIds. |

## zen\_api/em/workflow/v1/workflow\_state.proto

[Top](#title)

### WorkflowState

WorkflowState.

| Name | Number | Description |
| --- | --- | --- |
| WORKFLOW\_STATE\_UNSPECIFIED | 0 | Default value. |
| WORKFLOW\_STATE\_RUN\_ACTIVE | 1 | Execution running. |
| WORKFLOW\_STATE\_RUN\_PAUSED | 2 | Execution paused. |
| WORKFLOW\_STATE\_RUN\_COMPLETED | 3 | Execution completed. |
| WORKFLOW\_STATE\_RUN\_FAILED | 4 | Execution failed. |
| WORKFLOW\_STATE\_RUN\_UNKNOWN | 5 | Unknown status, e.g. no run so far. |

## zen\_api/lm/acquisition/v1/autofocus\_contrast\_measure.proto

[Top](#title)

### AutofocusContrastMeasure

The contrast measures of the software autofocus contrast mode.

| Name | Number | Description |
| --- | --- | --- |
| AUTOFOCUS\_CONTRAST\_MEASURE\_UNSPECIFIED | 0 | Default enum value. |
| AUTOFOCUS\_CONTRAST\_MEASURE\_DEFAULT | 1 | The default contrast measure. |
| AUTOFOCUS\_CONTRAST\_MEASURE\_LOW\_SIGNAL | 2 | The contrast measure to use in low-signal and calibration situations. |

## zen\_api/lm/acquisition/v1/autofocus\_mode.proto

[Top](#title)

### AutofocusMode

The autofocus modes.

| Name | Number | Description |
| --- | --- | --- |
| AUTOFOCUS\_MODE\_UNSPECIFIED | 0 | Default enum value. |
| AUTOFOCUS\_MODE\_CONTRAST | 1 | Sharpness is measured on the basis of contrast values. |
| AUTOFOCUS\_MODE\_INTENSITY | 2 | Sharpness is measured on the basis of intensity values. |
| AUTOFOCUS\_MODE\_AUTO | 3 | Automatic determination of measure method (Contrast or Intensity) in dependency of used hardware. |
| AUTOFOCUS\_MODE\_REFLEX | 4 | Sharpness is measured with the reflection mode autofocus. |

## zen\_api/lm/acquisition/v1/autofocus\_sampling.proto

[Top](#title)

### AutofocusSampling

Scales the depth of focus by predefined values given here.

| Name | Number | Description |
| --- | --- | --- |
| AUTOFOCUS\_SAMPLING\_UNSPECIFIED | 0 | Default enum value. |
| AUTOFOCUS\_SAMPLING\_FINE | 1 | Do oversampling. |
| AUTOFOCUS\_SAMPLING\_DEFAULT | 2 | Do sampling according to depth of focus. |
| AUTOFOCUS\_SAMPLING\_MEDIUM | 3 | Do under sampling. |
| AUTOFOCUS\_SAMPLING\_COARSE | 4 | Coarser than medium. |

## zen\_api/lm/acquisition/v1/channel\_info.proto

[Top](#title)

### ChannelInfo

Information about a channel.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| name | [string](#string) |  | The channel name. |
| is\_activated | [bool](#bool) |  | A value indicating whether the channel is activated. |

## zen\_api/lm/acquisition/v1/definite\_focus\_service.proto

[Top](#title)

### DefiniteFocusServiceFindSurfaceRequest

The DefiniteFocusServiceFindSurfaceRequest class.

### DefiniteFocusServiceFindSurfaceResponse

Response for FindSurface.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| zposition | [double](#double) |  | The Z position. |

### DefiniteFocusServiceLockFocusRequest

The DefiniteFocusServiceLockFocusRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| timeout | [int32](#int32) |  | Timeout in seconds. |

### DefiniteFocusServiceLockFocusResponse

Response for LockFocus.

### DefiniteFocusServiceRecallFocusRequest

The DefiniteFocusServiceRecallFocusRequest class.

### DefiniteFocusServiceRecallFocusResponse

Response for RecallFocus.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| zposition | [double](#double) |  | The Z position. |

### DefiniteFocusServiceStoreFocusRequest

The DefiniteFocusServiceStoreFocusRequest class.

### DefiniteFocusServiceStoreFocusResponse

Response for StoreFocus.

### DefiniteFocusServiceUnlockFocusRequest

The DefiniteFocusServiceUnlockFocusRequest class.

### DefiniteFocusServiceUnlockFocusResponse

Response for UnlockFocus.

### DefiniteFocusService

The IDefiniteFocusService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | FindSurface | [DefiniteFocusServiceFindSurfaceRequest](#zen_api.lm.acquisition.v1.DefiniteFocusServiceFindSurfaceRequest) | [DefiniteFocusServiceFindSurfaceResponse](#zen_api.lm.acquisition.v1.DefiniteFocusServiceFindSurfaceResponse) | Finds the surface of the probe. |
|  | LockFocus | [DefiniteFocusServiceLockFocusRequest](#zen_api.lm.acquisition.v1.DefiniteFocusServiceLockFocusRequest) | [DefiniteFocusServiceLockFocusResponse](#zen_api.lm.acquisition.v1.DefiniteFocusServiceLockFocusResponse) | Locks the focus. |
|  | RecallFocus | [DefiniteFocusServiceRecallFocusRequest](#zen_api.lm.acquisition.v1.DefiniteFocusServiceRecallFocusRequest) | [DefiniteFocusServiceRecallFocusResponse](#zen_api.lm.acquisition.v1.DefiniteFocusServiceRecallFocusResponse) | Recall the focus for the component. |
|  | StoreFocus | [DefiniteFocusServiceStoreFocusRequest](#zen_api.lm.acquisition.v1.DefiniteFocusServiceStoreFocusRequest) | [DefiniteFocusServiceStoreFocusResponse](#zen_api.lm.acquisition.v1.DefiniteFocusServiceStoreFocusResponse) | Stores the focus for the component. |
|  | UnlockFocus | [DefiniteFocusServiceUnlockFocusRequest](#zen_api.lm.acquisition.v1.DefiniteFocusServiceUnlockFocusRequest) | [DefiniteFocusServiceUnlockFocusResponse](#zen_api.lm.acquisition.v1.DefiniteFocusServiceUnlockFocusResponse) | Unlocks the focus. |

## zen\_api/lm/acquisition/v1/experiment\_sw\_autofocus\_service.proto

[Top](#title)

### ExperimentSwAutofocusServiceExportRequest

The ExperimentSwAutofocusServiceExportRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment id. |

### ExperimentSwAutofocusServiceExportResponse

Response object representing the values of xml string.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| xml\_string | [string](#string) |  | A value of the xml string. |

### ExperimentSwAutofocusServiceFindAutoFocusRequest

The ExperimentSwAutofocusServiceFindAutoFocusRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment id. |
| timeout | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The timeout in seconds. |

### ExperimentSwAutofocusServiceFindAutoFocusResponse

Response object representing the focus position.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| focus\_position | [double](#double) |  | The focus position (unit: m). |

### ExperimentSwAutofocusServiceGetAutofocusParametersRequest

The ExperimentSwAutofocusServiceGetAutofocusParametersRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment id. |

### ExperimentSwAutofocusServiceGetAutofocusParametersResponse

Response object representing the values of software autofocus parameters for the experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | A value of the experiment id. |
| auto\_focus\_mode | [AutofocusMode](#zen_api.lm.acquisition.v1.AutofocusMode) |  | A value of autofocus mode. |
| contrast\_measure | [AutofocusContrastMeasure](#zen_api.lm.acquisition.v1.AutofocusContrastMeasure) |  | A value of sharpness measure for contrast mode. |
| search\_strategy | [string](#string) |  | A value of search strategy. Either "Smart", "Full", "FullNoChecks" or the name of an extension strategy. |
| autofocus\_sampling | [AutofocusSampling](#zen_api.lm.acquisition.v1.AutofocusSampling) |  | A value of the predefined step size. |
| offset | [double](#double) |  | A value of the reflection mode offset (unit: m). |
| use\_acquisition\_roi | [bool](#bool) |  | A value indicating whether the acquisition ROI is used for the software autofocus. |
| reference\_channel\_name | [string](#string) |  | A name of the focus reference channel. |
| relative\_range\_is\_automatic | [bool](#bool) |  | A value indicating whether the relative search range size is determined automatically. |
| relative\_search\_range | [double](#double) |  | A value of the relative search range of the Z drive (unit: m). |
| lower\_limit | [double](#double) |  | A value of the lower search range limit of the Z drive (unit: m). |
| upper\_limit | [double](#double) |  | A value of the upper search range limit of the Z drive (unit: m). |

### ExperimentSwAutofocusServiceImportRequest

The ExperimentSwAutofocusServiceImportRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment id. |
| xml\_string | [string](#string) |  | Xml string to be imported. |

### ExperimentSwAutofocusServiceImportResponse

The ExperimentSwAutofocusServiceImportResponse class.

### ExperimentSwAutofocusServiceSetAutofocusParametersRequest

The ExperimentSwAutofocusServiceSetAutofocusParametersRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment id. |
| autofocus\_mode | [AutofocusMode](#zen_api.lm.acquisition.v1.AutofocusMode) |  | The autofocus mode. |
| contrast\_measure | [AutofocusContrastMeasure](#zen_api.lm.acquisition.v1.AutofocusContrastMeasure) |  | The sharpness measure for contrast mode. |
| search\_strategy | [string](#string) |  | The strategy, either "Smart", "Full", "FullNoChecks" or the name of an extension strategy, or null to leave unmodified. This parameter is case-insensitive. |
| autofocus\_sampling | [AutofocusSampling](#zen_api.lm.acquisition.v1.AutofocusSampling) |  | The predefined step size, or null to leave unmodified. |
| offset | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The reflection mode offset (unit: m), or null to leave unmodified. |
| use\_acquisition\_roi | [google.protobuf.BoolValue](https://protobuf.dev/reference/protobuf/google.protobuf/#bool-value) |  | True if the acquisition ROI is used for the software autofocus; otherwise, false, or null to leave unmodified. |
| reference\_channel\_name | [string](#string) |  | The case-insensitive name of the focus reference channel, or null to leave unmodified. |
| relative\_range\_is\_automatic | [google.protobuf.BoolValue](https://protobuf.dev/reference/protobuf/google.protobuf/#bool-value) |  | True if the relative search range size is determined automatically; otherwise, false, or null to leave unmodified. |
| relative\_search\_range | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The relative search range in units of the Z drive (unit: m), or null to leave unmodified. |
| lower\_limit | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The lower search range limit in units of the Z drive (unit: m), or null to leave unmodified. |
| upper\_limit | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The upper limit in units of the Z drive (unit: m), or null to leave unmodified. |

### ExperimentSwAutofocusServiceSetAutofocusParametersResponse

The ExperimentSwAutofocusServiceSetAutofocusParametersResponse class.

### ExperimentSwAutofocusService

The IExperimentSwAutofocusService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | Export | [ExperimentSwAutofocusServiceExportRequest](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceExportRequest) | [ExperimentSwAutofocusServiceExportResponse](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceExportResponse) | Exports the software autofocus parameters to an xml string. |
|  | FindAutoFocus | [ExperimentSwAutofocusServiceFindAutoFocusRequest](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceFindAutoFocusRequest) | [ExperimentSwAutofocusServiceFindAutoFocusResponse](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceFindAutoFocusResponse) | Gets the the focus position. |
|  | GetAutofocusParameters | [ExperimentSwAutofocusServiceGetAutofocusParametersRequest](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceGetAutofocusParametersRequest) | [ExperimentSwAutofocusServiceGetAutofocusParametersResponse](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceGetAutofocusParametersResponse) | Gets the software autofocus parameters for the specified experiment. |
|  | Import | [ExperimentSwAutofocusServiceImportRequest](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceImportRequest) | [ExperimentSwAutofocusServiceImportResponse](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceImportResponse) | Imports the software autofocus parameters from an xml string. |
|  | SetAutofocusParameters | [ExperimentSwAutofocusServiceSetAutofocusParametersRequest](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceSetAutofocusParametersRequest) | [ExperimentSwAutofocusServiceSetAutofocusParametersResponse](#zen_api.lm.acquisition.v1.ExperimentSwAutofocusServiceSetAutofocusParametersResponse) | Sets the software autofocus parameters for the specified experiment. |

## zen\_api/lm/acquisition/v1/position3d.proto

[Top](#title)

### Position3d

A position in three dimensions (XYZ).

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [double](#double) |  | The X position (unit: m). |
| y | [double](#double) |  | The Y position (unit: m). |
| z | [double](#double) |  | The Z position (unit: m). |

## zen\_api/lm/acquisition/v1/region\_contour.proto

[Top](#title)

### RegionContour

General data contract for all region contour types.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| region\_ellipse | [RegionEllipse](#zen_api.lm.acquisition.v1.RegionEllipse) |  |  |
| region\_rectangle | [RegionRectangle](#zen_api.lm.acquisition.v1.RegionRectangle) |  |  |
| region\_polygon | [RegionPolygon](#zen_api.lm.acquisition.v1.RegionPolygon) |  |  |

### RegionEllipse

Represents an elliptical region defined by a bounding rectangle.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| bounding\_box | [RegionRect](#zen_api.lm.acquisition.v1.RegionRect) |  | The rectangle that defines the bounding box of the ellipse. The ellipse is fully contained within this rectangle. The ZenApi.LM.Acquisition.V1.RegionRect specifies the position and size of the bounding rectangle using four values: X (left), Y (top), Width, and Height. For example, a rectangle with X = 10, Y = 20, Width = 100, and Height = 50 defines an ellipse centered at (60, 45) with a horizontal radius of 50 and a vertical radius of 25. |

### RegionPolygon

Represents a polygonal region defined by an ordered list of vertices.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| points | [RegionPoint](#zen_api.lm.acquisition.v1.RegionPoint) | repeated | The ordered list of ZenApi.LM.Acquisition.V1.RegionPoint instances that define the vertices of the polygon. Each point specifies an (X, Y) coordinate in the region's coordinate space. The polygon is formed by connecting each consecutive point in the list, and finally connecting the last point back to the first to close the shape. |

### RegionRectangle

Represents a rectangular region within the slide scan area.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| rectangle | [RegionRect](#zen_api.lm.acquisition.v1.RegionRect) |  | The ZenApi.LM.Acquisition.V1.RegionRect that defines the position and size of the rectangular region within the slide scan area. |

## zen\_api/lm/acquisition/v1/region\_point.proto

[Top](#title)

### RegionPoint

Represents a two-dimensional point with X and Y coordinates for use in region-based acquisition scenarios.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [double](#double) |  | The X coordinate of the point. |
| y | [double](#double) |  | The Y coordinate of the point. |

## zen\_api/lm/acquisition/v1/region\_rect.proto

[Top](#title)

### RegionRect

Represents a rectangular region defined by its left (X), top (Y) coordinates, width, and height.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [double](#double) |  | The left coordinate of the rectangle. |
| y | [double](#double) |  | The top coordinate of the rectangle. |
| width | [double](#double) |  | The width of the rectangle. |
| height | [double](#double) |  | The height of the rectangle. |

## zen\_api/lm/acquisition/v1/tiles\_service.proto

[Top](#title)

### TilesServiceAddEllipseTileRegionRequest

The TilesServiceAddEllipseTileRegionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment Id. |
| center\_x | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The center x position of the tile region to be added (unit: m). |
| center\_y | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The center y position of the tile region to be added (unit: m). |
| width | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The width of the tile region to be added (unit: m). |
| height | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The height of the tile region to be added (unit: m). |
| z | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The z position of the tile region to be added (unit: m). |

### TilesServiceAddEllipseTileRegionResponse

The TilesServiceAddEllipseTileRegionResponse class.

### TilesServiceAddPolygonTileRegionRequest

The TilesServiceAddPolygonTileRegionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment Id. |
| polygon\_points | [zen\_api.common.v1.DoublePoint](#zen_api.common.v1.DoublePoint) | repeated | The list of points which define the polygon. This list has to contain at least one point (unit: m). |
| z | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The z position of the tile region to be added (unit: m). |

### TilesServiceAddPolygonTileRegionResponse

The TilesServiceAddPolygonTileRegionResponse class.

### TilesServiceAddPositionsRequest

The TilesServiceAddPositionsRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment Id. |
| positions | [Position3d](#zen_api.lm.acquisition.v1.Position3d) | repeated | The positions to be added. |

### TilesServiceAddPositionsResponse

The TilesServiceAddPositionsResponse class.

### TilesServiceAddRectangleTileRegionRequest

The TilesServiceAddRectangleTileRegionRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |
| center\_x | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The center x position of the tile region to be added (unit: m). |
| center\_y | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The center y position of the tile region to be added (unit: m). |
| width | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The width of the tile region to be added (unit: m). |
| height | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The height of the tile region to be added (unit: m). |
| z | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The z position of the tile region to be added (unit: m). |

### TilesServiceAddRectangleTileRegionResponse

The TilesServiceAddRectangleTileRegionResponse class.

### TilesServiceClearRequest

The TilesServiceClearRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |

### TilesServiceClearResponse

The TilesServiceClearResponse class.

### TilesServiceIsTilesExperimentRequest

The TilesServiceIsTilesExperimentRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |

### TilesServiceIsTilesExperimentResponse

Response object representing the value of IsTiles for the experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| is\_tiles\_experiment | [bool](#bool) |  | A value indicating whether the experiment is a tiles experiment. |

### TilesService

The ITilesService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | AddEllipseTileRegion | [TilesServiceAddEllipseTileRegionRequest](#zen_api.lm.acquisition.v1.TilesServiceAddEllipseTileRegionRequest) | [TilesServiceAddEllipseTileRegionResponse](#zen_api.lm.acquisition.v1.TilesServiceAddEllipseTileRegionResponse) | Adds an ellipse tile region with the specified position and size values to the acquisition block with the specified index in the specified experiment. |
|  | AddPolygonTileRegion | [TilesServiceAddPolygonTileRegionRequest](#zen_api.lm.acquisition.v1.TilesServiceAddPolygonTileRegionRequest) | [TilesServiceAddPolygonTileRegionResponse](#zen_api.lm.acquisition.v1.TilesServiceAddPolygonTileRegionResponse) | Adds a polygon tile region with the specified points list to the acquisition block with the specified index in the specified experiment. |
|  | AddPositions | [TilesServiceAddPositionsRequest](#zen_api.lm.acquisition.v1.TilesServiceAddPositionsRequest) | [TilesServiceAddPositionsResponse](#zen_api.lm.acquisition.v1.TilesServiceAddPositionsResponse) | Adds positions with the specified coordinates to the specified experiment. |
|  | AddRectangleTileRegion | [TilesServiceAddRectangleTileRegionRequest](#zen_api.lm.acquisition.v1.TilesServiceAddRectangleTileRegionRequest) | [TilesServiceAddRectangleTileRegionResponse](#zen_api.lm.acquisition.v1.TilesServiceAddRectangleTileRegionResponse) | Adds a rectangle tile region with the specified position and size values to the specified experiment. |
|  | Clear | [TilesServiceClearRequest](#zen_api.lm.acquisition.v1.TilesServiceClearRequest) | [TilesServiceClearResponse](#zen_api.lm.acquisition.v1.TilesServiceClearResponse) | Clears all tile regions and positions in the current acquisition block. |
|  | IsTilesExperiment | [TilesServiceIsTilesExperimentRequest](#zen_api.lm.acquisition.v1.TilesServiceIsTilesExperimentRequest) | [TilesServiceIsTilesExperimentResponse](#zen_api.lm.acquisition.v1.TilesServiceIsTilesExperimentResponse) | Determines whether the current experiment block in the specified experiment is a Tiles experiment. This means that the corresponding Tiles dimension is activated. |

## zen\_api/lm/acquisition/v1/time\_series\_info.proto

[Top](#title)

### TimeSeriesInfo

Object representing the value of TimeSeriesInfo for the experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| duration | [double](#double) |  | The value of the Duration. |
| duration\_unit | [TimeUnitExtended](#zen_api.lm.acquisition.v1.TimeUnitExtended) |  | The value of the Duration Unit of measure. |
| is\_long\_as\_possible | [bool](#bool) |  | A value indicating whether the duration is as long as possible. |
| interval | [double](#double) |  | The value of the Interval. |
| interval\_unit | [TimeUnit](#zen_api.lm.acquisition.v1.TimeUnit) |  | The value of the Interval Uunit of measure. |
| is\_fast\_as\_possible | [bool](#bool) |  | A value indicating whether the imaging is as fast as possible. |
| is\_burst\_mode | [bool](#bool) |  | A value indicating whether Burst Mode is used. |

## zen\_api/lm/acquisition/v1/time\_series\_service.proto

[Top](#title)

### TimeSeriesServiceGetTimeSeriesInfoRequest

The TimeSeriesServiceGetTimeSeriesInfoRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment Id. |

### TimeSeriesServiceGetTimeSeriesInfoResponse

Response object containing the value of Time Series info for the experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| time\_series | [TimeSeriesInfo](#zen_api.lm.acquisition.v1.TimeSeriesInfo) |  | The value of the Time Series info. |

### TimeSeriesServiceSetTimeSeriesInfoRequest

Request object for setting the value of TimeSeriesInfo for the experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The Experiment Id. |
| time\_series | [TimeSeriesInfo](#zen_api.lm.acquisition.v1.TimeSeriesInfo) |  | The value of the Time Series info. |

### TimeSeriesServiceSetTimeSeriesInfoResponse

Empty response object upon setting the Time Series info for the experiment.

### TimeSeriesService

The ITimeSeriesService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetTimeSeriesInfo | [TimeSeriesServiceGetTimeSeriesInfoRequest](#zen_api.lm.acquisition.v1.TimeSeriesServiceGetTimeSeriesInfoRequest) | [TimeSeriesServiceGetTimeSeriesInfoResponse](#zen_api.lm.acquisition.v1.TimeSeriesServiceGetTimeSeriesInfoResponse) | Gets the information about Time Series of an experiment. |
|  | SetTimeSeriesInfo | [TimeSeriesServiceSetTimeSeriesInfoRequest](#zen_api.lm.acquisition.v1.TimeSeriesServiceSetTimeSeriesInfoRequest) | [TimeSeriesServiceSetTimeSeriesInfoResponse](#zen_api.lm.acquisition.v1.TimeSeriesServiceSetTimeSeriesInfoResponse) | Sets the information about Time Series of an experiment. |

## zen\_api/lm/acquisition/v1/time\_series\_service\_time\_series\_info.proto

[Top](#title)

### TimeSeriesServiceTimeSeriesInfo

Object representing the value of TimeSeriesInfo for the experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| duration | [double](#double) |  | The value of the Duration. |
| duration\_unit | [TimeSeriesServiceTimeUnitExtended](#zen_api.lm.acquisition.v1.TimeSeriesServiceTimeUnitExtended) |  | The value of the Duration Unit of measure. |
| is\_long\_as\_possible | [bool](#bool) |  | A value indicating whether the duration is as long as possible. |
| interval | [double](#double) |  | The value of the Interval. |
| interval\_unit | [TimeSeriesServiceTimeUnit](#zen_api.lm.acquisition.v1.TimeSeriesServiceTimeUnit) |  | The value of the Interval Uunit of measure. |
| is\_fast\_as\_possible | [bool](#bool) |  | A value indicating whether the imaging is as fast as possible. |
| is\_burst\_mode | [bool](#bool) |  | A value indicating whether Burst Mode is used. |

## zen\_api/lm/acquisition/v1/time\_series\_service\_time\_unit.proto

[Top](#title)

### TimeSeriesServiceTimeUnit

Extended time units to match TimeUnit enum.

| Name | Number | Description |
| --- | --- | --- |
| TIME\_SERIES\_SERVICE\_TIME\_UNIT\_UNSPECIFIED | 0 | Unspecified. |
| TIME\_SERIES\_SERVICE\_TIME\_UNIT\_MS | 1 | Time unit milliseconds. |
| TIME\_SERIES\_SERVICE\_TIME\_UNIT\_S | 2 | Time unit seconds. |
| TIME\_SERIES\_SERVICE\_TIME\_UNIT\_MIN | 3 | Time unit minutes. |
| TIME\_SERIES\_SERVICE\_TIME\_UNIT\_H | 4 | Time unit hours. |
| TIME\_SERIES\_SERVICE\_TIME\_UNIT\_DAYS | 5 | Time unit days. |

## zen\_api/lm/acquisition/v1/time\_series\_service\_time\_unit\_extended.proto

[Top](#title)

### TimeSeriesServiceTimeUnitExtended

Extended time units to match TimeUnitExtended enum.

| Name | Number | Description |
| --- | --- | --- |
| TIME\_SERIES\_SERVICE\_TIME\_UNIT\_EXTENDED\_UNSPECIFIED | 0 | Unspecified. |
| TIME\_SERIES\_SERVICE\_TIME\_UNIT\_EXTENDED\_CYCLES | 1 | Cycles is the count of time points. |
| TIME\_SERIES\_SERVICE\_TIME\_UNIT\_EXTENDED\_MS | 2 | Time unit milliseconds. |
| TIME\_SERIES\_SERVICE\_TIME\_UNIT\_EXTENDED\_S | 3 | Time unit seconds. |
| TIME\_SERIES\_SERVICE\_TIME\_UNIT\_EXTENDED\_MIN | 4 | Time unit minutes. |
| TIME\_SERIES\_SERVICE\_TIME\_UNIT\_EXTENDED\_H | 5 | Time unit hours. |
| TIME\_SERIES\_SERVICE\_TIME\_UNIT\_EXTENDED\_DAYS | 6 | Time unit days. |

## zen\_api/lm/acquisition/v1/time\_unit.proto

[Top](#title)

### TimeUnit

Extended time units to match TimeUnit enum.

| Name | Number | Description |
| --- | --- | --- |
| TIME\_UNIT\_UNSPECIFIED | 0 | Unspecified. |
| TIME\_UNIT\_MS | 1 | Time unit milliseconds. |
| TIME\_UNIT\_S | 2 | Time unit seconds. |
| TIME\_UNIT\_MIN | 3 | Time unit minutes. |
| TIME\_UNIT\_H | 4 | Time unit hours. |
| TIME\_UNIT\_DAYS | 5 | Time unit days. |

## zen\_api/lm/acquisition/v1/time\_unit\_extended.proto

[Top](#title)

### TimeUnitExtended

Extended time units to match TimeUnitExtended enum.

| Name | Number | Description |
| --- | --- | --- |
| TIME\_UNIT\_EXTENDED\_UNSPECIFIED | 0 | Unspecified. |
| TIME\_UNIT\_EXTENDED\_CYCLES | 1 | Cycles is the count of time points. |
| TIME\_UNIT\_EXTENDED\_MS | 2 | Time unit milliseconds. |
| TIME\_UNIT\_EXTENDED\_S | 3 | Time unit seconds. |
| TIME\_UNIT\_EXTENDED\_MIN | 4 | Time unit minutes. |
| TIME\_UNIT\_EXTENDED\_H | 5 | Time unit hours. |
| TIME\_UNIT\_EXTENDED\_DAYS | 6 | Time unit days. |

## zen\_api/lm/acquisition/v1/track\_info.proto

[Top](#title)

### TrackInfo

Information about a track.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| is\_activated | [bool](#bool) |  | A value indicating whether the track is activated. |
| channels | [ChannelInfo](#zen_api.lm.acquisition.v1.ChannelInfo) | repeated | The info for all channels in the track. |

## zen\_api/lm/acquisition/v1/track\_service.proto

[Top](#title)

### TrackServiceActivateChannelRequest

The TrackServiceActivateChannelRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |
| track\_index | [int32](#int32) |  | An index of a track. |
| channel\_index | [int32](#int32) |  | An index of a channel in the track to be activated. |

### TrackServiceActivateChannelResponse

The TrackServiceActivateChannelResponse class.

### TrackServiceActivateTrackRequest

The TrackServiceActivateTrackRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |
| track\_index | [int32](#int32) |  | An index of a track to be activated. |

### TrackServiceActivateTrackResponse

The TrackServiceActivateTrackResponse class.

### TrackServiceDeactivateChannelRequest

The TrackServiceDeactivateChannelRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |
| track\_index | [int32](#int32) |  | An index of a track. |
| channel\_index | [int32](#int32) |  | An index of a channel in the track to be deactivated. |

### TrackServiceDeactivateChannelResponse

The TrackServiceDeactivateChannelResponse class.

### TrackServiceDeactivateTrackRequest

The TrackServiceDeactivateTrackRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |
| track\_index | [int32](#int32) |  | An index of a track to be deactivated. |

### TrackServiceDeactivateTrackResponse

The TrackServiceDeactivateTrackResponse class.

### TrackServiceGetTrackInfoRequest

The TrackServiceGetTrackInfoRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment id. |

### TrackServiceGetTrackInfoResponse

Response object representing the value of track information.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| track\_info | [TrackInfo](#zen_api.lm.acquisition.v1.TrackInfo) | repeated | The track information. |

### TrackService

The ITrackService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | ActivateChannel | [TrackServiceActivateChannelRequest](#zen_api.lm.acquisition.v1.TrackServiceActivateChannelRequest) | [TrackServiceActivateChannelResponse](#zen_api.lm.acquisition.v1.TrackServiceActivateChannelResponse) | Activates a channel with a specific index in a specific track. |
|  | ActivateTrack | [TrackServiceActivateTrackRequest](#zen_api.lm.acquisition.v1.TrackServiceActivateTrackRequest) | [TrackServiceActivateTrackResponse](#zen_api.lm.acquisition.v1.TrackServiceActivateTrackResponse) | Activates a track with a specific index. |
|  | DeactivateChannel | [TrackServiceDeactivateChannelRequest](#zen_api.lm.acquisition.v1.TrackServiceDeactivateChannelRequest) | [TrackServiceDeactivateChannelResponse](#zen_api.lm.acquisition.v1.TrackServiceDeactivateChannelResponse) | Deactivates a channel with a specific index in a specific track. |
|  | DeactivateTrack | [TrackServiceDeactivateTrackRequest](#zen_api.lm.acquisition.v1.TrackServiceDeactivateTrackRequest) | [TrackServiceDeactivateTrackResponse](#zen_api.lm.acquisition.v1.TrackServiceDeactivateTrackResponse) | Deactivates a track with a specific index. |
|  | GetTrackInfo | [TrackServiceGetTrackInfoRequest](#zen_api.lm.acquisition.v1.TrackServiceGetTrackInfoRequest) | [TrackServiceGetTrackInfoResponse](#zen_api.lm.acquisition.v1.TrackServiceGetTrackInfoResponse) | Gets the track information. |

## zen\_api/lm/acquisition/v1/zstack\_service.proto

[Top](#title)

### ZStackServiceGetZStackInfoRequest

The ZStackServiceGetZStackInfoRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment Id. |

### ZStackServiceGetZStackInfoResponse

Response object representing the value of GetZStackInfo for the experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| interval | [double](#double) |  | The value of the interval between 2 slices (unit: m). |
| first\_slice | [double](#double) |  | The position of the first slice in Z-stack (unit: m). |
| last\_slice | [double](#double) |  | The position of the last slice in Z-stack (unit: m). |
| range | [double](#double) |  | The distance between the first and last slice (unit: m). |
| num\_slices | [int32](#int32) |  | The number of slices. |
| is\_center\_mode | [bool](#bool) |  | A value indicating whether the Z-stack is in center mode. |
| offset | [double](#double) |  | The value of the offset which is applied to the whole Z-stack. |

### ZStackServiceIsZStackExperimentRequest

The ZStackServiceIsZStackExperimentRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment Id. |

### ZStackServiceIsZStackExperimentResponse

Response object representing the value of IsZStackExperiment for the experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| is\_zstack\_experiment | [bool](#bool) |  | A value indicating whether the experiment is a Z-Stack experiment. |

### ZStackServiceModifyZStackCenterRangeRequest

The ZStackServiceModifyZStackCenterRangeRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment Id. |
| center | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The center position between the first and last slice (unit: m). |
| interval | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The interval between 2 slices (unit: m). |
| range | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | Distance between the first and last slice (unit: m). |

### ZStackServiceModifyZStackCenterRangeResponse

The ZStackServiceModifyZStackCenterRangeResponse class.

### ZStackServiceModifyZStackFirstLastRequest

The ZStackServiceModifyZStackFirstLastRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | The experiment Id. |
| first | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | Position of the first slice in Z-stack (unit: m). |
| last | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | Position of the last slice in Z-stack (unit: m). |
| interval | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |  | The interval between 2 slices (unit: m). |

### ZStackServiceModifyZStackFirstLastResponse

The ZStackServiceModifyZStackFirstLastResponse class.

### ZStackService

The IZStackService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetZStackInfo | [ZStackServiceGetZStackInfoRequest](#zen_api.lm.acquisition.v1.ZStackServiceGetZStackInfoRequest) | [ZStackServiceGetZStackInfoResponse](#zen_api.lm.acquisition.v1.ZStackServiceGetZStackInfoResponse) | Gets the information about a Z-stack. |
|  | IsZStackExperiment | [ZStackServiceIsZStackExperimentRequest](#zen_api.lm.acquisition.v1.ZStackServiceIsZStackExperimentRequest) | [ZStackServiceIsZStackExperimentResponse](#zen_api.lm.acquisition.v1.ZStackServiceIsZStackExperimentResponse) | Determines whether the current experiment block in the specified experiment is a Z-stack experiment. This means that the corresponding Z-stack setup dimension is activated. |
|  | ModifyZStackCenterRange | [ZStackServiceModifyZStackCenterRangeRequest](#zen_api.lm.acquisition.v1.ZStackServiceModifyZStackCenterRangeRequest) | [ZStackServiceModifyZStackCenterRangeResponse](#zen_api.lm.acquisition.v1.ZStackServiceModifyZStackCenterRangeResponse) | Modifies the dimensions of the Z-stack inside the experiment. |
|  | ModifyZStackFirstLast | [ZStackServiceModifyZStackFirstLastRequest](#zen_api.lm.acquisition.v1.ZStackServiceModifyZStackFirstLastRequest) | [ZStackServiceModifyZStackFirstLastResponse](#zen_api.lm.acquisition.v1.ZStackServiceModifyZStackFirstLastResponse) | Modifies the dimensions of the Z-stack inside the experiment. |

## zen\_api/lm/acquisition/v2/region\_contour.proto

[Top](#title)

### RegionContour

General data contract for all region contour types.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| name | [string](#string) |  | The region contour name. |
| region\_ellipse | [RegionEllipse](#zen_api.lm.acquisition.v2.RegionEllipse) |  |  |
| region\_rectangle | [RegionRectangle](#zen_api.lm.acquisition.v2.RegionRectangle) |  |  |
| region\_polygon | [RegionPolygon](#zen_api.lm.acquisition.v2.RegionPolygon) |  |  |

### RegionEllipse

Represents an elliptical region defined by a bounding rectangle.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| bounding\_box | [RegionRect](#zen_api.lm.acquisition.v2.RegionRect) |  | The rectangle that defines the bounding box of the ellipse. The ellipse is fully contained within this rectangle. The ZenApi.LM.Acquisition.V2.RegionRect specifies the position and size of the bounding rectangle using four values: X (left), Y (top), Width, and Height. For example, a rectangle with X = 10, Y = 20, Width = 100, and Height = 50 defines an ellipse centered at (60, 45) with a horizontal radius of 50 and a vertical radius of 25. |

### RegionPolygon

Represents a polygonal region defined by an ordered list of vertices.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| points | [RegionPoint](#zen_api.lm.acquisition.v2.RegionPoint) | repeated | The ordered list of ZenApi.LM.Acquisition.V2.RegionPoint instances that define the vertices of the polygon. Each point specifies an (X, Y) coordinate in the region's coordinate space. The polygon is formed by connecting each consecutive point in the list, and finally connecting the last point back to the first to close the shape. |

### RegionRectangle

Represents a rectangular region within the scan area.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| rectangle | [RegionRect](#zen_api.lm.acquisition.v2.RegionRect) |  | The ZenApi.LM.Acquisition.V2.RegionRect that defines the position and size of the rectangular region within the scan area. |

## zen\_api/lm/acquisition/v2/region\_point.proto

[Top](#title)

### RegionPoint

Represents a two-dimensional point with X and Y coordinates for use in region-based acquisition scenarios.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [double](#double) |  | The X coordinate of the point. |
| y | [double](#double) |  | The Y coordinate of the point. |

## zen\_api/lm/acquisition/v2/region\_rect.proto

[Top](#title)

### RegionRect

Represents a rectangular region defined by its left (X), top (Y) coordinates, width, and height.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| x | [double](#double) |  | The left coordinate of the rectangle. |
| y | [double](#double) |  | The top coordinate of the rectangle. |
| width | [double](#double) |  | The width of the rectangle. |
| height | [double](#double) |  | The height of the rectangle. |

## zen\_api/lm/hardware/v1/configured\_container\_info.proto

[Top](#title)

### ConfiguredContainerInfo

Contains the information about a configured container in an experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| container\_name | [string](#string) |  | The name of the container (e.g., "B1"). |
| is\_activated | [bool](#bool) |  | A value indicating whether the container is activated or not. |

## zen\_api/lm/hardware/v1/focus\_service.proto

[Top](#title)

### FocusServiceGetAccelerationRequest

The FocusServiceGetAccelerationRequest class.

### FocusServiceGetAccelerationResponse

Acceleration of the focus in %.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [double](#double) |  | The acceleration in %. |

### FocusServiceGetPositionRequest

The FocusServiceGetPositionRequest class.

### FocusServiceGetPositionResponse

Position of the focus in µm.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [double](#double) |  | The position in µm. |

### FocusServiceGetSpeedRequest

The FocusServiceGetSpeedRequest class.

### FocusServiceGetSpeedResponse

Speed of the focus in %.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [double](#double) |  | The speed in %. |

### FocusServiceMoveToRequest

The FocusServiceMoveToRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [double](#double) |  | New position in µm. |

### FocusServiceMoveToResponse

Describes the result of a Focus.MoveTo request.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| position\_changed | [bool](#bool) |  | A value indicating whether the position was changed. |

### FocusServiceSetAccelerationRequest

The FocusServiceSetAccelerationRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| acceleration | [double](#double) |  | Acceleration in percent, i.e. values from range [0;100]. |

### FocusServiceSetAccelerationResponse

The FocusServiceSetAccelerationResponse class.

### FocusServiceSetSpeedRequest

The FocusServiceSetSpeedRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| speed | [double](#double) |  | Speed in percent, i.e. values from range [0;100]. |

### FocusServiceSetSpeedResponse

The FocusServiceSetSpeedResponse class.

### FocusServiceStopRequest

The FocusServiceStopRequest class.

### FocusServiceStopResponse

The FocusServiceStopResponse class.

### FocusService

The IFocusService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetAcceleration | [FocusServiceGetAccelerationRequest](#zen_api.lm.hardware.v1.FocusServiceGetAccelerationRequest) | [FocusServiceGetAccelerationResponse](#zen_api.lm.hardware.v1.FocusServiceGetAccelerationResponse) | Gets the focus acceleration. |
|  | GetPosition | [FocusServiceGetPositionRequest](#zen_api.lm.hardware.v1.FocusServiceGetPositionRequest) | [FocusServiceGetPositionResponse](#zen_api.lm.hardware.v1.FocusServiceGetPositionResponse) | Gets the focus position. |
|  | GetSpeed | [FocusServiceGetSpeedRequest](#zen_api.lm.hardware.v1.FocusServiceGetSpeedRequest) | [FocusServiceGetSpeedResponse](#zen_api.lm.hardware.v1.FocusServiceGetSpeedResponse) | Gets the focus speed. |
|  | MoveTo | [FocusServiceMoveToRequest](#zen_api.lm.hardware.v1.FocusServiceMoveToRequest) | [FocusServiceMoveToResponse](#zen_api.lm.hardware.v1.FocusServiceMoveToResponse) | Moves the focus to the given position in µm. |
|  | SetAcceleration | [FocusServiceSetAccelerationRequest](#zen_api.lm.hardware.v1.FocusServiceSetAccelerationRequest) | [FocusServiceSetAccelerationResponse](#zen_api.lm.hardware.v1.FocusServiceSetAccelerationResponse) | Sets the acceleration of the focus in percent. |
|  | SetSpeed | [FocusServiceSetSpeedRequest](#zen_api.lm.hardware.v1.FocusServiceSetSpeedRequest) | [FocusServiceSetSpeedResponse](#zen_api.lm.hardware.v1.FocusServiceSetSpeedResponse) | Sets the speed of the focus in percent. |
|  | Stop | [FocusServiceStopRequest](#zen_api.lm.hardware.v1.FocusServiceStopRequest) | [FocusServiceStopResponse](#zen_api.lm.hardware.v1.FocusServiceStopResponse) | Stops the focus if it is moving. |

## zen\_api/lm/hardware/v1/sample\_carrier\_service.proto

[Top](#title)

### SampleCarrierServiceActivateContainerRangeRequest

The SampleCarrierServiceActivateContainerRangeRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment ID. |
| start\_container\_name | [string](#string) |  | Name of the container where the range starts (e.g., "C3"). |
| end\_container\_name | [string](#string) |  | Name of the container where the range ends (e.g., "D8"). |

### SampleCarrierServiceActivateContainerRangeResponse

The SampleCarrierServiceActivateContainerRangeResponse class.

### SampleCarrierServiceActivateContainerRequest

The SampleCarrierServiceActivateContainerRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment ID. |
| container\_name | [string](#string) |  | Name of the container (e.g., "B1"). |

### SampleCarrierServiceActivateContainerResponse

The SampleCarrierServiceActivateContainerResponse class.

### SampleCarrierServiceActivateContainersRequest

The SampleCarrierServiceActivateContainersRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment ID. |
| container\_names | [string](#string) | repeated | Names of the containers (e.g., ["A1", "A2", "B7"]). |

### SampleCarrierServiceActivateContainersResponse

The SampleCarrierServiceActivateContainersResponse class.

### SampleCarrierServiceDeactivateContainerRangeRequest

The SampleCarrierServiceDeactivateContainerRangeRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment ID. |
| start\_container\_name | [string](#string) |  | Name of the container where the range starts (e.g., "C3"). |
| end\_container\_name | [string](#string) |  | Name of the container where the range ends (e.g., "D8"). |

### SampleCarrierServiceDeactivateContainerRangeResponse

The SampleCarrierServiceDeactivateContainerRangeResponse class.

### SampleCarrierServiceDeactivateContainerRequest

The SampleCarrierServiceDeactivateContainerRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment ID. |
| container\_name | [string](#string) |  | Name of the container (e.g., "B1"). |

### SampleCarrierServiceDeactivateContainerResponse

The SampleCarrierServiceDeactivateContainerResponse class.

### SampleCarrierServiceDeactivateContainersRequest

The SampleCarrierServiceDeactivateContainersRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment ID. |
| container\_names | [string](#string) | repeated | Names of the containers (e.g., ["A1", "A2", "B7"]). |

### SampleCarrierServiceDeactivateContainersResponse

The SampleCarrierServiceDeactivateContainersResponse class.

### SampleCarrierServiceGetConfiguredContainersRequest

The SampleCarrierServiceGetConfiguredContainersRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| experiment\_id | [string](#string) |  | Experiment ID. |

### SampleCarrierServiceGetConfiguredContainersResponse

Contains the information about the configured containers in an experiment.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| configured\_containers | [ConfiguredContainerInfo](#zen_api.lm.hardware.v1.ConfiguredContainerInfo) | repeated | The information about the configured containers in an experiment. |

### SampleCarrierServiceGetCurrentContainerRequest

The SampleCarrierServiceGetCurrentContainerRequest class.

### SampleCarrierServiceGetCurrentContainerResponse

Contains the information in which container of the sample carrier the stage is positioned at.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| row\_index | [int32](#int32) |  | The row index of the container in the sample carrier (starts with index 0). |
| column\_index | [int32](#int32) |  | The column index of the container in the sample carrier (starts with index 0). |

### SampleCarrierServiceGetInfoRequest

The SampleCarrierServiceGetInfoRequest class.

### SampleCarrierServiceGetInfoResponse

Contains the sample carrier information.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| rows | [int32](#int32) |  | The number of rows in the sample carrier. |
| columns | [int32](#int32) |  | The number of columns in the sample carrier. |
| name | [string](#string) |  | The name of the sample carrier. |
| material | [string](#string) |  | The bottom material which is used for this sample carrier. |
| thickness | [double](#double) |  | The bottom thickness of this sample carrier (in meters). |
| skirt | [double](#double) |  | The skirt (i.e. bottom offset) of this sample carrier (in meters). |
| refractive\_index | [double](#double) |  | The refractive index of the bottom material of this sample carrier. |

### SampleCarrierServiceMoveToContainerRequest

The SampleCarrierServiceMoveToContainerRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| row\_index | [int32](#int32) |  | The row index of the container (starts with index 0). |
| column\_index | [int32](#int32) |  | The column index of the container (starts with index 0). |

### SampleCarrierServiceMoveToContainerResponse

The SampleCarrierServiceMoveToContainerResponse class.

### SampleCarrierService

The ISampleCarrierService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | ActivateContainer | [SampleCarrierServiceActivateContainerRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceActivateContainerRequest) | [SampleCarrierServiceActivateContainerResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceActivateContainerResponse) | Activates a tile region or position that is placed in the specified container. |
|  | ActivateContainerRange | [SampleCarrierServiceActivateContainerRangeRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceActivateContainerRangeRequest) | [SampleCarrierServiceActivateContainerRangeResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceActivateContainerRangeResponse) | Activates all tile regions and/or positions that are placed in the specified container range (e.g., "C3-D8"). |
|  | ActivateContainers | [SampleCarrierServiceActivateContainersRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceActivateContainersRequest) | [SampleCarrierServiceActivateContainersResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceActivateContainersResponse) | Activates all tile regions and/or positions that are placed in the specified containers (e.g., ["A1", "A2", "B7"]). |
|  | DeactivateContainer | [SampleCarrierServiceDeactivateContainerRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceDeactivateContainerRequest) | [SampleCarrierServiceDeactivateContainerResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceDeactivateContainerResponse) | Deactivates a tile region or position that is placed in the specified container. |
|  | DeactivateContainerRange | [SampleCarrierServiceDeactivateContainerRangeRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceDeactivateContainerRangeRequest) | [SampleCarrierServiceDeactivateContainerRangeResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceDeactivateContainerRangeResponse) | Deactivates all tile regions and/or positions that are placed in the specified container range (e.g., "C3-D8"). |
|  | DeactivateContainers | [SampleCarrierServiceDeactivateContainersRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceDeactivateContainersRequest) | [SampleCarrierServiceDeactivateContainersResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceDeactivateContainersResponse) | Deactivates all tile regions and/or positions that are placed in the specified containers (e.g., ["A1", "A2", "B7"]). |
|  | GetConfiguredContainers | [SampleCarrierServiceGetConfiguredContainersRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceGetConfiguredContainersRequest) | [SampleCarrierServiceGetConfiguredContainersResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceGetConfiguredContainersResponse) | Gets the information about the configured containers in an experiment. |
|  | GetCurrentContainer | [SampleCarrierServiceGetCurrentContainerRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceGetCurrentContainerRequest) | [SampleCarrierServiceGetCurrentContainerResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceGetCurrentContainerResponse) | Gets the information in which container of the sample carrier the stage is positioned at. Note that the stage might not be positioned exactly in the center of the container. |
|  | GetInfo | [SampleCarrierServiceGetInfoRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceGetInfoRequest) | [SampleCarrierServiceGetInfoResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceGetInfoResponse) | Gets the information of the currently inserted sample carrier. |
|  | MoveToContainer | [SampleCarrierServiceMoveToContainerRequest](#zen_api.lm.hardware.v1.SampleCarrierServiceMoveToContainerRequest) | [SampleCarrierServiceMoveToContainerResponse](#zen_api.lm.hardware.v1.SampleCarrierServiceMoveToContainerResponse) | Move the stage to a sample holder container. |

## zen\_api/lm/hardware/v2/camera\_service.proto

[Top](#title)

### CameraServiceConfigureCameraRequest

The CameraServiceConfigureCameraRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| data | [SetCameraData](#zen_api.lm.hardware.v2.SetCameraData) |  | New configuration data. |

### CameraServiceConfigureCameraResponse

Describes the result of a configure camera request.

### CameraServiceGetAllCamerasResponse

A list of available cameras.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| cameras | [GetCameraData](#zen_api.lm.hardware.v2.GetCameraData) | repeated | The cameras. |

### CameraServiceGetCameraRequest

The CameraServiceGetCameraRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| id | [string](#string) |  | Id of the camera. |

### CameraServiceGetCameraResponse

Position index of the camera.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| camera | [GetCameraData](#zen_api.lm.hardware.v2.GetCameraData) |  | The position index. |

### CameraServiceGetCamerasRequest

The CameraServiceGetCamerasRequest class.

### CameraService

The ICameraService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | ConfigureCamera | [CameraServiceConfigureCameraRequest](#zen_api.lm.hardware.v2.CameraServiceConfigureCameraRequest) | [CameraServiceConfigureCameraResponse](#zen_api.lm.hardware.v2.CameraServiceConfigureCameraResponse) | Configures a camera based on the given data. |
|  | GetCamera | [CameraServiceGetCameraRequest](#zen_api.lm.hardware.v2.CameraServiceGetCameraRequest) | [CameraServiceGetCameraResponse](#zen_api.lm.hardware.v2.CameraServiceGetCameraResponse) | Gets the camera by id. |
|  | GetCameras | [CameraServiceGetCamerasRequest](#zen_api.lm.hardware.v2.CameraServiceGetCamerasRequest) | [CameraServiceGetAllCamerasResponse](#zen_api.lm.hardware.v2.CameraServiceGetAllCamerasResponse) | Gets the cameras. |

## zen\_api/lm/hardware/v2/filter\_data.proto

[Top](#title)

### FilterData

Describes a filter.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| name | [string](#string) |  | The name/ id of the filter. |
| id | [string](#string) |  | The id. |
| is\_present | [bool](#bool) |  | A value indicating whether the filter is present. |
| position | [int32](#int32) |  | The position index, starting at 1. |

## zen\_api/lm/hardware/v2/filter\_wheel\_service.proto

[Top](#title)

### FilterWheelServiceGetFiltersRequest

The FilterWheelServiceGetFiltersRequest class.

### FilterWheelServiceGetFiltersResponse

A list of available filters.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| filters | [FilterData](#zen_api.lm.hardware.v2.FilterData) | repeated | The filters. |

### FilterWheelServiceGetPositionRequest

The FilterWheelServiceGetPositionRequest class.

### FilterWheelServiceGetPositionResponse

Position index of the filter wheel.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [int32](#int32) |  | The position index. |

### FilterWheelServiceMoveToRequest

The FilterWheelServiceMoveToRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| position\_index | [int32](#int32) |  | New position index. |

### FilterWheelServiceMoveToResponse

Describes the result of a filter wheel MoveTo request.

### FilterWheelService

The IFilterWheelService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetFilters | [FilterWheelServiceGetFiltersRequest](#zen_api.lm.hardware.v2.FilterWheelServiceGetFiltersRequest) | [FilterWheelServiceGetFiltersResponse](#zen_api.lm.hardware.v2.FilterWheelServiceGetFiltersResponse) | Gets the filters. |
|  | GetPosition | [FilterWheelServiceGetPositionRequest](#zen_api.lm.hardware.v2.FilterWheelServiceGetPositionRequest) | [FilterWheelServiceGetPositionResponse](#zen_api.lm.hardware.v2.FilterWheelServiceGetPositionResponse) | Gets the filter wheel position, starting at 1. |
|  | MoveTo | [FilterWheelServiceMoveToRequest](#zen_api.lm.hardware.v2.FilterWheelServiceMoveToRequest) | [FilterWheelServiceMoveToResponse](#zen_api.lm.hardware.v2.FilterWheelServiceMoveToResponse) | Moves the filter wheel to the given position index. |

## zen\_api/lm/hardware/v2/focus\_service.proto

[Top](#title)

### FocusServiceGetAccelerationRequest

The FocusServiceGetAccelerationRequest class.

### FocusServiceGetAccelerationResponse

Acceleration of the focus in %.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [double](#double) |  | The acceleration in %. |

### FocusServiceGetPositionRequest

The FocusServiceGetPositionRequest class.

### FocusServiceGetPositionResponse

Position of the focus in meters.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [double](#double) |  | The position in meters. |

### FocusServiceGetSpeedRequest

The FocusServiceGetSpeedRequest class.

### FocusServiceGetSpeedResponse

Speed of the focus in %.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [double](#double) |  | The speed in %. |

### FocusServiceMoveToRequest

The FocusServiceMoveToRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [double](#double) |  | New position in meters. |

### FocusServiceMoveToResponse

Describes the result of a Focus.MoveTo request.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| position\_changed | [bool](#bool) |  | A value indicating whether the position was changed. |

### FocusServiceSetAccelerationRequest

The FocusServiceSetAccelerationRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| acceleration | [double](#double) |  | Acceleration in percent, i.e. values from range [0;100]. |

### FocusServiceSetAccelerationResponse

The FocusServiceSetAccelerationResponse class.

### FocusServiceSetSpeedRequest

The FocusServiceSetSpeedRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| speed | [double](#double) |  | Speed in percent, i.e. values from range [0;100]. |

### FocusServiceSetSpeedResponse

The FocusServiceSetSpeedResponse class.

### FocusServiceStopRequest

The FocusServiceStopRequest class.

### FocusServiceStopResponse

The FocusServiceStopResponse class.

### FocusService

The IFocusService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetAcceleration | [FocusServiceGetAccelerationRequest](#zen_api.lm.hardware.v2.FocusServiceGetAccelerationRequest) | [FocusServiceGetAccelerationResponse](#zen_api.lm.hardware.v2.FocusServiceGetAccelerationResponse) | Gets the focus acceleration. |
|  | GetPosition | [FocusServiceGetPositionRequest](#zen_api.lm.hardware.v2.FocusServiceGetPositionRequest) | [FocusServiceGetPositionResponse](#zen_api.lm.hardware.v2.FocusServiceGetPositionResponse) | Gets the focus position. |
|  | GetSpeed | [FocusServiceGetSpeedRequest](#zen_api.lm.hardware.v2.FocusServiceGetSpeedRequest) | [FocusServiceGetSpeedResponse](#zen_api.lm.hardware.v2.FocusServiceGetSpeedResponse) | Gets the focus speed. |
|  | MoveTo | [FocusServiceMoveToRequest](#zen_api.lm.hardware.v2.FocusServiceMoveToRequest) | [FocusServiceMoveToResponse](#zen_api.lm.hardware.v2.FocusServiceMoveToResponse) | Moves the focus to the given position in meters. |
|  | SetAcceleration | [FocusServiceSetAccelerationRequest](#zen_api.lm.hardware.v2.FocusServiceSetAccelerationRequest) | [FocusServiceSetAccelerationResponse](#zen_api.lm.hardware.v2.FocusServiceSetAccelerationResponse) | Sets the acceleration of the focus in percent. |
|  | SetSpeed | [FocusServiceSetSpeedRequest](#zen_api.lm.hardware.v2.FocusServiceSetSpeedRequest) | [FocusServiceSetSpeedResponse](#zen_api.lm.hardware.v2.FocusServiceSetSpeedResponse) | Sets the speed of the focus in percent. |
|  | Stop | [FocusServiceStopRequest](#zen_api.lm.hardware.v2.FocusServiceStopRequest) | [FocusServiceStopResponse](#zen_api.lm.hardware.v2.FocusServiceStopResponse) | Stops the focus if it is moving. |

## zen\_api/lm/hardware/v2/get\_camera\_data.proto

[Top](#title)

### GetCameraData

Describes a camera.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| name | [string](#string) |  | The Name. |
| id | [string](#string) |  | The Id. |
| is\_preset | [bool](#bool) |  | A value indicating whether the camera is preset. |
| exposure\_time | [double](#double) |  | The ExposureTime. |
| min\_exposure\_time | [double](#double) |  | The MinExposureTime. |
| max\_exposure\_time | [double](#double) |  | The MaxExposureTime. |
| binning | [int32](#int32) |  | The Binning. |
| binning\_description | [string](#string) |  | The BinningDescription. |
| available\_binnings | [string](#string) | repeated | The AvailableBinnings. |
| frame | [zen\_api.common.v1.DoubleFrame](#zen_api.common.v1.DoubleFrame) |  | The Frame. |
| max\_frame\_size | [zen\_api.common.v1.DoubleSize](#zen_api.common.v1.DoubleSize) |  | The MaxFrameWidth. |

## zen\_api/lm/hardware/v2/objective\_changer\_immersion\_types.proto

[Top](#title)

### ObjectiveChangerImmersionTypes

Immersion types to match ObjectiveImmersionTypes

| Name | Number | Description |
| --- | --- | --- |
| OBJECTIVE\_CHANGER\_IMMERSION\_TYPES\_UNSPECIFIED | 0 | Unspecified |
| OBJECTIVE\_CHANGER\_IMMERSION\_TYPES\_AIR | 1 | Air |
| OBJECTIVE\_CHANGER\_IMMERSION\_TYPES\_WATER | 2 | Water |
| OBJECTIVE\_CHANGER\_IMMERSION\_TYPES\_OIL | 4 | Oil |
| OBJECTIVE\_CHANGER\_IMMERSION\_TYPES\_GLYCERINE | 8 | Glycerin |
| OBJECTIVE\_CHANGER\_IMMERSION\_TYPES\_SILICONE | 16 | Silicone |
| OBJECTIVE\_CHANGER\_IMMERSION\_TYPES\_HIOIL | 32 | HI Oil |
| OBJECTIVE\_CHANGER\_IMMERSION\_TYPES\_POLYOL | 64 | Polyol |

## zen\_api/lm/hardware/v2/objective\_changer\_service.proto

[Top](#title)

### ObjectiveChangerServiceGetObjectivesRequest

The ObjectiveChangerServiceGetObjectivesRequest class.

### ObjectiveChangerServiceGetObjectivesResponse

A list of available objectives.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| objectives | [ObjectiveData](#zen_api.lm.hardware.v2.ObjectiveData) | repeated | The objectives. |

### ObjectiveChangerServiceGetPositionRequest

The ObjectiveChangerServiceGetPositionRequest class.

### ObjectiveChangerServiceGetPositionResponse

Position index of the objective.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [int32](#int32) |  | The position index. |

### ObjectiveChangerServiceMoveToRequest

The ObjectiveChangerServiceMoveToRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| position\_index | [int32](#int32) |  | New position index. |

### ObjectiveChangerServiceMoveToResponse

Describes the result of a ObjectiveChanger.MoveTo request.

### ObjectiveChangerService

The IObjectiveChangerService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetObjectives | [ObjectiveChangerServiceGetObjectivesRequest](#zen_api.lm.hardware.v2.ObjectiveChangerServiceGetObjectivesRequest) | [ObjectiveChangerServiceGetObjectivesResponse](#zen_api.lm.hardware.v2.ObjectiveChangerServiceGetObjectivesResponse) | Gets the objectives |
|  | GetPosition | [ObjectiveChangerServiceGetPositionRequest](#zen_api.lm.hardware.v2.ObjectiveChangerServiceGetPositionRequest) | [ObjectiveChangerServiceGetPositionResponse](#zen_api.lm.hardware.v2.ObjectiveChangerServiceGetPositionResponse) | Gets the objective position. |
|  | MoveTo | [ObjectiveChangerServiceMoveToRequest](#zen_api.lm.hardware.v2.ObjectiveChangerServiceMoveToRequest) | [ObjectiveChangerServiceMoveToResponse](#zen_api.lm.hardware.v2.ObjectiveChangerServiceMoveToResponse) | Moves the objective to the given position index. |

## zen\_api/lm/hardware/v2/objective\_data.proto

[Top](#title)

### ObjectiveData

Describes an objective.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| name | [string](#string) |  | The name. |
| na | [double](#double) |  | The Numerical Apperture. |
| immersion\_type | [ObjectiveChangerImmersionTypes](#zen_api.lm.hardware.v2.ObjectiveChangerImmersionTypes) |  | The immersion type. |
| magnification | [double](#double) |  | The magnification. |
| position | [int32](#int32) |  | The position index. |

## zen\_api/lm/hardware/v2/optovar\_data.proto

[Top](#title)

### OptovarData

Describes an optovar.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| name | [string](#string) |  | The name. |
| magnification | [double](#double) |  | The magnification. |
| position | [int32](#int32) |  | The position index. |

## zen\_api/lm/hardware/v2/optovar\_service.proto

[Top](#title)

### OptovarServiceGetOptovarsRequest

The OptovarServiceGetOptovarsRequest class.

### OptovarServiceGetOptovarsResponse

A list of available optovars.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| optovars | [OptovarData](#zen_api.lm.hardware.v2.OptovarData) | repeated | The optovars. |

### OptovarServiceGetPositionRequest

The OptovarServiceGetPositionRequest class.

### OptovarServiceGetPositionResponse

Position index of the optovar.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [int32](#int32) |  | The position index. |

### OptovarServiceMoveToRequest

The OptovarServiceMoveToRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| position\_index | [int32](#int32) |  | New position index. |

### OptovarServiceMoveToResponse

Describes the result of a Optovar.MoveTo request.

### OptovarService

The IOptovarService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetOptovars | [OptovarServiceGetOptovarsRequest](#zen_api.lm.hardware.v2.OptovarServiceGetOptovarsRequest) | [OptovarServiceGetOptovarsResponse](#zen_api.lm.hardware.v2.OptovarServiceGetOptovarsResponse) | Gets the optovars. |
|  | GetPosition | [OptovarServiceGetPositionRequest](#zen_api.lm.hardware.v2.OptovarServiceGetPositionRequest) | [OptovarServiceGetPositionResponse](#zen_api.lm.hardware.v2.OptovarServiceGetPositionResponse) | Gets the optovar position. |
|  | MoveTo | [OptovarServiceMoveToRequest](#zen_api.lm.hardware.v2.OptovarServiceMoveToRequest) | [OptovarServiceMoveToResponse](#zen_api.lm.hardware.v2.OptovarServiceMoveToResponse) | Moves the optovar to the given position index. |

## zen\_api/lm/hardware/v2/reflector\_changer\_service.proto

[Top](#title)

### ReflectorChangerServiceGetPositionRequest

The ReflectorChangerServiceGetPositionRequest class.

### ReflectorChangerServiceGetPositionResponse

Position index of the objective.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| value | [int32](#int32) |  | The position index. |

### ReflectorChangerServiceGetReflectorsRequest

The ReflectorChangerServiceGetReflectorsRequest class.

### ReflectorChangerServiceGetReflectorsResponse

A list of available objectives.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| reflectors | [ReflectorData](#zen_api.lm.hardware.v2.ReflectorData) | repeated | The objectives. |

### ReflectorChangerServiceMoveToRequest

The ReflectorChangerServiceMoveToRequest class.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| position\_index | [int32](#int32) |  | New position index. |

### ReflectorChangerServiceMoveToResponse

Describes the result of a ReflectorChanger.MoveTo request.

### ReflectorChangerService

The IReflectorChangerService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetPosition | [ReflectorChangerServiceGetPositionRequest](#zen_api.lm.hardware.v2.ReflectorChangerServiceGetPositionRequest) | [ReflectorChangerServiceGetPositionResponse](#zen_api.lm.hardware.v2.ReflectorChangerServiceGetPositionResponse) | Gets the reflector position. |
|  | GetReflectors | [ReflectorChangerServiceGetReflectorsRequest](#zen_api.lm.hardware.v2.ReflectorChangerServiceGetReflectorsRequest) | [ReflectorChangerServiceGetReflectorsResponse](#zen_api.lm.hardware.v2.ReflectorChangerServiceGetReflectorsResponse) | Gets the reflectors. |
|  | MoveTo | [ReflectorChangerServiceMoveToRequest](#zen_api.lm.hardware.v2.ReflectorChangerServiceMoveToRequest) | [ReflectorChangerServiceMoveToResponse](#zen_api.lm.hardware.v2.ReflectorChangerServiceMoveToResponse) | Moves the reflector changer to the given position index. |

## zen\_api/lm/hardware/v2/reflector\_data.proto

[Top](#title)

### ReflectorData

Describes a reflector.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| name | [string](#string) |  | The name. |
| position | [int32](#int32) |  | The position index. |

## zen\_api/lm/hardware/v2/set\_camera\_data.proto

[Top](#title)

### SetCameraData

Describes the info needed to set a camera.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| id | [string](#string) |  | The Id. |
| exposure\_time | [double](#double) |  | The ExposureTime. |
| binning | [int32](#int32) |  | The Binning. |
| frame | [zen\_api.common.v1.DoubleFrame](#zen_api.common.v1.DoubleFrame) |  | The Frame. |

## zen\_api/lm/live\_scan/v1/live\_scan\_service.proto

[Top](#title)

### LiveScanServiceEjectTrayRequest

The LiveScanServiceEjectTrayRequest class.

### LiveScanServiceEjectTrayResponse

Empty response upon ejecting the tray.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| notifications | [string](#string) | repeated | The list of notifications. |

### LiveScanServiceGetConfigurationRequest

The LiveScanServiceGetConfigurationRequest class.

### LiveScanServiceGetConfigurationResponse

Request for getting the configuration.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| config | [LiveScanServiceConfiguration](#zen_api.lm.live_scan.v1.LiveScanServiceConfiguration) |  | Configuration. |

### LiveScanServiceLoadTrayAndPrescanRequest

The LiveScanServiceLoadTrayAndPrescanRequest class.

### LiveScanServiceLoadTrayAndPrescanResponse

Empty response upon loading the tray.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| notifications | [string](#string) | repeated | The list of notifications. |

### LiveScanServiceSetConfigurationRequest

Request for setting the configuration.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| config | [LiveScanServiceConfiguration](#zen_api.lm.live_scan.v1.LiveScanServiceConfiguration) |  | Configuration. |

### LiveScanServiceSetConfigurationResponse

Empty response upon setting the configuration.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| notifications | [string](#string) | repeated | The list of notifications. |

### LiveScanService

The ILiveScanService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | EjectTray | [LiveScanServiceEjectTrayRequest](#zen_api.lm.live_scan.v1.LiveScanServiceEjectTrayRequest) | [LiveScanServiceEjectTrayResponse](#zen_api.lm.live_scan.v1.LiveScanServiceEjectTrayResponse) | Eject tray. |
|  | GetConfiguration | [LiveScanServiceGetConfigurationRequest](#zen_api.lm.live_scan.v1.LiveScanServiceGetConfigurationRequest) | [LiveScanServiceGetConfigurationResponse](#zen_api.lm.live_scan.v1.LiveScanServiceGetConfigurationResponse) | Get configuration. |
|  | LoadTrayAndPrescan | [LiveScanServiceLoadTrayAndPrescanRequest](#zen_api.lm.live_scan.v1.LiveScanServiceLoadTrayAndPrescanRequest) | [LiveScanServiceLoadTrayAndPrescanResponse](#zen_api.lm.live_scan.v1.LiveScanServiceLoadTrayAndPrescanResponse) | Load tray and start prescan. |
|  | SetConfiguration | [LiveScanServiceSetConfigurationRequest](#zen_api.lm.live_scan.v1.LiveScanServiceSetConfigurationRequest) | [LiveScanServiceSetConfigurationResponse](#zen_api.lm.live_scan.v1.LiveScanServiceSetConfigurationResponse) | Set configuration. |

## zen\_api/lm/live\_scan/v1/live\_scan\_service\_configuration.proto

[Top](#title)

### LiveScanServiceConfiguration

Response object representing the configuration.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| sample\_holder\_template | [string](#string) |  | Gets the type template. |
| live\_scan\_detection | [bool](#bool) |  | Gets a value indicating whether sample carrier detection is active. |
| measure\_bottom\_thickness | [bool](#bool) |  | Gets a value indicating whether bottom thickness has to be measured. |
| determine\_bottom\_material | [bool](#bool) |  | Gets a value indicating whether bottom material determination is active. |
| create\_carrier\_overview | [bool](#bool) |  | Gets a value indicating whether sample carrier detection is active. |
| read\_barcodes | [bool](#bool) |  | Gets a value indicating whether barcodes must be read. |
| use\_left\_barcode | [bool](#bool) |  | Gets a value indicating whether the left barcode must be read. |
| use\_right\_barcode | [bool](#bool) |  | Gets a value indicating whether the right barcode must be read. |
| automatic\_live\_scan\_calibration | [bool](#bool) |  | Gets a value indicating whether automatic sample carrier calibration is active. |
| refractive\_index | [double](#double) |  | The refractive index of the bottom material of this sample carrier. |
| material | [string](#string) |  | The bottom material of this sample carrier. |

## zen\_api/lm/slide\_scan/v1/channel\_settings.proto

[Top](#title)

### ChannelSettings

Settings for a channel.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| channel\_identifier | [string](#string) |  | The identifier for the master channel. |
| channel\_name | [string](#string) |  | The name for the channel. |
| channel\_description | [string](#string) |  | The description for the channel. |
| dye\_name | [string](#string) |  | The fluorescence dye. |
| intensity | [double](#double) |  | The lamp intensity that should be used for a channel. The intensity is set in percent. (Values ranging from 0 to 100). |
| exposure\_time | [double](#double) |  | The exposure time that should be used for a channel. The exposure time is set in milliseconds. (Values ranging from 0.1 to 2000ms). |

## zen\_api/lm/slide\_scan/v1/information\_base.proto

[Top](#title)

### InformationBase

Base class for all information types.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| simple\_information | [SimpleInformation](#zen_api.lm.slide_scan.v1.SimpleInformation) |  |  |
| slide\_scan\_system\_information | [SlideScanSystemInformation](#zen_api.lm.slide_scan.v1.SlideScanSystemInformation) |  |  |
| magazine\_information | [MagazineInformation](#zen_api.lm.slide_scan.v1.MagazineInformation) |  |  |

### MagazineInformation

Data container for inforamtion about the magazine state.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| is\_door\_closed | [bool](#bool) |  | A value indicating whether the Axioscan tray door is closed. |
| trays | [TrayInformation](#zen_api.lm.slide_scan.v1.TrayInformation) | repeated | The magazine state by providing the list of available trays. |

### SimpleInformation

Data container for a simple message inforamtion.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| message | [string](#string) |  | The simple string message. |

### SlideScanSystemInformation

Data container for information about the hardware state.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| is\_idle | [bool](#bool) |  | A value indicating whether an Axioscan system is idle. |
| is\_scan\_running | [bool](#bool) |  | A value indicating whether a scan is running. |
| is\_preview\_scan\_running | [bool](#bool) |  | A value indicating whether a preview scan is running. |
| is\_tray\_initializing | [bool](#bool) |  | A value indicating whether a tray is being initialized. |

## zen\_api/lm/slide\_scan/v1/profile\_information.proto

[Top](#title)

### ProfileInformation

ProfileInformation contains information about the scan profile associated with a specific slide.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| profile\_name | [string](#string) |  | The profile name associated with the slides acquisition. |

## zen\_api/lm/slide\_scan/v1/region\_definition.proto

[Top](#title)

### RegionDefinition

Represents definition of scan region.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| contour | [zen\_api.lm.acquisition.v2.RegionContour](#zen_api.lm.acquisition.v2.RegionContour) |  | The region contour definition. The type of the contour can be: ZenApi.LM.Acquisition.V2.RegionRectangle, ZenApi.LM.Acquisition.V2.RegionEllipse or ZenApi.LM.Acquisition.V2.RegionPolygon. |

## zen\_api/lm/slide\_scan/v1/response\_code.proto

[Top](#title)

### ResponseCode

Numerical result code.

| Name | Number | Description |
| --- | --- | --- |
| RESPONSE\_CODE\_UNSPECIFIED | 0 | Default value if the status is not specified. |
| RESPONSE\_CODE\_INVALID\_ARGUMENT | 1 | The required parameter is missing. |
| RESPONSE\_CODE\_NOT\_FOUND | 2 | The requested resource could not be found. |
| RESPONSE\_CODE\_NOT\_ALLOWED | 3 | The operation is not allowed. |

## zen\_api/lm/slide\_scan/v1/response\_type.proto

[Top](#title)

### ResponseType

Kind of failure with implication to error recovery.

| Name | Number | Description |
| --- | --- | --- |
| RESPONSE\_TYPE\_UNSPECIFIED | 0 | Default value if the ResponseType is not specified. |
| RESPONSE\_TYPE\_SUCCESS | 1 | The API call is accepted and will be processed. In this case the response code can be unspecified. |
| RESPONSE\_TYPE\_WARNING | 2 | The API call is accepted and will be processed. In this case, the response contains an indication of possible problem settings. |
| RESPONSE\_TYPE\_FAILED | 3 | Something went wrong. This is the usual error type. |
| RESPONSE\_TYPE\_EXCEPTION | 4 | The call threw an exeption. |

## zen\_api/lm/slide\_scan/v1/scan\_profile\_options\_override.proto

[Top](#title)

### ScanProfileOptionsOverride

Data container for overriding options of a scan profile.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| make\_prescan\_preview | [google.protobuf.BoolValue](https://protobuf.dev/reference/protobuf/google.protobuf/#bool-value) |  | A value indicating whether the prescan preview should be made or only a preview with the preview cam. If set to perform a prescan, the prescan will be done according to existing settings in the scan profile without modifications (resp. default settings will be used). |
| use\_manual\_segmentation | [google.protobuf.BoolValue](https://protobuf.dev/reference/protobuf/google.protobuf/#bool-value) |  | A value indicating whether the segmentation mode shall be manual. If not set or set to false, the segmentation will be performed as defined in the scan profile. |
| disable\_label\_detection | [google.protobuf.BoolValue](https://protobuf.dev/reference/protobuf/google.protobuf/#bool-value) |  | A value indicating whether the label detection shall be disabled. If set to true, the barcode and ocr recognition will be disabled. If not set or set to false, the label detection will be performed as defined in the scan profile. |

## zen\_api/lm/slide\_scan/v1/slide\_information.proto

[Top](#title)

### SlideInformation

SlideInformation holds information about an Axioscan slide.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| slide\_on\_frame\_position | [int32](#int32) |  | The slide position on the frame - range [1, 4]. The maximum value depending on frame type. |
| state | [SlideState](#zen_api.lm.slide_scan.v1.SlideState) |  | The ZenApi.LM.SlideScan.V1.SlideState of the slide. |
| profile\_information | [ProfileInformation](#zen_api.lm.slide_scan.v1.ProfileInformation) |  | The corresponding ZenApi.LM.SlideScan.V1.SlideInformation.ProfileInformation of the slide. |
| is\_selected\_for\_processing | [bool](#bool) |  | A value indicating whether this slide is selected for processing. |
| barcode | [string](#string) |  | The barcode of the slide. |
| label\_image\_path | [string](#string) |  | The path to the label image. |
| preview\_image\_path | [string](#string) |  | The path to the preview image. |
| scan\_image\_path | [string](#string) |  | The path to the scan image. |
| state\_last\_error | [string](#string) |  | The SlideItem.LastError of the slide. |

## zen\_api/lm/slide\_scan/v1/slide\_position\_information.proto

[Top](#title)

### SlidePositionInformation

SlidePositionInformation holds information about an AxioScan slide position.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| slide\_on\_frame\_position | [int32](#int32) |  | The slide position on the frame - range [1, 4]. The maximum value depending on frame type. |
| tray\_position | [int32](#int32) |  | The position of the tray inside the Axioscan magazine in the range of [1, 26]. |
| image\_name | [string](#string) |  | The image name for the slide. |

## zen\_api/lm/slide\_scan/v1/slide\_scan\_service.proto

[Top](#title)

### GeneralResponse

A general response for all asynchronous requests that do not return any results or data.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| type | [ResponseType](#zen_api.lm.slide_scan.v1.ResponseType) |  | The type of resonse message. |
| code | [ResponseCode](#zen_api.lm.slide_scan.v1.ResponseCode) |  | The code of resonse message. |
| description | [string](#string) |  | A description. Explanation text, for developers only. |
| user\_message | [string](#string) |  | A message suitable to be shown in user interfaces, will be translated by Api. |

### SlideScanServiceGetChannelSettingsRequest

Describes the input parameters for retrieving the configured channels.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| scan\_profile\_path | [string](#string) |  | The path of the specified scan profile. |

### SlideScanServiceGetChannelSettingsResponse

Lists the configured channel settings in the specified scan profile.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| channel\_setting\_list | [ChannelSettings](#zen_api.lm.slide_scan.v1.ChannelSettings) | repeated | The configured channel settings. |

### SlideScanServiceGetMagazineStateRequest

Describes the input parameters for a call to retrieve the magazine state.

### SlideScanServiceGetMagazineStateResponse

Lists the populated slides of each tray.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| trays | [TrayInformation](#zen_api.lm.slide_scan.v1.TrayInformation) | repeated | The loaded slides per tray. |

### SlideScanServiceGetStorageFolderRequest

Describes the input parameters for a call to retrieve the storage folder for slide scans.

### SlideScanServiceGetStorageFolderResponse

Describes the result for a call to retrieve the storage folder for slide scans.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| path | [string](#string) |  | The storage folder path. |

### SlideScanServiceObserveRequest

Describes the input parameters for a call to observe the events and progress

that happen either during acquisition or while the microscope is idling.

### SlideScanServiceObserveResponse

Describes the output parameters for a call to observe the events, progress

and additional information like warnings and errors of a running scan profile acquisition.

The response might be a stream of different information types (e.g. Progress, Error, Hardware State, ...).

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| information | [InformationBase](#zen_api.lm.slide_scan.v1.InformationBase) |  | The flexible, variable information. |

### SlideScanServiceResetSlideStatesRequest

Describes the input parameters for resetting the state of specified slides to new.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| slide\_position\_list | [SlidePositionInformation](#zen_api.lm.slide_scan.v1.SlidePositionInformation) | repeated | The position of the slide list to be reset. |

### SlideScanServiceResetSlideStatesResponse

Describes the output parameters for resetting the state of specified slides.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| response | [GeneralResponse](#zen_api.lm.slide_scan.v1.GeneralResponse) |  | A general response about the success/error state of the request. |

### SlideScanServiceSetStorageFolderRequest

Describes the input parameters for setting the storage folder for slide scans.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| path | [string](#string) |  | The path to the storage folder where slide scans should be stored. |

### SlideScanServiceSetStorageFolderResponse

Describes the result for a call to set the storage folder.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| response | [GeneralResponse](#zen_api.lm.slide_scan.v1.GeneralResponse) |  | A general response to inform about the requests success/error state. |

### SlideScanServiceStartScanPreviewRequest

Describes the input parameters for the preview start.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| scan\_profile\_name | [string](#string) |  | The name of the scan profile that should be started. |
| slide\_position\_list | [SlidePositionInformation](#zen_api.lm.slide_scan.v1.SlidePositionInformation) | repeated | The list of tray/slides to be processed. |
| scan\_profile\_options\_override | [ScanProfileOptionsOverride](#zen_api.lm.slide_scan.v1.ScanProfileOptionsOverride) |  | Optional overrides for scan profile options. |

### SlideScanServiceStartScanPreviewResponse

Response of starting a preview in the slide scan service.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| response | [GeneralResponse](#zen_api.lm.slide_scan.v1.GeneralResponse) |  | A general response to inform about the requests success/error state. |

### SlideScanServiceStartScanProfileRequest

Describes the input parameters for the scan profile start.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| scan\_profile\_name | [string](#string) |  | The name of the scan profile that should be started. |
| slide\_position\_list | [SlidePositionInformation](#zen_api.lm.slide_scan.v1.SlidePositionInformation) | repeated | The list of tray/slides to be processed. |
| channel\_settings | [ChannelSettings](#zen_api.lm.slide_scan.v1.ChannelSettings) | repeated | The list of changed channel settings. |
| region\_definitions | [RegionDefinition](#zen_api.lm.slide_scan.v1.RegionDefinition) | repeated | The list of region contour definition. |
| scan\_profile\_options\_override | [ScanProfileOptionsOverride](#zen_api.lm.slide_scan.v1.ScanProfileOptionsOverride) |  | Optional overrides for scan profile options. |

### SlideScanServiceStartScanProfileResponse

Describes the output parameters for a call to start the scan profile.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| response | [GeneralResponse](#zen_api.lm.slide_scan.v1.GeneralResponse) |  | A general response to inform about the requests success/error state. |

### SlideScanServiceStopScanPreviewRequest

Represents a request to stop the preview in the SlideScan service.

### SlideScanServiceStopScanPreviewResponse

Represents the response for stopping the preview in the slide scan service.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| response | [GeneralResponse](#zen_api.lm.slide_scan.v1.GeneralResponse) |  | A general response to inform about the requests success/error state. |

### SlideScanServiceStopScanProfileRequest

Describes the input parameters for stopping the scan profile.

### SlideScanServiceStopScanProfileResponse

Describes the output parameters for a call to stop the scan profile.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| response | [GeneralResponse](#zen_api.lm.slide_scan.v1.GeneralResponse) |  | A general response to inform about the requests success/error state. |

### SlideScanServiceUnmarkSlidesRequest

Describes the input parameters for unmark slides.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| slide\_position\_list | [SlidePositionInformation](#zen_api.lm.slide_scan.v1.SlidePositionInformation) | repeated | The position of the slide list to be unmarked. |

### SlideScanServiceUnmarkSlidesResponse

Describes the output parameters for a call to unmark slides.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| response | [GeneralResponse](#zen_api.lm.slide_scan.v1.GeneralResponse) |  | A general response to inform about the requests success/error state. |

### SlideScanService

The ISlideScanService interface.

| Kind | Method Name | Request Type | Response Type | Description |
| --- | --- | --- | --- | --- |
|  | GetChannelSettings | [SlideScanServiceGetChannelSettingsRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceGetChannelSettingsRequest) | [SlideScanServiceGetChannelSettingsResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceGetChannelSettingsResponse) | Gets a list of configured channel settings of a scan profile. |
|  | GetMagazineState | [SlideScanServiceGetMagazineStateRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceGetMagazineStateRequest) | [SlideScanServiceGetMagazineStateResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceGetMagazineStateResponse) | Gets the magazine state. |
|  | GetStorageFolder | [SlideScanServiceGetStorageFolderRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceGetStorageFolderRequest) | [SlideScanServiceGetStorageFolderResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceGetStorageFolderResponse) | Gets the current storage folder for images. |
|  | Observe | [SlideScanServiceObserveRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceObserveRequest) | [SlideScanServiceObserveResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceObserveResponse) stream | Monitors anything that happens within ZEN or the microscope. The main purpose is to observe the scan profile acquisition progress. |
|  | ResetSlideStates | [SlideScanServiceResetSlideStatesRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceResetSlideStatesRequest) | [SlideScanServiceResetSlideStatesResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceResetSlideStatesResponse) | Resets the specified slides to new. |
|  | SetStorageFolder | [SlideScanServiceSetStorageFolderRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceSetStorageFolderRequest) | [SlideScanServiceSetStorageFolderResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceSetStorageFolderResponse) | Sets the storage folder for images. |
|  | StartScanPreview | [SlideScanServiceStartScanPreviewRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceStartScanPreviewRequest) | [SlideScanServiceStartScanPreviewResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceStartScanPreviewResponse) | Starts the preview with the specified input. |
|  | StartScanProfile | [SlideScanServiceStartScanProfileRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceStartScanProfileRequest) | [SlideScanServiceStartScanProfileResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceStartScanProfileResponse) | Starts the scan profile with the specified input. |
|  | StopScanPreview | [SlideScanServiceStopScanPreviewRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceStopScanPreviewRequest) | [SlideScanServiceStopScanPreviewResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceStopScanPreviewResponse) | Stops the preview execution. |
|  | StopScanProfile | [SlideScanServiceStopScanProfileRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceStopScanProfileRequest) | [SlideScanServiceStopScanProfileResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceStopScanProfileResponse) | Stops the scan profile execution. |
|  | UnmarkSlides | [SlideScanServiceUnmarkSlidesRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceUnmarkSlidesRequest) | [SlideScanServiceUnmarkSlidesResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceUnmarkSlidesResponse) | Unmark the specified slides. In the case of empty slide list, unmark all slides. If in the list of slides to be unselected, a slide is currently being previewed or scanned, the command is denied with an error message explaining the reason. |

## zen\_api/lm/slide\_scan/v1/slide\_state.proto

[Top](#title)

### SlideState

This enumeration names all possible slide processing states.

| Name | Number | Description |
| --- | --- | --- |
| SLIDE\_STATE\_UNSPECIFIED | 0 | Default value if status is not specified. |
| SLIDE\_STATE\_STOPPED | 1 | Processing was stopped. |
| SLIDE\_STATE\_NEW | 2 | New (not processed). |
| SLIDE\_STATE\_PREVIEW\_IN\_PROGRESS | 3 | Preview currently in work. |
| SLIDE\_STATE\_INPUT\_REQUIRED | 4 | Preview processing finished, but input required. |
| SLIDE\_STATE\_PREVIEWED | 5 | Preview processing finished. |
| SLIDE\_STATE\_SCAN\_IN\_PROGRESS | 6 | Scan currently in work. |
| SLIDE\_STATE\_FINISHED | 7 | Processing finished. |
| SLIDE\_STATE\_ERROR | 8 | Processing error occurred. |
| SLIDE\_STATE\_SKIPPED | 9 | Slide was skipped by user. |

## zen\_api/lm/slide\_scan/v1/tray\_information.proto

[Top](#title)

### TrayInformation

TrayInformation contains information about an Axioscan tray.

| Field | Type | Label | Description |
| --- | --- | --- | --- |
| position | [int32](#int32) |  | The position of the tray inside the Axioscan magazine in the range of [1, 26]. |
| type | [TrayType](#zen_api.lm.slide_scan.v1.TrayType) |  | The ZenApi.LM.SlideScan.V1.TrayType of the tray. The type determines the number of possible slides on the tray. |
| working\_state | [TrayWorkingState](#zen_api.lm.slide_scan.v1.TrayWorkingState) |  | The ZenApi.LM.SlideScan.V1.TrayWorkingState of the tray. The working state of the entire tray. |
| slot\_state | [TraySlotState](#zen_api.lm.slide_scan.v1.TraySlotState) |  | The ZenApi.LM.SlideScan.V1.TraySlotState of the tray. The status of the tray slot ( open/closed statuses). |
| slides | [SlideInformation](#zen_api.lm.slide_scan.v1.SlideInformation) | repeated | ZenApi.LM.SlideScan.V1.SlideInformation of the slides. |

## zen\_api/lm/slide\_scan/v1/tray\_slot\_state.proto

[Top](#title)

### TraySlotState

Enum defining the states of slide scanner slot LEDs.

| Name | Number | Description |
| --- | --- | --- |
| TRAY\_SLOT\_STATE\_UNSPECIFIED | 0 | Default value if status is not specified. |
| TRAY\_SLOT\_STATE\_SLOT\_OPEN\_SYSTEM\_PAUSED | 1 | Slot swiveled out for assembling. |
| TRAY\_SLOT\_STATE\_SLOT\_OPEN\_TRAY\_LOADED | 2 | Slot swiveled out for assembling but Tray is on stage. |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_TRAY\_NOT\_PROCESSED | 3 | Slot swiveled in with tray containing unprocessed slides. |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_TRAY\_PROCESSED | 4 | Slot swiveled in with tray containing processed slides. |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_PROCESS\_ERROR | 5 | Slot swiveled in with tray but an processing error was occurred. |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_TRAY\_PRESCANNED | 6 | Slot swiveled in with tray containing pre-scanned slides. |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_TRAY\_LOADED | 7 | Slot swiveled in and tray is on stage. |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_NO\_TRAY | 8 | Slot swiveled in without tray. |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_TRAY\_IN\_SYSTEM\_AND\_SLOT | 9 | Slot swiveled in with tray and a tray on the stage (Error case). |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_UNKNOWN\_TRAY | 10 | Slot swiveled in with an unknown tray type. |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_NO\_SLIDES | 11 | Slot swiveled in with an empty tray. |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_TRAY\_PARTLY\_PROCESSED\_WITH\_ERRORS | 12 | Slot swiveled in with tray containing processed slides. |
| TRAY\_SLOT\_STATE\_UNKNOWN | 255 | Unknown type (tray is inserted but could not be determined). |

## zen\_api/lm/slide\_scan/v1/tray\_type.proto

[Top](#title)

### TrayType

Enum defining the types of slide scanner trays.

| Name | Number | Description |
| --- | --- | --- |
| TRAY\_TYPE\_UNSPECIFIED | 0 | Default value if status is not specified. |
| TRAY\_TYPE\_NONE | 1 | No tray. |
| TRAY\_TYPE\_SCAN1X3 | 2 | Scan tray for 4 slides of size 1'x3'. |
| TRAY\_TYPE\_SCAN2X3 | 3 | Scan tray for 2 slides of size 2'x3'. |
| TRAY\_TYPE\_SCAN1X3\_2X3 | 4 | Scan tray for 2 slides, one of size 1'x3', one of size 2'x3'. |
| TRAY\_TYPE\_CALIBRATION\_STAGE | 5 | Stage calibration slide holder tray. |
| TRAY\_TYPE\_SCAN1X3\_BASIC | 6 | Scan tray for 4 slides of size 1'x3', basic design. |
| TRAY\_TYPE\_SCAN4X3 | 7 | Scan tray for 1 slide of size 4'x3' or a combination of slides of unknown size. |
| TRAY\_TYPE\_PARKING | 152 | Arbitrary tray type to indicate the parking position. Is only available at parking position of the magazine changer. |
| TRAY\_TYPE\_UNKNOWN | 153 | Unknown type (tray is inserted but could not be determined). |

## zen\_api/lm/slide\_scan/v1/tray\_working\_state.proto

[Top](#title)

### TrayWorkingState

Enum defining the types of slide scanner trays working state.

| Name | Number | Description |
| --- | --- | --- |
| TRAY\_WORKING\_STATE\_UNSPECIFIED | 0 | Default value if status is not specified. |
| TRAY\_WORKING\_STATE\_NOT\_SCANNED | 1 | The tray is not scanned. |
| TRAY\_WORKING\_STATE\_PRESCANNED | 2 | The tray was pre scanned. |
| TRAY\_WORKING\_STATE\_SCANNED | 3 | The tray was successfully scanned. |
| TRAY\_WORKING\_STATE\_ERROR | 4 | There occurred an error while scanning or pre scanning the tray. |
| TRAY\_WORKING\_STATE\_NOT\_AVAILABLE | 5 | There is no tray available at this position. |

## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| double |  | double | double | float | float64 | double | float | Float |
| float |  | float | float | float | float32 | float | float | Float |
| int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |