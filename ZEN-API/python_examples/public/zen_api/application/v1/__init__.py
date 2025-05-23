# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: zen_api/application/v1/composition_service.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Dict,
    Optional,
)

import betterproto
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase


if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


@dataclass(eq=False, repr=False)
class CompositionServiceCreateModuleRequest(betterproto.Message):
    """The CompositionServiceCreateModuleRequest class."""

    module_id: str = betterproto.string_field(1)
    """The id of the module."""

    display_name: str = betterproto.string_field(2)
    """The display name of the module."""

    description: str = betterproto.string_field(3)
    """The description of the module."""

    license_string: str = betterproto.string_field(4)
    """The license string."""

    minimum_required_version: str = betterproto.string_field(5)
    """The minimum required feature version."""


@dataclass(eq=False, repr=False)
class CompositionServiceCreateModuleResponse(betterproto.Message):
    """The CompositionServiceCreateModuleResponse class."""

    pass


@dataclass(eq=False, repr=False)
class CompositionServiceIsModuleAvailableRequest(betterproto.Message):
    """The CompositionServiceIsModuleAvailableRequest class."""

    module_id: str = betterproto.string_field(1)
    """The module id."""


@dataclass(eq=False, repr=False)
class IsModuleAvailableResponse(betterproto.Message):
    """
    Response object of the method for checking the availability state of a composition module.
    """

    is_available: bool = betterproto.bool_field(1)
    """A value indicating whether the module is available or not."""


class CompositionServiceStub(betterproto.ServiceStub):
    async def create_module(
        self,
        composition_service_create_module_request: "CompositionServiceCreateModuleRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "CompositionServiceCreateModuleResponse":
        return await self._unary_unary(
            "/zen_api.application.v1.CompositionService/CreateModule",
            composition_service_create_module_request,
            CompositionServiceCreateModuleResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def is_module_available(
        self,
        composition_service_is_module_available_request: "CompositionServiceIsModuleAvailableRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "IsModuleAvailableResponse":
        return await self._unary_unary(
            "/zen_api.application.v1.CompositionService/IsModuleAvailable",
            composition_service_is_module_available_request,
            IsModuleAvailableResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class CompositionServiceBase(ServiceBase):

    async def create_module(
        self,
        composition_service_create_module_request: "CompositionServiceCreateModuleRequest",
    ) -> "CompositionServiceCreateModuleResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def is_module_available(
        self,
        composition_service_is_module_available_request: "CompositionServiceIsModuleAvailableRequest",
    ) -> "IsModuleAvailableResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_create_module(
        self,
        stream: "grpclib.server.Stream[CompositionServiceCreateModuleRequest, CompositionServiceCreateModuleResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.create_module(request)
        await stream.send_message(response)

    async def __rpc_is_module_available(
        self,
        stream: "grpclib.server.Stream[CompositionServiceIsModuleAvailableRequest, IsModuleAvailableResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.is_module_available(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/zen_api.application.v1.CompositionService/CreateModule": grpclib.const.Handler(
                self.__rpc_create_module,
                grpclib.const.Cardinality.UNARY_UNARY,
                CompositionServiceCreateModuleRequest,
                CompositionServiceCreateModuleResponse,
            ),
            "/zen_api.application.v1.CompositionService/IsModuleAvailable": grpclib.const.Handler(
                self.__rpc_is_module_available,
                grpclib.const.Cardinality.UNARY_UNARY,
                CompositionServiceIsModuleAvailableRequest,
                IsModuleAvailableResponse,
            ),
        }
