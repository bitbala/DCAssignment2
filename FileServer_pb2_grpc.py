# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import FileServer_pb2 as FileServer__pb2


class FileServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.DownloadFile = channel.unary_unary(
                '/FileServer/DownloadFile',
                request_serializer=FileServer__pb2.DownloadFileRequest.SerializeToString,
                response_deserializer=FileServer__pb2.DownloadFileResponse.FromString,
                )
        self.SaveFile = channel.unary_unary(
                '/FileServer/SaveFile',
                request_serializer=FileServer__pb2.SaveFileRequest.SerializeToString,
                response_deserializer=FileServer__pb2.SaveFileResponse.FromString,
                )
        self.ListFiles = channel.unary_unary(
                '/FileServer/ListFiles',
                request_serializer=FileServer__pb2.ListFilesRequest.SerializeToString,
                response_deserializer=FileServer__pb2.ListFilesResponse.FromString,
                )
        self.GetLock = channel.unary_unary(
                '/FileServer/GetLock',
                request_serializer=FileServer__pb2.LockRequest.SerializeToString,
                response_deserializer=FileServer__pb2.LockResponse.FromString,
                )
        self.ReleaseLock = channel.unary_unary(
                '/FileServer/ReleaseLock',
                request_serializer=FileServer__pb2.ReleaseLockRequest.SerializeToString,
                response_deserializer=FileServer__pb2.ReleaseLockResponse.FromString,
                )


class FileServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def DownloadFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListFiles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReleaseLock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'DownloadFile': grpc.unary_unary_rpc_method_handler(
                    servicer.DownloadFile,
                    request_deserializer=FileServer__pb2.DownloadFileRequest.FromString,
                    response_serializer=FileServer__pb2.DownloadFileResponse.SerializeToString,
            ),
            'SaveFile': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveFile,
                    request_deserializer=FileServer__pb2.SaveFileRequest.FromString,
                    response_serializer=FileServer__pb2.SaveFileResponse.SerializeToString,
            ),
            'ListFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.ListFiles,
                    request_deserializer=FileServer__pb2.ListFilesRequest.FromString,
                    response_serializer=FileServer__pb2.ListFilesResponse.SerializeToString,
            ),
            'GetLock': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLock,
                    request_deserializer=FileServer__pb2.LockRequest.FromString,
                    response_serializer=FileServer__pb2.LockResponse.SerializeToString,
            ),
            'ReleaseLock': grpc.unary_unary_rpc_method_handler(
                    servicer.ReleaseLock,
                    request_deserializer=FileServer__pb2.ReleaseLockRequest.FromString,
                    response_serializer=FileServer__pb2.ReleaseLockResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'FileServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FileServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def DownloadFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FileServer/DownloadFile',
            FileServer__pb2.DownloadFileRequest.SerializeToString,
            FileServer__pb2.DownloadFileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FileServer/SaveFile',
            FileServer__pb2.SaveFileRequest.SerializeToString,
            FileServer__pb2.SaveFileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FileServer/ListFiles',
            FileServer__pb2.ListFilesRequest.SerializeToString,
            FileServer__pb2.ListFilesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetLock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FileServer/GetLock',
            FileServer__pb2.LockRequest.SerializeToString,
            FileServer__pb2.LockResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReleaseLock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FileServer/ReleaseLock',
            FileServer__pb2.ReleaseLockRequest.SerializeToString,
            FileServer__pb2.ReleaseLockResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
