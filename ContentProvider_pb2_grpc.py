# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import ContentProvider_pb2 as ContentProvider__pb2


class ContentProviderServiceStub(object):
    """The gRPC service definition for ContentProvider nodes
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RequestCriticalSection = channel.unary_unary(
                '/contentprovider.ContentProviderService/RequestCriticalSection',
                request_serializer=ContentProvider__pb2.CriticalSectionRequest.SerializeToString,
                response_deserializer=ContentProvider__pb2.CriticalSectionResponse.FromString,
                )
        self.ReceiveReply = channel.unary_unary(
                '/contentprovider.ContentProviderService/ReceiveReply',
                request_serializer=ContentProvider__pb2.ReplyRequest.SerializeToString,
                response_deserializer=ContentProvider__pb2.ReplyResponse.FromString,
                )


class ContentProviderServiceServicer(object):
    """The gRPC service definition for ContentProvider nodes
    """

    def RequestCriticalSection(self, request, context):
        """Sends a request to enter the critical section
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReceiveReply(self, request, context):
        """Sends a reply after receiving a critical section request
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ContentProviderServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RequestCriticalSection': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestCriticalSection,
                    request_deserializer=ContentProvider__pb2.CriticalSectionRequest.FromString,
                    response_serializer=ContentProvider__pb2.CriticalSectionResponse.SerializeToString,
            ),
            'ReceiveReply': grpc.unary_unary_rpc_method_handler(
                    servicer.ReceiveReply,
                    request_deserializer=ContentProvider__pb2.ReplyRequest.FromString,
                    response_serializer=ContentProvider__pb2.ReplyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'contentprovider.ContentProviderService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ContentProviderService(object):
    """The gRPC service definition for ContentProvider nodes
    """

    @staticmethod
    def RequestCriticalSection(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/contentprovider.ContentProviderService/RequestCriticalSection',
            ContentProvider__pb2.CriticalSectionRequest.SerializeToString,
            ContentProvider__pb2.CriticalSectionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReceiveReply(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/contentprovider.ContentProviderService/ReceiveReply',
            ContentProvider__pb2.ReplyRequest.SerializeToString,
            ContentProvider__pb2.ReplyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
