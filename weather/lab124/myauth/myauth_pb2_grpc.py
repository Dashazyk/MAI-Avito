# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import myauth_pb2 as myauth__pb2


class AuthCheckerStub(object):
    """The greeting service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CheckAuth = channel.unary_unary(
                '/myauth.AuthChecker/CheckAuth',
                request_serializer=myauth__pb2.AuthRequest.SerializeToString,
                response_deserializer=myauth__pb2.AuthReply.FromString,
                )


class AuthCheckerServicer(object):
    """The greeting service definition.
    """

    def CheckAuth(self, request, context):
        """Sends a greeting
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthCheckerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CheckAuth': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckAuth,
                    request_deserializer=myauth__pb2.AuthRequest.FromString,
                    response_serializer=myauth__pb2.AuthReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'myauth.AuthChecker', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AuthChecker(object):
    """The greeting service definition.
    """

    @staticmethod
    def CheckAuth(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/myauth.AuthChecker/CheckAuth',
            myauth__pb2.AuthRequest.SerializeToString,
            myauth__pb2.AuthReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
