# ZEN API Documentation

ZEN Release 3.12 - Spring 2025 (2025-05-09)

## Table of Contents

- [ZEN API Documentation](#zen-api-documentation)
  - [Table of Contents](#table-of-contents)
  - [zen\_api/acquisition/v1beta/experiment\_descriptor.proto](#zen_apiacquisitionv1betaexperiment_descriptorproto)
    - [ExperimentDescriptor](#experimentdescriptor)
  - [zen\_api/acquisition/v1beta/experiment\_service.proto](#zen_apiacquisitionv1betaexperiment_serviceproto)
    - [ExperimentServiceCloneRequest](#experimentserviceclonerequest)
    - [ExperimentServiceCloneResponse](#experimentservicecloneresponse)
    - [ExperimentServiceDeleteRequest](#experimentservicedeleterequest)
    - [ExperimentServiceDeleteResponse](#experimentservicedeleteresponse)
    - [ExperimentServiceExportRequest](#experimentserviceexportrequest)
    - [ExperimentServiceExportResponse](#experimentserviceexportresponse)
    - [ExperimentServiceGetAvailableExperimentsRequest](#experimentservicegetavailableexperimentsrequest)
    - [ExperimentServiceGetAvailableExperimentsResponse](#experimentservicegetavailableexperimentsresponse)
    - [ExperimentServiceGetImageOutputPathRequest](#experimentservicegetimageoutputpathrequest)
    - [ExperimentServiceGetImageOutputPathResponse](#experimentservicegetimageoutputpathresponse)
    - [ExperimentServiceGetStatusRequest](#experimentservicegetstatusrequest)
    - [ExperimentServiceGetStatusResponse](#experimentservicegetstatusresponse)
    - [ExperimentServiceImportRequest](#experimentserviceimportrequest)
    - [ExperimentServiceImportResponse](#experimentserviceimportresponse)
    - [ExperimentServiceLoadRequest](#experimentserviceloadrequest)
    - [ExperimentServiceLoadResponse](#experimentserviceloadresponse)
    - [ExperimentServiceRegisterOnStatusChangedRequest](#experimentserviceregisteronstatuschangedrequest)
    - [ExperimentServiceRegisterOnStatusChangedResponse](#experimentserviceregisteronstatuschangedresponse)
    - [ExperimentServiceRunExperimentRequest](#experimentservicerunexperimentrequest)
    - [ExperimentServiceRunExperimentResponse](#experimentservicerunexperimentresponse)
    - [ExperimentServiceRunSnapRequest](#experimentservicerunsnaprequest)
    - [ExperimentServiceRunSnapResponse](#experimentservicerunsnapresponse)
    - [ExperimentServiceSaveRequest](#experimentservicesaverequest)
    - [ExperimentServiceSaveResponse](#experimentservicesaveresponse)
    - [ExperimentServiceStartContinuousRequest](#experimentservicestartcontinuousrequest)
    - [ExperimentServiceStartExperimentRequest](#experimentservicestartexperimentrequest)
    - [ExperimentServiceStartExperimentResponse](#experimentservicestartexperimentresponse)
    - [ExperimentServiceStartLiveRequest](#experimentservicestartliverequest)
    - [ExperimentServiceStartSnapRequest](#experimentservicestartsnaprequest)
    - [ExperimentServiceStartSnapResponse](#experimentservicestartsnapresponse)
    - [ExperimentServiceStopRequest](#experimentservicestoprequest)
    - [ExperimentServiceStopResponse](#experimentservicestopresponse)
    - [ExperimentService](#experimentservice)
  - [zen\_api/acquisition/v1beta/experiment\_status.proto](#zen_apiacquisitionv1betaexperiment_statusproto)
    - [ExperimentStatus](#experimentstatus)
  - [zen\_api/acquisition/v1beta/experiment\_streaming\_service.proto](#zen_apiacquisitionv1betaexperiment_streaming_serviceproto)
    - [ExperimentStreamingServiceMonitorAllExperimentsRequest](#experimentstreamingservicemonitorallexperimentsrequest)
    - [ExperimentStreamingServiceMonitorAllExperimentsResponse](#experimentstreamingservicemonitorallexperimentsresponse)
    - [ExperimentStreamingServiceMonitorExperimentRequest](#experimentstreamingservicemonitorexperimentrequest)
    - [ExperimentStreamingServiceMonitorExperimentResponse](#experimentstreamingservicemonitorexperimentresponse)
    - [ExperimentStreamingService](#experimentstreamingservice)
  - [zen\_api/acquisition/v1beta/frame\_data.proto](#zen_apiacquisitionv1betaframe_dataproto)
    - [FrameData](#framedata)
  - [zen\_api/acquisition/v1beta/frame\_pixel\_data.proto](#zen_apiacquisitionv1betaframe_pixel_dataproto)
    - [FramePixelData](#framepixeldata)
  - [zen\_api/acquisition/v1beta/frame\_position.proto](#zen_apiacquisitionv1betaframe_positionproto)
    - [FramePosition](#frameposition)
  - [zen\_api/acquisition/v1beta/frame\_stage\_position.proto](#zen_apiacquisitionv1betaframe_stage_positionproto)
    - [FrameStagePosition](#framestageposition)
  - [zen\_api/acquisition/v1beta/pixel\_type.proto](#zen_apiacquisitionv1betapixel_typeproto)
    - [PixelType](#pixeltype)
  - [zen\_api/acquisition/v1beta/scaling.proto](#zen_apiacquisitionv1betascalingproto)
    - [Scaling](#scaling)
  - [zen\_api/application/v1/composition\_service.proto](#zen_apiapplicationv1composition_serviceproto)
    - [CompositionServiceCreateModuleRequest](#compositionservicecreatemodulerequest)
    - [CompositionServiceCreateModuleResponse](#compositionservicecreatemoduleresponse)
    - [CompositionServiceIsModuleAvailableRequest](#compositionserviceismoduleavailablerequest)
    - [IsModuleAvailableResponse](#ismoduleavailableresponse)
    - [CompositionService](#compositionservice)
  - [zen\_api/common/v1/double\_point.proto](#zen_apicommonv1double_pointproto)
    - [DoublePoint](#doublepoint)
  - [zen\_api/common/v1/int\_point.proto](#zen_apicommonv1int_pointproto)
    - [IntPoint](#intpoint)
  - [zen\_api/common/v1/int\_size.proto](#zen_apicommonv1int_sizeproto)
    - [IntSize](#intsize)
  - [zen\_api/hardware/v1/axis\_identifier.proto](#zen_apihardwarev1axis_identifierproto)
    - [AxisIdentifier](#axisidentifier)
  - [zen\_api/hardware/v1/stage\_axis.proto](#zen_apihardwarev1stage_axisproto)
    - [StageAxis](#stageaxis)
  - [zen\_api/hardware/v1/stage\_motion\_state.proto](#zen_apihardwarev1stage_motion_stateproto)
    - [StageMotionState](#stagemotionstate)
  - [zen\_api/hardware/v1/stage\_service.proto](#zen_apihardwarev1stage_serviceproto)
    - [StageServiceAxisVelocityResponse](#stageserviceaxisvelocityresponse)
    - [StageServiceGetAvailableStageAxisRequest](#stageservicegetavailablestageaxisrequest)
    - [StageServiceGetAvailableStageAxisResponse](#stageservicegetavailablestageaxisresponse)
    - [StageServiceGetAxisPositionRequest](#stageservicegetaxispositionrequest)
    - [StageServiceGetAxisPositionResponse](#stageservicegetaxispositionresponse)
    - [StageServiceGetAxisVelocityRequest](#stageservicegetaxisvelocityrequest)
    - [StageServiceGetAxisVelocityResponse](#stageservicegetaxisvelocityresponse)
    - [StageServiceGetStageMotionStateRequest](#stageservicegetstagemotionstaterequest)
    - [StageServiceGetStageMotionStateResponse](#stageservicegetstagemotionstateresponse)
    - [StageServiceGetStagePositionRequest](#stageservicegetstagepositionrequest)
    - [StageServiceGetStagePositionResponse](#stageservicegetstagepositionresponse)
    - [StageServiceGetStageStateRequest](#stageservicegetstagestaterequest)
    - [StageServiceGetStageStateResponse](#stageservicegetstagestateresponse)
    - [StageServiceGetStageVelocityRequest](#stageservicegetstagevelocityrequest)
    - [StageServiceGetStageVelocityResponse](#stageservicegetstagevelocityresponse)
    - [StageServiceInitializeStageRequest](#stageserviceinitializestagerequest)
    - [StageServiceInitializeStageResponse](#stageserviceinitializestageresponse)
    - [StageServiceMoveToRequest](#stageservicemovetorequest)
    - [StageServiceMoveToResponse](#stageservicemovetoresponse)
    - [StageServiceRegisterOnStageMotionStateChangedRequest](#stageserviceregisteronstagemotionstatechangedrequest)
    - [StageServiceRegisterOnStageMotionStateChangedResponse](#stageserviceregisteronstagemotionstatechangedresponse)
    - [StageServiceRegisterOnStagePositionChangedRequest](#stageserviceregisteronstagepositionchangedrequest)
    - [StageServiceRegisterOnStagePositionChangedResponse](#stageserviceregisteronstagepositionchangedresponse)
    - [StageServiceRegisterOnStageStateChangedRequest](#stageserviceregisteronstagestatechangedrequest)
    - [StageServiceRegisterOnStageStateChangedResponse](#stageserviceregisteronstagestatechangedresponse)
    - [StageServiceRegisterOnStageVelocityChangedRequest](#stageserviceregisteronstagevelocitychangedrequest)
    - [StageServiceRegisterOnStageVelocityChangedResponse](#stageserviceregisteronstagevelocitychangedresponse)
    - [StageServiceStopRequest](#stageservicestoprequest)
    - [StageServiceStopResponse](#stageservicestopresponse)
    - [StageService](#stageservice)
  - [zen\_api/hardware/v1/stage\_state.proto](#zen_apihardwarev1stage_stateproto)
    - [StageState](#stagestate)
  - [zen\_api/workflows/v1/start\_job\_options.proto](#zen_apiworkflowsv1start_job_optionsproto)
    - [StartJobOptions](#startjoboptions)
  - [zen\_api/workflows/v1beta/job\_resources\_service.proto](#zen_apiworkflowsv1betajob_resources_serviceproto)
    - [JobResourcesServiceGetAvailableResourcesRequest](#jobresourcesservicegetavailableresourcesrequest)
    - [JobResourcesServiceGetAvailableResourcesResponse](#jobresourcesservicegetavailableresourcesresponse)
    - [JobResourcesServiceGetBooleanValueRequest](#jobresourcesservicegetbooleanvaluerequest)
    - [JobResourcesServiceGetBooleanValueResponse](#jobresourcesservicegetbooleanvalueresponse)
    - [JobResourcesServiceGetDateTimeValueRequest](#jobresourcesservicegetdatetimevaluerequest)
    - [JobResourcesServiceGetDateTimeValueResponse](#jobresourcesservicegetdatetimevalueresponse)
    - [JobResourcesServiceGetDateValueRequest](#jobresourcesservicegetdatevaluerequest)
    - [JobResourcesServiceGetDateValueResponse](#jobresourcesservicegetdatevalueresponse)
    - [JobResourcesServiceGetDoubleValueRequest](#jobresourcesservicegetdoublevaluerequest)
    - [JobResourcesServiceGetDoubleValueResponse](#jobresourcesservicegetdoublevalueresponse)
    - [JobResourcesServiceGetFloatValueRequest](#jobresourcesservicegetfloatvaluerequest)
    - [JobResourcesServiceGetFloatValueResponse](#jobresourcesservicegetfloatvalueresponse)
    - [JobResourcesServiceGetIntegerValueRequest](#jobresourcesservicegetintegervaluerequest)
    - [JobResourcesServiceGetIntegerValueResponse](#jobresourcesservicegetintegervalueresponse)
    - [JobResourcesServiceGetLongValueRequest](#jobresourcesservicegetlongvaluerequest)
    - [JobResourcesServiceGetLongValueResponse](#jobresourcesservicegetlongvalueresponse)
    - [JobResourcesServiceGetStringValueRequest](#jobresourcesservicegetstringvaluerequest)
    - [JobResourcesServiceGetStringValueResponse](#jobresourcesservicegetstringvalueresponse)
    - [JobResourcesServiceGetTimeValueRequest](#jobresourcesservicegettimevaluerequest)
    - [JobResourcesServiceGetTimeValueResponse](#jobresourcesservicegettimevalueresponse)
    - [JobResourcesServiceHasResourceRequest](#jobresourcesservicehasresourcerequest)
    - [JobResourcesServiceHasResourceResponse](#jobresourcesservicehasresourceresponse)
    - [JobResourcesServiceIsJobLoadedRequest](#jobresourcesserviceisjobloadedrequest)
    - [JobResourcesServiceIsJobLoadedResponse](#jobresourcesserviceisjobloadedresponse)
    - [JobResourcesServiceSetBooleanValueRequest](#jobresourcesservicesetbooleanvaluerequest)
    - [JobResourcesServiceSetBooleanValueResponse](#jobresourcesservicesetbooleanvalueresponse)
    - [JobResourcesServiceSetDateTimeValueRequest](#jobresourcesservicesetdatetimevaluerequest)
    - [JobResourcesServiceSetDateTimeValueResponse](#jobresourcesservicesetdatetimevalueresponse)
    - [JobResourcesServiceSetDateValueRequest](#jobresourcesservicesetdatevaluerequest)
    - [JobResourcesServiceSetDateValueResponse](#jobresourcesservicesetdatevalueresponse)
    - [JobResourcesServiceSetDoubleValueRequest](#jobresourcesservicesetdoublevaluerequest)
    - [JobResourcesServiceSetDoubleValueResponse](#jobresourcesservicesetdoublevalueresponse)
    - [JobResourcesServiceSetFloatValueRequest](#jobresourcesservicesetfloatvaluerequest)
    - [JobResourcesServiceSetFloatValueResponse](#jobresourcesservicesetfloatvalueresponse)
    - [JobResourcesServiceSetIntegerValueRequest](#jobresourcesservicesetintegervaluerequest)
    - [JobResourcesServiceSetIntegerValueResponse](#jobresourcesservicesetintegervalueresponse)
    - [JobResourcesServiceSetLongValueRequest](#jobresourcesservicesetlongvaluerequest)
    - [JobResourcesServiceSetLongValueResponse](#jobresourcesservicesetlongvalueresponse)
    - [JobResourcesServiceSetStringValueRequest](#jobresourcesservicesetstringvaluerequest)
    - [JobResourcesServiceSetStringValueResponse](#jobresourcesservicesetstringvalueresponse)
    - [JobResourcesServiceSetTimeValueRequest](#jobresourcesservicesettimevaluerequest)
    - [JobResourcesServiceSetTimeValueResponse](#jobresourcesservicesettimevalueresponse)
    - [JobResourcesService](#jobresourcesservice)
  - [zen\_api/workflows/v2/job\_info.proto](#zen_apiworkflowsv2job_infoproto)
    - [JobInfo](#jobinfo)
  - [zen\_api/workflows/v2/job\_status.proto](#zen_apiworkflowsv2job_statusproto)
    - [JobStatus](#jobstatus)
  - [zen\_api/workflows/v2/workflow\_service.proto](#zen_apiworkflowsv2workflow_serviceproto)
    - [WorkflowServiceGetJobInfoRequest](#workflowservicegetjobinforequest)
    - [WorkflowServiceGetJobInfoResponse](#workflowservicegetjobinforesponse)
    - [WorkflowServiceStartJobRequest](#workflowservicestartjobrequest)
    - [WorkflowServiceStartJobResponse](#workflowservicestartjobresponse)
    - [WorkflowServiceStopJobRequest](#workflowservicestopjobrequest)
    - [WorkflowServiceStopJobResponse](#workflowservicestopjobresponse)
    - [WorkflowServiceWaitJobRequest](#workflowservicewaitjobrequest)
    - [WorkflowServiceWaitJobResponse](#workflowservicewaitjobresponse)
    - [WorkflowService](#workflowservice)
  - [zen\_api/workflows/v3beta/job\_status.proto](#zen_apiworkflowsv3betajob_statusproto)
    - [JobStatus](#jobstatus-1)
  - [zen\_api/workflows/v3beta/job\_template\_info.proto](#zen_apiworkflowsv3betajob_template_infoproto)
    - [JobTemplateInfo](#jobtemplateinfo)
  - [zen\_api/workflows/v3beta/workflow\_service.proto](#zen_apiworkflowsv3betaworkflow_serviceproto)
    - [WorkflowServiceGetAvailableJobTemplatesRequest](#workflowservicegetavailablejobtemplatesrequest)
    - [WorkflowServiceGetAvailableJobTemplatesResponse](#workflowservicegetavailablejobtemplatesresponse)
    - [WorkflowServiceGetStatusRequest](#workflowservicegetstatusrequest)
    - [WorkflowServiceGetStatusResponse](#workflowservicegetstatusresponse)
    - [WorkflowServiceIsJobRunningRequest](#workflowserviceisjobrunningrequest)
    - [WorkflowServiceIsJobRunningResponse](#workflowserviceisjobrunningresponse)
    - [WorkflowServiceIsJobTemplateLoadedRequest](#workflowserviceisjobtemplateloadedrequest)
    - [WorkflowServiceIsJobTemplateLoadedResponse](#workflowserviceisjobtemplateloadedresponse)
    - [WorkflowServiceLoadJobTemplateRequest](#workflowserviceloadjobtemplaterequest)
    - [WorkflowServiceLoadJobTemplateResponse](#workflowserviceloadjobtemplateresponse)
    - [WorkflowServiceRegisterOnStatusChangedRequest](#workflowserviceregisteronstatuschangedrequest)
    - [WorkflowServiceRegisterOnStatusChangedResponse](#workflowserviceregisteronstatuschangedresponse)
    - [WorkflowServiceRunJobRequest](#workflowservicerunjobrequest)
    - [WorkflowServiceRunJobResponse](#workflowservicerunjobresponse)
    - [WorkflowServiceStartJobRequest](#workflowservicestartjobrequest-1)
    - [WorkflowServiceStartJobResponse](#workflowservicestartjobresponse-1)
    - [WorkflowServiceStopJobRequest](#workflowservicestopjobrequest-1)
    - [WorkflowServiceStopJobResponse](#workflowservicestopjobresponse-1)
    - [WorkflowServiceUnloadJobTemplateRequest](#workflowserviceunloadjobtemplaterequest)
    - [WorkflowServiceUnloadJobTemplateResponse](#workflowserviceunloadjobtemplateresponse)
    - [WorkflowServiceWaitJobRequest](#workflowservicewaitjobrequest-1)
    - [WorkflowServiceWaitJobResponse](#workflowservicewaitjobresponse-1)
    - [WorkflowService](#workflowservice-1)
  - [zen\_api/lm/acquisition/v1beta/autofocus\_contrast\_measure.proto](#zen_apilmacquisitionv1betaautofocus_contrast_measureproto)
    - [AutofocusContrastMeasure](#autofocuscontrastmeasure)
  - [zen\_api/lm/acquisition/v1beta/autofocus\_mode.proto](#zen_apilmacquisitionv1betaautofocus_modeproto)
    - [AutofocusMode](#autofocusmode)
  - [zen\_api/lm/acquisition/v1beta/autofocus\_sampling.proto](#zen_apilmacquisitionv1betaautofocus_samplingproto)
    - [AutofocusSampling](#autofocussampling)
  - [zen\_api/lm/acquisition/v1beta/channel\_info.proto](#zen_apilmacquisitionv1betachannel_infoproto)
    - [ChannelInfo](#channelinfo)
  - [zen\_api/lm/acquisition/v1beta/experiment\_sw\_autofocus\_service.proto](#zen_apilmacquisitionv1betaexperiment_sw_autofocus_serviceproto)
    - [ExperimentSwAutofocusServiceExportRequest](#experimentswautofocusserviceexportrequest)
    - [ExperimentSwAutofocusServiceExportResponse](#experimentswautofocusserviceexportresponse)
    - [ExperimentSwAutofocusServiceFindAutoFocusRequest](#experimentswautofocusservicefindautofocusrequest)
    - [ExperimentSwAutofocusServiceFindAutoFocusResponse](#experimentswautofocusservicefindautofocusresponse)
    - [ExperimentSwAutofocusServiceGetAutofocusParametersRequest](#experimentswautofocusservicegetautofocusparametersrequest)
    - [ExperimentSwAutofocusServiceGetAutofocusParametersResponse](#experimentswautofocusservicegetautofocusparametersresponse)
    - [ExperimentSwAutofocusServiceImportRequest](#experimentswautofocusserviceimportrequest)
    - [ExperimentSwAutofocusServiceImportResponse](#experimentswautofocusserviceimportresponse)
    - [ExperimentSwAutofocusServiceSetAutofocusParametersRequest](#experimentswautofocusservicesetautofocusparametersrequest)
    - [ExperimentSwAutofocusServiceSetAutofocusParametersResponse](#experimentswautofocusservicesetautofocusparametersresponse)
    - [ExperimentSwAutofocusService](#experimentswautofocusservice)
  - [zen\_api/lm/acquisition/v1beta/position3d.proto](#zen_apilmacquisitionv1betaposition3dproto)
    - [Position3d](#position3d)
  - [zen\_api/lm/acquisition/v1beta/tiles\_service.proto](#zen_apilmacquisitionv1betatiles_serviceproto)
    - [TilesServiceAddEllipseTileRegionRequest](#tilesserviceaddellipsetileregionrequest)
    - [TilesServiceAddEllipseTileRegionResponse](#tilesserviceaddellipsetileregionresponse)
    - [TilesServiceAddPolygonTileRegionRequest](#tilesserviceaddpolygontileregionrequest)
    - [TilesServiceAddPolygonTileRegionResponse](#tilesserviceaddpolygontileregionresponse)
    - [TilesServiceAddPositionsRequest](#tilesserviceaddpositionsrequest)
    - [TilesServiceAddPositionsResponse](#tilesserviceaddpositionsresponse)
    - [TilesServiceAddRectangleTileRegionRequest](#tilesserviceaddrectangletileregionrequest)
    - [TilesServiceAddRectangleTileRegionResponse](#tilesserviceaddrectangletileregionresponse)
    - [TilesServiceClearRequest](#tilesserviceclearrequest)
    - [TilesServiceClearResponse](#tilesserviceclearresponse)
    - [TilesServiceIsTilesExperimentRequest](#tilesserviceistilesexperimentrequest)
    - [TilesServiceIsTilesExperimentResponse](#tilesserviceistilesexperimentresponse)
    - [TilesService](#tilesservice)
  - [zen\_api/lm/acquisition/v1beta/track\_info.proto](#zen_apilmacquisitionv1betatrack_infoproto)
    - [TrackInfo](#trackinfo)
  - [zen\_api/lm/acquisition/v1beta/track\_service.proto](#zen_apilmacquisitionv1betatrack_serviceproto)
    - [TrackServiceActivateChannelRequest](#trackserviceactivatechannelrequest)
    - [TrackServiceActivateChannelResponse](#trackserviceactivatechannelresponse)
    - [TrackServiceActivateTrackRequest](#trackserviceactivatetrackrequest)
    - [TrackServiceActivateTrackResponse](#trackserviceactivatetrackresponse)
    - [TrackServiceDeactivateChannelRequest](#trackservicedeactivatechannelrequest)
    - [TrackServiceDeactivateChannelResponse](#trackservicedeactivatechannelresponse)
    - [TrackServiceDeactivateTrackRequest](#trackservicedeactivatetrackrequest)
    - [TrackServiceDeactivateTrackResponse](#trackservicedeactivatetrackresponse)
    - [TrackServiceGetTrackInfoRequest](#trackservicegettrackinforequest)
    - [TrackServiceGetTrackInfoResponse](#trackservicegettrackinforesponse)
    - [TrackService](#trackservice)
  - [zen\_api/lm/acquisition/v1beta/zstack\_service.proto](#zen_apilmacquisitionv1betazstack_serviceproto)
    - [ZStackServiceGetZStackInfoRequest](#zstackservicegetzstackinforequest)
    - [ZStackServiceGetZStackInfoResponse](#zstackservicegetzstackinforesponse)
    - [ZStackServiceIsZStackExperimentRequest](#zstackserviceiszstackexperimentrequest)
    - [ZStackServiceIsZStackExperimentResponse](#zstackserviceiszstackexperimentresponse)
    - [ZStackServiceModifyZStackCenterRangeRequest](#zstackservicemodifyzstackcenterrangerequest)
    - [ZStackServiceModifyZStackCenterRangeResponse](#zstackservicemodifyzstackcenterrangeresponse)
    - [ZStackServiceModifyZStackFirstLastRequest](#zstackservicemodifyzstackfirstlastrequest)
    - [ZStackServiceModifyZStackFirstLastResponse](#zstackservicemodifyzstackfirstlastresponse)
    - [ZStackService](#zstackservice)
  - [zen\_api/lm/hardware/v1/focus\_service.proto](#zen_apilmhardwarev1focus_serviceproto)
    - [FocusServiceGetAccelerationRequest](#focusservicegetaccelerationrequest)
    - [FocusServiceGetAccelerationResponse](#focusservicegetaccelerationresponse)
    - [FocusServiceGetPositionRequest](#focusservicegetpositionrequest)
    - [FocusServiceGetPositionResponse](#focusservicegetpositionresponse)
    - [FocusServiceGetSpeedRequest](#focusservicegetspeedrequest)
    - [FocusServiceGetSpeedResponse](#focusservicegetspeedresponse)
    - [FocusServiceMoveToRequest](#focusservicemovetorequest)
    - [FocusServiceMoveToResponse](#focusservicemovetoresponse)
    - [FocusServiceSetAccelerationRequest](#focusservicesetaccelerationrequest)
    - [FocusServiceSetAccelerationResponse](#focusservicesetaccelerationresponse)
    - [FocusServiceSetSpeedRequest](#focusservicesetspeedrequest)
    - [FocusServiceSetSpeedResponse](#focusservicesetspeedresponse)
    - [FocusServiceStopRequest](#focusservicestoprequest)
    - [FocusServiceStopResponse](#focusservicestopresponse)
    - [FocusService](#focusservice)
  - [zen\_api/lm/hardware/v1/stage\_service.proto](#zen_apilmhardwarev1stage_serviceproto)
    - [StageServiceGetAccelerationRequest](#stageservicegetaccelerationrequest)
    - [StageServiceGetAccelerationResponse](#stageservicegetaccelerationresponse)
    - [StageServiceGetPositionRequest](#stageservicegetpositionrequest)
    - [StageServiceGetPositionResponse](#stageservicegetpositionresponse)
    - [StageServiceGetSpeedRequest](#stageservicegetspeedrequest)
    - [StageServiceGetSpeedResponse](#stageservicegetspeedresponse)
    - [StageServiceMoveToRequest](#stageservicemovetorequest-1)
    - [StageServiceMoveToResponse](#stageservicemovetoresponse-1)
    - [StageServiceSetAccelerationRequest](#stageservicesetaccelerationrequest)
    - [StageServiceSetAccelerationResponse](#stageservicesetaccelerationresponse)
    - [StageServiceSetSpeedRequest](#stageservicesetspeedrequest)
    - [StageServiceSetSpeedResponse](#stageservicesetspeedresponse)
    - [StageServiceStopRequest](#stageservicestoprequest-1)
    - [StageServiceStopResponse](#stageservicestopresponse-1)
    - [StageService](#stageservice-1)
  - [zen\_api/lm/hardware/v2/focus\_service.proto](#zen_apilmhardwarev2focus_serviceproto)
    - [FocusServiceGetAccelerationRequest](#focusservicegetaccelerationrequest-1)
    - [FocusServiceGetAccelerationResponse](#focusservicegetaccelerationresponse-1)
    - [FocusServiceGetPositionRequest](#focusservicegetpositionrequest-1)
    - [FocusServiceGetPositionResponse](#focusservicegetpositionresponse-1)
    - [FocusServiceGetSpeedRequest](#focusservicegetspeedrequest-1)
    - [FocusServiceGetSpeedResponse](#focusservicegetspeedresponse-1)
    - [FocusServiceMoveToRequest](#focusservicemovetorequest-1)
    - [FocusServiceMoveToResponse](#focusservicemovetoresponse-1)
    - [FocusServiceSetAccelerationRequest](#focusservicesetaccelerationrequest-1)
    - [FocusServiceSetAccelerationResponse](#focusservicesetaccelerationresponse-1)
    - [FocusServiceSetSpeedRequest](#focusservicesetspeedrequest-1)
    - [FocusServiceSetSpeedResponse](#focusservicesetspeedresponse-1)
    - [FocusServiceStopRequest](#focusservicestoprequest-1)
    - [FocusServiceStopResponse](#focusservicestopresponse-1)
    - [FocusService](#focusservice-1)
  - [zen\_api/lm/hardware/v2/stage\_service.proto](#zen_apilmhardwarev2stage_serviceproto)
    - [StageServiceGetAccelerationRequest](#stageservicegetaccelerationrequest-1)
    - [StageServiceGetAccelerationResponse](#stageservicegetaccelerationresponse-1)
    - [StageServiceGetPositionRequest](#stageservicegetpositionrequest-1)
    - [StageServiceGetPositionResponse](#stageservicegetpositionresponse-1)
    - [StageServiceGetSpeedRequest](#stageservicegetspeedrequest-1)
    - [StageServiceGetSpeedResponse](#stageservicegetspeedresponse-1)
    - [StageServiceMoveToRequest](#stageservicemovetorequest-2)
    - [StageServiceMoveToResponse](#stageservicemovetoresponse-2)
    - [StageServiceSetAccelerationRequest](#stageservicesetaccelerationrequest-1)
    - [StageServiceSetAccelerationResponse](#stageservicesetaccelerationresponse-1)
    - [StageServiceSetSpeedRequest](#stageservicesetspeedrequest-1)
    - [StageServiceSetSpeedResponse](#stageservicesetspeedresponse-1)
    - [StageServiceStopRequest](#stageservicestoprequest-2)
    - [StageServiceStopResponse](#stageservicestopresponse-2)
    - [StageService](#stageservice-2)
  - [zen\_api/lm/slide\_scan/v1/channel\_settings.proto](#zen_apilmslide_scanv1channel_settingsproto)
    - [ChannelSettings](#channelsettings)
  - [zen\_api/lm/slide\_scan/v1/information\_base.proto](#zen_apilmslide_scanv1information_baseproto)
    - [InformationBase](#informationbase)
    - [MagazineInformation](#magazineinformation)
    - [SimpleInformation](#simpleinformation)
    - [SlideScanSystemInformation](#slidescansysteminformation)
  - [zen\_api/lm/slide\_scan/v1/profile\_information.proto](#zen_apilmslide_scanv1profile_informationproto)
    - [ProfileInformation](#profileinformation)
  - [zen\_api/lm/slide\_scan/v1/response\_code.proto](#zen_apilmslide_scanv1response_codeproto)
    - [ResponseCode](#responsecode)
  - [zen\_api/lm/slide\_scan/v1/response\_type.proto](#zen_apilmslide_scanv1response_typeproto)
    - [ResponseType](#responsetype)
  - [zen\_api/lm/slide\_scan/v1/slide\_information.proto](#zen_apilmslide_scanv1slide_informationproto)
    - [SlideInformation](#slideinformation)
  - [zen\_api/lm/slide\_scan/v1/slide\_position\_information.proto](#zen_apilmslide_scanv1slide_position_informationproto)
    - [SlidePositionInformation](#slidepositioninformation)
  - [zen\_api/lm/slide\_scan/v1/slide\_scan\_service.proto](#zen_apilmslide_scanv1slide_scan_serviceproto)
    - [GeneralResponse](#generalresponse)
    - [SlideScanServiceGetChannelSettingsRequest](#slidescanservicegetchannelsettingsrequest)
    - [SlideScanServiceGetChannelSettingsResponse](#slidescanservicegetchannelsettingsresponse)
    - [SlideScanServiceGetMagazineStateRequest](#slidescanservicegetmagazinestaterequest)
    - [SlideScanServiceGetMagazineStateResponse](#slidescanservicegetmagazinestateresponse)
    - [SlideScanServiceObserveRequest](#slidescanserviceobserverequest)
    - [SlideScanServiceObserveResponse](#slidescanserviceobserveresponse)
    - [SlideScanServiceResetSlideStatesRequest](#slidescanserviceresetslidestatesrequest)
    - [SlideScanServiceResetSlideStatesResponse](#slidescanserviceresetslidestatesresponse)
    - [SlideScanServiceStartScanPreviewRequest](#slidescanservicestartscanpreviewrequest)
    - [SlideScanServiceStartScanPreviewResponse](#slidescanservicestartscanpreviewresponse)
    - [SlideScanServiceStartScanProfileRequest](#slidescanservicestartscanprofilerequest)
    - [SlideScanServiceStartScanProfileResponse](#slidescanservicestartscanprofileresponse)
    - [SlideScanServiceStopScanPreviewRequest](#slidescanservicestopscanpreviewrequest)
    - [SlideScanServiceStopScanPreviewResponse](#slidescanservicestopscanpreviewresponse)
    - [SlideScanServiceStopScanProfileRequest](#slidescanservicestopscanprofilerequest)
    - [SlideScanServiceStopScanProfileResponse](#slidescanservicestopscanprofileresponse)
    - [SlideScanService](#slidescanservice)
  - [zen\_api/lm/slide\_scan/v1/slide\_state.proto](#zen_apilmslide_scanv1slide_stateproto)
    - [SlideState](#slidestate)
  - [zen\_api/lm/slide\_scan/v1/tray\_information.proto](#zen_apilmslide_scanv1tray_informationproto)
    - [TrayInformation](#trayinformation)
  - [zen\_api/lm/slide\_scan/v1/tray\_slot\_state.proto](#zen_apilmslide_scanv1tray_slot_stateproto)
    - [TraySlotState](#trayslotstate)
  - [zen\_api/lm/slide\_scan/v1/tray\_type.proto](#zen_apilmslide_scanv1tray_typeproto)
    - [TrayType](#traytype)
  - [zen\_api/lm/slide\_scan/v1/tray\_working\_state.proto](#zen_apilmslide_scanv1tray_working_stateproto)
    - [TrayWorkingState](#trayworkingstate)
  - [Scalar Value Types](#scalar-value-types)

## zen\_api/acquisition/v1beta/experiment\_descriptor.proto

[Top](#title)

### ExperimentDescriptor

Descriptors for experiment.

| Field | Type              | Label | Description      |
| ----- | ----------------- | ----- | ---------------- |
| name  | [string](#string) |       | Experiment name. |

## zen\_api/acquisition/v1beta/experiment\_service.proto

[Top](#title)

### ExperimentServiceCloneRequest

The ExperimentServiceCloneRequest class.

| Field          | Type              | Label | Description                        |
| -------------- | ----------------- | ----- | ---------------------------------- |
| experiment\_id | [string](#string) |       | Id of the experiment to be cloned. |

### ExperimentServiceCloneResponse

Response object of the method for cloning an experiment.

| Field          | Type              | Label | Description                                                         |
| -------------- | ----------------- | ----- | ------------------------------------------------------------------- |
| experiment\_id | [string](#string) |       | The experiment id which is used to reference the cloned experiment. |

### ExperimentServiceDeleteRequest

The ExperimentServiceDeleteRequest class.

| Field            | Type              | Label | Description                           |
| ---------------- | ----------------- | ----- | ------------------------------------- |
| experiment\_name | [string](#string) |       | Name of the experiment to be deleted. |

### ExperimentServiceDeleteResponse

The ExperimentServiceDeleteResponse class.

### ExperimentServiceExportRequest

The ExperimentServiceExportRequest class.

| Field          | Type              | Label | Description    |
| -------------- | ----------------- | ----- | -------------- |
| experiment\_id | [string](#string) |       | Experiment id. |

### ExperimentServiceExportResponse

Response object of the method for exporting an experiment.

| Field | Type              | Label | Description               |
| ----- | ----------------- | ----- | ------------------------- |
| xml   | [string](#string) |       | Xml string of experiment. |

### ExperimentServiceGetAvailableExperimentsRequest

The ExperimentServiceGetAvailableExperimentsRequest class.

### ExperimentServiceGetAvailableExperimentsResponse

Response object of available experiments.

| Field       | Type                                                                     | Label    | Description                    |
| ----------- | ------------------------------------------------------------------------ | -------- | ------------------------------ |
| experiments | [ExperimentDescriptor](#zen_api.acquisition.v1beta.ExperimentDescriptor) | repeated | List of available experiments. |

### ExperimentServiceGetImageOutputPathRequest

The ExperimentServiceGetImageOutputPathRequest class.

### ExperimentServiceGetImageOutputPathResponse

Response object of the method for getting the image output path.

| Field               | Type              | Label | Description            |
| ------------------- | ----------------- | ----- | ---------------------- |
| image\_output\_path | [string](#string) |       | The image output path. |

### ExperimentServiceGetStatusRequest

The ExperimentServiceGetStatusRequest class.

| Field          | Type              | Label | Description                                                                                                                                                                                                                                                                                                |
| -------------- | ----------------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| experiment\_id | [string](#string) |       | ID of an experiment for which status is requested. If ID is provided, the status can be retrieved for both active and finished experiments. If ID is not provided, status of one of the active experiments is returned. If ID is not provided and there are no active experiments, an exception is thrown. |

### ExperimentServiceGetStatusResponse

Response object representing the status of an experiment.

| Field  | Type                                                             | Label | Description            |
| ------ | ---------------------------------------------------------------- | ----- | ---------------------- |
| status | [ExperimentStatus](#zen_api.acquisition.v1beta.ExperimentStatus) |       | The experiment status. |

### ExperimentServiceImportRequest

The ExperimentServiceImportRequest class.

| Field       | Type              | Label | Description                   |
| ----------- | ----------------- | ----- | ----------------------------- |
| xml\_string | [string](#string) |       | Xml string of the experiment. |

### ExperimentServiceImportResponse

Response object of the method for importing an experiment.

| Field          | Type              | Label | Description                                                           |
| -------------- | ----------------- | ----- | --------------------------------------------------------------------- |
| experiment\_id | [string](#string) |       | The experiment id which is used to reference the imported experiment. |

### ExperimentServiceLoadRequest

The ExperimentServiceLoadRequest class.

| Field            | Type              | Label | Description             |
| ---------------- | ----------------- | ----- | ----------------------- |
| experiment\_name | [string](#string) |       | Name of the experiment. |

### ExperimentServiceLoadResponse

Response object of the method for loading an experiment.

| Field          | Type              | Label | Description                                                         |
| -------------- | ----------------- | ----- | ------------------------------------------------------------------- |
| experiment\_id | [string](#string) |       | The experiment id which is used to reference the loaded experiment. |

### ExperimentServiceRegisterOnStatusChangedRequest

The ExperimentServiceRegisterOnStatusChangedRequest class.

| Field          | Type              | Label | Description                                                                                                                            |
| -------------- | ----------------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------- |
| experiment\_id | [string](#string) |       | ID of an active experiment for which status is monitored. If ID is not provided, status of one of the active experiments is monitored. |

### ExperimentServiceRegisterOnStatusChangedResponse

Response object representing the status of an experiment.

It contains full set of status information, which can consist a single or multiple new states.

| Field  | Type                                                             | Label | Description            |
| ------ | ---------------------------------------------------------------- | ----- | ---------------------- |
| status | [ExperimentStatus](#zen_api.acquisition.v1beta.ExperimentStatus) |       | The experiment status. |

### ExperimentServiceRunExperimentRequest

The ExperimentServiceRunExperimentRequest class.

| Field          | Type              | Label | Description                                                                                                                                                                                                             |
| -------------- | ----------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| experiment\_id | [string](#string) |       | Experiment id.                                                                                                                                                                                                          |
| output\_name   | [string](#string) |       | Optional name of the experiment's output. If a null or an empty name is provided, the output name will be created automatically, otherwise the output name must be in a format of a file name without a file extension. |

### ExperimentServiceRunExperimentResponse

Information about execution of an experiment.

| Field        | Type              | Label | Description                                                                                |
| ------------ | ----------------- | ----- | ------------------------------------------------------------------------------------------ |
| output\_name | [string](#string) |       | The name of the experiment's output (in a format of a file name without a file extension). |

### ExperimentServiceRunSnapRequest

The ExperimentServiceRunSnapRequest class.

| Field          | Type              | Label | Description                                                                                                                                                                                                             |
| -------------- | ----------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| experiment\_id | [string](#string) |       | Experiment id.                                                                                                                                                                                                          |
| output\_name   | [string](#string) |       | Optional name of the experiment's output. If a null or an empty name is provided, the output name will be created automatically, otherwise the output name must be in a format of a file name without a file extension. |

### ExperimentServiceRunSnapResponse

Information about execution of a snap experiment.

| Field        | Type              | Label | Description                                                                          |
| ------------ | ----------------- | ----- | ------------------------------------------------------------------------------------ |
| output\_name | [string](#string) |       | The name of the snap's output (in a format of a file name without a file extension). |

### ExperimentServiceSaveRequest

The ExperimentServiceSaveRequest class.

| Field            | Type              | Label | Description                                                       |
| ---------------- | ----------------- | ----- | ----------------------------------------------------------------- |
| experiment\_id   | [string](#string) |       | Experiment id.                                                    |
| experiment\_name | [string](#string) |       | Name to be used when saving the experiment.                       |
| allow\_override  | [bool](#bool)     |       | Allow override of already existing experiment with the same name. |

### ExperimentServiceSaveResponse

The ExperimentServiceSaveResponse class.

### ExperimentServiceStartContinuousRequest

The ExperimentServiceStartContinuousRequest class.

| Field          | Type              | Label | Description    |
| -------------- | ----------------- | ----- | -------------- |
| experiment\_id | [string](#string) |       | Experiment id. |

### ExperimentServiceStartExperimentRequest

The ExperimentServiceStartExperimentRequest class.

| Field          | Type              | Label | Description                                                                                                                                                                                                             |
| -------------- | ----------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| experiment\_id | [string](#string) |       | Experiment id.                                                                                                                                                                                                          |
| output\_name   | [string](#string) |       | Optional name of the experiment's output. If a null or an empty name is provided, the output name will be created automatically, otherwise the output name must be in a format of a file name without a file extension. |

### ExperimentServiceStartExperimentResponse

Information about execution of an experiment.

| Field        | Type              | Label | Description                                                                                |
| ------------ | ----------------- | ----- | ------------------------------------------------------------------------------------------ |
| output\_name | [string](#string) |       | The name of the experiment's output (in a format of a file name without a file extension). |

### ExperimentServiceStartLiveRequest

The ExperimentServiceStartLiveRequest class.

| Field          | Type                                                                                               | Label | Description                                                                                                                                                                                                                      |
| -------------- | -------------------------------------------------------------------------------------------------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| experiment\_id | [string](#string)                                                                                  |       | Experiment id.                                                                                                                                                                                                                   |
| track\_index   | [google.protobuf.Int32Value](https://protobuf.dev/reference/protobuf/google.protobuf/#int32-value) |       | Optional track index. When index is not provided the first selected or activated track (in that order) will be used, but when the index is provided the track with than index will be selected. The track index starts with "0". |

### ExperimentServiceStartSnapRequest

The ExperimentServiceStartSnapRequest class.

| Field          | Type              | Label | Description                                                                                                                                                                                                             |
| -------------- | ----------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| experiment\_id | [string](#string) |       | Experiment id.                                                                                                                                                                                                          |
| output\_name   | [string](#string) |       | Optional name of the experiment's output. If a null or an empty name is provided, the output name will be created automatically, otherwise the output name must be in a format of a file name without a file extension. |

### ExperimentServiceStartSnapResponse

Information about execution of a snap experiment.

| Field        | Type              | Label | Description                                                                          |
| ------------ | ----------------- | ----- | ------------------------------------------------------------------------------------ |
| output\_name | [string](#string) |       | The name of the snap's output (in a format of a file name without a file extension). |

### ExperimentServiceStopRequest

The ExperimentServiceStopRequest class.

| Field          | Type              | Label | Description                                                                         |
| -------------- | ----------------- | ----- | ----------------------------------------------------------------------------------- |
| experiment\_id | [string](#string) |       | ID of an experiment to stop or an empty GUID to stop one of the active experiments. |

### ExperimentServiceStopResponse

Information about execution of an experiment.

| Field          | Type              | Label | Description                                                                 |
| -------------- | ----------------- | ----- | --------------------------------------------------------------------------- |
| experiment\_id | [string](#string) |       | The ID of the experiment which is used to reference the stopped experiment. |

### ExperimentService

The IExperimentService interface.

KindMethod NameRequest TypeResponse TypeDescription

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Clone [ExperimentServiceCloneRequest](#zen_api.acquisition.v1beta.ExperimentServiceCloneRequest) [ExperimentServiceCloneResponse](#zen_api.acquisition.v1beta.ExperimentServiceCloneResponse)

Clones an already loaded experiment. Useful when one wants to clone an experiment before modifying it in order to preserve the original experiment. This method returns the info needed to reference the cloned experiment.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Delete [ExperimentServiceDeleteRequest](#zen_api.acquisition.v1beta.ExperimentServiceDeleteRequest) [ExperimentServiceDeleteResponse](#zen_api.acquisition.v1beta.ExperimentServiceDeleteResponse)

Deletes an experiment file from the predefined location on disk. It does not delete the corresponding loaded experiment instance.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

Export [ExperimentServiceExportRequest](#zen_api.acquisition.v1beta.ExperimentServiceExportRequest) [ExperimentServiceExportResponse](#zen_api.acquisition.v1beta.ExperimentServiceExportResponse)

Returns xml representation of an experiment.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetAvailableExperiments [ExperimentServiceGetAvailableExperimentsRequest](#zen_api.acquisition.v1beta.ExperimentServiceGetAvailableExperimentsRequest) [ExperimentServiceGetAvailableExperimentsResponse](#zen_api.acquisition.v1beta.ExperimentServiceGetAvailableExperimentsResponse)

Retrieves a list of all available experiments of the system.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetImageOutputPath [ExperimentServiceGetImageOutputPathRequest](#zen_api.acquisition.v1beta.ExperimentServiceGetImageOutputPathRequest) [ExperimentServiceGetImageOutputPathResponse](#zen_api.acquisition.v1beta.ExperimentServiceGetImageOutputPathResponse)

Gets the location where the images will be stored on the machine where ZEN Client is running.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetStatus [ExperimentServiceGetStatusRequest](#zen_api.acquisition.v1beta.ExperimentServiceGetStatusRequest) [ExperimentServiceGetStatusResponse](#zen_api.acquisition.v1beta.ExperimentServiceGetStatusResponse)

Gets status of an experiment. The information is updated in interval (several times per seconds). As a result, some status updates could be skipped.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Import [ExperimentServiceImportRequest](#zen_api.acquisition.v1beta.ExperimentServiceImportRequest) [ExperimentServiceImportResponse](#zen_api.acquisition.v1beta.ExperimentServiceImportResponse)

Imports an experiment from the provided experiment xml string. This method returns the info needed to reference the imported experiment.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Load [ExperimentServiceLoadRequest](#zen_api.acquisition.v1beta.ExperimentServiceLoadRequest) [ExperimentServiceLoadResponse](#zen_api.acquisition.v1beta.ExperimentServiceLoadResponse)

Loads an experiment from the available experiments. Consequently, the experiment is ready to be executed or modified. This method returns the info needed to reference the loaded experiment.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

RegisterOnStatusChanged [ExperimentServiceRegisterOnStatusChangedRequest](#zen_api.acquisition.v1beta.ExperimentServiceRegisterOnStatusChangedRequest) [ExperimentServiceRegisterOnStatusChangedResponse](#zen_api.acquisition.v1beta.ExperimentServiceRegisterOnStatusChangedResponse) stream

Register on experiment status changed events. The information is updated in interval (several times per seconds). As a result, some status updates could be skipped. The notifications can be retrieved for experiments which are active at the time the method is invoked. If the method is invoked after an experiment is finished, the call will throw an exception.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

RunExperiment [ExperimentServiceRunExperimentRequest](#zen_api.acquisition.v1beta.ExperimentServiceRunExperimentRequest) [ExperimentServiceRunExperimentResponse](#zen_api.acquisition.v1beta.ExperimentServiceRunExperimentResponse)

Executes an experiment and waits until the experiment execution is finished. This means that the method will block until the experiment was successfully completed, it fails, or it is cancelled. If the call is interrupted (e.g., caller is not available anymore) the experiment will be stopped.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

RunSnap [ExperimentServiceRunSnapRequest](#zen_api.acquisition.v1beta.ExperimentServiceRunSnapRequest) [ExperimentServiceRunSnapResponse](#zen_api.acquisition.v1beta.ExperimentServiceRunSnapResponse)

Acquires a single snap image with the activated channels in the specified experiment and waits until the process of acquiring snap is finished. This means that the method will block until the experiment was successfully completed, it fails, or it is cancelled. If the call is interrupted (e.g., caller is not available anymore) the snap will be stopped.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Save [ExperimentServiceSaveRequest](#zen_api.acquisition.v1beta.ExperimentServiceSaveRequest) [ExperimentServiceSaveResponse](#zen_api.acquisition.v1beta.ExperimentServiceSaveResponse)

Saves a loaded experiment to the predefined location on disk.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

StartContinuous [ExperimentServiceStartContinuousRequest](#zen_api.acquisition.v1beta.ExperimentServiceStartContinuousRequest) [.google.protobuf.Empty](https://protobuf.dev/reference/protobuf/google.protobuf/#empty)

Starts the continuous with the activated channels in the specified experiment and waits for the acquisition to start. After that point continuous will run until it is explicitly stopped or it fails - even if the caller is not available anymore.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

StartExperiment [ExperimentServiceStartExperimentRequest](#zen_api.acquisition.v1beta.ExperimentServiceStartExperimentRequest) [ExperimentServiceStartExperimentResponse](#zen_api.acquisition.v1beta.ExperimentServiceStartExperimentResponse)

Starts the process of executing an experiment and waits for the acquisition to start. After that point the experiment will either run to completion (successful or not) or until it is explicitly stopped - even if the caller is not available anymore.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

StartLive [ExperimentServiceStartLiveRequest](#zen_api.acquisition.v1beta.ExperimentServiceStartLiveRequest) [.google.protobuf.Empty](https://protobuf.dev/reference/protobuf/google.protobuf/#empty)

Starts live with the requested track in the specified experiment and waits for the acquisition to start. After that point live will run until it is explicitly stopped or it fails - even if the caller is not available anymore.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

StartSnap [ExperimentServiceStartSnapRequest](#zen_api.acquisition.v1beta.ExperimentServiceStartSnapRequest) [ExperimentServiceStartSnapResponse](#zen_api.acquisition.v1beta.ExperimentServiceStartSnapResponse)

Starts the process of acquiring a single snap image with the activated channels in the specified experiment and waits for the acquisition to start. After that point the snap will either run to completion (successful or not) or until it is explicitly stopped - even if the caller is not available anymore.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Stop [ExperimentServiceStopRequest](#zen_api.acquisition.v1beta.ExperimentServiceStopRequest) [ExperimentServiceStopResponse](#zen_api.acquisition.v1beta.ExperimentServiceStopResponse)

Stops the specified experiment or one of the active experiments if the experiment ID is not provided. This will stop any type of experiment (i.e., experiment, snap, continuous, live) if it is active and known to this service. This method returns the info needed to reference the stopped experiment.

## zen\_api/acquisition/v1beta/experiment\_status.proto

[Top](#title)

### ExperimentStatus

Status of an experiment.

The index properties are 0-based.

If a value is 0 or -1 it means the value is not initialized or

the running experiment does not have the corresponding dimension.

In case of indices, 0 value can also refer to the first element.

| Field                    | Type                                                                                          | Label | Description                                                                                                                                                                                                                                       |
| ------------------------ | --------------------------------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tiles\_index             | [int32](#int32)                                                                               |       | The current or already acquired (depending of the dimension order) tiles position index of the currently acquired scene.                                                                                                                          |
| tiles\_count             | [int32](#int32)                                                                               |       | The tiles count of the currently acquired scene.                                                                                                                                                                                                  |
| cumulated\_tiles\_count  | [int32](#int32)                                                                               |       | The total tiles count of all scenes.                                                                                                                                                                                                              |
| scenes\_index            | [int32](#int32)                                                                               |       | The current or already acquired (depending of the dimension order) scene index (= tile region/position index).                                                                                                                                    |
| scenes\_count            | [int32](#int32)                                                                               |       | The total scene count (= tile region/position count).                                                                                                                                                                                             |
| time\_points\_index      | [int32](#int32)                                                                               |       | The current or already acquired (depending of the dimension order) time point index in time series.                                                                                                                                               |
| time\_points\_count      | [int32](#int32)                                                                               |       | The number of time points in time series.                                                                                                                                                                                                         |
| zstack\_slices\_index    | [int32](#int32)                                                                               |       | The current or already acquired (depending of the dimension order) z-stack slice index.                                                                                                                                                           |
| zstack\_slices\_count    | [int32](#int32)                                                                               |       | The total count of z-stack slices.                                                                                                                                                                                                                |
| channels\_index          | [int32](#int32)                                                                               |       | The current or already acquired (depending of the dimension order) channel index.                                                                                                                                                                 |
| channels\_count          | [int32](#int32)                                                                               |       | The total channel count.                                                                                                                                                                                                                          |
| images\_acquired\_index  | [int32](#int32)                                                                               |       | The number of acquired images over all dimensions (channels, time series, z-stack, cumulated tiles).                                                                                                                                              |
| images\_count            | [int32](#int32)                                                                               |       | The images count over all dimensions (channels, time series, z-stack, cumulated tiles). This value is relevant only for acquisition where end is determined (standard experiment and Snap), therefore it is not relevant for Continuous and Live. |
| is\_experiment\_running  | [bool](#bool)                                                                                 |       | A value indicating whether the experiment is currently running.                                                                                                                                                                                   |
| is\_acquisition\_running | [bool](#bool)                                                                                 |       | A value indicating whether an acquisition is currently running.                                                                                                                                                                                   |
| total\_elapsed\_time     | [google.protobuf.Duration](https://protobuf.dev/reference/protobuf/google.protobuf/#duration) |       | The total time that elapsed since the start of the running experiment.                                                                                                                                                                            |

## zen\_api/acquisition/v1beta/experiment\_streaming\_service.proto

[Top](#title)

### ExperimentStreamingServiceMonitorAllExperimentsRequest

The ExperimentStreamingServiceMonitorAllExperimentsRequest class.

| Field             | Type                                                                                               | Label | Description                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------- | -------------------------------------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| channel\_index    | [google.protobuf.Int32Value](https://protobuf.dev/reference/protobuf/google.protobuf/#int32-value) |       | Optional parameter for filtering by specific channel. If the channel index is provided, then only that channel will be monitored, but if the channel index is not provided, then all channels will be monitored.                                                                                                                                                                                                                                  |
| enable\_raw\_data | [bool](#bool)                                                                                      |       | Value indicating whether the streamed frame data contains raw frames as received from the acquisition (when set), which can be either full or partial frames (e.g., in general LM cameras produce full frames and LSM and EM detectors produce partial frames/lines). Otherwise (when not set) the streamed frame data contains only full frames, which means that in the case of partial frames/lines, they would be assembled into full frames. |

### ExperimentStreamingServiceMonitorAllExperimentsResponse

Response object of the method for monitoring all experiments.

| Field       | Type                                               | Label | Description                  |
| ----------- | -------------------------------------------------- | ----- | ---------------------------- |
| frame\_data | [FrameData](#zen_api.acquisition.v1beta.FrameData) |       | The experiment's frame data. |

### ExperimentStreamingServiceMonitorExperimentRequest

The ExperimentStreamingServiceMonitorExperimentRequest class.

| Field             | Type                                                                                               | Label | Description                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------- | -------------------------------------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| experiment\_id    | [string](#string)                                                                                  |       | ID of the experiment to monitor.                                                                                                                                                                                                                                                                                                                                                                                                                  |
| channel\_index    | [google.protobuf.Int32Value](https://protobuf.dev/reference/protobuf/google.protobuf/#int32-value) |       | Optional parameter for filtering by specific channel. If the channel index is provided, then only that channel will be monitored, but if the channel index is not provided, then all channels will be monitored.                                                                                                                                                                                                                                  |
| enable\_raw\_data | [bool](#bool)                                                                                      |       | Value indicating whether the streamed frame data contains raw frames as received from the acquisition (when set), which can be either full or partial frames (e.g., in general LM cameras produce full frames and LSM and EM detectors produce partial frames/lines). Otherwise (when not set) the streamed frame data contains only full frames, which means that in the case of partial frames/lines, they would be assembled into full frames. |

### ExperimentStreamingServiceMonitorExperimentResponse

Response object of the method for monitoring an experiment.

| Field       | Type                                               | Label | Description                  |
| ----------- | -------------------------------------------------- | ----- | ---------------------------- |
| frame\_data | [FrameData](#zen_api.acquisition.v1beta.FrameData) |       | The experiment's frame data. |

### ExperimentStreamingService

The IExperimentStreamingService interface.

KindMethod NameRequest TypeResponse TypeDescription

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

MonitorAllExperiments [ExperimentStreamingServiceMonitorAllExperimentsRequest](#zen_api.acquisition.v1beta.ExperimentStreamingServiceMonitorAllExperimentsRequest) [ExperimentStreamingServiceMonitorAllExperimentsResponse](#zen_api.acquisition.v1beta.ExperimentStreamingServiceMonitorAllExperimentsResponse) stream

Starts monitoring all experiments.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

MonitorExperiment [ExperimentStreamingServiceMonitorExperimentRequest](#zen_api.acquisition.v1beta.ExperimentStreamingServiceMonitorExperimentRequest) [ExperimentStreamingServiceMonitorExperimentResponse](#zen_api.acquisition.v1beta.ExperimentStreamingServiceMonitorExperimentResponse) stream

Starts monitoring the specified experiment.

## zen\_api/acquisition/v1beta/frame\_data.proto

[Top](#title)

### FrameData

A simple container for the frame data. This can contain either a full frame or only a part

of it (e.g., in case of partial acquisition when working with EM and LSM).

| Field                  | Type                                                                 | Label | Description                                                                                                                                                                                                                                |
| ---------------------- | -------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| experiment\_id         | [string](#string)                                                    |       | The ID of the experiment.                                                                                                                                                                                                                  |
| frame\_number          | [int32](#int32)                                                      |       | The frame sequence number. One frame can represent either a single image taken by the camera or one full scan in case of partial acquisition. One frame can also contain multiple channels if they are acquired in the same image or scan. |
| frame\_position        | [FramePosition](#zen_api.acquisition.v1beta.FramePosition)           |       | The position of the full frame.                                                                                                                                                                                                            |
| frame\_size            | [zen\_api.common.v1.IntSize](#zen_api.common.v1.IntSize)             |       | The size of the full frame (in pixels).                                                                                                                                                                                                    |
| frame\_stage\_position | [FrameStagePosition](#zen_api.acquisition.v1beta.FrameStagePosition) |       | The stage position of the acquired full frame.                                                                                                                                                                                             |
| scaling                | [Scaling](#zen_api.acquisition.v1beta.Scaling)                       |       | The scaling of the frame.                                                                                                                                                                                                                  |
| pixel\_data            | [FramePixelData](#zen_api.acquisition.v1beta.FramePixelData)         |       | The pixel data of the frame. This can contain either the pixels of a full frame or only a part of it (e.g., a line or a rectangle in case of partial acquisition when working with EM and LSM).                                            |

## zen\_api/acquisition/v1beta/frame\_pixel\_data.proto

[Top](#title)

### FramePixelData

A simple container for the frame pixel data. This can contain either the pixels of a full

frame or only a part of it (e.g., a line or a rectangle in case of partial acquisition when

working with EM and LSM).

| Field           | Type                                                       | Label | Description                                                                                                                                                                                                                                                                                                                                                           |
| --------------- | ---------------------------------------------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| start\_position | [zen\_api.common.v1.IntPoint](#zen_api.common.v1.IntPoint) |       | The start position (in pixels) of the pixel data in the frame. Together with the size property, this represents the rectangle where the pixels are located inside the full frame. For ordinary acquisition this will be the top left corner of the frame, but for partial acquisition this can be any position inside the full frame relative to the top left corner. |
| size            | [zen\_api.common.v1.IntSize](#zen_api.common.v1.IntSize)   |       | Size (in pixels) of the pixel data. Together with the start position property, this represents the rectangle where the pixels are located inside the full frame. For ordinary acquisition this will be the full frame size, but for partial acquisition this can be just one part of the full frame.                                                                  |
| pixel\_type     | [PixelType](#zen_api.acquisition.v1beta.PixelType)         |       | The pixel type of the frame.                                                                                                                                                                                                                                                                                                                                          |
| raw\_data       | [bytes](#bytes)                                            |       | The raw pixel data. The value of individual pixels is contained in this container. The pixel values need to be extracted from the raw byte data. The number of bits needed to extract a single pixel from the raw byte data and the format it is stored in is determined by the pixel type property.                                                                  |

## zen\_api/acquisition/v1beta/frame\_position.proto

[Top](#title)

### FramePosition

Defines the position of the frame in multiple dimensions.

| Field | Type            | Label | Description                                                                                                                                                                         |
| ----- | --------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| x     | [int32](#int32) |       | The pixel index in X direction of the top left corner of the frame.                                                                                                                 |
| y     | [int32](#int32) |       | The pixel index in Y direction of the top left corner of the frame.                                                                                                                 |
| z     | [int32](#int32) |       | The Z slice index of the of the frame.                                                                                                                                              |
| t     | [int32](#int32) |       | The time point of the frame in a sequentially acquired series of data. Note that this doesn't represents the exact time of acquisition but only the sequence of the acquired image. |
| s     | [int32](#int32) |       | The scene index.                                                                                                                                                                    |
| m     | [int32](#int32) |       | The mosaic tile index.                                                                                                                                                              |
| c     | [int32](#int32) |       | The channel index in a multi-channel data set.                                                                                                                                      |
| h     | [int32](#int32) |       | The raw data index.                                                                                                                                                                 |

## zen\_api/acquisition/v1beta/frame\_stage\_position.proto

[Top](#title)

### FrameStagePosition

Defines the stage position of the acquired frame.

| Field | Type                                                                                                 | Label | Description                                  |
| ----- | ---------------------------------------------------------------------------------------------------- | ----- | -------------------------------------------- |
| x     | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The stage position in X direction (unit: m). |
| y     | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The stage position in Y direction (unit: m). |
| z     | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The stage position in Z direction (unit: m). |

## zen\_api/acquisition/v1beta/pixel\_type.proto

[Top](#title)

### PixelType

Pixel type of image data.

| Name                     | Number | Description                                                          |
| ------------------------ | ------ | -------------------------------------------------------------------- |
| PIXEL\_TYPE\_UNSPECIFIED | 0      | Default value if status is not specified.                            |
| PIXEL\_TYPE\_GRAY8       | 1      | 8 bit unsigned.                                                      |
| PIXEL\_TYPE\_GRAY16      | 2      | 16 bit unsigned.                                                     |
| PIXEL\_TYPE\_BGR24       | 4      | 8 bit triples, representing the color channels Blue, Green and Red.  |
| PIXEL\_TYPE\_BGR48       | 5      | 16 bit triples, representing the color channels Blue, Green and Red. |

## zen\_api/acquisition/v1beta/scaling.proto

[Top](#title)

### Scaling

Defines the scaling of the acquired frame.

| Field | Type              | Label | Description                                 |
| ----- | ----------------- | ----- | ------------------------------------------- |
| x     | [double](#double) |       | The scaling in X dimension (unit: m/pixel). |
| y     | [double](#double) |       | The scaling in Y dimension (unit: m/pixel). |

## zen\_api/application/v1/composition\_service.proto

[Top](#title)

### CompositionServiceCreateModuleRequest

The CompositionServiceCreateModuleRequest class.

| Field                      | Type              | Label | Description                           |
| -------------------------- | ----------------- | ----- | ------------------------------------- |
| module\_id                 | [string](#string) |       | The id of the module.                 |
| display\_name              | [string](#string) |       | The display name of the module.       |
| description                | [string](#string) |       | The description of the module.        |
| license\_string            | [string](#string) |       | The license string.                   |
| minimum\_required\_version | [string](#string) |       | The minimum required feature version. |

### CompositionServiceCreateModuleResponse

The CompositionServiceCreateModuleResponse class.

### CompositionServiceIsModuleAvailableRequest

The CompositionServiceIsModuleAvailableRequest class.

| Field      | Type              | Label | Description    |
| ---------- | ----------------- | ----- | -------------- |
| module\_id | [string](#string) |       | The module id. |

### IsModuleAvailableResponse

Response object of the method for checking the availability state of a composition module.

| Field         | Type          | Label | Description                                                |
| ------------- | ------------- | ----- | ---------------------------------------------------------- |
| is\_available | [bool](#bool) |       | A value indicating whether the module is available or not. |

### CompositionService

The ICompositionService interface.

KindMethod NameRequest TypeResponse TypeDescription

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

CreateModule [CompositionServiceCreateModuleRequest](#zen_api.application.v1.CompositionServiceCreateModuleRequest) [CompositionServiceCreateModuleResponse](#zen_api.application.v1.CompositionServiceCreateModuleResponse)

Creates a module and adds it to the selected profile. With this method, a client can 'inject' a new module at runtime (e.g. via OAD script or ZEN API). After adding the module, it will appear as optional module of the selected profile just as any other module. The Module Manager can be used to verify this. After adding the module, the client can make use of the 'normal' license infrastructure to check the avaiability of the newly added module. Note: A module is available, if the module is licensed AND the user has enabled it (via the Module Manager). In case a module gets added via this method, the module is enabled by default.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

IsModuleAvailable [CompositionServiceIsModuleAvailableRequest](#zen_api.application.v1.CompositionServiceIsModuleAvailableRequest) [IsModuleAvailableResponse](#zen_api.application.v1.IsModuleAvailableResponse)

Returns the availability state of the given module.

## zen\_api/common/v1/double\_point.proto

[Top](#title)

### DoublePoint

Double-based point object.

| Field | Type              | Label | Description                  |
| ----- | ----------------- | ----- | ---------------------------- |
| x     | [double](#double) |       | The coordinate X of a point. |
| y     | [double](#double) |       | The coordinate Y of a point. |

## zen\_api/common/v1/int\_point.proto

[Top](#title)

### IntPoint

Integer-based point.

| Field | Type            | Label | Description                  |
| ----- | --------------- | ----- | ---------------------------- |
| x     | [int32](#int32) |       | The coordinate X of a point. |
| y     | [int32](#int32) |       | The coordinate Y of a point. |

## zen\_api/common/v1/int\_size.proto

[Top](#title)

### IntSize

Integer-based size.

| Field  | Type            | Label | Description |
| ------ | --------------- | ----- | ----------- |
| width  | [int32](#int32) |       | The width.  |
| height | [int32](#int32) |       | The height. |

## zen\_api/hardware/v1/axis\_identifier.proto

[Top](#title)

### AxisIdentifier

Unique identifier for axis.

| Name                          | Number | Description                                                              |
| ----------------------------- | ------ | ------------------------------------------------------------------------ |
| AXIS\_IDENTIFIER\_UNSPECIFIED | 0      | Default enum value.                                                      |
| AXIS\_IDENTIFIER\_X           | 1      | X axis (translation axis). Controlled by length, default unit is meters. |
| AXIS\_IDENTIFIER\_Y           | 2      | Y axis (translation axis). Controlled by length, default unit is meters. |
| AXIS\_IDENTIFIER\_Z           | 3      | Z axis (translation axis). Controlled by length, default unit is meters. |
| AXIS\_IDENTIFIER\_R           | 4      | R axis (rotation axis). Controlled by angle, default unit is radians.    |
| AXIS\_IDENTIFIER\_T           | 5      | T axis (rotation axis). Controlled by angle, default unit is radians.    |
| AXIS\_IDENTIFIER\_M           | 6      | M axis (translation axis). Controlled by length, default unit is meters. |

## zen\_api/hardware/v1/stage\_axis.proto

[Top](#title)

### StageAxis

Abstract representation of an arbitrary axis.

| Field    | Type                                                  | Label | Description                                    |
| -------- | ----------------------------------------------------- | ----- | ---------------------------------------------- |
| axis     | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |       | The axis identifier.                           |
| position | [double](#double)                                     |       | The position of the axis in meters or radians. |

## zen\_api/hardware/v1/stage\_motion\_state.proto

[Top](#title)

### StageMotionState

Stage motion state for ZenApi.

| Name                              | Number | Description                                                                                   |
| --------------------------------- | ------ | --------------------------------------------------------------------------------------------- |
| STAGE\_MOTION\_STATE\_UNSPECIFIED | 0      | Default enum value.                                                                           |
| STAGE\_MOTION\_STATE\_UNKNOWN     | 1      | Should not occur in a well configured system.                                                 |
| STAGE\_MOTION\_STATE\_ERROR       | 2      | The stage cannot perform any task. Software restart and/or physical intervention is required. |
| STAGE\_MOTION\_STATE\_IDLE        | 3      | The stage is not moving.                                                                      |
| STAGE\_MOTION\_STATE\_MOVING      | 4      | The stage is in motion.                                                                       |

## zen\_api/hardware/v1/stage\_service.proto

[Top](#title)

### StageServiceAxisVelocityResponse

Abstract representation of an arbitrary axis and it's velocity.

| Field    | Type                                                  | Label | Description                                                          |
| -------- | ----------------------------------------------------- | ----- | -------------------------------------------------------------------- |
| axis     | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |       | The axis identifier.                                                 |
| velocity | [double](#double)                                     |       | The velocity of the axis in meters per second or radians per second. |

### StageServiceGetAvailableStageAxisRequest

The StageServiceGetAvailableStageAxisRequest class.

### StageServiceGetAvailableStageAxisResponse

Response object of available stage axis.

| Field           | Type                                                  | Label    | Description |
| --------------- | ----------------------------------------------------- | -------- | ----------- |
| available\_axis | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) | repeated |             |

### StageServiceGetAxisPositionRequest

The StageServiceGetAxisPositionRequest class.

| Field    | Type                                                  | Label | Description        |
| -------- | ----------------------------------------------------- | ----- | ------------------ |
| axis\_id | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |       | The requested axe. |

### StageServiceGetAxisPositionResponse

Abstract representation of an arbitrary axis.

| Field    | Type                                                  | Label | Description                                    |
| -------- | ----------------------------------------------------- | ----- | ---------------------------------------------- |
| axis     | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |       | The axis identifier.                           |
| position | [double](#double)                                     |       | The position of the axis in meters or radians. |

### StageServiceGetAxisVelocityRequest

The StageServiceGetAxisVelocityRequest class.

| Field    | Type                                                  | Label | Description         |
| -------- | ----------------------------------------------------- | ----- | ------------------- |
| axis\_id | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |       | The requested axis. |

### StageServiceGetAxisVelocityResponse

Abstract representation of an arbitrary axis and it's velocity.

| Field    | Type                                                  | Label | Description                                                          |
| -------- | ----------------------------------------------------- | ----- | -------------------------------------------------------------------- |
| axis     | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |       | The axis identifier.                                                 |
| velocity | [double](#double)                                     |       | The velocity of the axis in meters per second or radians per second. |

### StageServiceGetStageMotionStateRequest

The StageServiceGetStageMotionStateRequest class.

### StageServiceGetStageMotionStateResponse

StageMotionState enum response.

| Field | Type                                                      | Label | Description             |
| ----- | --------------------------------------------------------- | ----- | ----------------------- |
| state | [StageMotionState](#zen_api.hardware.v1.StageMotionState) |       | The stage motion state. |

### StageServiceGetStagePositionRequest

The StageServiceGetStagePositionRequest class.

### StageServiceGetStagePositionResponse

Response object of stage axis positions.

| Field           | Type                                        | Label    | Description                             |
| --------------- | ------------------------------------------- | -------- | --------------------------------------- |
| axis\_positions | [StageAxis](#zen_api.hardware.v1.StageAxis) | repeated | The available axis and their positions. |

### StageServiceGetStageStateRequest

The StageServiceGetStageStateRequest class.

### StageServiceGetStageStateResponse

StageState enum response.

| Field | Type                                          | Label | Description      |
| ----- | --------------------------------------------- | ----- | ---------------- |
| state | [StageState](#zen_api.hardware.v1.StageState) |       | The stage state. |

### StageServiceGetStageVelocityRequest

The StageServiceGetStageVelocityRequest class.

### StageServiceGetStageVelocityResponse

Response object of stage axis velocities.

| Field            | Type                                                                                      | Label    | Description                              |
| ---------------- | ----------------------------------------------------------------------------------------- | -------- | ---------------------------------------- |
| axis\_velocities | [StageServiceAxisVelocityResponse](#zen_api.hardware.v1.StageServiceAxisVelocityResponse) | repeated | The available axis and their velocities. |

### StageServiceInitializeStageRequest

The StageServiceInitializeStageRequest class.

### StageServiceInitializeStageResponse

Response object of the initialize stage method.

| Field         | Type          | Label | Description                                                                   |
| ------------- | ------------- | ----- | ----------------------------------------------------------------------------- |
| task\_success | [bool](#bool) |       | A value indicating whether the task to initialize the stage succeeded or not. |

### StageServiceMoveToRequest

The StageServiceMoveToRequest class.

| Field          | Type                                        | Label    | Description                                                 |
| -------------- | ------------------------------------------- | -------- | ----------------------------------------------------------- |
| axis\_to\_move | [StageAxis](#zen_api.hardware.v1.StageAxis) | repeated | The stage axis that should move. The position is in meters. |

### StageServiceMoveToResponse

Response object of the MoveStage method.

| Field         | Type          | Label | Description                                                             |
| ------------- | ------------- | ----- | ----------------------------------------------------------------------- |
| task\_success | [bool](#bool) |       | A value indicating whether the task to move the stage succeeded or not. |

### StageServiceRegisterOnStageMotionStateChangedRequest

The StageServiceRegisterOnStageMotionStateChangedRequest class.

### StageServiceRegisterOnStageMotionStateChangedResponse

StageMotionState enum response.

| Field | Type                                                      | Label | Description             |
| ----- | --------------------------------------------------------- | ----- | ----------------------- |
| state | [StageMotionState](#zen_api.hardware.v1.StageMotionState) |       | The stage motion state. |

### StageServiceRegisterOnStagePositionChangedRequest

The StageServiceRegisterOnStagePositionChangedRequest class.

### StageServiceRegisterOnStagePositionChangedResponse

Abstract representation of an arbitrary axis.

| Field    | Type                                                  | Label | Description                                    |
| -------- | ----------------------------------------------------- | ----- | ---------------------------------------------- |
| axis     | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |       | The axis identifier.                           |
| position | [double](#double)                                     |       | The position of the axis in meters or radians. |

### StageServiceRegisterOnStageStateChangedRequest

The StageServiceRegisterOnStageStateChangedRequest class.

### StageServiceRegisterOnStageStateChangedResponse

StageState enum response.

| Field | Type                                          | Label | Description      |
| ----- | --------------------------------------------- | ----- | ---------------- |
| state | [StageState](#zen_api.hardware.v1.StageState) |       | The stage state. |

### StageServiceRegisterOnStageVelocityChangedRequest

The StageServiceRegisterOnStageVelocityChangedRequest class.

### StageServiceRegisterOnStageVelocityChangedResponse

Abstract representation of an arbitrary axis and it's velocity.

| Field    | Type                                                  | Label | Description                                                          |
| -------- | ----------------------------------------------------- | ----- | -------------------------------------------------------------------- |
| axis     | [AxisIdentifier](#zen_api.hardware.v1.AxisIdentifier) |       | The axis identifier.                                                 |
| velocity | [double](#double)                                     |       | The velocity of the axis in meters per second or radians per second. |

### StageServiceStopRequest

The StageServiceStopRequest class.

### StageServiceStopResponse

The StageServiceStopResponse class.

### StageService

The IStageService interface.

KindMethod NameRequest TypeResponse TypeDescription

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetAvailableStageAxis [StageServiceGetAvailableStageAxisRequest](#zen_api.hardware.v1.StageServiceGetAvailableStageAxisRequest) [StageServiceGetAvailableStageAxisResponse](#zen_api.hardware.v1.StageServiceGetAvailableStageAxisResponse)

Retrieves all available stage axis on this system.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetAxisPosition [StageServiceGetAxisPositionRequest](#zen_api.hardware.v1.StageServiceGetAxisPositionRequest) [StageServiceGetAxisPositionResponse](#zen_api.hardware.v1.StageServiceGetAxisPositionResponse)

Gets the current position of an axis of the stage.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetAxisVelocity [StageServiceGetAxisVelocityRequest](#zen_api.hardware.v1.StageServiceGetAxisVelocityRequest) [StageServiceGetAxisVelocityResponse](#zen_api.hardware.v1.StageServiceGetAxisVelocityResponse)

Gets the current velocity of an axis of the stage.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetStageMotionState [StageServiceGetStageMotionStateRequest](#zen_api.hardware.v1.StageServiceGetStageMotionStateRequest) [StageServiceGetStageMotionStateResponse](#zen_api.hardware.v1.StageServiceGetStageMotionStateResponse)

Retrieves the current stage motion state.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetStagePosition [StageServiceGetStagePositionRequest](#zen_api.hardware.v1.StageServiceGetStagePositionRequest) [StageServiceGetStagePositionResponse](#zen_api.hardware.v1.StageServiceGetStagePositionResponse)

Retrieves the current stage position. This will return the positions of all available axis..

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetStageState [StageServiceGetStageStateRequest](#zen_api.hardware.v1.StageServiceGetStageStateRequest) [StageServiceGetStageStateResponse](#zen_api.hardware.v1.StageServiceGetStageStateResponse)

Retrieves the current stage state.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetStageVelocity [StageServiceGetStageVelocityRequest](#zen_api.hardware.v1.StageServiceGetStageVelocityRequest) [StageServiceGetStageVelocityResponse](#zen_api.hardware.v1.StageServiceGetStageVelocityResponse)

Retrieves the current stage velocity. This will return the velocity of all available axis.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

InitializeStage [StageServiceInitializeStageRequest](#zen_api.hardware.v1.StageServiceInitializeStageRequest) [StageServiceInitializeStageResponse](#zen_api.hardware.v1.StageServiceInitializeStageResponse)

Starts an initialization routine for the stage to initialize all stage axis. This may take a while and the stage is moving in this time.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

MoveTo [StageServiceMoveToRequest](#zen_api.hardware.v1.StageServiceMoveToRequest) [StageServiceMoveToResponse](#zen_api.hardware.v1.StageServiceMoveToResponse)

Moves the stage.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

RegisterOnStageMotionStateChanged [StageServiceRegisterOnStageMotionStateChangedRequest](#zen_api.hardware.v1.StageServiceRegisterOnStageMotionStateChangedRequest) [StageServiceRegisterOnStageMotionStateChangedResponse](#zen_api.hardware.v1.StageServiceRegisterOnStageMotionStateChangedResponse) stream

Notification about changes of the stage motion state.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

RegisterOnStagePositionChanged [StageServiceRegisterOnStagePositionChangedRequest](#zen_api.hardware.v1.StageServiceRegisterOnStagePositionChangedRequest) [StageServiceRegisterOnStagePositionChangedResponse](#zen_api.hardware.v1.StageServiceRegisterOnStagePositionChangedResponse) stream

Notification about changes of all stage axis positions.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

RegisterOnStageStateChanged [StageServiceRegisterOnStageStateChangedRequest](#zen_api.hardware.v1.StageServiceRegisterOnStageStateChangedRequest) [StageServiceRegisterOnStageStateChangedResponse](#zen_api.hardware.v1.StageServiceRegisterOnStageStateChangedResponse) stream

Notification about changes of the stage state.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

RegisterOnStageVelocityChanged [StageServiceRegisterOnStageVelocityChangedRequest](#zen_api.hardware.v1.StageServiceRegisterOnStageVelocityChangedRequest) [StageServiceRegisterOnStageVelocityChangedResponse](#zen_api.hardware.v1.StageServiceRegisterOnStageVelocityChangedResponse) stream

Notification about changes of all stage axis velocities.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Stop [StageServiceStopRequest](#zen_api.hardware.v1.StageServiceStopRequest) [StageServiceStopResponse](#zen_api.hardware.v1.StageServiceStopResponse)

Immediately stops the stage.

## zen\_api/hardware/v1/stage\_state.proto

[Top](#title)

### StageState

Stage state for ZenApi.

| Name                                 | Number | Description                                                                                                                                   |
| ------------------------------------ | ------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| STAGE\_STATE\_UNSPECIFIED            | 0      | Default enum value.                                                                                                                           |
| STAGE\_STATE\_UNKNOWN                | 1      | Should not occur in a well configured system.                                                                                                 |
| STAGE\_STATE\_ERROR                  | 2      | The stage cannot perform any task. Software restart and/or physical intervention is required.                                                 |
| STAGE\_STATE\_NORMAL                 | 3      | The state is functioning normally and can be used.                                                                                            |
| STAGE\_STATE\_INITIALIZING           | 4      | The stage is in the process of reinitializing one or more axes, should not be used, and will ignore value sets and commands other than stop.  |
| STAGE\_STATE\_INITIALIZATION\_NEEDED | 5      | The stage will respond to motion commands, but positions may be reported erroneously, and the stage should be initialized before further use. |

## zen\_api/workflows/v1/start\_job\_options.proto

[Top](#title)

### StartJobOptions

Start Job options.

| Field        | Type              | Label | Description                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ----------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| result\_path | [string](#string) |       | A value indicating a path for saving a Job results in the file system. -- If value is given than Job output will be copied to given path in filesystem and not uploaded to ZEN Archive. Have to be in the Windows-supported directory path format (local drive or network share). -- If value is null (or empty/whitespace) than Job output will be uploaded to ZEN Archive and not copied to anywhere. |

## zen\_api/workflows/v1beta/job\_resources\_service.proto

[Top](#title)

### JobResourcesServiceGetAvailableResourcesRequest

The JobResourcesServiceGetAvailableResourcesRequest class.

### JobResourcesServiceGetAvailableResourcesResponse

Response containing the list of all available resource workflow parameters.

| Field     | Type              | Label    | Description                                             |
| --------- | ----------------- | -------- | ------------------------------------------------------- |
| resources | [string](#string) | repeated | The list of all available resource workflow parameters. |

### JobResourcesServiceGetBooleanValueRequest

The JobResourcesServiceGetBooleanValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |

### JobResourcesServiceGetBooleanValueResponse

Response containing the resource's value.

| Field | Type          | Label | Description           |
| ----- | ------------- | ----- | --------------------- |
| value | [bool](#bool) |       | The resource's value. |

### JobResourcesServiceGetDateTimeValueRequest

The JobResourcesServiceGetDateTimeValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |

### JobResourcesServiceGetDateTimeValueResponse

Response containing the resource's value.

| Field | Type              | Label | Description                                                   |
| ----- | ----------------- | ----- | ------------------------------------------------------------- |
| value | [string](#string) |       | The resource's date and time string value in ISO 8601 format. |

### JobResourcesServiceGetDateValueRequest

The JobResourcesServiceGetDateValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |

### JobResourcesServiceGetDateValueResponse

Response containing the resource's value.

| Field | Type              | Label | Description                                          |
| ----- | ----------------- | ----- | ---------------------------------------------------- |
| value | [string](#string) |       | The resource's date string value in ISO 8601 format. |

### JobResourcesServiceGetDoubleValueRequest

The JobResourcesServiceGetDoubleValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |

### JobResourcesServiceGetDoubleValueResponse

Response containing the resource's value.

| Field | Type              | Label | Description           |
| ----- | ----------------- | ----- | --------------------- |
| value | [double](#double) |       | The resource's value. |

### JobResourcesServiceGetFloatValueRequest

The JobResourcesServiceGetFloatValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |

### JobResourcesServiceGetFloatValueResponse

Response containing the resource's value.

| Field | Type            | Label | Description           |
| ----- | --------------- | ----- | --------------------- |
| value | [float](#float) |       | The resource's value. |

### JobResourcesServiceGetIntegerValueRequest

The JobResourcesServiceGetIntegerValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |

### JobResourcesServiceGetIntegerValueResponse

Response containing the resource's value.

| Field | Type            | Label | Description           |
| ----- | --------------- | ----- | --------------------- |
| value | [int32](#int32) |       | The resource's value. |

### JobResourcesServiceGetLongValueRequest

The JobResourcesServiceGetLongValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |

### JobResourcesServiceGetLongValueResponse

Response containing the resource's value.

| Field | Type            | Label | Description           |
| ----- | --------------- | ----- | --------------------- |
| value | [int64](#int64) |       | The resource's value. |

### JobResourcesServiceGetStringValueRequest

The JobResourcesServiceGetStringValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |

### JobResourcesServiceGetStringValueResponse

Response containing the resource's value.

| Field | Type              | Label | Description           |
| ----- | ----------------- | ----- | --------------------- |
| value | [string](#string) |       | The resource's value. |

### JobResourcesServiceGetTimeValueRequest

The JobResourcesServiceGetTimeValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |

### JobResourcesServiceGetTimeValueResponse

Response containing the resource's value.

| Field | Type              | Label | Description                                          |
| ----- | ----------------- | ----- | ---------------------------------------------------- |
| value | [string](#string) |       | The resource's time string value in ISO 8601 format. |

### JobResourcesServiceHasResourceRequest

The JobResourcesServiceHasResourceRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |

### JobResourcesServiceHasResourceResponse

Response containing information if the current job has a resource with the specified ID.

| Field         | Type          | Label | Description                                                                      |
| ------------- | ------------- | ----- | -------------------------------------------------------------------------------- |
| has\_resource | [bool](#bool) |       | A value indicating whether the current job has a resource with the specified ID. |

### JobResourcesServiceIsJobLoadedRequest

The JobResourcesServiceIsJobLoadedRequest class.

### JobResourcesServiceIsJobLoadedResponse

Response containing information if a job is loaded.

| Field           | Type          | Label | Description                                 |
| --------------- | ------------- | ----- | ------------------------------------------- |
| is\_job\_loaded | [bool](#bool) |       | A value indicating whether a job is loaded. |

### JobResourcesServiceSetBooleanValueRequest

The JobResourcesServiceSetBooleanValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |
| value        | [bool](#bool)     |       | The resource's value.   |

### JobResourcesServiceSetBooleanValueResponse

The JobResourcesServiceSetBooleanValueResponse class.

### JobResourcesServiceSetDateTimeValueRequest

The JobResourcesServiceSetDateTimeValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |
| value        | [string](#string) |       | The resource's value.   |

### JobResourcesServiceSetDateTimeValueResponse

The JobResourcesServiceSetDateTimeValueResponse class.

### JobResourcesServiceSetDateValueRequest

The JobResourcesServiceSetDateValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |
| value        | [string](#string) |       | The resource's value.   |

### JobResourcesServiceSetDateValueResponse

The JobResourcesServiceSetDateValueResponse class.

### JobResourcesServiceSetDoubleValueRequest

The JobResourcesServiceSetDoubleValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |
| value        | [double](#double) |       | The resource's value.   |

### JobResourcesServiceSetDoubleValueResponse

The JobResourcesServiceSetDoubleValueResponse class.

### JobResourcesServiceSetFloatValueRequest

The JobResourcesServiceSetFloatValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |
| value        | [float](#float)   |       | The resource's value.   |

### JobResourcesServiceSetFloatValueResponse

The JobResourcesServiceSetFloatValueResponse class.

### JobResourcesServiceSetIntegerValueRequest

The JobResourcesServiceSetIntegerValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |
| value        | [int32](#int32)   |       | The resource's value.   |

### JobResourcesServiceSetIntegerValueResponse

The JobResourcesServiceSetIntegerValueResponse class.

### JobResourcesServiceSetLongValueRequest

The JobResourcesServiceSetLongValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |
| value        | [int64](#int64)   |       | The resource's value.   |

### JobResourcesServiceSetLongValueResponse

The JobResourcesServiceSetLongValueResponse class.

### JobResourcesServiceSetStringValueRequest

The JobResourcesServiceSetStringValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |
| value        | [string](#string) |       | The resource's value.   |

### JobResourcesServiceSetStringValueResponse

The JobResourcesServiceSetStringValueResponse class.

### JobResourcesServiceSetTimeValueRequest

The JobResourcesServiceSetTimeValueRequest class.

| Field        | Type              | Label | Description             |
| ------------ | ----------------- | ----- | ----------------------- |
| resource\_id | [string](#string) |       | The ID of the resource. |
| value        | [string](#string) |       | The resource's value.   |

### JobResourcesServiceSetTimeValueResponse

The JobResourcesServiceSetTimeValueResponse class.

### JobResourcesService

The IJobResourcesService interface.

KindMethod NameRequest TypeResponse TypeDescription

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetAvailableResources [JobResourcesServiceGetAvailableResourcesRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetAvailableResourcesRequest) [JobResourcesServiceGetAvailableResourcesResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetAvailableResourcesResponse)

Retrieves a list of all available resource workflow parameters.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetBooleanValue [JobResourcesServiceGetBooleanValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetBooleanValueRequest) [JobResourcesServiceGetBooleanValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetBooleanValueResponse)

Gets the value of the resource with the specified ID from the current job as a boolean value.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetDateTimeValue [JobResourcesServiceGetDateTimeValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetDateTimeValueRequest) [JobResourcesServiceGetDateTimeValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetDateTimeValueResponse)

Gets the value of the resource with the specified ID from the current job as a date and time string value in ISO 8601 format.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetDateValue [JobResourcesServiceGetDateValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetDateValueRequest) [JobResourcesServiceGetDateValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetDateValueResponse)

Gets the value of the resource with the specified ID from the current job as a date string value in ISO 8601 format.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetDoubleValue [JobResourcesServiceGetDoubleValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetDoubleValueRequest) [JobResourcesServiceGetDoubleValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetDoubleValueResponse)

Gets the value of the resource with the specified ID from the current job as a double precision floating point value.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetFloatValue [JobResourcesServiceGetFloatValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetFloatValueRequest) [JobResourcesServiceGetFloatValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetFloatValueResponse)

Gets the value of the resource with the specified ID from the current job as a single precision floating point value.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetIntegerValue [JobResourcesServiceGetIntegerValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetIntegerValueRequest) [JobResourcesServiceGetIntegerValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetIntegerValueResponse)

Gets the value of the resource with the specified ID from the current job as an integer value.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetLongValue [JobResourcesServiceGetLongValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetLongValueRequest) [JobResourcesServiceGetLongValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetLongValueResponse)

Gets the value of the resource with the specified ID from the current job as a long integer value.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetStringValue [JobResourcesServiceGetStringValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetStringValueRequest) [JobResourcesServiceGetStringValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetStringValueResponse)

Gets the value of the resource with the specified ID from the current job as a string value.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetTimeValue [JobResourcesServiceGetTimeValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceGetTimeValueRequest) [JobResourcesServiceGetTimeValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceGetTimeValueResponse)

Gets the value of the resource with the specified ID from the current job as a time string value in ISO 8601 format.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

HasResource [JobResourcesServiceHasResourceRequest](#zen_api.workflows.v1beta.JobResourcesServiceHasResourceRequest) [JobResourcesServiceHasResourceResponse](#zen_api.workflows.v1beta.JobResourcesServiceHasResourceResponse)

Checks if the current job has a resource with the specified ID.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

IsJobLoaded [JobResourcesServiceIsJobLoadedRequest](#zen_api.workflows.v1beta.JobResourcesServiceIsJobLoadedRequest) [JobResourcesServiceIsJobLoadedResponse](#zen_api.workflows.v1beta.JobResourcesServiceIsJobLoadedResponse)

Checks if a job is loaded.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetBooleanValue [JobResourcesServiceSetBooleanValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetBooleanValueRequest) [JobResourcesServiceSetBooleanValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetBooleanValueResponse)

Sets the value of the resource with the specified ID in the current job as a boolean value or creates the resource if it doesn't exist.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetDateTimeValue [JobResourcesServiceSetDateTimeValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetDateTimeValueRequest) [JobResourcesServiceSetDateTimeValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetDateTimeValueResponse)

Sets the value of the resource with the specified ID in the current job as a date and time string value in ISO 8601 format or creates the resource if it doesn't exist.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetDateValue [JobResourcesServiceSetDateValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetDateValueRequest) [JobResourcesServiceSetDateValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetDateValueResponse)

Sets the value of the resource with the specified ID in the current job as a date string value in ISO 8601 format or creates the resource if it doesn't exist.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetDoubleValue [JobResourcesServiceSetDoubleValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetDoubleValueRequest) [JobResourcesServiceSetDoubleValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetDoubleValueResponse)

Sets the value of the resource with the specified ID in the current job as a double precision floating point value or creates the resource if it doesn't exist.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetFloatValue [JobResourcesServiceSetFloatValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetFloatValueRequest) [JobResourcesServiceSetFloatValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetFloatValueResponse)

Sets the value of the resource with the specified ID in the current job as a single precision floating point value or creates the resource if it doesn't exist.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetIntegerValue [JobResourcesServiceSetIntegerValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetIntegerValueRequest) [JobResourcesServiceSetIntegerValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetIntegerValueResponse)

Sets the value of the resource with the specified ID in the current job as an integer value or creates the resource if it doesn't exist.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetLongValue [JobResourcesServiceSetLongValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetLongValueRequest) [JobResourcesServiceSetLongValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetLongValueResponse)

Sets the value of the resource with the specified ID in the current job as a long integer value or creates the resource if it doesn't exist.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetStringValue [JobResourcesServiceSetStringValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetStringValueRequest) [JobResourcesServiceSetStringValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetStringValueResponse)

Sets the value of the resource with the specified ID in the current job as a string value or creates the resource if it doesn't exist.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetTimeValue [JobResourcesServiceSetTimeValueRequest](#zen_api.workflows.v1beta.JobResourcesServiceSetTimeValueRequest) [JobResourcesServiceSetTimeValueResponse](#zen_api.workflows.v1beta.JobResourcesServiceSetTimeValueResponse)

Sets the value of the resource with the specified ID in the current job as a time string value in ISO 8601 format or creates the resource if it doesn't exist.

## zen\_api/workflows/v2/job\_info.proto

[Top](#title)

### JobInfo

Information about Job executed by the workflow runner contains a real-time updates and Job's events with Job state.

| Field          | Type                                                                                            | Label | Description                               |
| -------------- | ----------------------------------------------------------------------------------------------- | ----- | ----------------------------------------- |
| job\_id        | [string](#string)                                                                               |       | A Job unique runtime ID.                  |
| create\_date   | [google.protobuf.Timestamp](https://protobuf.dev/reference/protobuf/google.protobuf/#timestamp) |       | A date and time when JobInfo was created. |
| status         | [JobStatus](#zen_api.workflows.v2.JobStatus)                                                    |       | A Job execution state.                    |
| start\_options | [zen\_api.workflows.v1.StartJobOptions](#zen_api.workflows.v1.StartJobOptions)                  |       | A Job starting options.                   |

## zen\_api/workflows/v2/job\_status.proto

[Top](#title)

### JobStatus

Runtime status of the Job.

| Name                     | Number | Description                                                                                                           |
| ------------------------ | ------ | --------------------------------------------------------------------------------------------------------------------- |
| JOB\_STATUS\_UNSPECIFIED | 0      | Default value if status is not specified.                                                                             |
| JOB\_STATUS\_RUNNING     | 1      | Job is currently executed by the workflow runner.                                                                     |
| JOB\_STATUS\_PAUSED      | 2      | Job execution is paused (not supported for now and reserved only for future purposes for saving numeration sequence). |
| JOB\_STATUS\_COMPLETED   | 3      | Job execution is successfully completed.                                                                              |
| JOB\_STATUS\_FAILED      | 4      | Job execution was failed.                                                                                             |
| JOB\_STATUS\_CANCELLED   | 5      | Job execution was interrupted (cancelled).                                                                            |
| JOB\_STATUS\_PENDING     | 6      | Job is created but still not started and waiting for beginning of execution.                                          |

## zen\_api/workflows/v2/workflow\_service.proto

[Top](#title)

### WorkflowServiceGetJobInfoRequest

The WorkflowServiceGetJobInfoRequest class.

| Field   | Type              | Label | Description    |
| ------- | ----------------- | ----- | -------------- |
| job\_id | [string](#string) |       | Target Job ID. |

### WorkflowServiceGetJobInfoResponse

Response object representing the job info.

| Field     | Type                                     | Label | Description   |
| --------- | ---------------------------------------- | ----- | ------------- |
| job\_info | [JobInfo](#zen_api.workflows.v2.JobInfo) |       | The job info. |

### WorkflowServiceStartJobRequest

The WorkflowServiceStartJobRequest class.

| Field     | Type                                                                           | Label | Description           |
| --------- | ------------------------------------------------------------------------------ | ----- | --------------------- |
| job\_name | [string](#string)                                                              |       | Job display name.     |
| options   | [zen\_api.workflows.v1.StartJobOptions](#zen_api.workflows.v1.StartJobOptions) |       | Job starting options. |

### WorkflowServiceStartJobResponse

Response object representing the starting of a job.

| Field     | Type                                     | Label | Description   |
| --------- | ---------------------------------------- | ----- | ------------- |
| job\_info | [JobInfo](#zen_api.workflows.v2.JobInfo) |       | The job info. |

### WorkflowServiceStopJobRequest

The WorkflowServiceStopJobRequest class.

| Field   | Type              | Label | Description    |
| ------- | ----------------- | ----- | -------------- |
| job\_id | [string](#string) |       | Target Job ID. |

### WorkflowServiceStopJobResponse

The WorkflowServiceStopJobResponse class.

### WorkflowServiceWaitJobRequest

The WorkflowServiceWaitJobRequest class.

| Field   | Type              | Label | Description    |
| ------- | ----------------- | ----- | -------------- |
| job\_id | [string](#string) |       | Target Job ID. |

### WorkflowServiceWaitJobResponse

The WorkflowServiceWaitJobResponse class.

### WorkflowService

The IWorkflowService interface.

KindMethod NameRequest TypeResponse TypeDescription

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetJobInfo [WorkflowServiceGetJobInfoRequest](#zen_api.workflows.v2.WorkflowServiceGetJobInfoRequest) [WorkflowServiceGetJobInfoResponse](#zen_api.workflows.v2.WorkflowServiceGetJobInfoResponse)

Get Job information.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

StartJob [WorkflowServiceStartJobRequest](#zen_api.workflows.v2.WorkflowServiceStartJobRequest) [WorkflowServiceStartJobResponse](#zen_api.workflows.v2.WorkflowServiceStartJobResponse)

Start Job execution.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

StopJob [WorkflowServiceStopJobRequest](#zen_api.workflows.v2.WorkflowServiceStopJobRequest) [WorkflowServiceStopJobResponse](#zen_api.workflows.v2.WorkflowServiceStopJobResponse)

Stop the Job execution.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

WaitJob [WorkflowServiceWaitJobRequest](#zen_api.workflows.v2.WorkflowServiceWaitJobRequest) [WorkflowServiceWaitJobResponse](#zen_api.workflows.v2.WorkflowServiceWaitJobResponse)

Wait for the Job execution will be finished.

## zen\_api/workflows/v3beta/job\_status.proto

[Top](#title)

### JobStatus

Enumerates possible job statuses.

| Name                     | Number | Description                                                      |
| ------------------------ | ------ | ---------------------------------------------------------------- |
| JOB\_STATUS\_UNSPECIFIED | 0      | Default enum value.                                              |
| JOB\_STATUS\_NOT\_LOADED | 1      | Job template is not loaded.                                      |
| JOB\_STATUS\_LOADED      | 2      | Job template is loaded.                                          |
| JOB\_STATUS\_RUNNING     | 3      | Job is running.                                                  |
| JOB\_STATUS\_FINALIZING  | 4      | Finalizing job results after the job was completed successfully. |
| JOB\_STATUS\_ARCHIVING   | 5      | Archiving job results after they were finalized.                 |
| JOB\_STATUS\_COMPLETED   | 6      | Job was completed successfully.                                  |
| JOB\_STATUS\_ABORTED     | 7      | Job was aborted.                                                 |
| JOB\_STATUS\_CANCELED    | 8      | Job was canceled.                                                |

## zen\_api/workflows/v3beta/job\_template\_info.proto

[Top](#title)

### JobTemplateInfo

Contains information about a job template.

| Field       | Type              | Label | Description                     |
| ----------- | ----------------- | ----- | ------------------------------- |
| name        | [string](#string) |       | The job template's name.        |
| description | [string](#string) |       | The job template's description. |
| category    | [string](#string) |       | The job template's category.    |
| subcategory | [string](#string) |       | The job template's subcategory. |

## zen\_api/workflows/v3beta/workflow\_service.proto

[Top](#title)

### WorkflowServiceGetAvailableJobTemplatesRequest

The WorkflowServiceGetAvailableJobTemplatesRequest class.

| Field       | Type              | Label | Description                                                                                                                                 |
| ----------- | ----------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| category    | [string](#string) |       | Optional filter for job templates. If category is provided then only job templates that are in the specified category will be listed.       |
| subcategory | [string](#string) |       | Optional filter for job templates. If subcategory is provided then only job templates that are in the specified subcategory will be listed. |

### WorkflowServiceGetAvailableJobTemplatesResponse

Represents a list of all available job templates.

| Field          | Type                                                         | Label    | Description                  |
| -------------- | ------------------------------------------------------------ | -------- | ---------------------------- |
| job\_templates | [JobTemplateInfo](#zen_api.workflows.v3beta.JobTemplateInfo) | repeated | The available job templates. |

### WorkflowServiceGetStatusRequest

The WorkflowServiceGetStatusRequest class.

### WorkflowServiceGetStatusResponse

Response containing the job status.

| Field       | Type                                             | Label | Description     |
| ----------- | ------------------------------------------------ | ----- | --------------- |
| job\_status | [JobStatus](#zen_api.workflows.v3beta.JobStatus) |       | The job status. |

### WorkflowServiceIsJobRunningRequest

The WorkflowServiceIsJobRunningRequest class.

### WorkflowServiceIsJobRunningResponse

Response object representing the return value of IsJobRunning() method of the

Workflow service.

| Field            | Type          | Label | Description                                                     |
| ---------------- | ------------- | ----- | --------------------------------------------------------------- |
| is\_job\_running | [bool](#bool) |       | A value indicating whether the loaded job is currently running. |

### WorkflowServiceIsJobTemplateLoadedRequest

The WorkflowServiceIsJobTemplateLoadedRequest class.

### WorkflowServiceIsJobTemplateLoadedResponse

Response object representing the return value of IsJobTemplateLoaded() method of the

Workflow service.

| Field                     | Type          | Label | Description                                          |
| ------------------------- | ------------- | ----- | ---------------------------------------------------- |
| is\_job\_template\_loaded | [bool](#bool) |       | A value indicating whether a job template is loaded. |

### WorkflowServiceLoadJobTemplateRequest

The WorkflowServiceLoadJobTemplateRequest class.

| Field               | Type              | Label | Description                                                                                                                                                                   |
| ------------------- | ----------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| job\_template\_name | [string](#string) |       | The name of the job template.                                                                                                                                                 |
| result\_path        | [string](#string) |       | Optional parameter for storing the result outside of ZEN archive. If provided the job result will be stored in the selected location and will not be uploaded to the archive. |

### WorkflowServiceLoadJobTemplateResponse

The WorkflowServiceLoadJobTemplateResponse class.

### WorkflowServiceRegisterOnStatusChangedRequest

The WorkflowServiceRegisterOnStatusChangedRequest class.

### WorkflowServiceRegisterOnStatusChangedResponse

Response containing the job status.

| Field       | Type                                             | Label | Description     |
| ----------- | ------------------------------------------------ | ----- | --------------- |
| job\_status | [JobStatus](#zen_api.workflows.v3beta.JobStatus) |       | The job status. |

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

KindMethod NameRequest TypeResponse TypeDescription

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetAvailableJobTemplates [WorkflowServiceGetAvailableJobTemplatesRequest](#zen_api.workflows.v3beta.WorkflowServiceGetAvailableJobTemplatesRequest) [WorkflowServiceGetAvailableJobTemplatesResponse](#zen_api.workflows.v3beta.WorkflowServiceGetAvailableJobTemplatesResponse)

Retrieves a list of all available job templates.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

GetStatus [WorkflowServiceGetStatusRequest](#zen_api.workflows.v3beta.WorkflowServiceGetStatusRequest) [WorkflowServiceGetStatusResponse](#zen_api.workflows.v3beta.WorkflowServiceGetStatusResponse)

Gets the job status.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

IsJobRunning [WorkflowServiceIsJobRunningRequest](#zen_api.workflows.v3beta.WorkflowServiceIsJobRunningRequest) [WorkflowServiceIsJobRunningResponse](#zen_api.workflows.v3beta.WorkflowServiceIsJobRunningResponse)

Checks if the loaded job is currently running.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

IsJobTemplateLoaded [WorkflowServiceIsJobTemplateLoadedRequest](#zen_api.workflows.v3beta.WorkflowServiceIsJobTemplateLoadedRequest) [WorkflowServiceIsJobTemplateLoadedResponse](#zen_api.workflows.v3beta.WorkflowServiceIsJobTemplateLoadedResponse)

Checks if a job template is loaded.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

LoadJobTemplate [WorkflowServiceLoadJobTemplateRequest](#zen_api.workflows.v3beta.WorkflowServiceLoadJobTemplateRequest) [WorkflowServiceLoadJobTemplateResponse](#zen_api.workflows.v3beta.WorkflowServiceLoadJobTemplateResponse)

Loads a job template and prepares it for execution.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

RegisterOnStatusChanged [WorkflowServiceRegisterOnStatusChangedRequest](#zen_api.workflows.v3beta.WorkflowServiceRegisterOnStatusChangedRequest) [WorkflowServiceRegisterOnStatusChangedResponse](#zen_api.workflows.v3beta.WorkflowServiceRegisterOnStatusChangedResponse) stream

Register on job status changed events.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

RunJob [WorkflowServiceRunJobRequest](#zen_api.workflows.v3beta.WorkflowServiceRunJobRequest) [WorkflowServiceRunJobResponse](#zen_api.workflows.v3beta.WorkflowServiceRunJobResponse)

Runs the loaded job template to completion.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

StartJob [WorkflowServiceStartJobRequest](#zen_api.workflows.v3beta.WorkflowServiceStartJobRequest) [WorkflowServiceStartJobResponse](#zen_api.workflows.v3beta.WorkflowServiceStartJobResponse)

Starts the loaded job template but it doesn't wait for it to complete.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

StopJob [WorkflowServiceStopJobRequest](#zen_api.workflows.v3beta.WorkflowServiceStopJobRequest) [WorkflowServiceStopJobResponse](#zen_api.workflows.v3beta.WorkflowServiceStopJobResponse)

Stops the currently running job and waits for it to complete.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

UnloadJobTemplate [WorkflowServiceUnloadJobTemplateRequest](#zen_api.workflows.v3beta.WorkflowServiceUnloadJobTemplateRequest) [WorkflowServiceUnloadJobTemplateResponse](#zen_api.workflows.v3beta.WorkflowServiceUnloadJobTemplateResponse)

Unloads the loaded job template.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

WaitJob [WorkflowServiceWaitJobRequest](#zen_api.workflows.v3beta.WorkflowServiceWaitJobRequest) [WorkflowServiceWaitJobResponse](#zen_api.workflows.v3beta.WorkflowServiceWaitJobResponse)

Waits for currently running job to complete.

## zen\_api/lm/acquisition/v1beta/autofocus\_contrast\_measure.proto

[Top](#title)

### AutofocusContrastMeasure

The contrast measures of the software autofocus contrast mode.

| Name                                      | Number | Description                                                           |
| ----------------------------------------- | ------ | --------------------------------------------------------------------- |
| AUTOFOCUS\_CONTRAST\_MEASURE\_UNSPECIFIED | 0      | Default enum value.                                                   |
| AUTOFOCUS\_CONTRAST\_MEASURE\_DEFAULT     | 1      | The default contrast measure.                                         |
| AUTOFOCUS\_CONTRAST\_MEASURE\_LOW\_SIGNAL | 2      | The contrast measure to use in low-signal and calibration situations. |

## zen\_api/lm/acquisition/v1beta/autofocus\_mode.proto

[Top](#title)

### AutofocusMode

The autofocus modes.

| Name                         | Number | Description                                                                                       |
| ---------------------------- | ------ | ------------------------------------------------------------------------------------------------- |
| AUTOFOCUS\_MODE\_UNSPECIFIED | 0      | Default enum value.                                                                               |
| AUTOFOCUS\_MODE\_CONTRAST    | 1      | Sharpness is measured on the basis of contrast values.                                            |
| AUTOFOCUS\_MODE\_INTENSITY   | 2      | Sharpness is measured on the basis of intensity values.                                           |
| AUTOFOCUS\_MODE\_AUTO        | 3      | Automatic determination of measure method (Contrast or Intensity) in dependency of used hardware. |
| AUTOFOCUS\_MODE\_REFLEX      | 4      | Sharpness is measured with the reflection mode autofocus.                                         |

## zen\_api/lm/acquisition/v1beta/autofocus\_sampling.proto

[Top](#title)

### AutofocusSampling

Scales the depth of focus by predefined values given here.

| Name                             | Number | Description                              |
| -------------------------------- | ------ | ---------------------------------------- |
| AUTOFOCUS\_SAMPLING\_UNSPECIFIED | 0      | Default enum value.                      |
| AUTOFOCUS\_SAMPLING\_FINE        | 1      | Do oversampling.                         |
| AUTOFOCUS\_SAMPLING\_DEFAULT     | 2      | Do sampling according to depth of focus. |
| AUTOFOCUS\_SAMPLING\_MEDIUM      | 3      | Do under sampling.                       |
| AUTOFOCUS\_SAMPLING\_COARSE      | 4      | Coarser than medium.                     |

## zen\_api/lm/acquisition/v1beta/channel\_info.proto

[Top](#title)

### ChannelInfo

Information about a channel.

| Field         | Type              | Label | Description                                          |
| ------------- | ----------------- | ----- | ---------------------------------------------------- |
| name          | [string](#string) |       | The channel name.                                    |
| is\_activated | [bool](#bool)     |       | A value indicating whether the channel is activated. |

## zen\_api/lm/acquisition/v1beta/experiment\_sw\_autofocus\_service.proto

[Top](#title)

### ExperimentSwAutofocusServiceExportRequest

The ExperimentSwAutofocusServiceExportRequest class.

| Field          | Type              | Label | Description        |
| -------------- | ----------------- | ----- | ------------------ |
| experiment\_id | [string](#string) |       | The experiment id. |

### ExperimentSwAutofocusServiceExportResponse

Response object representing the values of xml string.

| Field       | Type              | Label | Description                |
| ----------- | ----------------- | ----- | -------------------------- |
| xml\_string | [string](#string) |       | A value of the xml string. |

### ExperimentSwAutofocusServiceFindAutoFocusRequest

The ExperimentSwAutofocusServiceFindAutoFocusRequest class.

| Field          | Type                                                                                                 | Label | Description             |
| -------------- | ---------------------------------------------------------------------------------------------------- | ----- | ----------------------- |
| experiment\_id | [string](#string)                                                                                    |       | The experiment id.      |
| timeout        | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The timeout in seconds. |

### ExperimentSwAutofocusServiceFindAutoFocusResponse

Response object representing the focus position.

| Field           | Type              | Label | Description                   |
| --------------- | ----------------- | ----- | ----------------------------- |
| focus\_position | [double](#double) |       | The focus position (unit: m). |

### ExperimentSwAutofocusServiceGetAutofocusParametersRequest

The ExperimentSwAutofocusServiceGetAutofocusParametersRequest class.

| Field          | Type              | Label | Description        |
| -------------- | ----------------- | ----- | ------------------ |
| experiment\_id | [string](#string) |       | The experiment id. |

### ExperimentSwAutofocusServiceGetAutofocusParametersResponse

Response object representing the values of software autofocus parameters for the experiment.

| Field                          | Type                                                                                | Label | Description                                                                                              |
| ------------------------------ | ----------------------------------------------------------------------------------- | ----- | -------------------------------------------------------------------------------------------------------- |
| experiment\_id                 | [string](#string)                                                                   |       | A value of the experiment id.                                                                            |
| auto\_focus\_mode              | [AutofocusMode](#zen_api.lm.acquisition.v1beta.AutofocusMode)                       |       | A value of autofocus mode.                                                                               |
| contrast\_measure              | [AutofocusContrastMeasure](#zen_api.lm.acquisition.v1beta.AutofocusContrastMeasure) |       | A value of sharpness measure for contrast mode.                                                          |
| search\_strategy               | [string](#string)                                                                   |       | A value of search strategy. Either "Smart", "Full", "FullNoChecks" or the name of an extension strategy. |
| autofocus\_sampling            | [AutofocusSampling](#zen_api.lm.acquisition.v1beta.AutofocusSampling)               |       | A value of the predefined step size.                                                                     |
| offset                         | [double](#double)                                                                   |       | A value of the reflection mode offset (unit: m).                                                         |
| use\_acquisition\_roi          | [bool](#bool)                                                                       |       | A value indicating whether the acquisition ROI is used for the software autofocus.                       |
| reference\_channel\_name       | [string](#string)                                                                   |       | A name of the focus reference channel.                                                                   |
| relative\_range\_is\_automatic | [bool](#bool)                                                                       |       | A value indicating whether the relative search range size is determined automatically.                   |
| relative\_search\_range        | [double](#double)                                                                   |       | A value of the relative search range of the Z drive (unit: m).                                           |
| lower\_limit                   | [double](#double)                                                                   |       | A value of the lower search range limit of the Z drive (unit: m).                                        |
| upper\_limit                   | [double](#double)                                                                   |       | A value of the upper search range limit of the Z drive (unit: m).                                        |

### ExperimentSwAutofocusServiceImportRequest

The ExperimentSwAutofocusServiceImportRequest class.

| Field          | Type              | Label | Description                |
| -------------- | ----------------- | ----- | -------------------------- |
| experiment\_id | [string](#string) |       | The experiment id.         |
| xml\_string    | [string](#string) |       | Xml string to be imported. |

### ExperimentSwAutofocusServiceImportResponse

The ExperimentSwAutofocusServiceImportResponse class.

### ExperimentSwAutofocusServiceSetAutofocusParametersRequest

The ExperimentSwAutofocusServiceSetAutofocusParametersRequest class.

| Field                          | Type                                                                                                 | Label | Description                                                                                                                                                 |
| ------------------------------ | ---------------------------------------------------------------------------------------------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| experiment\_id                 | [string](#string)                                                                                    |       | The experiment id.                                                                                                                                          |
| autofocus\_mode                | [AutofocusMode](#zen_api.lm.acquisition.v1beta.AutofocusMode)                                        |       | The autofocus mode.                                                                                                                                         |
| contrast\_measure              | [AutofocusContrastMeasure](#zen_api.lm.acquisition.v1beta.AutofocusContrastMeasure)                  |       | The sharpness measure for contrast mode.                                                                                                                    |
| search\_strategy               | [string](#string)                                                                                    |       | The strategy, either "Smart", "Full", "FullNoChecks" or the name of an extension strategy, or null to leave unmodified. This parameter is case-insensitive. |
| autofocus\_sampling            | [AutofocusSampling](#zen_api.lm.acquisition.v1beta.AutofocusSampling)                                |       | The predefined step size, or null to leave unmodified.                                                                                                      |
| offset                         | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The reflection mode offset (unit: m), or null to leave unmodified.                                                                                          |
| use\_acquisition\_roi          | [google.protobuf.BoolValue](https://protobuf.dev/reference/protobuf/google.protobuf/#bool-value)     |       | True if the acquisition ROI is used for the software autofocus; otherwise, false, or null to leave unmodified.                                              |
| reference\_channel\_name       | [string](#string)                                                                                    |       | The case-insensitive name of the focus reference channel, or null to leave unmodified.                                                                      |
| relative\_range\_is\_automatic | [google.protobuf.BoolValue](https://protobuf.dev/reference/protobuf/google.protobuf/#bool-value)     |       | True if the relative search range size is determined automatically; otherwise, false, or null to leave unmodified.                                          |
| relative\_search\_range        | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The relative search range in units of the Z drive (unit: m), or null to leave unmodified.                                                                   |
| lower\_limit                   | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The lower search range limit in units of the Z drive (unit: m), or null to leave unmodified.                                                                |
| upper\_limit                   | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The upper limit in units of the Z drive (unit: m), or null to leave unmodified.                                                                             |

### ExperimentSwAutofocusServiceSetAutofocusParametersResponse

The ExperimentSwAutofocusServiceSetAutofocusParametersResponse class.

### ExperimentSwAutofocusService

The IExperimentSwAutofocusService interface.

KindMethod NameRequest TypeResponse TypeDescription

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Export [ExperimentSwAutofocusServiceExportRequest](#zen_api.lm.acquisition.v1beta.ExperimentSwAutofocusServiceExportRequest) [ExperimentSwAutofocusServiceExportResponse](#zen_api.lm.acquisition.v1beta.ExperimentSwAutofocusServiceExportResponse)

Exports the software autofocus parameters to an xml string.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

FindAutoFocus [ExperimentSwAutofocusServiceFindAutoFocusRequest](#zen_api.lm.acquisition.v1beta.ExperimentSwAutofocusServiceFindAutoFocusRequest) [ExperimentSwAutofocusServiceFindAutoFocusResponse](#zen_api.lm.acquisition.v1beta.ExperimentSwAutofocusServiceFindAutoFocusResponse)

Gets the the focus position.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetAutofocusParameters [ExperimentSwAutofocusServiceGetAutofocusParametersRequest](#zen_api.lm.acquisition.v1beta.ExperimentSwAutofocusServiceGetAutofocusParametersRequest) [ExperimentSwAutofocusServiceGetAutofocusParametersResponse](#zen_api.lm.acquisition.v1beta.ExperimentSwAutofocusServiceGetAutofocusParametersResponse)

Gets the software autofocus parameters for the specified experiment.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Import [ExperimentSwAutofocusServiceImportRequest](#zen_api.lm.acquisition.v1beta.ExperimentSwAutofocusServiceImportRequest) [ExperimentSwAutofocusServiceImportResponse](#zen_api.lm.acquisition.v1beta.ExperimentSwAutofocusServiceImportResponse)

Imports the software autofocus parameters from an xml string.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetAutofocusParameters [ExperimentSwAutofocusServiceSetAutofocusParametersRequest](#zen_api.lm.acquisition.v1beta.ExperimentSwAutofocusServiceSetAutofocusParametersRequest) [ExperimentSwAutofocusServiceSetAutofocusParametersResponse](#zen_api.lm.acquisition.v1beta.ExperimentSwAutofocusServiceSetAutofocusParametersResponse)

Sets the software autofocus parameters for the specified experiment.

## zen\_api/lm/acquisition/v1beta/position3d.proto

[Top](#title)

### Position3d

A position in three dimensions (XYZ).

| Field | Type              | Label | Description               |
| ----- | ----------------- | ----- | ------------------------- |
| x     | [double](#double) |       | The X position (unit: m). |
| y     | [double](#double) |       | The Y position (unit: m). |
| z     | [double](#double) |       | The Z position (unit: m). |

## zen\_api/lm/acquisition/v1beta/tiles\_service.proto

[Top](#title)

### TilesServiceAddEllipseTileRegionRequest

The TilesServiceAddEllipseTileRegionRequest class.

| Field          | Type                                                                                                 | Label | Description                                                     |
| -------------- | ---------------------------------------------------------------------------------------------------- | ----- | --------------------------------------------------------------- |
| experiment\_id | [string](#string)                                                                                    |       | The experiment Id.                                              |
| center\_x      | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The center x position of the tile region to be added (unit: m). |
| center\_y      | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The center y position of the tile region to be added (unit: m). |
| width          | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The width of the tile region to be added (unit: m).             |
| height         | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The height of the tile region to be added (unit: m).            |
| z              | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The z position of the tile region to be added (unit: m).        |

### TilesServiceAddEllipseTileRegionResponse

The TilesServiceAddEllipseTileRegionResponse class.

### TilesServiceAddPolygonTileRegionRequest

The TilesServiceAddPolygonTileRegionRequest class.

| Field           | Type                                                                                                 | Label    | Description                                                                                         |
| --------------- | ---------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------- |
| experiment\_id  | [string](#string)                                                                                    |          | The experiment Id.                                                                                  |
| polygon\_points | [zen\_api.common.v1.DoublePoint](#zen_api.common.v1.DoublePoint)                                     | repeated | The list of points which define the polygon. This list has to contain at least one point (unit: m). |
| z               | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |          | The z position of the tile region to be added (unit: m).                                            |

### TilesServiceAddPolygonTileRegionResponse

The TilesServiceAddPolygonTileRegionResponse class.

### TilesServiceAddPositionsRequest

The TilesServiceAddPositionsRequest class.

| Field          | Type                                                    | Label    | Description                |
| -------------- | ------------------------------------------------------- | -------- | -------------------------- |
| experiment\_id | [string](#string)                                       |          | The experiment Id.         |
| positions      | [Position3d](#zen_api.lm.acquisition.v1beta.Position3d) | repeated | The positions to be added. |

### TilesServiceAddPositionsResponse

The TilesServiceAddPositionsResponse class.

### TilesServiceAddRectangleTileRegionRequest

The TilesServiceAddRectangleTileRegionRequest class.

| Field          | Type                                                                                                 | Label | Description                                                     |
| -------------- | ---------------------------------------------------------------------------------------------------- | ----- | --------------------------------------------------------------- |
| experiment\_id | [string](#string)                                                                                    |       | Experiment id.                                                  |
| center\_x      | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The center x position of the tile region to be added (unit: m). |
| center\_y      | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The center y position of the tile region to be added (unit: m). |
| width          | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The width of the tile region to be added (unit: m).             |
| height         | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The height of the tile region to be added (unit: m).            |
| z              | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The z position of the tile region to be added (unit: m).        |

### TilesServiceAddRectangleTileRegionResponse

The TilesServiceAddRectangleTileRegionResponse class.

### TilesServiceClearRequest

The TilesServiceClearRequest class.

| Field          | Type              | Label | Description    |
| -------------- | ----------------- | ----- | -------------- |
| experiment\_id | [string](#string) |       | Experiment id. |

### TilesServiceClearResponse

The TilesServiceClearResponse class.

### TilesServiceIsTilesExperimentRequest

The TilesServiceIsTilesExperimentRequest class.

| Field          | Type              | Label | Description    |
| -------------- | ----------------- | ----- | -------------- |
| experiment\_id | [string](#string) |       | Experiment id. |

### TilesServiceIsTilesExperimentResponse

Response object representing the value of IsTiles for the experiment.

| Field                 | Type          | Label | Description                                                      |
| --------------------- | ------------- | ----- | ---------------------------------------------------------------- |
| is\_tiles\_experiment | [bool](#bool) |       | A value indicating whether the experiment is a tiles experiment. |

### TilesService

The ITilesService interface.

KindMethod NameRequest TypeResponse TypeDescription

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

AddEllipseTileRegion [TilesServiceAddEllipseTileRegionRequest](#zen_api.lm.acquisition.v1beta.TilesServiceAddEllipseTileRegionRequest) [TilesServiceAddEllipseTileRegionResponse](#zen_api.lm.acquisition.v1beta.TilesServiceAddEllipseTileRegionResponse)

Adds an ellipse tile region with the specified position and size values to the acquisition block with the specified index in the specified experiment.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

AddPolygonTileRegion [TilesServiceAddPolygonTileRegionRequest](#zen_api.lm.acquisition.v1beta.TilesServiceAddPolygonTileRegionRequest) [TilesServiceAddPolygonTileRegionResponse](#zen_api.lm.acquisition.v1beta.TilesServiceAddPolygonTileRegionResponse)

Adds a polygon tile region with the specified points list to the acquisition block with the specified index in the specified experiment.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

AddPositions [TilesServiceAddPositionsRequest](#zen_api.lm.acquisition.v1beta.TilesServiceAddPositionsRequest) [TilesServiceAddPositionsResponse](#zen_api.lm.acquisition.v1beta.TilesServiceAddPositionsResponse)

Adds positions with the specified coordinates to the specified experiment.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

AddRectangleTileRegion [TilesServiceAddRectangleTileRegionRequest](#zen_api.lm.acquisition.v1beta.TilesServiceAddRectangleTileRegionRequest) [TilesServiceAddRectangleTileRegionResponse](#zen_api.lm.acquisition.v1beta.TilesServiceAddRectangleTileRegionResponse)

Adds a rectangle tile region with the specified position and size values to the specified experiment.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Clear [TilesServiceClearRequest](#zen_api.lm.acquisition.v1beta.TilesServiceClearRequest) [TilesServiceClearResponse](#zen_api.lm.acquisition.v1beta.TilesServiceClearResponse)

Clears all tile regions and positions in the current acquisition block.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

IsTilesExperiment [TilesServiceIsTilesExperimentRequest](#zen_api.lm.acquisition.v1beta.TilesServiceIsTilesExperimentRequest) [TilesServiceIsTilesExperimentResponse](#zen_api.lm.acquisition.v1beta.TilesServiceIsTilesExperimentResponse)

Determines whether the current experiment block in the specified experiment is a Tiles experiment. This means that the corresponding Tiles dimension is activated.

## zen\_api/lm/acquisition/v1beta/track\_info.proto

[Top](#title)

### TrackInfo

Information about a track.

| Field         | Type                                                      | Label    | Description                                        |
| ------------- | --------------------------------------------------------- | -------- | -------------------------------------------------- |
| is\_activated | [bool](#bool)                                             |          | A value indicating whether the track is activated. |
| channels      | [ChannelInfo](#zen_api.lm.acquisition.v1beta.ChannelInfo) | repeated | The info for all channels in the track.            |

## zen\_api/lm/acquisition/v1beta/track\_service.proto

[Top](#title)

### TrackServiceActivateChannelRequest

The TrackServiceActivateChannelRequest class.

| Field          | Type              | Label | Description                                         |
| -------------- | ----------------- | ----- | --------------------------------------------------- |
| experiment\_id | [string](#string) |       | Experiment id.                                      |
| track\_index   | [int32](#int32)   |       | An index of a track.                                |
| channel\_index | [int32](#int32)   |       | An index of a channel in the track to be activated. |

### TrackServiceActivateChannelResponse

The TrackServiceActivateChannelResponse class.

### TrackServiceActivateTrackRequest

The TrackServiceActivateTrackRequest class.

| Field          | Type              | Label | Description                          |
| -------------- | ----------------- | ----- | ------------------------------------ |
| experiment\_id | [string](#string) |       | Experiment id.                       |
| track\_index   | [int32](#int32)   |       | An index of a track to be activated. |

### TrackServiceActivateTrackResponse

The TrackServiceActivateTrackResponse class.

### TrackServiceDeactivateChannelRequest

The TrackServiceDeactivateChannelRequest class.

| Field          | Type              | Label | Description                                           |
| -------------- | ----------------- | ----- | ----------------------------------------------------- |
| experiment\_id | [string](#string) |       | Experiment id.                                        |
| track\_index   | [int32](#int32)   |       | An index of a track.                                  |
| channel\_index | [int32](#int32)   |       | An index of a channel in the track to be deactivated. |

### TrackServiceDeactivateChannelResponse

The TrackServiceDeactivateChannelResponse class.

### TrackServiceDeactivateTrackRequest

The TrackServiceDeactivateTrackRequest class.

| Field          | Type              | Label | Description                            |
| -------------- | ----------------- | ----- | -------------------------------------- |
| experiment\_id | [string](#string) |       | Experiment id.                         |
| track\_index   | [int32](#int32)   |       | An index of a track to be deactivated. |

### TrackServiceDeactivateTrackResponse

The TrackServiceDeactivateTrackResponse class.

### TrackServiceGetTrackInfoRequest

The TrackServiceGetTrackInfoRequest class.

| Field          | Type              | Label | Description    |
| -------------- | ----------------- | ----- | -------------- |
| experiment\_id | [string](#string) |       | Experiment id. |

### TrackServiceGetTrackInfoResponse

Response object representing the value of track information.

| Field       | Type                                                  | Label    | Description            |
| ----------- | ----------------------------------------------------- | -------- | ---------------------- |
| track\_info | [TrackInfo](#zen_api.lm.acquisition.v1beta.TrackInfo) | repeated | The track information. |

### TrackService

The ITrackService interface.

KindMethod NameRequest TypeResponse TypeDescription

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

ActivateChannel [TrackServiceActivateChannelRequest](#zen_api.lm.acquisition.v1beta.TrackServiceActivateChannelRequest) [TrackServiceActivateChannelResponse](#zen_api.lm.acquisition.v1beta.TrackServiceActivateChannelResponse)

Activates a channel with a specific index in a specific track.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

ActivateTrack [TrackServiceActivateTrackRequest](#zen_api.lm.acquisition.v1beta.TrackServiceActivateTrackRequest) [TrackServiceActivateTrackResponse](#zen_api.lm.acquisition.v1beta.TrackServiceActivateTrackResponse)

Activates a track with a specific index.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

DeactivateChannel [TrackServiceDeactivateChannelRequest](#zen_api.lm.acquisition.v1beta.TrackServiceDeactivateChannelRequest) [TrackServiceDeactivateChannelResponse](#zen_api.lm.acquisition.v1beta.TrackServiceDeactivateChannelResponse)

Deactivates a channel with a specific index in a specific track.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

DeactivateTrack [TrackServiceDeactivateTrackRequest](#zen_api.lm.acquisition.v1beta.TrackServiceDeactivateTrackRequest) [TrackServiceDeactivateTrackResponse](#zen_api.lm.acquisition.v1beta.TrackServiceDeactivateTrackResponse)

Deactivates a track with a specific index.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetTrackInfo [TrackServiceGetTrackInfoRequest](#zen_api.lm.acquisition.v1beta.TrackServiceGetTrackInfoRequest) [TrackServiceGetTrackInfoResponse](#zen_api.lm.acquisition.v1beta.TrackServiceGetTrackInfoResponse)

Gets the track information.

## zen\_api/lm/acquisition/v1beta/zstack\_service.proto

[Top](#title)

### ZStackServiceGetZStackInfoRequest

The ZStackServiceGetZStackInfoRequest class.

| Field          | Type              | Label | Description        |
| -------------- | ----------------- | ----- | ------------------ |
| experiment\_id | [string](#string) |       | The experiment Id. |

### ZStackServiceGetZStackInfoResponse

Response object representing the value of GetZStackInfo for the experiment.

| Field            | Type              | Label | Description                                                    |
| ---------------- | ----------------- | ----- | -------------------------------------------------------------- |
| interval         | [double](#double) |       | The value of the interval between 2 slices (unit: m).          |
| first\_slice     | [double](#double) |       | The position of the first slice in Z-stack (unit: m).          |
| last\_slice      | [double](#double) |       | The position of the last slice in Z-stack (unit: m).           |
| range            | [double](#double) |       | The distance between the first and last slice (unit: m).       |
| num\_slices      | [int32](#int32)   |       | The number of slices.                                          |
| is\_center\_mode | [bool](#bool)     |       | A value indicating whether the Z-stack is in center mode.      |
| offset           | [double](#double) |       | The value of the offset which is applied to the whole Z-stack. |

### ZStackServiceIsZStackExperimentRequest

The ZStackServiceIsZStackExperimentRequest class.

| Field          | Type              | Label | Description        |
| -------------- | ----------------- | ----- | ------------------ |
| experiment\_id | [string](#string) |       | The experiment Id. |

### ZStackServiceIsZStackExperimentResponse

Response object representing the value of IsZStackExperiment for the experiment.

| Field                  | Type          | Label | Description                                                        |
| ---------------------- | ------------- | ----- | ------------------------------------------------------------------ |
| is\_zstack\_experiment | [bool](#bool) |       | A value indicating whether the experiment is a Z-Stack experiment. |

### ZStackServiceModifyZStackCenterRangeRequest

The ZStackServiceModifyZStackCenterRangeRequest class.

| Field          | Type                                                                                                 | Label | Description                                                     |
| -------------- | ---------------------------------------------------------------------------------------------------- | ----- | --------------------------------------------------------------- |
| experiment\_id | [string](#string)                                                                                    |       | The experiment Id.                                              |
| center         | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The center position between the first and last slice (unit: m). |
| interval       | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The interval between 2 slices (unit: m).                        |
| range          | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Distance between the first and last slice (unit: m).            |

### ZStackServiceModifyZStackCenterRangeResponse

The ZStackServiceModifyZStackCenterRangeResponse class.

### ZStackServiceModifyZStackFirstLastRequest

The ZStackServiceModifyZStackFirstLastRequest class.

| Field          | Type                                                                                                 | Label | Description                                       |
| -------------- | ---------------------------------------------------------------------------------------------------- | ----- | ------------------------------------------------- |
| experiment\_id | [string](#string)                                                                                    |       | The experiment Id.                                |
| first          | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Position of the first slice in Z-stack (unit: m). |
| last           | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Position of the last slice in Z-stack (unit: m).  |
| interval       | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | The interval between 2 slices (unit: m).          |

### ZStackServiceModifyZStackFirstLastResponse

The ZStackServiceModifyZStackFirstLastResponse class.

### ZStackService

The IZStackService interface.

KindMethod NameRequest TypeResponse TypeDescription

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetZStackInfo [ZStackServiceGetZStackInfoRequest](#zen_api.lm.acquisition.v1beta.ZStackServiceGetZStackInfoRequest) [ZStackServiceGetZStackInfoResponse](#zen_api.lm.acquisition.v1beta.ZStackServiceGetZStackInfoResponse)

Gets the information about a Z-stack.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

IsZStackExperiment [ZStackServiceIsZStackExperimentRequest](#zen_api.lm.acquisition.v1beta.ZStackServiceIsZStackExperimentRequest) [ZStackServiceIsZStackExperimentResponse](#zen_api.lm.acquisition.v1beta.ZStackServiceIsZStackExperimentResponse)

Determines whether the current experiment block in the specified experiment is a Z-stack experiment. This means that the corresponding Z-stack setup dimension is activated.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

ModifyZStackCenterRange [ZStackServiceModifyZStackCenterRangeRequest](#zen_api.lm.acquisition.v1beta.ZStackServiceModifyZStackCenterRangeRequest) [ZStackServiceModifyZStackCenterRangeResponse](#zen_api.lm.acquisition.v1beta.ZStackServiceModifyZStackCenterRangeResponse)

Modifies the dimensions of the Z-stack inside the experiment.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

ModifyZStackFirstLast [ZStackServiceModifyZStackFirstLastRequest](#zen_api.lm.acquisition.v1beta.ZStackServiceModifyZStackFirstLastRequest) [ZStackServiceModifyZStackFirstLastResponse](#zen_api.lm.acquisition.v1beta.ZStackServiceModifyZStackFirstLastResponse)

Modifies the dimensions of the Z-stack inside the experiment.

## zen\_api/lm/hardware/v1/focus\_service.proto

[Top](#title)

### FocusServiceGetAccelerationRequest

The FocusServiceGetAccelerationRequest class.

### FocusServiceGetAccelerationResponse

Acceleration of the focus in %.

| Field | Type              | Label | Description            |
| ----- | ----------------- | ----- | ---------------------- |
| value | [double](#double) |       | The acceleration in %. |

### FocusServiceGetPositionRequest

The FocusServiceGetPositionRequest class.

### FocusServiceGetPositionResponse

Position of the focus in µm.

| Field | Type              | Label | Description         |
| ----- | ----------------- | ----- | ------------------- |
| value | [double](#double) |       | The position in µm. |

### FocusServiceGetSpeedRequest

The FocusServiceGetSpeedRequest class.

### FocusServiceGetSpeedResponse

Speed of the focus in %.

| Field | Type              | Label | Description     |
| ----- | ----------------- | ----- | --------------- |
| value | [double](#double) |       | The speed in %. |

### FocusServiceMoveToRequest

The FocusServiceMoveToRequest class.

| Field | Type              | Label | Description         |
| ----- | ----------------- | ----- | ------------------- |
| value | [double](#double) |       | New position in µm. |

### FocusServiceMoveToResponse

Describes the result of a Focus.MoveTo request.

| Field             | Type          | Label | Description                                          |
| ----------------- | ------------- | ----- | ---------------------------------------------------- |
| position\_changed | [bool](#bool) |       | A value indicating whether the position was changed. |

### FocusServiceSetAccelerationRequest

The FocusServiceSetAccelerationRequest class.

| Field        | Type              | Label | Description                                               |
| ------------ | ----------------- | ----- | --------------------------------------------------------- |
| acceleration | [double](#double) |       | Acceleration in percent, i.e. values from range \[0;100]. |

### FocusServiceSetAccelerationResponse

The FocusServiceSetAccelerationResponse class.

### FocusServiceSetSpeedRequest

The FocusServiceSetSpeedRequest class.

| Field | Type              | Label | Description                                        |
| ----- | ----------------- | ----- | -------------------------------------------------- |
| speed | [double](#double) |       | Speed in percent, i.e. values from range \[0;100]. |

### FocusServiceSetSpeedResponse

The FocusServiceSetSpeedResponse class.

### FocusServiceStopRequest

The FocusServiceStopRequest class.

### FocusServiceStopResponse

The FocusServiceStopResponse class.

### FocusService

The IFocusService interface.

KindMethod NameRequest TypeResponse TypeDescription

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetAcceleration [FocusServiceGetAccelerationRequest](#zen_api.lm.hardware.v1.FocusServiceGetAccelerationRequest) [FocusServiceGetAccelerationResponse](#zen_api.lm.hardware.v1.FocusServiceGetAccelerationResponse)

Gets the focus acceleration.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetPosition [FocusServiceGetPositionRequest](#zen_api.lm.hardware.v1.FocusServiceGetPositionRequest) [FocusServiceGetPositionResponse](#zen_api.lm.hardware.v1.FocusServiceGetPositionResponse)

Gets the focus position.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetSpeed [FocusServiceGetSpeedRequest](#zen_api.lm.hardware.v1.FocusServiceGetSpeedRequest) [FocusServiceGetSpeedResponse](#zen_api.lm.hardware.v1.FocusServiceGetSpeedResponse)

Gets the focus speed.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

MoveTo [FocusServiceMoveToRequest](#zen_api.lm.hardware.v1.FocusServiceMoveToRequest) [FocusServiceMoveToResponse](#zen_api.lm.hardware.v1.FocusServiceMoveToResponse)

Moves the focus to the given position in µm.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetAcceleration [FocusServiceSetAccelerationRequest](#zen_api.lm.hardware.v1.FocusServiceSetAccelerationRequest) [FocusServiceSetAccelerationResponse](#zen_api.lm.hardware.v1.FocusServiceSetAccelerationResponse)

Sets the acceleration of the focus in percent.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetSpeed [FocusServiceSetSpeedRequest](#zen_api.lm.hardware.v1.FocusServiceSetSpeedRequest) [FocusServiceSetSpeedResponse](#zen_api.lm.hardware.v1.FocusServiceSetSpeedResponse)

Sets the speed of the focus in percent.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Stop [FocusServiceStopRequest](#zen_api.lm.hardware.v1.FocusServiceStopRequest) [FocusServiceStopResponse](#zen_api.lm.hardware.v1.FocusServiceStopResponse)

Stops the focus if it is moving.

## zen\_api/lm/hardware/v1/stage\_service.proto

[Top](#title)

### StageServiceGetAccelerationRequest

The StageServiceGetAccelerationRequest class.

### StageServiceGetAccelerationResponse

Acceleration of the stage.

| Field | Type              | Label | Description                               |
| ----- | ----------------- | ----- | ----------------------------------------- |
| x     | [double](#double) |       | The X component of the position in in μm. |
| y     | [double](#double) |       | The Y component of the position in in μm. |

### StageServiceGetPositionRequest

The StageServiceGetPositionRequest class.

### StageServiceGetPositionResponse

Position of the stage in µm.

| Field | Type              | Label | Description                            |
| ----- | ----------------- | ----- | -------------------------------------- |
| x     | [double](#double) |       | The X component of the position in μm. |
| y     | [double](#double) |       | The Y component of the position in μm. |

### StageServiceGetSpeedRequest

The StageServiceGetSpeedRequest class.

### StageServiceGetSpeedResponse

Speed of the stage.

| Field | Type              | Label | Description                        |
| ----- | ----------------- | ----- | ---------------------------------- |
| x     | [double](#double) |       | The X component of the speed in %. |
| y     | [double](#double) |       | The Y component of the speed in %. |

### StageServiceMoveToRequest

The StageServiceMoveToRequest class.

| Field | Type                                                                                                 | Label | Description                                                             |
| ----- | ---------------------------------------------------------------------------------------------------- | ----- | ----------------------------------------------------------------------- |
| x     | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Target position x in μm. Leave out if x position should not be changed. |
| y     | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Target position y in μm. Leave out if y position should not be changed. |

### StageServiceMoveToResponse

Describes the result of a Stage.MoveTo request.

| Field             | Type          | Label | Description                                          |
| ----------------- | ------------- | ----- | ---------------------------------------------------- |
| position\_changed | [bool](#bool) |       | A value indicating whether the position was changed. |

### StageServiceSetAccelerationRequest

The StageServiceSetAccelerationRequest class.

| Field           | Type                                                                                                 | Label | Description                                                              |
| --------------- | ---------------------------------------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------ |
| acceleration\_x | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Acceleration in x direction in percent, i.e. values from range \[0;100]. |
| acceleration\_y | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Acceleration in y direction in percent, i.e. values from range \[0;100]. |

### StageServiceSetAccelerationResponse

The StageServiceSetAccelerationResponse class.

### StageServiceSetSpeedRequest

The StageServiceSetSpeedRequest class.

| Field    | Type                                                                                                 | Label | Description                                                       |
| -------- | ---------------------------------------------------------------------------------------------------- | ----- | ----------------------------------------------------------------- |
| speed\_x | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Speed in x direction in percent, i.e. values from range \[0;100]. |
| speed\_y | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Speed in y direction in percent, i.e. values from range \[0;100]. |

### StageServiceSetSpeedResponse

The StageServiceSetSpeedResponse class.

### StageServiceStopRequest

The StageServiceStopRequest class.

### StageServiceStopResponse

The StageServiceStopResponse class.

### StageService

The IStageService interface.

KindMethod NameRequest TypeResponse TypeDescription

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetAcceleration [StageServiceGetAccelerationRequest](#zen_api.lm.hardware.v1.StageServiceGetAccelerationRequest) [StageServiceGetAccelerationResponse](#zen_api.lm.hardware.v1.StageServiceGetAccelerationResponse)

Gets the acceleration of the stage.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetPosition [StageServiceGetPositionRequest](#zen_api.lm.hardware.v1.StageServiceGetPositionRequest) [StageServiceGetPositionResponse](#zen_api.lm.hardware.v1.StageServiceGetPositionResponse)

Gets the current stage position.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetSpeed [StageServiceGetSpeedRequest](#zen_api.lm.hardware.v1.StageServiceGetSpeedRequest) [StageServiceGetSpeedResponse](#zen_api.lm.hardware.v1.StageServiceGetSpeedResponse)

Gets the speed of the stage.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

MoveTo [StageServiceMoveToRequest](#zen_api.lm.hardware.v1.StageServiceMoveToRequest) [StageServiceMoveToResponse](#zen_api.lm.hardware.v1.StageServiceMoveToResponse)

Moves the stage to the given position. Is a value for a dimension is no supplied, the position in that dimension it is kept as is.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetAcceleration [StageServiceSetAccelerationRequest](#zen_api.lm.hardware.v1.StageServiceSetAccelerationRequest) [StageServiceSetAccelerationResponse](#zen_api.lm.hardware.v1.StageServiceSetAccelerationResponse)

Sets the acceleration of the stage in percent.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetSpeed [StageServiceSetSpeedRequest](#zen_api.lm.hardware.v1.StageServiceSetSpeedRequest) [StageServiceSetSpeedResponse](#zen_api.lm.hardware.v1.StageServiceSetSpeedResponse)

Sets the speed of the stage in percent.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Stop [StageServiceStopRequest](#zen_api.lm.hardware.v1.StageServiceStopRequest) [StageServiceStopResponse](#zen_api.lm.hardware.v1.StageServiceStopResponse)

Stops the stage if it is moving.

## zen\_api/lm/hardware/v2/focus\_service.proto

[Top](#title)

### FocusServiceGetAccelerationRequest

The FocusServiceGetAccelerationRequest class.

### FocusServiceGetAccelerationResponse

Acceleration of the focus in %.

| Field | Type              | Label | Description            |
| ----- | ----------------- | ----- | ---------------------- |
| value | [double](#double) |       | The acceleration in %. |

### FocusServiceGetPositionRequest

The FocusServiceGetPositionRequest class.

### FocusServiceGetPositionResponse

Position of the focus in meters.

| Field | Type              | Label | Description             |
| ----- | ----------------- | ----- | ----------------------- |
| value | [double](#double) |       | The position in meters. |

### FocusServiceGetSpeedRequest

The FocusServiceGetSpeedRequest class.

### FocusServiceGetSpeedResponse

Speed of the focus in %.

| Field | Type              | Label | Description     |
| ----- | ----------------- | ----- | --------------- |
| value | [double](#double) |       | The speed in %. |

### FocusServiceMoveToRequest

The FocusServiceMoveToRequest class.

| Field | Type              | Label | Description             |
| ----- | ----------------- | ----- | ----------------------- |
| value | [double](#double) |       | New position in meters. |

### FocusServiceMoveToResponse

Describes the result of a Focus.MoveTo request.

| Field             | Type          | Label | Description                                          |
| ----------------- | ------------- | ----- | ---------------------------------------------------- |
| position\_changed | [bool](#bool) |       | A value indicating whether the position was changed. |

### FocusServiceSetAccelerationRequest

The FocusServiceSetAccelerationRequest class.

| Field        | Type              | Label | Description                                               |
| ------------ | ----------------- | ----- | --------------------------------------------------------- |
| acceleration | [double](#double) |       | Acceleration in percent, i.e. values from range \[0;100]. |

### FocusServiceSetAccelerationResponse

The FocusServiceSetAccelerationResponse class.

### FocusServiceSetSpeedRequest

The FocusServiceSetSpeedRequest class.

| Field | Type              | Label | Description                                        |
| ----- | ----------------- | ----- | -------------------------------------------------- |
| speed | [double](#double) |       | Speed in percent, i.e. values from range \[0;100]. |

### FocusServiceSetSpeedResponse

The FocusServiceSetSpeedResponse class.

### FocusServiceStopRequest

The FocusServiceStopRequest class.

### FocusServiceStopResponse

The FocusServiceStopResponse class.

### FocusService

The IFocusService interface.

KindMethod NameRequest TypeResponse TypeDescription

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetAcceleration [FocusServiceGetAccelerationRequest](#zen_api.lm.hardware.v2.FocusServiceGetAccelerationRequest) [FocusServiceGetAccelerationResponse](#zen_api.lm.hardware.v2.FocusServiceGetAccelerationResponse)

Gets the focus acceleration.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetPosition [FocusServiceGetPositionRequest](#zen_api.lm.hardware.v2.FocusServiceGetPositionRequest) [FocusServiceGetPositionResponse](#zen_api.lm.hardware.v2.FocusServiceGetPositionResponse)

Gets the focus position.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetSpeed [FocusServiceGetSpeedRequest](#zen_api.lm.hardware.v2.FocusServiceGetSpeedRequest) [FocusServiceGetSpeedResponse](#zen_api.lm.hardware.v2.FocusServiceGetSpeedResponse)

Gets the focus speed.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

MoveTo [FocusServiceMoveToRequest](#zen_api.lm.hardware.v2.FocusServiceMoveToRequest) [FocusServiceMoveToResponse](#zen_api.lm.hardware.v2.FocusServiceMoveToResponse)

Moves the focus to the given position in meters.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetAcceleration [FocusServiceSetAccelerationRequest](#zen_api.lm.hardware.v2.FocusServiceSetAccelerationRequest) [FocusServiceSetAccelerationResponse](#zen_api.lm.hardware.v2.FocusServiceSetAccelerationResponse)

Sets the acceleration of the focus in percent.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetSpeed [FocusServiceSetSpeedRequest](#zen_api.lm.hardware.v2.FocusServiceSetSpeedRequest) [FocusServiceSetSpeedResponse](#zen_api.lm.hardware.v2.FocusServiceSetSpeedResponse)

Sets the speed of the focus in percent.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Stop [FocusServiceStopRequest](#zen_api.lm.hardware.v2.FocusServiceStopRequest) [FocusServiceStopResponse](#zen_api.lm.hardware.v2.FocusServiceStopResponse)

Stops the focus if it is moving.

## zen\_api/lm/hardware/v2/stage\_service.proto

[Top](#title)

### StageServiceGetAccelerationRequest

The StageServiceGetAccelerationRequest class.

### StageServiceGetAccelerationResponse

Acceleration of the stage.

| Field | Type              | Label | Description                               |
| ----- | ----------------- | ----- | ----------------------------------------- |
| x     | [double](#double) |       | The X component of the acceleration in %. |
| y     | [double](#double) |       | The Y component of the acceleration in %. |

### StageServiceGetPositionRequest

The StageServiceGetPositionRequest class.

### StageServiceGetPositionResponse

Position of the stage.

| Field | Type              | Label | Description                                |
| ----- | ----------------- | ----- | ------------------------------------------ |
| x     | [double](#double) |       | The X component of the position in meters. |
| y     | [double](#double) |       | The Y component of the position in meters. |

### StageServiceGetSpeedRequest

The StageServiceGetSpeedRequest class.

### StageServiceGetSpeedResponse

Speed of the stage.

| Field | Type              | Label | Description                        |
| ----- | ----------------- | ----- | ---------------------------------- |
| x     | [double](#double) |       | The X component of the speed in %. |
| y     | [double](#double) |       | The Y component of the speed in %. |

### StageServiceMoveToRequest

The StageServiceMoveToRequest class.

| Field | Type                                                                                                 | Label | Description                                                                 |
| ----- | ---------------------------------------------------------------------------------------------------- | ----- | --------------------------------------------------------------------------- |
| x     | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Target position x in meters. Leave out if x position should not be changed. |
| y     | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Target position y in meters. Leave out if y position should not be changed. |

### StageServiceMoveToResponse

Describes the result of a Stage.MoveTo request.

| Field             | Type          | Label | Description                                          |
| ----------------- | ------------- | ----- | ---------------------------------------------------- |
| position\_changed | [bool](#bool) |       | A value indicating whether the position was changed. |

### StageServiceSetAccelerationRequest

The StageServiceSetAccelerationRequest class.

| Field           | Type                                                                                                 | Label | Description                                                              |
| --------------- | ---------------------------------------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------ |
| acceleration\_x | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Acceleration in x direction in percent, i.e. values from range \[0;100]. |
| acceleration\_y | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Acceleration in y direction in percent, i.e. values from range \[0;100]. |

### StageServiceSetAccelerationResponse

The StageServiceSetAccelerationResponse class.

### StageServiceSetSpeedRequest

The StageServiceSetSpeedRequest class.

| Field    | Type                                                                                                 | Label | Description                                                       |
| -------- | ---------------------------------------------------------------------------------------------------- | ----- | ----------------------------------------------------------------- |
| speed\_x | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Speed in x direction in percent, i.e. values from range \[0;100]. |
| speed\_y | [google.protobuf.DoubleValue](https://protobuf.dev/reference/protobuf/google.protobuf/#double-value) |       | Speed in y direction in percent, i.e. values from range \[0;100]. |

### StageServiceSetSpeedResponse

The StageServiceSetSpeedResponse class.

### StageServiceStopRequest

The StageServiceStopRequest class.

### StageServiceStopResponse

The StageServiceStopResponse class.

### StageService

The IStageService interface.

KindMethod NameRequest TypeResponse TypeDescription

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetAcceleration [StageServiceGetAccelerationRequest](#zen_api.lm.hardware.v2.StageServiceGetAccelerationRequest) [StageServiceGetAccelerationResponse](#zen_api.lm.hardware.v2.StageServiceGetAccelerationResponse)

Gets the acceleration of the stage.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetPosition [StageServiceGetPositionRequest](#zen_api.lm.hardware.v2.StageServiceGetPositionRequest) [StageServiceGetPositionResponse](#zen_api.lm.hardware.v2.StageServiceGetPositionResponse)

Gets the current stage position.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetSpeed [StageServiceGetSpeedRequest](#zen_api.lm.hardware.v2.StageServiceGetSpeedRequest) [StageServiceGetSpeedResponse](#zen_api.lm.hardware.v2.StageServiceGetSpeedResponse)

Gets the speed of the stage.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

MoveTo [StageServiceMoveToRequest](#zen_api.lm.hardware.v2.StageServiceMoveToRequest) [StageServiceMoveToResponse](#zen_api.lm.hardware.v2.StageServiceMoveToResponse)

Moves the stage to the given position. Is a value for a dimension is no supplied, the position in that dimension it is kept as is.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetAcceleration [StageServiceSetAccelerationRequest](#zen_api.lm.hardware.v2.StageServiceSetAccelerationRequest) [StageServiceSetAccelerationResponse](#zen_api.lm.hardware.v2.StageServiceSetAccelerationResponse)

Sets the acceleration of the stage in percent.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

SetSpeed [StageServiceSetSpeedRequest](#zen_api.lm.hardware.v2.StageServiceSetSpeedRequest) [StageServiceSetSpeedResponse](#zen_api.lm.hardware.v2.StageServiceSetSpeedResponse)

Sets the speed of the stage in percent.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

Stop [StageServiceStopRequest](#zen_api.lm.hardware.v2.StageServiceStopRequest) [StageServiceStopResponse](#zen_api.lm.hardware.v2.StageServiceStopResponse)

Stops the stage if it is moving.

## zen\_api/lm/slide\_scan/v1/channel\_settings.proto

[Top](#title)

### ChannelSettings

Settings for a channel.

| Field                | Type              | Label | Description                                                                                                                         |
| -------------------- | ----------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------- |
| channel\_identifier  | [string](#string) |       | The identifier for the master channel.                                                                                              |
| channel\_name        | [string](#string) |       | The name for the channel.                                                                                                           |
| channel\_description | [string](#string) |       | The description for the channel.                                                                                                    |
| dye\_name            | [string](#string) |       | The fluorescence dye.                                                                                                               |
| intensity            | [double](#double) |       | The lamp intensity that should be used for a channel. The intensity is set in percent. (Values ranging from 0 to 100).              |
| exposure\_time       | [double](#double) |       | The exposure time that should be used for a channel. The exposure time is set in milliseconds. (Values ranging from 0.1 to 2000ms). |

## zen\_api/lm/slide\_scan/v1/information\_base.proto

[Top](#title)

### InformationBase

Base class for all information types.

| Field                      | Type                                                                               | Label | Description |
| -------------------------- | ---------------------------------------------------------------------------------- | ----- | ----------- |
| SimpleInformation          | [SimpleInformation](#zen_api.lm.slide_scan.v1.SimpleInformation)                   |       |             |
| SlideScanSystemInformation | [SlideScanSystemInformation](#zen_api.lm.slide_scan.v1.SlideScanSystemInformation) |       |             |
| MagazineInformation        | [MagazineInformation](#zen_api.lm.slide_scan.v1.MagazineInformation)               |       |             |

### MagazineInformation

Data container for inforamtion about the magazine state.

| Field            | Type                                                         | Label    | Description                                                  |
| ---------------- | ------------------------------------------------------------ | -------- | ------------------------------------------------------------ |
| is\_door\_closed | [bool](#bool)                                                |          | A value indicating whether the Axioscan tray door is closed. |
| trays            | [TrayInformation](#zen_api.lm.slide_scan.v1.TrayInformation) | repeated | The magazine state by providing the list of available trays. |

### SimpleInformation

Data container for a simple message inforamtion.

| Field   | Type              | Label | Description                |
| ------- | ----------------- | ----- | -------------------------- |
| message | [string](#string) |       | The simple string message. |

### SlideScanSystemInformation

Data container for information about the hardware state.

| Field                      | Type          | Label | Description                                             |
| -------------------------- | ------------- | ----- | ------------------------------------------------------- |
| is\_idle                   | [bool](#bool) |       | A value indicating whether an Axioscan system is idle.  |
| is\_scan\_running          | [bool](#bool) |       | A value indicating whether a scan is running.           |
| is\_preview\_scan\_running | [bool](#bool) |       | A value indicating whether a preview scan is running.   |
| is\_tray\_initializing     | [bool](#bool) |       | A value indicating whether a tray is being initialized. |

## zen\_api/lm/slide\_scan/v1/profile\_information.proto

[Top](#title)

### ProfileInformation

ProfileInformation contains information about the scan profile associated with a specific slide.

| Field         | Type              | Label | Description                                              |
| ------------- | ----------------- | ----- | -------------------------------------------------------- |
| profile\_name | [string](#string) |       | The profile name associated with the slides acquisition. |

## zen\_api/lm/slide\_scan/v1/response\_code.proto

[Top](#title)

### ResponseCode

Numerical result code.

| Name                              | Number | Description                                   |
| --------------------------------- | ------ | --------------------------------------------- |
| RESPONSE\_CODE\_UNSPECIFIED       | 0      | Default value if the status is not specified. |
| RESPONSE\_CODE\_INVALID\_ARGUMENT | 1      | The required parameter is missing.            |
| RESPONSE\_CODE\_NOT\_FOUND        | 2      | The requested resource could not be found.    |
| RESPONSE\_CODE\_NOT\_ALLOWED      | 3      | The operation is not allowed.                 |

## zen\_api/lm/slide\_scan/v1/response\_type.proto

[Top](#title)

### ResponseType

Kind of failure with implication to error recovery.

| Name                        | Number | Description                                                                                                                     |
| --------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------- |
| RESPONSE\_TYPE\_UNSPECIFIED | 0      | Default value if the ResponseType is not specified.                                                                             |
| RESPONSE\_TYPE\_SUCCESS     | 1      | The API call is accepted and will be processed. In this case the response code can be unspecified.                              |
| RESPONSE\_TYPE\_WARNING     | 2      | The API call is accepted and will be processed. In this case, the response contains an indication of possible problem settings. |
| RESPONSE\_TYPE\_FAILED      | 3      | Something went wrong. This is the usual error type.                                                                             |
| RESPONSE\_TYPE\_EXCEPTION   | 4      | The call threw an exeption.                                                                                                     |

## zen\_api/lm/slide\_scan/v1/slide\_information.proto

[Top](#title)

### SlideInformation

SlideInformation holds information about an Axioscan slide.

| Field                         | Type                                                               | Label | Description                                                                                 |
| ----------------------------- | ------------------------------------------------------------------ | ----- | ------------------------------------------------------------------------------------------- |
| slide\_on\_frame\_position    | [int32](#int32)                                                    |       | The slide position on the frame - range \[1, 4]. The maximum value depending on frame type. |
| state                         | [SlideState](#zen_api.lm.slide_scan.v1.SlideState)                 |       | The ZenApi.LM.SlideScan.V1.SlideState of the slide.                                         |
| profile\_information          | [ProfileInformation](#zen_api.lm.slide_scan.v1.ProfileInformation) |       | The corresponding ZenApi.LM.SlideScan.V1.SlideInformation.ProfileInformation of the slide.  |
| is\_selected\_for\_processing | [bool](#bool)                                                      |       | A value indicating whether this slide is selected for processing.                           |
| barcode                       | [string](#string)                                                  |       | The barcode of the slide.                                                                   |
| label\_image\_path            | [string](#string)                                                  |       | The path to the label image.                                                                |
| preview\_image\_path          | [string](#string)                                                  |       | The path to the preview image.                                                              |
| scan\_image\_path             | [string](#string)                                                  |       | The path to the scan image.                                                                 |

## zen\_api/lm/slide\_scan/v1/slide\_position\_information.proto

[Top](#title)

### SlidePositionInformation

SlidePositionInformation holds information about an AxioScan slide position.

| Field                      | Type              | Label | Description                                                                                 |
| -------------------------- | ----------------- | ----- | ------------------------------------------------------------------------------------------- |
| slide\_on\_frame\_position | [int32](#int32)   |       | The slide position on the frame - range \[1, 4]. The maximum value depending on frame type. |
| tray\_position             | [int32](#int32)   |       | The position of the tray inside the Axioscan magazine in the range of \[1, 26].             |
| image\_name                | [string](#string) |       | The image name for the slide.                                                               |

## zen\_api/lm/slide\_scan/v1/slide\_scan\_service.proto

[Top](#title)

### GeneralResponse

A general response for all asynchronous requests that do not return any results or data.

| Field         | Type                                                   | Label | Description                                                                   |
| ------------- | ------------------------------------------------------ | ----- | ----------------------------------------------------------------------------- |
| type          | [ResponseType](#zen_api.lm.slide_scan.v1.ResponseType) |       | The type of resonse message.                                                  |
| code          | [ResponseCode](#zen_api.lm.slide_scan.v1.ResponseCode) |       | The code of resonse message.                                                  |
| description   | [string](#string)                                      |       | A description. Explanation text, for developers only.                         |
| user\_message | [string](#string)                                      |       | A message suitable to be shown in user interfaces, will be translated by Api. |

### SlideScanServiceGetChannelSettingsRequest

Describes the input parameters for retrieving the configured channels.

| Field               | Type              | Label | Description                             |
| ------------------- | ----------------- | ----- | --------------------------------------- |
| scan\_profile\_path | [string](#string) |       | The path of the specified scan profile. |

### SlideScanServiceGetChannelSettingsResponse

Lists the configured channel settings in the specified scan profile.

| Field                  | Type                                                         | Label    | Description                      |
| ---------------------- | ------------------------------------------------------------ | -------- | -------------------------------- |
| channel\_setting\_list | [ChannelSettings](#zen_api.lm.slide_scan.v1.ChannelSettings) | repeated | The configured channel settings. |

### SlideScanServiceGetMagazineStateRequest

Describes the input parameters for a call to retrieve the magazine state.

### SlideScanServiceGetMagazineStateResponse

Lists the populated slides of each tray.

| Field | Type                                                         | Label    | Description                 |
| ----- | ------------------------------------------------------------ | -------- | --------------------------- |
| trays | [TrayInformation](#zen_api.lm.slide_scan.v1.TrayInformation) | repeated | The loaded slides per tray. |

### SlideScanServiceObserveRequest

Describes the input parameters for a call to observe the events and progress

that happen either during acquisition or while the microscope is idling.

### SlideScanServiceObserveResponse

Describes the output parameters for a call to observe the events, progress

and additional information like warnings and errors of a running scan profile acquisition.

The response might be a stream of different information types (e.g. Progress, Error, Hardware State, ...).

| Field       | Type                                                         | Label | Description                         |
| ----------- | ------------------------------------------------------------ | ----- | ----------------------------------- |
| information | [InformationBase](#zen_api.lm.slide_scan.v1.InformationBase) |       | The flexible, variable information. |

### SlideScanServiceResetSlideStatesRequest

Describes the input parameters for resetting the state of specified slides to new.

| Field                 | Type                                                                           | Label    | Description                                 |
| --------------------- | ------------------------------------------------------------------------------ | -------- | ------------------------------------------- |
| slide\_position\_list | [SlidePositionInformation](#zen_api.lm.slide_scan.v1.SlidePositionInformation) | repeated | The position of the slide list to be reset. |

### SlideScanServiceResetSlideStatesResponse

Describes the output parameters for resetting the state of specified slides.

| Field    | Type                                                         | Label | Description                                                      |
| -------- | ------------------------------------------------------------ | ----- | ---------------------------------------------------------------- |
| response | [GeneralResponse](#zen_api.lm.slide_scan.v1.GeneralResponse) |       | A general response about the success/error state of the request. |

### SlideScanServiceStartScanPreviewRequest

Describes the input parameters for the preview start.

| Field                 | Type                                                                           | Label    | Description                                          |
| --------------------- | ------------------------------------------------------------------------------ | -------- | ---------------------------------------------------- |
| scan\_profile\_name   | [string](#string)                                                              |          | The name of the scan profile that should be started. |
| slide\_position\_list | [SlidePositionInformation](#zen_api.lm.slide_scan.v1.SlidePositionInformation) | repeated | The list of tray/slides to be processed.             |

### SlideScanServiceStartScanPreviewResponse

Response of starting a preview in the slide scan service.

| Field    | Type                                                         | Label | Description                                                          |
| -------- | ------------------------------------------------------------ | ----- | -------------------------------------------------------------------- |
| response | [GeneralResponse](#zen_api.lm.slide_scan.v1.GeneralResponse) |       | A general response to inform about the requests success/error state. |

### SlideScanServiceStartScanProfileRequest

Describes the input parameters for the scan profile start.

| Field                 | Type                                                                           | Label    | Description                                          |
| --------------------- | ------------------------------------------------------------------------------ | -------- | ---------------------------------------------------- |
| scan\_profile\_name   | [string](#string)                                                              |          | The name of the scan profile that should be started. |
| slide\_position\_list | [SlidePositionInformation](#zen_api.lm.slide_scan.v1.SlidePositionInformation) | repeated | The list of tray/slides to be processed.             |
| channel\_settings     | [ChannelSettings](#zen_api.lm.slide_scan.v1.ChannelSettings)                   | repeated | The list of changed channel settings.                |

### SlideScanServiceStartScanProfileResponse

Describes the output parameters for a call to start the scan profile.

| Field    | Type                                                         | Label | Description                                                          |
| -------- | ------------------------------------------------------------ | ----- | -------------------------------------------------------------------- |
| response | [GeneralResponse](#zen_api.lm.slide_scan.v1.GeneralResponse) |       | A general response to inform about the requests success/error state. |

### SlideScanServiceStopScanPreviewRequest

Represents a request to stop the preview in the SlideScan service.

### SlideScanServiceStopScanPreviewResponse

Represents the response for stopping the preview in the slide scan service.

| Field    | Type                                                         | Label | Description                                                          |
| -------- | ------------------------------------------------------------ | ----- | -------------------------------------------------------------------- |
| response | [GeneralResponse](#zen_api.lm.slide_scan.v1.GeneralResponse) |       | A general response to inform about the requests success/error state. |

### SlideScanServiceStopScanProfileRequest

Describes the input parameters for stopping the scan profile.

### SlideScanServiceStopScanProfileResponse

Describes the output parameters for a call to stop the scan profile.

| Field    | Type                                                         | Label | Description                                                          |
| -------- | ------------------------------------------------------------ | ----- | -------------------------------------------------------------------- |
| response | [GeneralResponse](#zen_api.lm.slide_scan.v1.GeneralResponse) |       | A general response to inform about the requests success/error state. |

### SlideScanService

The ISlideScanService interface.

KindMethod NameRequest TypeResponse TypeDescription

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetChannelSettings [SlideScanServiceGetChannelSettingsRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceGetChannelSettingsRequest) [SlideScanServiceGetChannelSettingsResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceGetChannelSettingsResponse)

Gets a list of configured channel settings of a scan profile.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

GetMagazineState [SlideScanServiceGetMagazineStateRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceGetMagazineStateRequest) [SlideScanServiceGetMagazineStateResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceGetMagazineStateResponse)

Gets the magazine state.

m**Monitoring method:**  
Does not change the state of the system and can be executed at any time.

Observe [SlideScanServiceObserveRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceObserveRequest) [SlideScanServiceObserveResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceObserveResponse) stream

Monitors anything that happens within ZEN or the microscope. The main purpose is to observe the scan profile acquisition progress.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

ResetSlideStates [SlideScanServiceResetSlideStatesRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceResetSlideStatesRequest) [SlideScanServiceResetSlideStatesResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceResetSlideStatesResponse)

Resets the specified slides to new.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

StartScanPreview [SlideScanServiceStartScanPreviewRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceStartScanPreviewRequest) [SlideScanServiceStartScanPreviewResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceStartScanPreviewResponse)

Starts the preview with the specified input.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

StartScanProfile [SlideScanServiceStartScanProfileRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceStartScanProfileRequest) [SlideScanServiceStartScanProfileResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceStartScanProfileResponse)

Starts the scan profile with the specified input.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

StopScanPreview [SlideScanServiceStopScanPreviewRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceStopScanPreviewRequest) [SlideScanServiceStopScanPreviewResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceStopScanPreviewResponse)

Stops the preview execution.

c**Controlling method:**  
Changes the state of the system and can only be executed if ZEN is in API mode (explicit or unsupervised) and a control token is provided.

StopScanProfile [SlideScanServiceStopScanProfileRequest](#zen_api.lm.slide_scan.v1.SlideScanServiceStopScanProfileRequest) [SlideScanServiceStopScanProfileResponse](#zen_api.lm.slide_scan.v1.SlideScanServiceStopScanProfileResponse)

Stops the scan profile execution.

## zen\_api/lm/slide\_scan/v1/slide\_state.proto

[Top](#title)

### SlideState

This enumeration names all possible slide processing states.

| Name                                | Number | Description                                      |
| ----------------------------------- | ------ | ------------------------------------------------ |
| SLIDE\_STATE\_UNSPECIFIED           | 0      | Default value if status is not specified.        |
| SLIDE\_STATE\_STOPPED               | 1      | Processing was stopped.                          |
| SLIDE\_STATE\_NEW                   | 2      | New (not processed).                             |
| SLIDE\_STATE\_PREVIEW\_IN\_PROGRESS | 3      | Preview currently in work.                       |
| SLIDE\_STATE\_INPUT\_REQUIRED       | 4      | Preview processing finished, but input required. |
| SLIDE\_STATE\_PREVIEWED             | 5      | Preview processing finished.                     |
| SLIDE\_STATE\_SCAN\_IN\_PROGRESS    | 6      | Scan currently in work.                          |
| SLIDE\_STATE\_FINISHED              | 7      | Processing finished.                             |
| SLIDE\_STATE\_ERROR                 | 8      | Processing error occurred.                       |
| SLIDE\_STATE\_SKIPPED               | 9      | Slide was skipped by user.                       |

## zen\_api/lm/slide\_scan/v1/tray\_information.proto

[Top](#title)

### TrayInformation

TrayInformation contains information about an Axioscan tray.

| Field          | Type                                                           | Label    | Description                                                                                                     |
| -------------- | -------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------- |
| position       | [int32](#int32)                                                |          | The position of the tray inside the Axioscan magazine in the range of \[1, 26].                                 |
| type           | [TrayType](#zen_api.lm.slide_scan.v1.TrayType)                 |          | The ZenApi.LM.SlideScan.V1.TrayType of the tray. The type determines the number of possible slides on the tray. |
| working\_state | [TrayWorkingState](#zen_api.lm.slide_scan.v1.TrayWorkingState) |          | The ZenApi.LM.SlideScan.V1.TrayWorkingState of the tray. The working state of the entire tray.                  |
| slot\_state    | [TraySlotState](#zen_api.lm.slide_scan.v1.TraySlotState)       |          | The ZenApi.LM.SlideScan.V1.TraySlotState of the tray. The status of the tray slot ( open/closed statuses).      |
| slides         | [SlideInformation](#zen_api.lm.slide_scan.v1.SlideInformation) | repeated | ZenApi.LM.SlideScan.V1.SlideInformation of the slides.                                                          |

## zen\_api/lm/slide\_scan/v1/tray\_slot\_state.proto

[Top](#title)

### TraySlotState

Enum defining the states of slide scanner slot LEDs.

| Name                                                                   | Number | Description                                                      |
| ---------------------------------------------------------------------- | ------ | ---------------------------------------------------------------- |
| TRAY\_SLOT\_STATE\_UNSPECIFIED                                         | 0      | Default value if status is not specified.                        |
| TRAY\_SLOT\_STATE\_SLOT\_OPEN\_SYSTEM\_PAUSED                          | 1      | Slot swiveled out for assembling.                                |
| TRAY\_SLOT\_STATE\_SLOT\_OPEN\_TRAY\_LOADED                            | 2      | Slot swiveled out for assembling but Tray is on stage.           |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_TRAY\_NOT\_PROCESSED                  | 3      | Slot swiveled in with tray containing unprocessed slides.        |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_TRAY\_PROCESSED                       | 4      | Slot swiveled in with tray containing processed slides.          |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_PROCESS\_ERROR                        | 5      | Slot swiveled in with tray but an processing error was occurred. |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_TRAY\_PRESCANNED                      | 6      | Slot swiveled in with tray containing pre-scanned slides.        |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_TRAY\_LOADED                          | 7      | Slot swiveled in and tray is on stage.                           |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_NO\_TRAY                              | 8      | Slot swiveled in without tray.                                   |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_TRAY\_IN\_SYSTEM\_AND\_SLOT           | 9      | Slot swiveled in with tray and a tray on the stage (Error case). |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_UNKNOWN\_TRAY                         | 10     | Slot swiveled in with an unknown tray type.                      |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_NO\_SLIDES                            | 11     | Slot swiveled in with an empty tray.                             |
| TRAY\_SLOT\_STATE\_SLOT\_CLOSED\_TRAY\_PARTLY\_PROCESSED\_WITH\_ERRORS | 12     | Slot swiveled in with tray containing processed slides.          |
| TRAY\_SLOT\_STATE\_UNKNOWN                                             | 255    | Unknown type (tray is inserted but could not be determined).     |

## zen\_api/lm/slide\_scan/v1/tray\_type.proto

[Top](#title)

### TrayType

Enum defining the types of slide scanner trays.

| Name                           | Number | Description                                                                                                          |
| ------------------------------ | ------ | -------------------------------------------------------------------------------------------------------------------- |
| TRAY\_TYPE\_UNSPECIFIED        | 0      | Default value if status is not specified.                                                                            |
| TRAY\_TYPE\_NONE               | 1      | No tray.                                                                                                             |
| TRAY\_TYPE\_SCAN1X3            | 2      | Scan tray for 4 slides of size 1'x3'.                                                                                |
| TRAY\_TYPE\_SCAN2X3            | 3      | Scan tray for 2 slides of size 2'x3'.                                                                                |
| TRAY\_TYPE\_SCAN1X3\_2X3       | 4      | Scan tray for 2 slides, one of size 1'x3', one of size 2'x3'.                                                        |
| TRAY\_TYPE\_CALIBRATION\_STAGE | 5      | Stage calibration slide holder tray.                                                                                 |
| TRAY\_TYPE\_SCAN1X3\_BASIC     | 6      | Scan tray for 4 slides of size 1'x3', basic design.                                                                  |
| TRAY\_TYPE\_SCAN4X3            | 7      | Scan tray for 1 slide of size 4'x3' or a combination of slides of unknown size.                                      |
| TRAY\_TYPE\_PARKING            | 152    | Arbitrary tray type to indicate the parking position. Is only available at parking position of the magazine changer. |
| TRAY\_TYPE\_UNKNOWN            | 153    | Unknown type (tray is inserted but could not be determined).                                                         |

## zen\_api/lm/slide\_scan/v1/tray\_working\_state.proto

[Top](#title)

### TrayWorkingState

Enum defining the types of slide scanner trays working state.

| Name                                 | Number | Description                                                      |
| ------------------------------------ | ------ | ---------------------------------------------------------------- |
| TRAY\_WORKING\_STATE\_UNSPECIFIED    | 0      | Default value if status is not specified.                        |
| TRAY\_WORKING\_STATE\_NOT\_SCANNED   | 1      | The tray is not scanned.                                         |
| TRAY\_WORKING\_STATE\_PRESCANNED     | 2      | The tray was pre scanned.                                        |
| TRAY\_WORKING\_STATE\_SCANNED        | 3      | The tray was successfully scanned.                               |
| TRAY\_WORKING\_STATE\_ERROR          | 4      | There occurred an error while scanning or pre scanning the tray. |
| TRAY\_WORKING\_STATE\_NOT\_AVAILABLE | 5      | There is no tray available at this position.                     |

## Scalar Value Types

| .proto Type | Notes                                                                                                                                           | C++    | Java       | Python      | Go      | C#         | PHP            | Ruby                           |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ---------- | ----------- | ------- | ---------- | -------------- | ------------------------------ |
| double      |                                                                                                                                                 | double | double     | float       | float64 | double     | float          | Float                          |
| float       |                                                                                                                                                 | float  | float      | float       | float32 | float      | float          | Float                          |
| int32       | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32  | int        | int         | int32   | int        | integer        | Bignum or Fixnum (as required) |
| int64       | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64  | long       | int/long    | int64   | long       | integer/string | Bignum                         |
| uint32      | Uses variable-length encoding.                                                                                                                  | uint32 | int        | int/long    | uint32  | uint       | integer        | Bignum or Fixnum (as required) |
| uint64      | Uses variable-length encoding.                                                                                                                  | uint64 | long       | int/long    | uint64  | ulong      | integer/string | Bignum or Fixnum (as required) |
| sint32      | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s.                            | int32  | int        | int         | int32   | int        | integer        | Bignum or Fixnum (as required) |
| sint64      | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s.                            | int64  | long       | int/long    | int64   | long       | integer/string | Bignum                         |
| fixed32     | Always four bytes. More efficient than uint32 if values are often greater than 2^28.                                                            | uint32 | int        | int         | uint32  | uint       | integer        | Bignum or Fixnum (as required) |
| fixed64     | Always eight bytes. More efficient than uint64 if values are often greater than 2^56.                                                           | uint64 | long       | int/long    | uint64  | ulong      | integer/string | Bignum                         |
| sfixed32    | Always four bytes.                                                                                                                              | int32  | int        | int         | int32   | int        | integer        | Bignum or Fixnum (as required) |
| sfixed64    | Always eight bytes.                                                                                                                             | int64  | long       | int/long    | int64   | long       | integer/string | Bignum                         |
| bool        |                                                                                                                                                 | bool   | boolean    | boolean     | bool    | bool       | boolean        | TrueClass/FalseClass           |
| string      | A string must always contain UTF-8 encoded or 7-bit ASCII text.                                                                                 | string | String     | str/unicode | string  | string     | string         | String (UTF-8)                 |
| bytes       | May contain any arbitrary sequence of bytes.                                                                                                    | string | ByteString | str         | \[]byte | ByteString | string         | String (ASCII-8BIT)            |